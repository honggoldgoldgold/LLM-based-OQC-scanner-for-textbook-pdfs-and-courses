"""
LLM 客户端 — OpenAI 兼容接口封装，支持多模态和 ASR。

通过依赖注入 AppConfig 使用，不依赖全局状态。
"""

from __future__ import annotations

import base64
import logging
import os
import time
from pathlib import Path
from threading import Event
from typing import Optional

import httpx
from openai import OpenAI, APIConnectionError, APITimeoutError, APIStatusError

from OCRLLM.config import AppConfig
from OCRLLM.core.task_runner import CancelledError

logger = logging.getLogger(__name__)

_NETWORK_ERRORS = (
    httpx.ConnectError, httpx.ReadError, httpx.WriteError,
    httpx.RemoteProtocolError, httpx.ConnectTimeout, httpx.ReadTimeout,
    httpx.PoolTimeout, httpx.HTTPStatusError,
    APIConnectionError, APITimeoutError,
    ConnectionError, ConnectionResetError, OSError, TimeoutError,
)
_RETRIABLE_STATUS_CODES = {429, 500, 502, 503, 504}


class EmptyResponseError(RuntimeError):
    """模型返回了空内容。"""


class FreeTierExhaustedError(RuntimeError):
    """该模型免费额度已用完 (DashScope 错误码 AllocationQuota.FreeTierOnly)。

    上层捕获到时应该尝试沿 free_*_chain() 切换下一个模型继续，
    所有候选都耗尽时再抛错给用户。
    """
    def __init__(self, model: str, original_message: str = ""):
        super().__init__(f"模型 {model} 免费额度耗尽: {original_message[:200]}")
        self.model = model
        self.original_message = original_message


def _looks_like_free_tier_exhausted(exc: Exception) -> bool:
    """检查异常是否对应 AllocationQuota.FreeTierOnly。"""
    msg = str(exc)
    if "AllocationQuota.FreeTierOnly" in msg or "FreeTierOnly" in msg:
        return True
    # 部分错误体形如：{"code":"FreeAllocationQuotaExceeded", ...}
    if "FreeAllocationQuota" in msg:
        return True
    return False


def _is_retriable(exc: Exception) -> bool:
    if isinstance(exc, FreeTierExhaustedError):
        return False  # 用模型切换处理，不要让 _retry_call 反复重试
    if isinstance(exc, _NETWORK_ERRORS):
        return True
    if isinstance(exc, EmptyResponseError):
        return True
    if isinstance(exc, APIStatusError) and exc.status_code in _RETRIABLE_STATUS_CODES:
        # 429 里也可能是 FreeTierOnly；先排除掉再说
        if _looks_like_free_tier_exhausted(exc):
            return False
        return True
    return False


# 进程级单例：免费模型切换通知回调（GUI 在启动时挂上去，弹一次警告）
_FREE_TIER_NOTIFIER = None


def set_free_tier_notifier(callback) -> None:
    """注册免费模型切换的回调。callback(old_model, new_model, kind) -> None。"""
    global _FREE_TIER_NOTIFIER
    _FREE_TIER_NOTIFIER = callback


def _notify_free_tier_switch(old_model: str, new_model: str, kind: str) -> None:
    if _FREE_TIER_NOTIFIER is None:
        return
    try:
        _FREE_TIER_NOTIFIER(old_model, new_model, kind)
    except Exception as exc:
        logger.warning("[FREE_TIER] 通知回调失败: %s", exc)


class LLMClient:
    """OpenAI 兼容多模态 LLM 客户端。线程安全（OpenAI SDK 内部使用 httpx 连接池）。"""

    def __init__(self, cfg: Optional[AppConfig] = None, cancel_event: Optional[Event] = None):
        self.cfg = cfg or AppConfig()
        self._cancel_event = cancel_event
        if not self.cfg.api.api_key:
            raise ValueError(
                "未配置 API Key。请设置环境变量 DASHSCOPE_API_KEY 或在配置中提供 api_key"
            )
        self.client = OpenAI(
            api_key=self.cfg.api.api_key,
            base_url=self.cfg.api.base_url,
            timeout=httpx.Timeout(300, connect=60),
            max_retries=0,
        )

    def set_cancel_event(self, cancel_event: Optional[Event]):
        """设置取消事件，用于协作式中断正在进行的请求。

        Args:
            cancel_event: 线程取消事件，或 None 清除。
        """
        self._cancel_event = cancel_event

    @staticmethod
    def _collect_stream(stream) -> str:
        parts = []
        chunk_count = 0
        for chunk in stream:
            chunk_count += 1
            if not chunk.choices:
                continue
            delta = chunk.choices[0].delta
            if delta.content:
                parts.append(delta.content)
        result = "".join(parts)
        if not result and chunk_count > 0:
            logger.warning("[LLM] 流式响应为空 (收到 %d 个 chunk)", chunk_count)
        return result

    @staticmethod
    def _extract_message_text(completion) -> str:
        content = completion.choices[0].message.content
        if isinstance(content, str):
            return content.strip()
        if isinstance(content, list):
            parts = []
            for part in content:
                text = getattr(part, "text", None)
                if text:
                    parts.append(text)
                    continue
                if isinstance(part, dict) and part.get("text"):
                    parts.append(str(part["text"]))
            return "".join(parts).strip()
        return ""

    @staticmethod
    def _encode_file(file_path: str, mime_map: dict[str, str], default_mime: str) -> str:
        ext = Path(file_path).suffix.lower()
        mime = mime_map.get(ext, default_mime)
        with open(file_path, "rb") as f:
            data = base64.b64encode(f.read()).decode("utf-8")
        return f"data:{mime};base64,{data}"

    _IMAGE_MIME_MAP = {
        ".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
        ".gif": "image/gif", ".webp": "image/webp", ".bmp": "image/bmp",
        ".tif": "image/tiff", ".tiff": "image/tiff",
    }
    _AUDIO_MIME_MAP = {
        ".mp3": "audio/mpeg", ".wav": "audio/wav", ".aac": "audio/aac",
        ".m4a": "audio/mp4", ".amr": "audio/amr", ".ogg": "audio/ogg",
        ".flac": "audio/flac", ".3gp": "audio/3gpp",
    }

    @classmethod
    def _encode_image(cls, image_path: str) -> str:
        return cls._encode_file(image_path, cls._IMAGE_MIME_MAP, "image/jpeg")

    @classmethod
    def _encode_audio(cls, audio_path: str) -> str:
        return cls._encode_file(audio_path, cls._AUDIO_MIME_MAP, "audio/mpeg")

    def _check_cancelled(self):
        if self._cancel_event and self._cancel_event.is_set():
            raise CancelledError("任务已取消")

    def _sleep_with_cancel(self, seconds: float):
        if seconds <= 0:
            return
        if not self._cancel_event:
            time.sleep(seconds)
            return

        deadline = time.monotonic() + seconds
        while True:
            self._check_cancelled()
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                return
            self._cancel_event.wait(min(0.2, remaining))

    def _chat_with_stream_fallback(self, model: str, messages: list[dict]) -> str:
        self._check_cancelled()
        try:
            stream = self.client.chat.completions.create(
                model=model,
                messages=messages,
                stream=True,
                extra_body={"enable_thinking": False},
            )
            result = self._collect_stream(stream)
        except Exception as exc:
            if _looks_like_free_tier_exhausted(exc):
                raise FreeTierExhaustedError(model, str(exc)) from exc
            raise
        if result:
            return result

        logger.warning("[LLM] 流式响应为空，回退到非流式请求")
        try:
            completion = self.client.chat.completions.create(
                model=model,
                messages=messages,
                stream=False,
                extra_body={"enable_thinking": False},
            )
        except Exception as exc:
            if _looks_like_free_tier_exhausted(exc):
                raise FreeTierExhaustedError(model, str(exc)) from exc
            raise
        result = self._extract_message_text(completion)
        if result:
            return result
        raise EmptyResponseError("LLM 响应为空")

    def _call_with_free_tier_fallback(
        self,
        primary_model: str,
        chain: list[str],
        kind: str,
        invoke,
    ):
        """在免费额度链上滑动调用 invoke(model)；遇到 FreeTierExhaustedError 自动切换。

        Args:
            primary_model: 用户优先选用的模型。
            chain: 整条免费链（catalog 提供）。
            kind: "vision" / "audio" 之类的标签，仅用于通知文案。
            invoke: callable(model_name) -> str。

        Returns:
            invoke 返回值。

        Raises:
            FreeTierExhaustedError: 链上所有模型都用完时抛出（携带最后一个模型名）。
        """
        # 把 primary_model 提到链头，避免重复
        ordered = [primary_model] + [m for m in chain if m != primary_model]
        last_exc: FreeTierExhaustedError | None = None
        previous_model = primary_model
        for idx, model_name in enumerate(ordered):
            try:
                if idx > 0:
                    logger.warning("[FREE_TIER] 切换到 %s 继续 (%s)", model_name, kind)
                    _notify_free_tier_switch(previous_model, model_name, kind)
                return invoke(model_name)
            except FreeTierExhaustedError as exc:
                logger.warning("[FREE_TIER] %s 免费额度耗尽 (%s)", model_name, exc.original_message[:120])
                last_exc = exc
                previous_model = model_name
                continue
        # 所有候选都耗尽
        if last_exc is not None:
            raise FreeTierExhaustedError(
                f"all-{kind}",
                f"所有 {kind} 免费额度模型均已耗尽，最后尝试的是 {previous_model}",
            )

    def _retry_call(self, fn, max_retries: int = 6, retry_delay: float = 5.0):
        for attempt in range(1, max_retries + 1):
            try:
                self._check_cancelled()
                return fn()
            except Exception as e:
                if not _is_retriable(e):
                    logger.error("[LLM] 不可重试错误，立即抛出: %s", e)
                    raise
                delay = min(retry_delay * (2 ** (attempt - 1)), 120)
                logger.warning("[LLM] 网络错误 (尝试 %d/%d, %.0fs 后重试): %s",
                               attempt, max_retries, delay, e)
                if attempt < max_retries:
                    self._sleep_with_cancel(delay)
                    continue
                raise

    def chat_with_images(
        self,
        prompt: str,
        image_paths: list[str],
        model: Optional[str] = None,
        max_retries: int = 6,
    ) -> str:
        """发送图片+文本的多模态请求。

        Args:
            prompt: 文本提示词。
            image_paths: 图片文件路径列表。
            model: 模型名称，默认使用 vision_model。
            max_retries: 最大重试次数。

        Returns:
            LLM 响应文本。

        Raises:
            EmptyResponseError: LLM 返回空响应。
        """
        primary_model = model or self.cfg.models.vision_model
        content = []
        for img in image_paths:
            content.append({
                "type": "image_url",
                "image_url": {"url": self._encode_image(img)},
            })
        content.append({"type": "text", "text": prompt})
        messages = [{"role": "user", "content": content}]

        def _call_one(model_name: str):
            def _call():
                logger.info("[LLM] 发送请求: model=%s, 图片=%d", model_name, len(image_paths))
                result = self._chat_with_stream_fallback(model_name, messages)
                logger.info("[LLM] 收到响应: %d 字符", len(result))
                return result
            return self._retry_call(_call, max_retries)

        from OCRLLM.core import model_catalog
        chain = model_catalog.free_vision_chain()
        return self._call_with_free_tier_fallback(primary_model, chain, "vision", _call_one)

    def chat_with_images_contextual(
        self,
        prompt: str,
        image_paths: list[str],
        history: Optional[list[dict]] = None,
        model: Optional[str] = None,
        max_retries: int = 6,
    ) -> str:
        """带历史上下文的图片+文本多模态请求。

        Args:
            prompt: 文本提示词。
            image_paths: 图片文件路径列表。
            history: 历史对话消息列表。
            model: 模型名称，默认使用 vision_model。
            max_retries: 最大重试次数。

        Returns:
            LLM 响应文本。
        """
        primary_model = model or self.cfg.models.vision_model
        messages = list(history) if history else []
        content = []
        for img in image_paths:
            content.append({
                "type": "image_url",
                "image_url": {"url": self._encode_image(img)},
            })
        content.append({"type": "text", "text": prompt})
        messages.append({"role": "user", "content": content})

        def _call_one(model_name: str):
            def _call():
                logger.info("[LLM] 上下文请求: model=%s, 图片=%d, 历史=%d",
                            model_name, len(image_paths), len(history or []))
                result = self._chat_with_stream_fallback(model_name, messages)
                logger.info("[LLM] 收到响应: %d 字符", len(result))
                return result
            return self._retry_call(_call, max_retries)

        from OCRLLM.core import model_catalog
        chain = model_catalog.free_vision_chain()
        return self._call_with_free_tier_fallback(primary_model, chain, "vision", _call_one)

    def chat_text(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        model: Optional[str] = None,
        history: Optional[list[dict]] = None,
        max_retries: int = 6,
    ) -> str:
        """发送纯文本请求。

        Args:
            prompt: 用户消息文本。
            system_prompt: 系统提示词。
            model: 模型名称，默认使用 text_model。
            history: 历史对话消息列表。
            max_retries: 最大重试次数。

        Returns:
            LLM 响应文本。
        """
        primary_model = model or self.cfg.models.text_model
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        if history:
            messages.extend(history)
        messages.append({"role": "user", "content": prompt})

        def _call_one(model_name: str):
            def _call():
                return self._chat_with_stream_fallback(model_name, messages)
            return self._retry_call(_call, max_retries)

        from OCRLLM.core import model_catalog
        chain = model_catalog.free_vision_chain()  # 文本任务沿用视觉链（含 general 类型）
        return self._call_with_free_tier_fallback(primary_model, chain, "text", _call_one)

    def transcribe_short_audio(
        self,
        audio_path: str,
        system_prompt: Optional[str] = None,
        model: Optional[str] = None,
        language: Optional[str] = None,
        enable_itn: bool = False,
        max_retries: int = 6,
    ) -> str:
        """调用 ASR 模型识别短音频。

        Args:
            audio_path: 音频文件路径或 data URI。
            system_prompt: 系统提示词。
            model: ASR 模型名称。
            language: 语言代码。
            enable_itn: 是否启用逆文本正则化。
            max_retries: 最大重试次数。

        Returns:
            音频转写文本。
        """
        model = model or self.cfg.models.asr_short_model

        if audio_path.startswith(("http://", "https://", "data:")):
            audio_ref = audio_path
        else:
            audio_ref = self._encode_audio(audio_path)

        messages = [{
            "role": "user",
            "content": [{"type": "input_audio", "input_audio": {"data": audio_ref}}],
        }]
        asr_options = {"enable_itn": enable_itn}
        if language:
            asr_options["language"] = language

        def _call():
            logger.info("[LLM] 短音频识别: model=%s, audio=%s",
                        model, os.path.basename(audio_path))
            completion = self.client.chat.completions.create(
                model=model, messages=messages, stream=False,
                extra_body={"asr_options": asr_options},
            )
            result = self._extract_message_text(completion)
            if not result:
                raise EmptyResponseError("ASR 响应为空")
            logger.info("[LLM] 短音频识别完成: %d 字符", len(result))
            return result

        return self._retry_call(_call, max_retries)

    # ------------------------------------------------------------------
    # 模型可用性探测
    # ------------------------------------------------------------------

    def probe_vision_model(self, model: str, image_path: str, timeout: float = 60.0) -> tuple[bool, str]:
        """用一张真实图片探测视觉模型是否可用。

        Args:
            model: 待测试模型 ID。
            image_path: 真实图片路径（建议尺寸不大）。
            timeout: 单次请求超时（秒）。

        Returns:
            (ok, message)。message 在失败时携带后端错误片段。
        """
        try:
            content = [
                {"type": "image_url", "image_url": {"url": self._encode_image(image_path)}},
                {"type": "text", "text": "请用一句话说明你看到了什么。"},
            ]
            completion = self.client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": content}],
                stream=False,
                timeout=timeout,
                extra_body={"enable_thinking": False},
            )
            text = self._extract_message_text(completion)
            if not text:
                return False, "模型返回空响应"
            return True, text[:80]
        except APIStatusError as e:
            return False, f"HTTP {e.status_code}: {str(e)[:200]}"
        except Exception as e:
            return False, f"{type(e).__name__}: {str(e)[:200]}"

    def probe_audio_short_model(self, model: str, audio_path: str, timeout: float = 60.0) -> tuple[bool, str]:
        """用一段真实音频探测 OpenAI-兼容 ASR/Omni 模型是否可用。"""
        try:
            audio_ref = self._encode_audio(audio_path)
            messages = [{
                "role": "user",
                "content": [{"type": "input_audio", "input_audio": {"data": audio_ref}}],
            }]
            completion = self.client.chat.completions.create(
                model=model, messages=messages, stream=False,
                timeout=timeout,
                extra_body={"asr_options": {"enable_itn": False}},
            )
            text = self._extract_message_text(completion)
            if not text:
                return False, "模型返回空响应"
            return True, text[:80]
        except APIStatusError as e:
            return False, f"HTTP {e.status_code}: {str(e)[:200]}"
        except Exception as e:
            return False, f"{type(e).__name__}: {str(e)[:200]}"

    def probe_audio_filetrans_model(
        self,
        model: str,
        audio_url: str,
        poll_interval: float = 5.0,
        max_wait: float = 600.0,
    ) -> tuple[bool, str]:
        """通过 DashScope 原生异步 API 提交 filetrans 任务，验证模型可用。

        Args:
            model: 待测模型 ID。
            audio_url: 公网可访问的音频 URL（必须 >5min 才能验证长音频能力）。
            poll_interval: 轮询间隔（秒）。
            max_wait: 最大等待时长（秒）。

        Returns:
            (ok, message)。
        """
        import requests

        api_key = self.cfg.api.api_key
        if not api_key:
            return False, "未配置 API Key"
        try:
            submit = requests.post(
                "https://dashscope.aliyuncs.com/api/v1/services/audio/asr/transcription",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                    "X-DashScope-Async": "enable",
                },
                json={
                    "model": model,
                    "input": {"file_urls": [audio_url]},
                    "parameters": {"channel_id": [0]},
                },
                timeout=30,
            )
            if submit.status_code != 200:
                return False, f"提交失败 HTTP {submit.status_code}: {submit.text[:200]}"
            task_id = submit.json().get("output", {}).get("task_id")
            if not task_id:
                return False, f"未返回 task_id: {submit.text[:200]}"
        except Exception as e:
            return False, f"提交异常 {type(e).__name__}: {str(e)[:200]}"

        deadline = time.monotonic() + max_wait
        url = f"https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}"
        while time.monotonic() < deadline:
            try:
                resp = requests.get(url, headers={"Authorization": f"Bearer {api_key}"}, timeout=30)
                if resp.status_code != 200:
                    return False, f"轮询失败 HTTP {resp.status_code}: {resp.text[:200]}"
                output = resp.json().get("output", {})
                status = output.get("task_status")
                if status == "SUCCEEDED":
                    return True, "异步任务成功"
                if status == "FAILED":
                    return False, f"任务失败: {output.get('message', '')[:200]}"
            except Exception as e:
                return False, f"轮询异常 {type(e).__name__}: {str(e)[:200]}"
            time.sleep(poll_interval)
        return False, f"超时 ({max_wait:.0f}s) 仍未完成"

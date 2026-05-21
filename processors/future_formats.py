"""
文档格式处理器 — DOCX / PPTX / DOC / PPT / HTML。

DOCX / PPTX: ZIP 内部直接解析 XML，提取纯文本，按页/幻灯片写入 Markdown。
DOC / PPT: OLE2 复合二进制，从文件流中提取可见文本。
HTML: 占位，暂未实现。

这些处理器不使用大模型，不需要 API Key。
"""

from __future__ import annotations

import logging
import os
import re
import struct
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path

from OCRLLM.core.document_model import SourceType
from OCRLLM.core.utils import ensure_dir
from OCRLLM.processors.base import BaseProcessor

logger = logging.getLogger(__name__)


class _TextOnlyProcessor(BaseProcessor):
    """不依赖 LLM 的轻量处理器基类。"""

    processor_key = "base_text"
    display_name = "文本提取"
    supported_extensions: tuple[str, ...] = ()
    source_type = SourceType.UNKNOWN
    requires_llm = False

    def _default_output_path(self, source_path: str, suffix: str = "_提取.md") -> str:
        stem = Path(source_path).stem
        return os.path.join(ensure_dir(self.cfg.paths.output_dir), f"{stem}{suffix}")


# ─── DOCX ──────────────────────────────────────────────────────────────

_WORD_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"


def _docx_extract_pages(zip_path: str) -> list[list[str]]:
    """从 DOCX ZIP 中解析 word/document.xml，按分页符切分段落文本。"""
    with zipfile.ZipFile(zip_path, "r") as zf:
        with zf.open("word/document.xml") as f:
            tree = ET.parse(f)

    root = tree.getroot()
    ns = {"w": _WORD_NS}

    pages: list[list[str]] = []
    current_page: list[str] = []

    for para in root.iter(f"{{{_WORD_NS}}}p"):
        # 检查是否有分页符 (w:br type="page" 或 w:lastRenderedPageBreak)
        has_page_break = False
        for br in para.iter(f"{{{_WORD_NS}}}br"):
            if br.get(f"{{{_WORD_NS}}}type") == "page":
                has_page_break = True
                break
        for _ in para.iter(f"{{{_WORD_NS}}}lastRenderedPageBreak"):
            has_page_break = True
            break

        if has_page_break and current_page:
            pages.append(current_page)
            current_page = []

        # 提取段落内全部 w:t 文本
        texts = []
        for t_elem in para.iter(f"{{{_WORD_NS}}}t"):
            if t_elem.text:
                texts.append(t_elem.text)
        line = "".join(texts).strip()
        if line:
            current_page.append(line)

    if current_page:
        pages.append(current_page)

    return pages


class DOCXProcessor(_TextOnlyProcessor):
    """DOCX 文档文本提取处理器。"""
    processor_key = "docx"
    display_name = "DOCX 文档"
    supported_extensions = (".docx",)
    source_type = SourceType.DOCX

    def process(self, source_path: str, output_path: str | None = None, **kwargs) -> str:
        """提取 DOCX 文档文本并输出为 Markdown。

        Args:
            source_path: DOCX 文件路径。
            output_path: 输出路径，None 则自动生成。

        Returns:
            输出文件路径。
        """
        source_path = os.path.abspath(source_path)
        if not os.path.isfile(source_path):
            raise FileNotFoundError(f"文件不存在: {source_path}")
        if not zipfile.is_zipfile(source_path):
            raise ValueError(f"文件不是有效的 DOCX (ZIP) 格式: {source_path}")

        output_path = output_path or self._default_output_path(source_path)
        self._report(0, 3, "解析 DOCX 文档结构...")

        pages = _docx_extract_pages(source_path)
        self._report(1, 3, f"共提取 {len(pages)} 页文本")

        md_lines: list[str] = [f"<!-- meta:document title={Path(source_path).stem} -->\n"]
        for idx, page_paragraphs in enumerate(pages, 1):
            self._check_cancelled()
            md_lines.append(f"<!-- meta:page number={idx} -->\n")
            for para in page_paragraphs:
                md_lines.append(para)
                md_lines.append("")

        md_text = "\n".join(md_lines).strip() + "\n"
        self._report(2, 3, "写入 Markdown...")

        ensure_dir(os.path.dirname(output_path))
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(md_text)

        self._report_content(md_text[:1000], "DOCX 文本提取完成")
        self._report(3, 3, f"完成: {output_path}")
        return output_path


# ─── PPTX ──────────────────────────────────────────────────────────────

_PPTX_A_NS = "http://schemas.openxmlformats.org/drawingml/2006/main"


def _pptx_extract_slides(zip_path: str) -> list[list[str]]:
    """从 PPTX ZIP 中逐张幻灯片提取文本。"""
    with zipfile.ZipFile(zip_path, "r") as zf:
        slide_names = sorted(
            [n for n in zf.namelist() if re.match(r"ppt/slides/slide\d+\.xml$", n)],
            key=lambda n: int(re.search(r"slide(\d+)", n).group(1)),
        )

        slides: list[list[str]] = []
        for slide_name in slide_names:
            with zf.open(slide_name) as f:
                tree = ET.parse(f)
            root = tree.getroot()

            texts: list[str] = []
            # 遍历所有 a:p (段落)
            for para in root.iter(f"{{{_PPTX_A_NS}}}p"):
                runs = []
                for r_elem in para.iter(f"{{{_PPTX_A_NS}}}r"):
                    for t_elem in r_elem.iter(f"{{{_PPTX_A_NS}}}t"):
                        if t_elem.text:
                            runs.append(t_elem.text)
                line = "".join(runs).strip()
                if line:
                    texts.append(line)

            slides.append(texts)

    return slides


class PPTXProcessor(_TextOnlyProcessor):
    """PPTX 课件文本提取处理器。"""
    processor_key = "pptx"
    display_name = "PPTX 课件"
    supported_extensions = (".pptx",)
    source_type = SourceType.PPTX

    def process(self, source_path: str, output_path: str | None = None, **kwargs) -> str:
        """提取 PPTX 课件文本并输出为 Markdown。

        Args:
            source_path: PPTX 文件路径。
            output_path: 输出路径，None 则自动生成。

        Returns:
            输出文件路径。
        """
        source_path = os.path.abspath(source_path)
        if not os.path.isfile(source_path):
            raise FileNotFoundError(f"文件不存在: {source_path}")
        if not zipfile.is_zipfile(source_path):
            raise ValueError(f"文件不是有效的 PPTX (ZIP) 格式: {source_path}")

        output_path = output_path or self._default_output_path(source_path)
        self._report(0, 3, "解析 PPTX 幻灯片...")

        slides = _pptx_extract_slides(source_path)
        self._report(1, 3, f"共提取 {len(slides)} 张幻灯片文本")

        md_lines: list[str] = [f"<!-- meta:document title={Path(source_path).stem} -->\n"]
        for idx, slide_texts in enumerate(slides, 1):
            self._check_cancelled()
            md_lines.append(f"<!-- meta:page number={idx} -->\n")
            if slide_texts:
                for text in slide_texts:
                    md_lines.append(text)
                    md_lines.append("")
            else:
                md_lines.append("（此页无文本内容）\n")

        md_text = "\n".join(md_lines).strip() + "\n"
        self._report(2, 3, "写入 Markdown...")

        ensure_dir(os.path.dirname(output_path))
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(md_text)

        self._report_content(md_text[:1000], "PPTX 文本提取完成")
        self._report(3, 3, f"完成: {output_path}")
        return output_path


# ─── DOC (OLE2 二进制) ─────────────────────────────────────────────────

def _doc_extract_text(file_path: str) -> str:
    """
    从 .doc (OLE2 Compound Binary) 文件中提取纯文本。

    Word Binary Format (.doc) 将文本存储在名为 "WordDocument" 的流中。
    文件头的 FIB (File Information Block) 包含文本的偏移和长度信息。
    文本可能是 CP1252 单字节或 UTF-16LE 双字节。

    此方法使用 FIB 中的 ccpText/ccpFtn 等字符计数字段来定位文本，
    当 FIB 解析失败时回退到暴力文本提取。
    """
    with open(file_path, "rb") as f:
        data = f.read()

    # 验证 OLE2 签名
    if data[:8] != b"\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1":
        raise ValueError(f"文件不是有效的 DOC (OLE2) 格式: {file_path}")

    # 尝试使用简化 OLE2 解析找到 WordDocument 流
    word_stream = _ole2_find_stream(data, "WordDocument")
    if word_stream is None:
        logger.warning("[DOC] 无法定位 WordDocument 流，回退到暴力文本提取")
        return _binary_extract_text(data)

    # 解析 FIB 基本信息
    if len(word_stream) < 100:
        return _binary_extract_text(data)

    try:
        # FIB base: offset 0x000A 处的标志位判断编码
        flags = struct.unpack_from("<H", word_stream, 0x000A)[0]
        is_complex = bool(flags & 0x0004)  # fComplex
        # ccpText: 正文字符数 (FIB offset 0x004C)
        ccp_text = struct.unpack_from("<i", word_stream, 0x004C)[0]

        if ccp_text <= 0 or ccp_text > 50_000_000:
            return _binary_extract_text(data)

        # fcMin: 文本流的起始偏移 (FIB offset 0x0018)
        fc_min = struct.unpack_from("<I", word_stream, 0x0018)[0]

        # 如果不是复杂格式，尝试直接读取
        if not is_complex and fc_min < len(word_stream):
            # 先尝试 CP1252
            end = min(fc_min + ccp_text, len(word_stream))
            raw = word_stream[fc_min:end]
            text = raw.decode("cp1252", errors="replace")
            # 清理控制字符，但保留换行
            text = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", "", text)
            text = text.replace("\r\n", "\n").replace("\r", "\n")
            if len(text.strip()) > 20:
                return text.strip()

        # 复杂格式或上面提取失败
        return _binary_extract_text(data)

    except (struct.error, IndexError):
        return _binary_extract_text(data)


def _ole2_find_stream(data: bytes, stream_name: str) -> bytes | None:
    """简化的 OLE2 目录扫描，查找指定名称的流并返回其数据。"""
    try:
        # OLE2 header
        if len(data) < 512:
            return None
        sector_size = 1 << struct.unpack_from("<H", data, 0x001E)[0]  # uSectorShift
        fat_sectors_count = struct.unpack_from("<I", data, 0x002C)[0]
        first_dir_sector = struct.unpack_from("<I", data, 0x0030)[0]

        # 构建 FAT
        header_difat = struct.unpack_from("<109I", data, 0x004C)
        fat = []
        for i in range(min(fat_sectors_count, 109)):
            sec_id = header_difat[i]
            if sec_id >= 0xFFFFFFFE:
                break
            offset = 512 + sec_id * sector_size
            for j in range(sector_size // 4):
                fat.append(struct.unpack_from("<I", data, offset + j * 4)[0])

        def read_chain(start_sector: int, size: int = -1) -> bytes:
            """链式读取二进制文件中的记录。"""
            result = bytearray()
            sec = start_sector
            visited = set()
            while sec < 0xFFFFFFFE and sec not in visited:
                visited.add(sec)
                offset = 512 + sec * sector_size
                result.extend(data[offset:offset + sector_size])
                if sec < len(fat):
                    sec = fat[sec]
                else:
                    break
            if size >= 0:
                result = result[:size]
            return bytes(result)

        # 读取目录
        dir_data = read_chain(first_dir_sector)
        entry_size = 128
        target_lower = stream_name.lower()

        for i in range(len(dir_data) // entry_size):
            entry = dir_data[i * entry_size:(i + 1) * entry_size]
            name_len = struct.unpack_from("<H", entry, 0x40)[0]
            if name_len < 2:
                continue
            name = entry[:name_len - 2].decode("utf-16-le", errors="replace")
            if name.lower() == target_lower:
                obj_type = entry[0x42]
                if obj_type not in (1, 2):  # storage or stream
                    continue
                start_sec = struct.unpack_from("<I", entry, 0x74)[0]
                stream_size = struct.unpack_from("<I", entry, 0x78)[0]
                return read_chain(start_sec, stream_size)

        return None
    except (struct.error, IndexError):
        return None


def _binary_extract_text(data: bytes) -> str:
    """暴力文本提取：尝试 UTF-16LE 和 CP1252 两种编码。"""
    # 先尝试 UTF-16LE 解码整个文件找长文本段
    chunks: list[str] = []
    try:
        utf16_text = data.decode("utf-16-le", errors="replace")
        # 找连续可打印 CJK / ASCII 区间
        for m in re.finditer(r"[\u0020-\u007e\u00a0-\u00ff\u2000-\u206f\u3000-\u9fff\uff00-\uffef]{10,}", utf16_text):
            chunks.append(m.group())
    except Exception:
        pass

    if len("".join(chunks)) > 100:
        return "\n".join(chunks)

    # 回退 CP1252
    try:
        cp_text = data.decode("cp1252", errors="replace")
        cp_text = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", "", cp_text)
        # 找连续文本段
        segments = re.findall(r"[\x20-\x7e\xa0-\xff]{20,}", cp_text)
        if segments:
            return "\n".join(segments)
    except Exception:
        pass

    return "（无法提取文本内容）"


class DOCProcessor(_TextOnlyProcessor):
    """DOC (OLE2) 文档文本提取处理器。"""
    processor_key = "doc"
    display_name = "DOC 文档"
    supported_extensions = (".doc",)
    source_type = SourceType.DOC

    def process(self, source_path: str, output_path: str | None = None, **kwargs) -> str:
        """提取 DOC 文档文本并输出为 Markdown。

        Args:
            source_path: DOC 文件路径。
            output_path: 输出路径，None 则自动生成。

        Returns:
            输出文件路径。
        """
        source_path = os.path.abspath(source_path)
        if not os.path.isfile(source_path):
            raise FileNotFoundError(f"文件不存在: {source_path}")

        output_path = output_path or self._default_output_path(source_path)
        self._report(0, 3, "解析 DOC 文档...")

        text = _doc_extract_text(source_path)
        self._report(1, 3, "提取文本完成，生成 Markdown...")

        # DOC 二进制格式没有可靠的分页符标记，整体输出
        paragraphs = [p.strip() for p in text.split("\n") if p.strip()]
        md_lines: list[str] = [f"<!-- meta:document title={Path(source_path).stem} -->\n"]
        for para in paragraphs:
            md_lines.append(para)
            md_lines.append("")

        md_text = "\n".join(md_lines).strip() + "\n"
        self._report(2, 3, "写入 Markdown...")

        ensure_dir(os.path.dirname(output_path))
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(md_text)

        self._report_content(md_text[:1000], "DOC 文本提取完成")
        self._report(3, 3, f"完成: {output_path}")
        return output_path


# ─── PPT (OLE2 二进制) ─────────────────────────────────────────────────

def _ppt_extract_slides(file_path: str) -> list[list[str]]:
    """
    从 .ppt (OLE2) 中提取幻灯片文本。

    PPT 二进制格式将幻灯片内容存储在 "PowerPoint Document" 流中，
    由一系列 Record 组成。TextBytesAtom(0x0FA8) 和 TextCharsAtom(0x0FA0)
    包含幻灯片文本。SlideListWithText 容器(0x0FF0) 标记幻灯片边界。
    """
    with open(file_path, "rb") as f:
        data = f.read()

    if data[:8] != b"\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1":
        raise ValueError(f"文件不是有效的 PPT (OLE2) 格式: {file_path}")

    ppt_stream = _ole2_find_stream(data, "PowerPoint Document")
    if ppt_stream is None:
        logger.warning("[PPT] 无法定位 PowerPoint Document 流")
        return [[_binary_extract_text(data)]]

    # 遍历记录，提取文本
    slides: list[list[str]] = []
    current_texts: list[str] = []
    pos = 0
    stream_len = len(ppt_stream)

    while pos + 8 <= stream_len:
        try:
            rec_ver_inst = struct.unpack_from("<H", ppt_stream, pos)[0]
            rec_type = struct.unpack_from("<H", ppt_stream, pos + 2)[0]
            rec_len = struct.unpack_from("<I", ppt_stream, pos + 4)[0]
        except struct.error:
            break

        rec_ver = rec_ver_inst & 0x0F
        header_len = 8

        # SlideListWithText 容器 — 新幻灯片组的边界
        if rec_type == 0x0FF0:
            if current_texts:
                slides.append(current_texts)
                current_texts = []
            # 容器类型：进入内部解析（不跳过 rec_len）
            pos += header_len
            continue

        # SlidePersistAtom — 幻灯片分隔
        if rec_type == 0x03F3:
            if current_texts:
                slides.append(current_texts)
                current_texts = []

        # TextCharsAtom (0x0FA0) — UTF-16LE 文本
        if rec_type == 0x0FA0 and rec_len > 0:
            end = min(pos + header_len + rec_len, stream_len)
            raw = ppt_stream[pos + header_len:end]
            try:
                text = raw.decode("utf-16-le", errors="replace").strip()
                text = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", "", text)
                if text:
                    current_texts.append(text)
            except Exception:
                pass

        # TextBytesAtom (0x0FA8) — CP1252 文本
        elif rec_type == 0x0FA8 and rec_len > 0:
            end = min(pos + header_len + rec_len, stream_len)
            raw = ppt_stream[pos + header_len:end]
            try:
                text = raw.decode("cp1252", errors="replace").strip()
                text = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", "", text)
                if text:
                    current_texts.append(text)
            except Exception:
                pass

        # 跳到下一条记录
        if rec_ver == 0x0F:
            # 容器：进入内部
            pos += header_len
        else:
            pos += header_len + rec_len

    if current_texts:
        slides.append(current_texts)

    # 如果解析没有得到任何文本，回退
    if not slides:
        fallback = _binary_extract_text(data)
        if fallback:
            slides = [[fallback]]

    return slides


class PPTProcessor(_TextOnlyProcessor):
    """PPT (OLE2) 课件文本提取处理器。"""
    processor_key = "ppt"
    display_name = "PPT 课件"
    supported_extensions = (".ppt",)
    source_type = SourceType.PPT

    def process(self, source_path: str, output_path: str | None = None, **kwargs) -> str:
        """提取 PPT 课件文本并输出为 Markdown。

        Args:
            source_path: PPT 文件路径。
            output_path: 输出路径，None 则自动生成。

        Returns:
            输出文件路径。
        """
        source_path = os.path.abspath(source_path)
        if not os.path.isfile(source_path):
            raise FileNotFoundError(f"文件不存在: {source_path}")

        output_path = output_path or self._default_output_path(source_path)
        self._report(0, 3, "解析 PPT 课件...")

        slides = _ppt_extract_slides(source_path)
        self._report(1, 3, f"共提取 {len(slides)} 张幻灯片文本")

        md_lines: list[str] = [f"<!-- meta:document title={Path(source_path).stem} -->\n"]
        for idx, slide_texts in enumerate(slides, 1):
            self._check_cancelled()
            md_lines.append(f"<!-- meta:page number={idx} -->\n")
            if slide_texts:
                for text in slide_texts:
                    md_lines.append(text)
                    md_lines.append("")
            else:
                md_lines.append("（此页无文本内容）\n")

        md_text = "\n".join(md_lines).strip() + "\n"
        self._report(2, 3, "写入 Markdown...")

        ensure_dir(os.path.dirname(output_path))
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(md_text)

        self._report_content(md_text[:1000], "PPT 文本提取完成")
        self._report(3, 3, f"完成: {output_path}")
        return output_path


# ─── HTML（占位）──────────────────────────────────────────────────────

class HTMLProcessor(_TextOnlyProcessor):
    """HTML 课件解析占位处理器（未实现）。"""
    processor_key = "html"
    display_name = "HTML 课件"
    supported_extensions = (".html", ".htm")
    source_type = SourceType.HTML

    def process(self, source_path: str, output_path: str | None = None, **kwargs):
        """解析 HTML 并输出为 Markdown（尚未实现）。

        Raises:
            NotImplementedError: 该处理器尚未实现。
        """
        raise NotImplementedError("HTMLProcessor.process 尚未实现")

    def extract_embedded_assets(self, source_path: str):
        """提取 HTML 中的内嵌资源（尚未实现）。

        Raises:
            NotImplementedError: 该处理器尚未实现。
        """
        raise NotImplementedError("HTMLProcessor.extract_embedded_assets 尚未实现")

    def render_dynamic_view(self, source_path: str):
        """渲染动态 HTML 视图（尚未实现）。

        Raises:
            NotImplementedError: 该处理器尚未实现。
        """
        raise NotImplementedError("HTMLProcessor.render_dynamic_view 尚未实现")

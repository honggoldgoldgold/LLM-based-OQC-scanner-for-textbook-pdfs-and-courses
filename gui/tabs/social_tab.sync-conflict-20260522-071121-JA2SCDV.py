"""
社交媒体视频处理选项卡 — B站/YouTube/抖音/小红书/X。

功能：
  - URL 输入（支持多个，每行一个）
  - 短视频/长视频/自动模式选择
  - B站分P 选择器（探测后可勾选指定 Part）
  - 弹幕/评论抓取开关
  - 可编辑提示词
  - 开始处理
"""

from __future__ import annotations

import os
import logging
from functools import partial
from typing import Optional

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QCheckBox, QTextEdit, QLineEdit, QMessageBox,
    QPushButton, QRadioButton, QButtonGroup,
    QGroupBox, QTreeWidget, QTreeWidgetItem,
    QSpinBox, QFrame,
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

from OCRLLM import prompts

logger = logging.getLogger(__name__)
MONO_FONT = QFont("Consolas", 9)


class SocialTab(QWidget):
    """社交媒体视频处理选项卡。"""

    def __init__(self, get_cfg, start_worker, get_tracker=None, get_output_in_place=None, parent=None):
        super().__init__(parent)
        self._get_cfg = get_cfg
        self._start_worker = start_worker
        self._get_tracker = get_tracker
        self._get_output_in_place = get_output_in_place or (lambda: False)
        self._probed_info: dict = {}  # 缓存探测结果
        self._build_ui()

    def _build_ui(self):
        vbox = QVBoxLayout(self)

        # ---- URL 输入 ----
        url_label = QLabel("视频 URL（每行一个，支持 B站/YouTube/抖音/小红书/X）:")
        vbox.addWidget(url_label)
        self._url_input = QTextEdit()
        self._url_input.setFont(MONO_FONT)
        self._url_input.setPlaceholderText(
            "https://b23.tv/xxxxx\n"
            "https://www.bilibili.com/video/BVxxxxx\n"
            "https://www.youtube.com/watch?v=xxxxx"
        )
        self._url_input.setMaximumHeight(80)
        vbox.addWidget(self._url_input)

        # ---- 探测按钮 ----
        probe_row = QHBoxLayout()
        self._btn_probe = QPushButton("🔍 探测视频信息")
        self._btn_probe.clicked.connect(self._probe_url)
        probe_row.addWidget(self._btn_probe)
        self._probe_status = QLabel("")
        probe_row.addWidget(self._probe_status, stretch=1)
        vbox.addLayout(probe_row)

        # ---- 模式选择 ----
        mode_row = QHBoxLayout()
        mode_row.addWidget(QLabel("处理模式:"))
        self._mode_group = QButtonGroup(self)
        self._mode_auto = QRadioButton("自动（按时长判断）")
        self._mode_auto.setChecked(True)
        self._mode_short = QRadioButton("短视频模式")
        self._mode_long = QRadioButton("长视频模式")
        self._mode_group.addButton(self._mode_auto, 0)
        self._mode_group.addButton(self._mode_short, 1)
        self._mode_group.addButton(self._mode_long, 2)
        mode_row.addWidget(self._mode_auto)
        mode_row.addWidget(self._mode_short)
        mode_row.addWidget(self._mode_long)
        mode_row.addStretch()
        vbox.addLayout(mode_row)

        # ---- B站分P 选择器 ----
        self._parts_group = QGroupBox("B站分P选择（探测后显示）")
        self._parts_group.setCheckable(True)
        self._parts_group.setChecked(False)
        self._parts_group.setVisible(False)
        parts_layout = QVBoxLayout(self._parts_group)

        parts_btn_row = QHBoxLayout()
        btn_select_all = QPushButton("全选")
        btn_select_all.clicked.connect(lambda: self._toggle_all_parts(True))
        btn_deselect_all = QPushButton("全不选")
        btn_deselect_all.clicked.connect(lambda: self._toggle_all_parts(False))
        parts_btn_row.addWidget(btn_select_all)
        parts_btn_row.addWidget(btn_deselect_all)
        parts_btn_row.addStretch()
        parts_layout.addLayout(parts_btn_row)

        self._parts_tree = QTreeWidget()
        self._parts_tree.setHeaderLabels(["选择", "P", "标题", "时长"])
        self._parts_tree.setMaximumHeight(200)
        parts_layout.addWidget(self._parts_tree)
        vbox.addWidget(self._parts_group)

        # ---- 选项 ----
        opts_row = QHBoxLayout()
        self._cb_danmaku = QCheckBox("获取弹幕")
        self._cb_danmaku.setChecked(True)
        self._cb_comments = QCheckBox("获取评论")
        self._cb_comments.setChecked(True)
        opts_row.addWidget(self._cb_danmaku)
        opts_row.addWidget(self._cb_comments)

        opts_row.addWidget(QLabel("  B站画质:"))
        self._quality_spin = QSpinBox()
        self._quality_spin.setRange(16, 120)
        self._quality_spin.setValue(80)
        self._quality_spin.setToolTip("16=360P, 32=480P, 64=720P, 80=1080P, 112=1080P+")
        opts_row.addWidget(self._quality_spin)
        opts_row.addStretch()
        vbox.addLayout(opts_row)

        # ---- 提示词（短视频使用的识别提示词） ----
        vbox.addWidget(QLabel("提示词 (短视频画面识别):"))
        self._prompt = QTextEdit()
        self._prompt.setFont(MONO_FONT)
        self._prompt.setPlainText(prompts.SHORT_VIDEO_RECOGNIZE)
        self._prompt.setMaximumHeight(150)
        vbox.addWidget(self._prompt)

        # ---- 按钮 ----
        from OCRLLM.gui.app import make_action_buttons
        vbox.addLayout(make_action_buttons(
            "▶ 开始处理", self._run,
            lambda: self._prompt.setPlainText(prompts.SHORT_VIDEO_RECOGNIZE),
        ))

    # ---- URL 解析 ----

    def _get_urls(self) -> list[str]:
        """提取输入框中的 URL 列表。"""
        text = self._url_input.toPlainText().strip()
        if not text:
            return []
        urls = []
        for line in text.splitlines():
            line = line.strip()
            if line and (line.startswith("http://") or line.startswith("https://")):
                urls.append(line)
        return urls

    # ---- 探测 ----

    def _probe_url(self):
        """探测第一个 URL 的视频信息（在后台线程执行）。"""
        urls = self._get_urls()
        if not urls:
            QMessageBox.warning(self, "提示", "请先输入视频 URL")
            return

        url = urls[0]
        self._probe_status.setText("探测中...")
        self._btn_probe.setEnabled(False)

        def task(reporter):
            from OCRLLM.processors.social.downloader import probe_video_info
            cfg = self._get_cfg()
            info = probe_video_info(url, cfg)
            self._probed_info = info
            return info

        def on_done(result):
            self._btn_probe.setEnabled(True)
            if isinstance(result, dict) and result.get("title"):
                info = result
                dur_min = info.get("duration", 0) / 60
                parts_count = info.get("total_parts", 1)
                self._probe_status.setText(
                    f"✅ {info['title'][:40]} | {dur_min:.1f}分钟 | {parts_count}P"
                )
                # 如果有多P，显示分P选择器
                parts = info.get("parts", [])
                if len(parts) > 1:
                    self._populate_parts_tree(parts)
                    self._parts_group.setVisible(True)
                    self._parts_group.setChecked(True)
                else:
                    self._parts_group.setVisible(False)
            else:
                self._probe_status.setText("❌ 探测失败")

        # 使用 start_worker（会在后台线程执行，完成后回调）
        # 但 start_worker 不支持回调，所以我们直接在这里做简单探测
        import threading

        def _bg():
            try:
                from OCRLLM.processors.social.downloader import probe_video_info
                cfg = self._get_cfg()
                info = probe_video_info(url, cfg)
                self._probed_info = info
                from PyQt5.QtCore import QMetaObject, Q_ARG
                QMetaObject.invokeMethod(
                    self, "_on_probe_done",
                    Qt.QueuedConnection,
                )
            except Exception as exc:
                logger.error("探测失败: %s", exc)
                self._probed_info = {}
                from PyQt5.QtCore import QMetaObject
                QMetaObject.invokeMethod(
                    self, "_on_probe_done",
                    Qt.QueuedConnection,
                )

        threading.Thread(target=_bg, daemon=True).start()

    def _on_probe_done(self):
        """探测完成回调（在主线程执行）。"""
        self._btn_probe.setEnabled(True)
        info = self._probed_info

        if info and info.get("title"):
            dur_min = info.get("duration", 0) / 60
            parts_count = info.get("total_parts", 1)
            self._probe_status.setText(
                f"✅ {info['title'][:40]} | {dur_min:.1f}分钟 | {parts_count}P"
            )
            parts = info.get("parts", [])
            if len(parts) > 1:
                self._populate_parts_tree(parts)
                self._parts_group.setVisible(True)
                self._parts_group.setChecked(True)
            else:
                self._parts_group.setVisible(False)
        else:
            self._probe_status.setText("❌ 探测失败")

    # Make _on_probe_done callable from QMetaObject.invokeMethod
    from PyQt5.QtCore import pyqtSlot
    _on_probe_done = pyqtSlot()(_on_probe_done)

    def _populate_parts_tree(self, parts: list[dict]):
        """填充分P 树形控件。"""
        self._parts_tree.clear()
        for p in parts:
            item = QTreeWidgetItem()
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            item.setCheckState(0, Qt.Checked)
            item.setText(1, f"P{p['page']}")
            item.setText(2, p.get("part", ""))
            dur = p.get("duration", 0)
            item.setText(3, f"{dur // 60:.0f}:{dur % 60:02.0f}")
            item.setData(0, Qt.UserRole, p["page"])
            self._parts_tree.addTopLevelItem(item)

    def _toggle_all_parts(self, checked: bool):
        """全选/全不选分P。"""
        state = Qt.Checked if checked else Qt.Unchecked
        for i in range(self._parts_tree.topLevelItemCount()):
            self._parts_tree.topLevelItem(i).setCheckState(0, state)

    def _get_selected_parts(self) -> Optional[list[int]]:
        """获取用户选中的分P编号列表；全选或未启用则返回 None。"""
        if not self._parts_group.isVisible() or not self._parts_group.isChecked():
            return None
        selected = []
        total = self._parts_tree.topLevelItemCount()
        for i in range(total):
            item = self._parts_tree.topLevelItem(i)
            if item.checkState(0) == Qt.Checked:
                selected.append(item.data(0, Qt.UserRole))
        if len(selected) == total:
            return None  # 全选 = 不限制
        return selected if selected else None

    # ---- 运行 ----

    def _run(self):
        """开始处理社交媒体视频。"""
        urls = self._get_urls()
        if not urls:
            QMessageBox.warning(self, "提示", "请先输入视频 URL")
            return

        mode_id = self._mode_group.checkedId()  # 0=auto, 1=short, 2=long
        part_indices = self._get_selected_parts()
        fetch_danmaku = self._cb_danmaku.isChecked()
        fetch_comments = self._cb_comments.isChecked()
        bili_quality = self._quality_spin.value()

        def task(reporter):
            from OCRLLM.processors.social.downloader import (
                download_media, detect_platform,
            )
            from OCRLLM.processors.social.platform_router import classify_video, VideoCategory
            from OCRLLM.processors.social.short_video import ShortVideoProcessor
            from OCRLLM.processors.social.long_video import SocialLongVideoProcessor

            cfg = self._get_cfg()
            # 应用社交媒体选项到配置
            cfg = cfg.with_updates(social={
                "fetch_danmaku": fetch_danmaku,
                "fetch_comments": fetch_comments,
                "bilibili_quality": bili_quality,
            })

            tracker = self._get_tracker() if self._get_tracker else None
            results = []

            for idx, url in enumerate(urls):
                reporter.progress(idx, len(urls), f"处理第 {idx + 1}/{len(urls)} 个 URL")

                # 确定模式
                if mode_id == 1:
                    is_short = True
                elif mode_id == 2:
                    is_short = False
                else:
                    # 自动：按统一路由策略分类，playlist 和长视频都走 long。
                    try:
                        route = classify_video(url, cfg)
                        is_short = route.category != VideoCategory.LONG
                    except Exception:
                        is_short = True  # 默认短视频

                # 输出目录
                platform = detect_platform(url)
                safe_label = f"{platform}_{idx + 1}"
                if self._get_output_in_place():
                    output_dir = os.path.join(
                        os.path.expanduser("~"), "OCRLLM_output", safe_label
                    )
                else:
                    output_dir = os.path.join(cfg.paths.output_dir, safe_label)

                try:
                    if is_short:
                        # 短视频: 下载 → ShortVideoProcessor
                        dl_dir = os.path.join(output_dir, "_downloads")
                        dl = download_media(url, dl_dir, cfg, part_indices=part_indices)
                        if not dl.video_path:
                            results.append(f"❌ {url}: 下载失败")
                            continue

                        proc = ShortVideoProcessor(
                            cfg=cfg, reporter=reporter, tracker=tracker,
                        )
                        md_path = proc.process(
                            dl.video_path,
                            output_dir=output_dir,
                            title=dl.title,
                            danmaku_texts=dl.danmaku_texts,
                            comment_texts=dl.comment_texts,
                        )
                        results.append(f"✅ 短视频: {dl.title} → {md_path}")
                    else:
                        # 长视频: SocialLongVideoProcessor
                        proc = SocialLongVideoProcessor(
                            cfg=cfg, reporter=reporter, tracker=tracker,
                        )
                        out = proc.process(
                            url,
                            output_dir=output_dir,
                            part_indices=part_indices,
                        )
                        results.append(f"✅ 长视频: {url} → {out}")

                except Exception as exc:
                    logger.error("处理失败: %s — %s", url, exc)
                    results.append(f"❌ {url}: {exc}")

            return "\n".join(results) if results else "处理完成"

        self._start_worker(task)

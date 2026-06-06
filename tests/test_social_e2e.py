"""
社交媒体短视频端到端测试 — 运行完整 ShortVideoProcessor Pipeline
输出到项目 output/ 目录供查阅
"""
import os
import sys
import logging
import shutil

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(name)s %(levelname)s: %(message)s",
    datefmt="%H:%M:%S",
)

from OCRLLM.config import AppConfig
from OCRLLM.processors.social.downloader import download_media
from OCRLLM.processors.social.short_video import ShortVideoProcessor

cfg = AppConfig.from_env()

TEST_URLS = [
    ("https://b23.tv/oGX5ast", "video1"),
    ("https://b23.tv/LmGncCM", "video2"),
]

# 输出到项目 output/ 目录
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_ROOT = os.path.join(PROJECT_ROOT, "output")
DL_ROOT = os.path.join(os.environ.get("TEMP", "."), "ocrllm_social_e2e")

for url, label in TEST_URLS:
    print(f"\n{'='*60}")
    print(f"处理: {url} ({label})")
    print(f"{'='*60}")

    dl_dir = os.path.join(DL_ROOT, label, "_downloads")
    out_dir = os.path.join(OUTPUT_ROOT, f"social_{label}")

    # 清理旧输出
    if os.path.isdir(out_dir):
        shutil.rmtree(out_dir)

    # 下载
    dl = download_media(url, dl_dir, cfg)
    print(f"  下载完成: {dl.title} ({dl.duration}s)")
    print(f"  弹幕: {len(dl.danmaku_texts)} 条, 评论: {len(dl.comment_texts)} 条")

    if not dl.video_path or not os.path.isfile(dl.video_path):
        print(f"  ❌ 视频文件不存在, 跳过")
        continue

    # 运行 ShortVideoProcessor
    proc = ShortVideoProcessor(cfg=cfg)
    md_path = proc.process(
        dl.video_path,
        output_dir=out_dir,
        title=dl.title,
        danmaku_texts=dl.danmaku_texts,
        comment_texts=dl.comment_texts,
    )

    if md_path and os.path.isfile(md_path):
        content = open(md_path, encoding="utf-8").read()
        print(f"\n  ✅ 输出: {md_path}")
        print(f"  大小: {len(content)} 字符 ({len(content)//1024} KB)")
        # 统计场景数和语音转写
        scene_count = content.count("<!-- meta:scene")
        has_asr = "语音转写" in content or "语音内容" in content
        print(f"  场景数: {scene_count}, 含语音: {has_asr}")
    else:
        print(f"  ❌ 未生成输出文件")

    # 列出生成的文件
    if os.path.isdir(out_dir):
        print(f"\n  生成的文件:")
        for root, dirs, files in os.walk(out_dir):
            for f in sorted(files):
                fp = os.path.join(root, f)
                rel = os.path.relpath(fp, out_dir)
                size = os.path.getsize(fp)
                if not rel.startswith("frames"):
                    print(f"    {rel} ({size//1024}KB)" if size > 1024 else f"    {rel} ({size}B)")
        # frames summary
        frames_dir = os.path.join(out_dir, "frames")
        if os.path.isdir(frames_dir):
            frame_files = os.listdir(frames_dir)
            print(f"    frames/ ({len(frame_files)} 帧)")

print("\n\n=== 测试完成 ===")

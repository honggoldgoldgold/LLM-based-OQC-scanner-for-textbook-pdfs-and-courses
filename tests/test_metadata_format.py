import re
import unittest

from OCRLLM.core.short_video_merge import parse_asr_segments
from OCRLLM.core.utils import count_page_headers, normalize_page_headers
from OCRLLM.processors.audio import AudioProcessor
from OCRLLM.processors.video import VideoProcessor


class PageMetadataFormatTests(unittest.TestCase):
    def test_normalize_page_headers_converts_legacy_page_headers_and_demotes_titles(self):
        text = "# Page 7\n\n# 章节标题\n\n内容A\n\n# Page 8\n\n# 小节\n\n内容B"

        normalized = normalize_page_headers(text, start_page=17, expected_pages=2)

        self.assertEqual(count_page_headers(normalized), 2)
        self.assertIn("<!-- meta:page number=17 -->", normalized)
        self.assertIn("<!-- meta:page number=18 -->", normalized)
        self.assertIn("## 章节标题", normalized)
        self.assertIn("## 小节", normalized)
        self.assertNotIn("# Page 7", normalized)


class VideoMetadataFormatTests(unittest.TestCase):
    def test_extract_hotword_fallback_text_keeps_body_under_html_comments(self):
        md_parts = [
            "<!-- meta:frame id=board_001_010s time=00:10 -->\n\n## 定义\n\n梯度下降",
            "<!-- meta:frame id=board_002_020s time=00:20 -->\n\n## 结论\n\n学习率",
        ]

        cleaned = VideoProcessor._extract_hotword_fallback_text(md_parts)

        self.assertIn("梯度下降", cleaned)
        self.assertIn("学习率", cleaned)
        self.assertNotIn("meta:frame", cleaned)

    def test_has_expected_batch_frame_markers_requires_full_batch_coverage(self):
        frames = (
            {"path": "board_001_010s.jpg", "timestamp": 10.0},
            {"path": "board_002_020s.jpg", "timestamp": 20.0},
        )
        partial = "<!-- meta:frame id=board_001_010s time=00:10 -->\n\n内容A\n\n内容B"
        complete = (
            "<!-- meta:frame id=board_001_010s time=00:10 -->\n\n内容A\n\n"
            "<!-- meta:frame id=board_002_020s time=00:20 -->\n\n内容B"
        )

        self.assertFalse(VideoProcessor._has_expected_batch_frame_markers(partial, frames))
        self.assertTrue(VideoProcessor._has_expected_batch_frame_markers(complete, frames))


class AudioMetadataFormatTests(unittest.TestCase):
    def test_format_transcripts_uses_time_range_for_text_only_segments(self):
        md = AudioProcessor._format_transcripts(
            [{"text": "课程开始", "sentences": [], "time_range_ms": (0, 12500)}],
            "lecture",
        )

        self.assertIn("<!-- meta:audio title=lecture -->", md)
        self.assertIn("<!-- meta:segment index=1 time=00:00~00:12 -->", md)
        self.assertIn("课程开始", md)

    def test_parse_asr_segments_strips_untimed_segment_markers(self):
        segments = parse_asr_segments(
            "<!-- meta:segment index=1 -->\n第一段\n\n<!-- meta:segment index=2 -->\n第二段"
        )

        self.assertEqual(len(segments), 1)
        self.assertEqual(segments[0][0], 0)
        self.assertEqual(segments[0][1], float("inf"))
        self.assertEqual(segments[0][2], "第一段\n\n第二段")


class FutureFormatsMetadataTests(unittest.TestCase):
    """Verify DOCX/PPTX/DOC/PPT processors emit new HTML-comment metadata."""

    _PAGE_META_RE = re.compile(r"^<!--\s*meta:page\s+number=\d+\s*-->$", re.MULTILINE)
    _DOC_META_RE = re.compile(r"^<!--\s*meta:document\s+title=.+\s*-->$", re.MULTILINE)
    _OLD_PAGE_RE = re.compile(r"^## 第 \d+ 页$", re.MULTILINE)
    _OLD_H1_RE = re.compile(r"^# [^<]", re.MULTILINE)

    def _assert_new_format(self, md_text: str, expected_pages: int = 0):
        self.assertTrue(self._DOC_META_RE.search(md_text), "Missing <!-- meta:document ... -->")
        self.assertFalse(self._OLD_H1_RE.search(md_text), "Old # title still present")
        self.assertFalse(self._OLD_PAGE_RE.search(md_text), "Old ## 第 X 页 still present")
        if expected_pages > 0:
            self.assertEqual(len(self._PAGE_META_RE.findall(md_text)), expected_pages)

    def test_docx_processor_emits_new_format(self):
        """DOCXProcessor output should use <!-- meta:page --> markers."""
        import zipfile, tempfile, os
        from OCRLLM.processors.future_formats import DOCXProcessor

        # Create a minimal DOCX (ZIP with word/document.xml)
        ns = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
        xml = (
            f'<?xml version="1.0" encoding="UTF-8"?>'
            f'<w:document xmlns:w="{ns}">'
            f'<w:body>'
            f'<w:p><w:r><w:t>Hello World</w:t></w:r></w:p>'
            f'<w:p><w:r><w:br w:type="page"/></w:r></w:p>'
            f'<w:p><w:r><w:t>Page Two</w:t></w:r></w:p>'
            f'</w:body></w:document>'
        )
        with tempfile.TemporaryDirectory() as tmp:
            docx_path = os.path.join(tmp, "test.docx")
            out_path = os.path.join(tmp, "test_提取.md")
            with zipfile.ZipFile(docx_path, "w") as zf:
                zf.writestr("word/document.xml", xml)
            proc = DOCXProcessor()
            proc.process(docx_path, output_path=out_path)
            md = open(out_path, encoding="utf-8").read()
            self._assert_new_format(md, expected_pages=2)

    def test_pptx_processor_emits_new_format(self):
        """PPTXProcessor output should use <!-- meta:page --> markers."""
        import zipfile, tempfile, os
        from OCRLLM.processors.future_formats import PPTXProcessor

        ns_a = "http://schemas.openxmlformats.org/drawingml/2006/main"
        ns_p = "http://schemas.openxmlformats.org/presentationml/2006/main"
        ns_r = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
        slide_xml = (
            f'<?xml version="1.0" encoding="UTF-8"?>'
            f'<p:sld xmlns:p="{ns_p}" xmlns:a="{ns_a}" xmlns:r="{ns_r}">'
            f'<p:cSld><p:spTree>'
            f'<p:sp><p:txBody><a:p><a:r><a:t>Slide text</a:t></a:r></a:p></p:txBody></p:sp>'
            f'</p:spTree></p:cSld></p:sld>'
        )
        with tempfile.TemporaryDirectory() as tmp:
            pptx_path = os.path.join(tmp, "test.pptx")
            out_path = os.path.join(tmp, "test_提取.md")
            with zipfile.ZipFile(pptx_path, "w") as zf:
                zf.writestr("ppt/slides/slide1.xml", slide_xml)
            proc = PPTXProcessor()
            proc.process(pptx_path, output_path=out_path)
            md = open(out_path, encoding="utf-8").read()
            self._assert_new_format(md, expected_pages=1)


if __name__ == "__main__":
    unittest.main()
from OCRLLM.gui.tabs.extract_social_urls import extract_social_urls


def test_extract_social_urls_accepts_plain_and_annotated_text():
    text = """
    public class link:
    https://www.bilibili.com/video/BV1nJ411z7fe?vd_source=abc&p=33
    note: https://youtu.be/example123.
    """

    assert extract_social_urls(text) == [
        "https://www.bilibili.com/video/BV1nJ411z7fe?vd_source=abc&p=33",
        "https://youtu.be/example123",
    ]


def test_extract_social_urls_accepts_markdown_links_and_deduplicates():
    text = (
        "[https://www.bilibili.com/video/BV1nJ411z7fe/?p=33]"
        "(https://www.bilibili.com/video/BV1nJ411z7fe/?p=33)"
    )

    assert extract_social_urls(text) == [
        "https://www.bilibili.com/video/BV1nJ411z7fe/?p=33",
    ]

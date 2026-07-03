"""
统一中间文档模型。

目标：让 PDF / 视频 / 音频 / PPTX / DOCX / HTML 等不同输入格式，
都先归一到同一套结构，再决定如何导出 Markdown / HTML / 其他格式。
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Iterable


class SourceType(str, Enum):
    """文档来源类型枚举（PDF、板书、视频、音频等）。"""
    PDF = "pdf"
    BOARD = "board"
    VIDEO = "video"
    AUDIO = "audio"
    PPTX = "pptx"
    PPT = "ppt"
    DOCX = "docx"
    DOC = "doc"
    HTML = "html"
    SOCIAL_VIDEO = "social_video"
    UNKNOWN = "unknown"


class BlockType(str, Enum):
    """文档内容块类型枚举（标题、段落、表格、公式等）。"""
    HEADING = "heading"
    PARAGRAPH = "paragraph"
    LIST_ITEM = "list_item"
    TABLE = "table"
    FORMULA = "formula"
    IMAGE = "image"
    CODE = "code"
    QUOTE = "quote"
    TRANSCRIPT = "transcript"
    PAGE_BREAK = "page_break"
    RAW_HTML = "raw_html"


@dataclass(slots=True)
class DocumentAsset:
    """文档关联资源（图片、音频片段等）。"""
    kind: str
    uri: str | None = None
    caption: str | None = None
    alt_text: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """序列化为字典。"""
        return {
            "kind": self.kind,
            "uri": self.uri,
            "caption": self.caption,
            "alt_text": self.alt_text,
            "metadata": dict(self.metadata),
        }


@dataclass(slots=True)
class DocumentBlock:
    """文档内容块（对应一个段落、公式、表格等）。"""
    kind: BlockType
    text: str | None = None
    level: int | None = None
    asset: DocumentAsset | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """序列化为字典。"""
        return {
            "kind": self.kind.value,
            "text": self.text,
            "level": self.level,
            "asset": self.asset.to_dict() if self.asset else None,
            "metadata": dict(self.metadata),
        }


@dataclass(slots=True)
class DocumentSection:
    """文档章节，包含标题和内容块列表。"""
    title: str | None = None
    level: int = 1
    blocks: list[DocumentBlock] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def add_block(
        self,
        kind: BlockType,
        text: str | None = None,
        *,
        level: int | None = None,
        asset: DocumentAsset | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> DocumentBlock:
        """向该章节添加一个内容块。

        Args:
            kind: 块类型。
            text: 文本内容。
            level: 标题层级（仅 HEADING 类型）。
            asset: 关联资源。
            metadata: 额外元数据。

        Returns:
            新创建的 DocumentBlock。
        """
        block = DocumentBlock(
            kind=kind,
            text=text,
            level=level,
            asset=asset,
            metadata=metadata or {},
        )
        self.blocks.append(block)
        return block

    def to_dict(self) -> dict[str, Any]:
        """序列化为字典。"""
        return {
            "title": self.title,
            "level": self.level,
            "blocks": [block.to_dict() for block in self.blocks],
            "metadata": dict(self.metadata),
        }


@dataclass(slots=True)
class DocumentMetadata:
    """文档元数据（标题、来源类型、语言、标签等）。"""
    title: str | None = None
    source_type: SourceType = SourceType.UNKNOWN
    source_path: str | None = None
    language: str | None = None
    tags: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """序列化为字典。"""
        return {
            "title": self.title,
            "source_type": self.source_type.value,
            "source_path": self.source_path,
            "language": self.language,
            "tags": list(self.tags),
            "metadata": dict(self.metadata),
        }


@dataclass(slots=True)
class UnifiedDocument:
    """统一中间文档模型，将不同格式的输入归一到统一结构。"""
    metadata: DocumentMetadata = field(default_factory=DocumentMetadata)
    sections: list[DocumentSection] = field(default_factory=list)
    assets: list[DocumentAsset] = field(default_factory=list)
    extras: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_source(
        cls,
        *,
        source_path: str | None = None,
        source_type: SourceType = SourceType.UNKNOWN,
        title: str | None = None,
        language: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> "UnifiedDocument":
        """从来源信息创建新文档实例。

        Args:
            source_path: 源文件路径。
            source_type: 来源类型。
            title: 文档标题。
            language: 语言代码。
            metadata: 额外元数据。

        Returns:
            新的 UnifiedDocument 实例。
        """
        return cls(
            metadata=DocumentMetadata(
                title=title,
                source_type=source_type,
                source_path=source_path,
                language=language,
                metadata=metadata or {},
            )
        )

    def add_section(
        self,
        title: str | None = None,
        *,
        level: int = 1,
        metadata: dict[str, Any] | None = None,
    ) -> DocumentSection:
        """添加一个新章节。

        Args:
            title: 章节标题。
            level: 标题层级。
            metadata: 额外元数据。

        Returns:
            新创建的 DocumentSection。
        """
        section = DocumentSection(title=title, level=level, metadata=metadata or {})
        self.sections.append(section)
        return section

    def extend_sections(self, sections: Iterable[DocumentSection]):
        """批量追加章节。

        Args:
            sections: 章节迭代器。
        """
        self.sections.extend(sections)

    def add_asset(
        self,
        kind: str,
        *,
        uri: str | None = None,
        caption: str | None = None,
        alt_text: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> DocumentAsset:
        """添加一个文档关联资源。

        Args:
            kind: 资源类型标识。
            uri: 资源 URI。
            caption: 说明文字。
            alt_text: 替代文本。
            metadata: 额外元数据。

        Returns:
            新创建的 DocumentAsset。
        """
        asset = DocumentAsset(
            kind=kind,
            uri=uri,
            caption=caption,
            alt_text=alt_text,
            metadata=metadata or {},
        )
        self.assets.append(asset)
        return asset

    def iter_blocks(self):
        """遍历所有章节中的所有内容块。

        Yields:
            DocumentBlock 实例。
        """
        for section in self.sections:
            for block in section.blocks:
                yield block

    def to_dict(self) -> dict[str, Any]:
        """将整个文档序列化为嵌套字典。

        Returns:
            完整文档结构的字典表示。
        """
        return {
            "metadata": self.metadata.to_dict(),
            "sections": [section.to_dict() for section in self.sections],
            "assets": [asset.to_dict() for asset in self.assets],
            "extras": dict(self.extras),
        }

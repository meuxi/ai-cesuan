"""
文档加载器

支持多种格式的文档加载和预处理
"""

import json
import os
import re
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional, Generator
from abc import ABC, abstractmethod

from .models import Document, DocumentType, KnowledgeCategory

logger = logging.getLogger(__name__)


class BaseDocumentLoader(ABC):
    """文档加载器基类"""
    
    @abstractmethod
    def load(self, source: str) -> List[Document]:
        """加载文档"""
        pass
    
    @abstractmethod
    def supports(self, source: str) -> bool:
        """检查是否支持该源"""
        pass


class JSONDocumentLoader(BaseDocumentLoader):
    """JSON 文档加载器"""
    
    def supports(self, source: str) -> bool:
        return source.endswith('.json')
    
    def load(self, source: str) -> List[Document]:
        documents = []
        try:
            with open(source, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # 支持多种 JSON 结构
            if isinstance(data, list):
                for idx, item in enumerate(data):
                    doc = self._parse_item(item, source, idx)
                    if doc:
                        documents.append(doc)
            elif isinstance(data, dict):
                # 如果有 documents 或 items 键
                items = data.get('documents') or data.get('items') or data.get('data') or [data]
                for idx, item in enumerate(items):
                    doc = self._parse_item(item, source, idx)
                    if doc:
                        documents.append(doc)
        except Exception as e:
            logger.error(f"加载 JSON 文件失败: {source}, 错误: {e}")
        
        return documents
    
    def _parse_item(self, item: Dict[str, Any], source: str, index: int) -> Optional[Document]:
        """解析单个条目"""
        if not isinstance(item, dict):
            return None
        
        # 尝试提取内容
        content = item.get('content') or item.get('text') or item.get('description') or ''
        if not content and isinstance(item, dict):
            # 如果没有明确的内容字段，序列化整个对象
            content = json.dumps(item, ensure_ascii=False, indent=2)
        
        title = item.get('title') or item.get('name') or f"条目_{index}"
        category = self._detect_category(item, source)
        
        return Document(
            title=title,
            content=content,
            doc_type=DocumentType.JSON,
            category=category,
            source=source,
            metadata=item,
        )
    
    def _detect_category(self, item: Dict[str, Any], source: str) -> KnowledgeCategory:
        """自动检测知识分类"""
        # 从文件路径推断
        source_lower = source.lower()
        category_map = {
            'bazi': KnowledgeCategory.BAZI,
            'liuyao': KnowledgeCategory.LIUYAO,
            'tarot': KnowledgeCategory.TAROT,
            'qimen': KnowledgeCategory.QIMEN,
            'ziwei': KnowledgeCategory.ZIWEI,
            'meihua': KnowledgeCategory.MEIHUA,
            'xiaoliu': KnowledgeCategory.XIAOLIU,
            'daliuren': KnowledgeCategory.DALIUREN,
            'fengshui': KnowledgeCategory.FENGSHUI,
            'wuxing': KnowledgeCategory.WUXING,
            'tiangan': KnowledgeCategory.TIANGAN_DIZHI,
            'dizhi': KnowledgeCategory.TIANGAN_DIZHI,
            'zodiac': KnowledgeCategory.ZODIAC,
            'terminology': KnowledgeCategory.TERMINOLOGY,
        }
        
        for key, category in category_map.items():
            if key in source_lower:
                return category
        
        # 从内容关键词推断
        content_str = json.dumps(item, ensure_ascii=False).lower()
        for key, category in category_map.items():
            if key in content_str:
                return category
        
        return KnowledgeCategory.GENERAL


class MarkdownDocumentLoader(BaseDocumentLoader):
    """Markdown 文档加载器"""
    
    def supports(self, source: str) -> bool:
        return source.endswith('.md') or source.endswith('.markdown')
    
    def load(self, source: str) -> List[Document]:
        documents = []
        try:
            with open(source, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 按标题分割文档
            sections = self._split_by_headers(content)
            
            for idx, (title, section_content) in enumerate(sections):
                if not section_content.strip():
                    continue
                
                doc = Document(
                    title=title or Path(source).stem,
                    content=section_content,
                    doc_type=DocumentType.MARKDOWN,
                    category=self._detect_category(source),
                    source=source,
                    metadata={"section_index": idx},
                )
                documents.append(doc)
        except Exception as e:
            logger.error(f"加载 Markdown 文件失败: {source}, 错误: {e}")
        
        return documents
    
    def _split_by_headers(self, content: str) -> List[tuple]:
        """按标题分割内容"""
        # 匹配 # 标题
        header_pattern = r'^(#{1,3})\s+(.+)$'
        lines = content.split('\n')
        sections = []
        current_title = None
        current_content = []
        
        for line in lines:
            match = re.match(header_pattern, line)
            if match:
                # 保存之前的内容
                if current_content:
                    sections.append((current_title, '\n'.join(current_content)))
                current_title = match.group(2).strip()
                current_content = []
            else:
                current_content.append(line)
        
        # 保存最后一段
        if current_content:
            sections.append((current_title, '\n'.join(current_content)))
        
        # 如果没有标题，返回整个文档
        if not sections:
            sections = [(None, content)]
        
        return sections
    
    def _detect_category(self, source: str) -> KnowledgeCategory:
        """检测分类"""
        source_lower = source.lower()
        for category in KnowledgeCategory:
            if category.value in source_lower:
                return category
        return KnowledgeCategory.GENERAL


class TextDocumentLoader(BaseDocumentLoader):
    """纯文本文档加载器"""
    
    def supports(self, source: str) -> bool:
        return source.endswith('.txt')
    
    def load(self, source: str) -> List[Document]:
        documents = []
        try:
            with open(source, 'r', encoding='utf-8') as f:
                content = f.read()
            
            doc = Document(
                title=Path(source).stem,
                content=content,
                doc_type=DocumentType.TEXT,
                category=KnowledgeCategory.GENERAL,
                source=source,
            )
            documents.append(doc)
        except Exception as e:
            logger.error(f"加载文本文件失败: {source}, 错误: {e}")
        
        return documents


class DirectoryLoader:
    """目录加载器 - 递归加载目录中的所有文档"""
    
    def __init__(self):
        self.loaders = [
            JSONDocumentLoader(),
            MarkdownDocumentLoader(),
            TextDocumentLoader(),
        ]
    
    def load(self, directory: str, recursive: bool = True) -> List[Document]:
        """加载目录中的所有文档"""
        documents = []
        path = Path(directory)
        
        if not path.exists():
            logger.warning(f"目录不存在: {directory}")
            return documents
        
        pattern = '**/*' if recursive else '*'
        
        for file_path in path.glob(pattern):
            if file_path.is_file():
                docs = self._load_file(str(file_path))
                documents.extend(docs)
        
        logger.info(f"从目录 {directory} 加载了 {len(documents)} 个文档")
        return documents
    
    def _load_file(self, file_path: str) -> List[Document]:
        """加载单个文件"""
        for loader in self.loaders:
            if loader.supports(file_path):
                return loader.load(file_path)
        return []


class DocumentChunker:
    """文档分块器"""
    
    def __init__(
        self,
        chunk_size: int = 500,
        chunk_overlap: int = 50,
        separators: List[str] = None,
    ):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.separators = separators or ["\n\n", "\n", "。", "！", "？", ".", "!", "?", " "]
    
    def split(self, text: str) -> List[str]:
        """将文本分割成块"""
        if len(text) <= self.chunk_size:
            return [text] if text.strip() else []
        
        chunks = []
        current_chunk = ""
        
        # 尝试按分隔符分割
        segments = self._split_by_separators(text)
        
        for segment in segments:
            if len(current_chunk) + len(segment) <= self.chunk_size:
                current_chunk += segment
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                
                # 如果单个段落太长，强制分割
                if len(segment) > self.chunk_size:
                    sub_chunks = self._force_split(segment)
                    chunks.extend(sub_chunks[:-1])
                    current_chunk = sub_chunks[-1] if sub_chunks else ""
                else:
                    # 保留重叠部分
                    overlap = current_chunk[-self.chunk_overlap:] if len(current_chunk) > self.chunk_overlap else ""
                    current_chunk = overlap + segment
        
        if current_chunk.strip():
            chunks.append(current_chunk.strip())
        
        return chunks
    
    def _split_by_separators(self, text: str) -> List[str]:
        """按分隔符分割"""
        segments = [text]
        
        for sep in self.separators:
            new_segments = []
            for segment in segments:
                parts = segment.split(sep)
                for i, part in enumerate(parts):
                    if i < len(parts) - 1:
                        new_segments.append(part + sep)
                    else:
                        new_segments.append(part)
            segments = [s for s in new_segments if s]
        
        return segments
    
    def _force_split(self, text: str) -> List[str]:
        """强制按字符数分割"""
        chunks = []
        for i in range(0, len(text), self.chunk_size - self.chunk_overlap):
            chunk = text[i:i + self.chunk_size]
            if chunk.strip():
                chunks.append(chunk.strip())
        return chunks


class KnowledgeDocumentLoader:
    """知识库文档加载器 - 统一入口"""
    
    def __init__(
        self,
        chunk_size: int = 500,
        chunk_overlap: int = 50,
    ):
        self.directory_loader = DirectoryLoader()
        self.chunker = DocumentChunker(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    
    def load_from_directory(
        self,
        directory: str,
        recursive: bool = True,
    ) -> List[Document]:
        """从目录加载文档"""
        return self.directory_loader.load(directory, recursive)
    
    def load_from_file(self, file_path: str) -> List[Document]:
        """从单个文件加载"""
        return self.directory_loader._load_file(file_path)
    
    def load_from_dict(
        self,
        data: Dict[str, Any],
        category: KnowledgeCategory = KnowledgeCategory.GENERAL,
    ) -> Document:
        """从字典创建文档"""
        content = data.get('content') or json.dumps(data, ensure_ascii=False)
        return Document(
            title=data.get('title', ''),
            content=content,
            doc_type=DocumentType.JSON,
            category=category,
            metadata=data,
        )
    
    def chunk_document(self, document: Document) -> List[str]:
        """将文档分块"""
        return self.chunker.split(document.content)

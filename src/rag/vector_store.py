"""
向量存储

轻量级向量存储实现，支持：
- 基于文件的持久化存储
- 高效的相似度搜索
- 动态索引管理
"""

import json
import math
import logging
import os
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime
import threading

from .models import DocumentChunk, KnowledgeCategory

logger = logging.getLogger(__name__)


@dataclass
class VectorEntry:
    """向量条目"""
    id: str
    document_id: str
    content: str
    embedding: List[float]
    category: str
    metadata: Dict[str, Any]


class VectorStore:
    """向量存储 - 基于文件的轻量级实现"""
    
    def __init__(
        self,
        store_path: str = None,
        dimension: int = 1536,
        auto_save: bool = True,
    ):
        self.store_path = Path(store_path) if store_path else Path("data/vector_store")
        self.store_path.mkdir(parents=True, exist_ok=True)
        self.dimension = dimension
        self.auto_save = auto_save
        
        self._entries: Dict[str, VectorEntry] = {}
        self._category_index: Dict[str, List[str]] = {}  # category -> [entry_ids]
        self._document_index: Dict[str, List[str]] = {}  # doc_id -> [entry_ids]
        self._lock = threading.Lock()
        
        # 加载已有数据
        self._load()
    
    def add(
        self,
        chunk: DocumentChunk,
        embedding: List[float],
        category: str = "general",
    ) -> str:
        """添加向量"""
        with self._lock:
            entry = VectorEntry(
                id=chunk.id,
                document_id=chunk.document_id,
                content=chunk.content,
                embedding=embedding,
                category=category,
                metadata=chunk.metadata,
            )
            
            self._entries[entry.id] = entry
            
            # 更新索引
            if category not in self._category_index:
                self._category_index[category] = []
            self._category_index[category].append(entry.id)
            
            if chunk.document_id not in self._document_index:
                self._document_index[chunk.document_id] = []
            self._document_index[chunk.document_id].append(entry.id)
            
            if self.auto_save:
                self._save_entry(entry)
            
            return entry.id
    
    def add_batch(
        self,
        chunks: List[DocumentChunk],
        embeddings: List[List[float]],
        category: str = "general",
    ) -> List[str]:
        """批量添加向量"""
        ids = []
        for chunk, embedding in zip(chunks, embeddings):
            entry_id = self.add(chunk, embedding, category)
            ids.append(entry_id)
        return ids
    
    def search(
        self,
        query_embedding: List[float],
        top_k: int = 5,
        categories: List[str] = None,
        score_threshold: float = 0.0,
    ) -> List[Tuple[VectorEntry, float]]:
        """相似度搜索"""
        with self._lock:
            # 确定搜索范围
            if categories:
                candidate_ids = set()
                for cat in categories:
                    candidate_ids.update(self._category_index.get(cat, []))
            else:
                candidate_ids = set(self._entries.keys())
            
            if not candidate_ids:
                return []
            
            # 计算相似度
            results = []
            for entry_id in candidate_ids:
                entry = self._entries.get(entry_id)
                if not entry:
                    continue
                
                score = self._cosine_similarity(query_embedding, entry.embedding)
                if score >= score_threshold:
                    results.append((entry, score))
            
            # 排序并返回 top_k
            results.sort(key=lambda x: x[1], reverse=True)
            return results[:top_k]
    
    def delete(self, entry_id: str) -> bool:
        """删除向量"""
        with self._lock:
            if entry_id not in self._entries:
                return False
            
            entry = self._entries.pop(entry_id)
            
            # 更新索引
            if entry.category in self._category_index:
                self._category_index[entry.category] = [
                    id for id in self._category_index[entry.category] if id != entry_id
                ]
            
            if entry.document_id in self._document_index:
                self._document_index[entry.document_id] = [
                    id for id in self._document_index[entry.document_id] if id != entry_id
                ]
            
            # 删除文件
            entry_file = self.store_path / f"{entry_id}.json"
            if entry_file.exists():
                entry_file.unlink()
            
            return True
    
    def delete_by_document(self, document_id: str) -> int:
        """删除文档的所有向量"""
        entry_ids = self._document_index.get(document_id, []).copy()
        count = 0
        for entry_id in entry_ids:
            if self.delete(entry_id):
                count += 1
        return count
    
    def delete_by_category(self, category: str) -> int:
        """删除分类的所有向量"""
        entry_ids = self._category_index.get(category, []).copy()
        count = 0
        for entry_id in entry_ids:
            if self.delete(entry_id):
                count += 1
        return count
    
    def get(self, entry_id: str) -> Optional[VectorEntry]:
        """获取向量"""
        return self._entries.get(entry_id)
    
    def get_by_document(self, document_id: str) -> List[VectorEntry]:
        """获取文档的所有向量"""
        entry_ids = self._document_index.get(document_id, [])
        return [self._entries[id] for id in entry_ids if id in self._entries]
    
    def count(self, category: str = None) -> int:
        """统计向量数量"""
        if category:
            return len(self._category_index.get(category, []))
        return len(self._entries)
    
    def list_categories(self) -> Dict[str, int]:
        """列出所有分类及数量"""
        return {cat: len(ids) for cat, ids in self._category_index.items()}
    
    def _cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """计算余弦相似度"""
        if len(vec1) != len(vec2):
            return 0.0
        
        dot_product = sum(a * b for a, b in zip(vec1, vec2))
        norm1 = math.sqrt(sum(a * a for a in vec1))
        norm2 = math.sqrt(sum(b * b for b in vec2))
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        return dot_product / (norm1 * norm2)
    
    def _save_entry(self, entry: VectorEntry):
        """保存单个条目到文件"""
        try:
            entry_file = self.store_path / f"{entry.id}.json"
            with open(entry_file, 'w', encoding='utf-8') as f:
                json.dump(asdict(entry), f, ensure_ascii=False)
        except Exception as e:
            logger.error(f"保存向量条目失败: {e}")
    
    def _load(self):
        """从文件加载所有条目"""
        try:
            for entry_file in self.store_path.glob("*.json"):
                if entry_file.name.startswith("_"):
                    continue
                
                try:
                    with open(entry_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    
                    entry = VectorEntry(**data)
                    self._entries[entry.id] = entry
                    
                    # 更新索引
                    if entry.category not in self._category_index:
                        self._category_index[entry.category] = []
                    self._category_index[entry.category].append(entry.id)
                    
                    if entry.document_id not in self._document_index:
                        self._document_index[entry.document_id] = []
                    self._document_index[entry.document_id].append(entry.id)
                except Exception as e:
                    logger.warning(f"加载向量文件失败 {entry_file}: {e}")
            
            logger.info(f"加载了 {len(self._entries)} 个向量条目")
        except Exception as e:
            logger.error(f"加载向量存储失败: {e}")
    
    def save_all(self):
        """保存所有条目"""
        with self._lock:
            for entry in self._entries.values():
                self._save_entry(entry)
            
            # 保存索引
            index_file = self.store_path / "_index.json"
            with open(index_file, 'w', encoding='utf-8') as f:
                json.dump({
                    "category_index": self._category_index,
                    "document_index": self._document_index,
                    "count": len(self._entries),
                    "updated_at": datetime.now().isoformat(),
                }, f, ensure_ascii=False)
    
    def clear(self):
        """清空存储"""
        with self._lock:
            self._entries.clear()
            self._category_index.clear()
            self._document_index.clear()
            
            for f in self.store_path.glob("*.json"):
                f.unlink()


class VectorStoreManager:
    """向量存储管理器 - 支持多知识库"""
    
    def __init__(self, base_path: str = None):
        self.base_path = Path(base_path) if base_path else Path("data/knowledge_bases")
        self.base_path.mkdir(parents=True, exist_ok=True)
        self._stores: Dict[str, VectorStore] = {}
    
    def get_store(self, kb_name: str, dimension: int = 1536) -> VectorStore:
        """获取或创建知识库的向量存储"""
        if kb_name not in self._stores:
            store_path = self.base_path / kb_name / "vectors"
            self._stores[kb_name] = VectorStore(
                store_path=str(store_path),
                dimension=dimension,
            )
        return self._stores[kb_name]
    
    def delete_store(self, kb_name: str) -> bool:
        """删除知识库"""
        if kb_name in self._stores:
            self._stores[kb_name].clear()
            del self._stores[kb_name]
        
        store_path = self.base_path / kb_name
        if store_path.exists():
            import shutil
            shutil.rmtree(store_path)
            return True
        return False
    
    def list_stores(self) -> List[str]:
        """列出所有知识库"""
        stores = set(self._stores.keys())
        for path in self.base_path.iterdir():
            if path.is_dir() and not path.name.startswith("_"):
                stores.add(path.name)
        return list(stores)
    
    def get_stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        stats = {}
        for name in self.list_stores():
            store = self.get_store(name)
            stats[name] = {
                "total_vectors": store.count(),
                "categories": store.list_categories(),
            }
        return stats

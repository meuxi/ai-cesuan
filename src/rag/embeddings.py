"""
向量嵌入服务

支持多种嵌入模型，提供文本向量化功能
"""

import os
import logging
import hashlib
import json
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from pathlib import Path

import httpx

logger = logging.getLogger(__name__)


class BaseEmbedding(ABC):
    """嵌入模型基类"""
    
    name: str = "base"
    dimension: int = 0
    
    @abstractmethod
    async def embed_text(self, text: str) -> List[float]:
        """嵌入单个文本"""
        pass
    
    @abstractmethod
    async def embed_texts(self, texts: List[str]) -> List[List[float]]:
        """批量嵌入文本"""
        pass


class OpenAIEmbedding(BaseEmbedding):
    """OpenAI 嵌入模型"""
    
    name = "openai"
    
    MODEL_DIMENSIONS = {
        "text-embedding-3-small": 1536,
        "text-embedding-3-large": 3072,
        "text-embedding-ada-002": 1536,
    }
    
    def __init__(
        self,
        api_key: str = None,
        base_url: str = None,
        model: str = "text-embedding-3-small",
        timeout: int = 60,
    ):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY", "")
        self.base_url = (base_url or os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")).rstrip("/")
        self.model = model
        self.dimension = self.MODEL_DIMENSIONS.get(model, 1536)
        self.timeout = timeout
    
    async def embed_text(self, text: str) -> List[float]:
        """嵌入单个文本"""
        results = await self.embed_texts([text])
        return results[0] if results else []
    
    async def embed_texts(self, texts: List[str]) -> List[List[float]]:
        """批量嵌入文本"""
        if not texts:
            return []
        
        if not self.api_key:
            logger.warning("OpenAI API Key 未配置，使用模拟嵌入")
            return [self._mock_embedding(text) for text in texts]
        
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.base_url}/embeddings",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json",
                    },
                    json={
                        "model": self.model,
                        "input": texts,
                    },
                )
                response.raise_for_status()
                data = response.json()
                
                # 按索引排序返回
                embeddings = sorted(data["data"], key=lambda x: x["index"])
                return [e["embedding"] for e in embeddings]
        except Exception as e:
            logger.error(f"OpenAI 嵌入请求失败: {e}")
            return [self._mock_embedding(text) for text in texts]
    
    def _mock_embedding(self, text: str) -> List[float]:
        """生成模拟嵌入（基于哈希的伪向量）"""
        hash_val = hashlib.md5(text.encode()).hexdigest()
        vector = []
        for i in range(0, min(len(hash_val), self.dimension * 2), 2):
            val = int(hash_val[i:i+2], 16) / 255.0 - 0.5
            vector.append(val)
        
        # 填充到目标维度
        while len(vector) < self.dimension:
            vector.extend(vector[:self.dimension - len(vector)])
        
        return vector[:self.dimension]


class LocalEmbedding(BaseEmbedding):
    """本地嵌入模型 (基于简单的 TF-IDF 或字符特征)"""
    
    name = "local"
    dimension = 384  # 模拟维度
    
    def __init__(self, dimension: int = 384):
        self.dimension = dimension
        self._vocab: Dict[str, int] = {}
        self._idf: Dict[str, float] = {}
    
    async def embed_text(self, text: str) -> List[float]:
        """基于字符特征的简单嵌入"""
        return self._compute_embedding(text)
    
    async def embed_texts(self, texts: List[str]) -> List[List[float]]:
        """批量嵌入"""
        return [self._compute_embedding(text) for text in texts]
    
    def _compute_embedding(self, text: str) -> List[float]:
        """计算简单的文本嵌入"""
        import math
        
        # 基于字符 n-gram 的特征
        ngrams = self._get_ngrams(text, n=3)
        
        vector = [0.0] * self.dimension
        for ngram in ngrams:
            idx = hash(ngram) % self.dimension
            vector[idx] += 1.0
        
        # 归一化
        norm = math.sqrt(sum(v * v for v in vector))
        if norm > 0:
            vector = [v / norm for v in vector]
        
        return vector
    
    def _get_ngrams(self, text: str, n: int = 3) -> List[str]:
        """获取 n-gram"""
        text = text.lower()
        ngrams = []
        for i in range(len(text) - n + 1):
            ngrams.append(text[i:i+n])
        return ngrams


class EmbeddingCache:
    """嵌入缓存"""
    
    def __init__(self, cache_dir: str = None):
        self.cache_dir = Path(cache_dir) if cache_dir else Path("data/embedding_cache")
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self._memory_cache: Dict[str, List[float]] = {}
    
    def _get_key(self, text: str, model: str) -> str:
        """生成缓存键"""
        content = f"{model}:{text}"
        return hashlib.md5(content.encode()).hexdigest()
    
    def get(self, text: str, model: str) -> Optional[List[float]]:
        """获取缓存的嵌入"""
        key = self._get_key(text, model)
        
        # 内存缓存
        if key in self._memory_cache:
            return self._memory_cache[key]
        
        # 文件缓存
        cache_file = self.cache_dir / f"{key}.json"
        if cache_file.exists():
            try:
                with open(cache_file, 'r') as f:
                    data = json.load(f)
                    embedding = data.get("embedding")
                    if embedding:
                        self._memory_cache[key] = embedding
                        return embedding
            except Exception:
                pass
        
        return None
    
    def set(self, text: str, model: str, embedding: List[float]):
        """缓存嵌入"""
        key = self._get_key(text, model)
        self._memory_cache[key] = embedding
        
        # 异步写入文件
        cache_file = self.cache_dir / f"{key}.json"
        try:
            with open(cache_file, 'w') as f:
                json.dump({"text": text[:100], "model": model, "embedding": embedding}, f)
        except Exception as e:
            logger.warning(f"缓存写入失败: {e}")
    
    def clear(self):
        """清除缓存"""
        self._memory_cache.clear()
        for f in self.cache_dir.glob("*.json"):
            f.unlink()


class EmbeddingService:
    """嵌入服务 - 统一入口"""
    
    def __init__(
        self,
        model_type: str = "openai",
        api_key: str = None,
        base_url: str = None,
        model_name: str = "text-embedding-3-small",
        use_cache: bool = True,
        cache_dir: str = None,
    ):
        self.model_type = model_type
        self.use_cache = use_cache
        
        if model_type == "openai":
            self.model = OpenAIEmbedding(
                api_key=api_key,
                base_url=base_url,
                model=model_name,
            )
        else:
            self.model = LocalEmbedding()
        
        self.cache = EmbeddingCache(cache_dir) if use_cache else None
    
    @property
    def dimension(self) -> int:
        return self.model.dimension
    
    async def embed(self, text: str) -> List[float]:
        """嵌入单个文本"""
        # 检查缓存
        if self.cache:
            cached = self.cache.get(text, self.model.name)
            if cached:
                return cached
        
        embedding = await self.model.embed_text(text)
        
        # 缓存结果
        if self.cache and embedding:
            self.cache.set(text, self.model.name, embedding)
        
        return embedding
    
    async def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """批量嵌入文本"""
        results = []
        uncached_texts = []
        uncached_indices = []
        
        # 检查缓存
        for i, text in enumerate(texts):
            if self.cache:
                cached = self.cache.get(text, self.model.name)
                if cached:
                    results.append((i, cached))
                    continue
            uncached_texts.append(text)
            uncached_indices.append(i)
        
        # 批量嵌入未缓存的文本
        if uncached_texts:
            embeddings = await self.model.embed_texts(uncached_texts)
            for idx, embedding in zip(uncached_indices, embeddings):
                results.append((idx, embedding))
                if self.cache:
                    self.cache.set(texts[idx], self.model.name, embedding)
        
        # 按原始顺序排序
        results.sort(key=lambda x: x[0])
        return [r[1] for r in results]

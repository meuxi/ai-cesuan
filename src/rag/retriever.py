"""
语义检索器

提供高效的知识检索能力，支持：
- 语义相似度检索
- 关键词混合检索
- 重排序优化
- 多知识库联合检索
"""

import logging
import re
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass

from .models import DocumentChunk, RetrievalResult, KnowledgeCategory
from .vector_store import VectorStore, VectorEntry
from .embeddings import EmbeddingService

logger = logging.getLogger(__name__)


@dataclass
class RetrievalConfig:
    """检索配置"""
    top_k: int = 5                      # 返回数量
    score_threshold: float = 0.5        # 相似度阈值
    use_keyword_filter: bool = True     # 是否使用关键词过滤
    use_rerank: bool = True             # 是否使用重排序
    rerank_top_k: int = 20              # 重排序候选数量
    categories: Optional[List[str]] = None  # 限定分类


class KeywordExtractor:
    """关键词提取器"""
    
    # 玄学领域停用词
    STOPWORDS = {
        "的", "是", "在", "有", "和", "与", "或", "了", "也", "就",
        "都", "而", "及", "这", "那", "个", "为", "以", "对", "等",
        "请问", "什么", "怎么", "如何", "能否", "可以", "帮我", "告诉",
    }
    
    # 玄学领域重要词汇
    IMPORTANT_TERMS = {
        # 八字相关
        "八字", "四柱", "天干", "地支", "年柱", "月柱", "日柱", "时柱",
        "甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸",
        "子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥",
        "大运", "流年", "命宫", "身宫", "喜神", "忌神", "用神", "仇神",
        "比肩", "劫财", "食神", "伤官", "正财", "偏财", "正官", "七杀", "正印", "偏印",
        # 五行相关
        "五行", "金", "木", "水", "火", "土", "相生", "相克", "生克",
        # 六爻相关
        "六爻", "卦象", "乾", "坤", "震", "巽", "坎", "离", "艮", "兑",
        "世爻", "应爻", "动爻", "变爻", "用神", "原神", "忌神", "仇神",
        # 塔罗相关
        "塔罗", "大阿尔卡那", "小阿尔卡那", "正位", "逆位", "牌阵",
        "愚者", "魔术师", "女祭司", "女皇", "皇帝", "教皇",
        "权杖", "圣杯", "宝剑", "星币",
        # 其他术数
        "紫微斗数", "奇门遁甲", "梅花易数", "大六壬", "小六壬",
        "风水", "方位", "吉凶", "运势", "财运", "事业", "婚姻", "健康",
    }
    
    def extract(self, text: str) -> List[str]:
        """提取关键词"""
        keywords = []
        
        # 提取重要术语
        for term in self.IMPORTANT_TERMS:
            if term in text:
                keywords.append(term)
        
        # 简单分词
        words = re.findall(r'[\u4e00-\u9fff]+', text)
        for word in words:
            if len(word) >= 2 and word not in self.STOPWORDS:
                keywords.append(word)
        
        return list(set(keywords))


class Reranker:
    """重排序器"""
    
    def __init__(self, keyword_extractor: KeywordExtractor = None):
        self.keyword_extractor = keyword_extractor or KeywordExtractor()
    
    def rerank(
        self,
        query: str,
        results: List[Tuple[VectorEntry, float]],
        top_k: int = 5,
    ) -> List[Tuple[VectorEntry, float]]:
        """重排序检索结果"""
        if not results:
            return []
        
        query_keywords = set(self.keyword_extractor.extract(query))
        
        scored_results = []
        for entry, vector_score in results:
            # 关键词匹配分数
            content_keywords = set(self.keyword_extractor.extract(entry.content))
            keyword_overlap = len(query_keywords & content_keywords)
            keyword_score = keyword_overlap / max(len(query_keywords), 1) if query_keywords else 0
            
            # 综合分数 (向量相似度 70% + 关键词匹配 30%)
            combined_score = vector_score * 0.7 + keyword_score * 0.3
            
            scored_results.append((entry, combined_score))
        
        # 按综合分数排序
        scored_results.sort(key=lambda x: x[1], reverse=True)
        return scored_results[:top_k]


class SemanticRetriever:
    """语义检索器"""
    
    def __init__(
        self,
        vector_store: VectorStore,
        embedding_service: EmbeddingService,
        reranker: Reranker = None,
    ):
        self.vector_store = vector_store
        self.embedding_service = embedding_service
        self.reranker = reranker or Reranker()
        self.keyword_extractor = KeywordExtractor()
    
    async def retrieve(
        self,
        query: str,
        config: RetrievalConfig = None,
    ) -> List[RetrievalResult]:
        """执行检索"""
        config = config or RetrievalConfig()
        
        # 1. 嵌入查询
        query_embedding = await self.embedding_service.embed(query)
        
        # 2. 向量搜索
        search_top_k = config.rerank_top_k if config.use_rerank else config.top_k
        candidates = self.vector_store.search(
            query_embedding=query_embedding,
            top_k=search_top_k,
            categories=config.categories,
            score_threshold=config.score_threshold * 0.5,  # 初筛用较低阈值
        )
        
        if not candidates:
            return []
        
        # 3. 关键词过滤 (可选)
        if config.use_keyword_filter:
            candidates = self._keyword_filter(query, candidates)
        
        # 4. 重排序 (可选)
        if config.use_rerank and len(candidates) > config.top_k:
            candidates = self.reranker.rerank(query, candidates, config.top_k)
        
        # 5. 过滤低分结果
        final_results = []
        for entry, score in candidates[:config.top_k]:
            if score >= config.score_threshold:
                chunk = DocumentChunk(
                    id=entry.id,
                    document_id=entry.document_id,
                    content=entry.content,
                    metadata=entry.metadata,
                )
                result = RetrievalResult(chunk=chunk, score=score)
                final_results.append(result)
        
        return final_results
    
    def _keyword_filter(
        self,
        query: str,
        candidates: List[Tuple[VectorEntry, float]],
    ) -> List[Tuple[VectorEntry, float]]:
        """关键词过滤"""
        query_keywords = set(self.keyword_extractor.extract(query))
        
        if not query_keywords:
            return candidates
        
        filtered = []
        for entry, score in candidates:
            content_keywords = set(self.keyword_extractor.extract(entry.content))
            # 至少有一个关键词匹配，或向量分数足够高
            if query_keywords & content_keywords or score > 0.8:
                filtered.append((entry, score))
        
        return filtered if filtered else candidates


class MultiStoreRetriever:
    """多知识库联合检索器"""
    
    def __init__(
        self,
        stores: Dict[str, VectorStore],
        embedding_service: EmbeddingService,
    ):
        self.stores = stores
        self.embedding_service = embedding_service
        self.reranker = Reranker()
    
    async def retrieve(
        self,
        query: str,
        store_names: List[str] = None,
        config: RetrievalConfig = None,
    ) -> List[RetrievalResult]:
        """从多个知识库检索"""
        config = config or RetrievalConfig()
        target_stores = store_names or list(self.stores.keys())
        
        # 嵌入查询
        query_embedding = await self.embedding_service.embed(query)
        
        # 从各知识库检索
        all_candidates = []
        for store_name in target_stores:
            if store_name not in self.stores:
                continue
            
            store = self.stores[store_name]
            candidates = store.search(
                query_embedding=query_embedding,
                top_k=config.rerank_top_k,
                categories=config.categories,
                score_threshold=config.score_threshold * 0.5,
            )
            
            # 添加来源标记
            for entry, score in candidates:
                entry.metadata["source_store"] = store_name
                all_candidates.append((entry, score))
        
        # 重排序合并结果
        if config.use_rerank:
            all_candidates = self.reranker.rerank(query, all_candidates, config.top_k)
        else:
            all_candidates.sort(key=lambda x: x[1], reverse=True)
            all_candidates = all_candidates[:config.top_k]
        
        # 转换结果
        results = []
        for entry, score in all_candidates:
            if score >= config.score_threshold:
                chunk = DocumentChunk(
                    id=entry.id,
                    document_id=entry.document_id,
                    content=entry.content,
                    metadata=entry.metadata,
                )
                results.append(RetrievalResult(chunk=chunk, score=score))
        
        return results

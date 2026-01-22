"""
RAG 服务层

提供统一的 RAG 服务接口，整合：
- 知识库管理
- 文档加载与向量化
- 语义检索
- 上下文增强生成
- 追问对话
"""

import os
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime

from .models import (
    Document, DocumentChunk, KnowledgeBase, KnowledgeCategory,
    RetrievalResult, RAGQuery, RAGResponse, MessageRole,
)
from .document_loader import KnowledgeDocumentLoader
from .embeddings import EmbeddingService
from .vector_store import VectorStore, VectorStoreManager
from .retriever import SemanticRetriever, RetrievalConfig
from .generator import RAGGenerator, GeneratorConfig
from .conversation import ConversationManager, ConversationSession

logger = logging.getLogger(__name__)


class RAGService:
    """RAG 服务 - 统一入口"""
    
    def __init__(
        self,
        data_path: str = None,
        embedding_model: str = "openai",
        embedding_api_key: str = None,
        embedding_base_url: str = None,
        embedding_model_name: str = "text-embedding-3-small",
        ai_client=None,
    ):
        """
        初始化 RAG 服务
        
        Args:
            data_path: 数据存储路径
            embedding_model: 嵌入模型类型 (openai/local)
            embedding_api_key: 嵌入模型 API Key
            embedding_base_url: 嵌入模型 API 地址
            embedding_model_name: 嵌入模型名称
            ai_client: AI 客户端（用于生成回答）
        """
        self.data_path = Path(data_path) if data_path else Path("data/rag")
        self.data_path.mkdir(parents=True, exist_ok=True)
        
        # 初始化组件
        self.document_loader = KnowledgeDocumentLoader()
        
        self.embedding_service = EmbeddingService(
            model_type=embedding_model,
            api_key=embedding_api_key or os.getenv("OPENAI_API_KEY"),
            base_url=embedding_base_url or os.getenv("OPENAI_API_BASE"),
            model_name=embedding_model_name,
            use_cache=True,
            cache_dir=str(self.data_path / "embedding_cache"),
        )
        
        self.vector_store_manager = VectorStoreManager(
            base_path=str(self.data_path / "knowledge_bases")
        )
        
        self.conversation_manager = ConversationManager(
            store_path=str(self.data_path / "conversations")
        )
        
        self.generator = RAGGenerator(ai_client=ai_client)
        
        # 知识库元数据
        self._knowledge_bases: Dict[str, KnowledgeBase] = {}
        self._load_knowledge_bases_meta()
    
    # ==================== 知识库管理 ====================
    
    def create_knowledge_base(
        self,
        name: str,
        description: str = "",
        category: KnowledgeCategory = KnowledgeCategory.GENERAL,
    ) -> KnowledgeBase:
        """创建知识库"""
        kb = KnowledgeBase(
            name=name,
            description=description,
            category=category,
            embedding_model=self.embedding_service.model.name,
        )
        
        self._knowledge_bases[kb.id] = kb
        self._save_knowledge_bases_meta()
        
        # 初始化向量存储
        self.vector_store_manager.get_store(kb.id, self.embedding_service.dimension)
        
        logger.info(f"创建知识库: {name} (ID: {kb.id})")
        return kb
    
    def get_knowledge_base(self, kb_id: str) -> Optional[KnowledgeBase]:
        """获取知识库"""
        return self._knowledge_bases.get(kb_id)
    
    def list_knowledge_bases(self) -> List[KnowledgeBase]:
        """列出所有知识库"""
        return list(self._knowledge_bases.values())
    
    def delete_knowledge_base(self, kb_id: str) -> bool:
        """删除知识库"""
        if kb_id not in self._knowledge_bases:
            return False
        
        del self._knowledge_bases[kb_id]
        self._save_knowledge_bases_meta()
        self.vector_store_manager.delete_store(kb_id)
        
        logger.info(f"删除知识库: {kb_id}")
        return True
    
    # ==================== 文档管理 ====================
    
    async def add_documents_from_directory(
        self,
        kb_id: str,
        directory: str,
        recursive: bool = True,
    ) -> Dict[str, Any]:
        """从目录添加文档"""
        kb = self.get_knowledge_base(kb_id)
        if not kb:
            raise ValueError(f"知识库不存在: {kb_id}")
        
        # 加载文档
        documents = self.document_loader.load_from_directory(directory, recursive)
        
        if not documents:
            return {"added": 0, "chunks": 0}
        
        # 处理文档
        result = await self._process_documents(kb_id, documents)
        
        # 更新知识库统计
        kb.document_count += result["added"]
        kb.chunk_count += result["chunks"]
        kb.updated_at = datetime.now()
        self._save_knowledge_bases_meta()
        
        return result
    
    async def add_document(
        self,
        kb_id: str,
        title: str,
        content: str,
        category: KnowledgeCategory = None,
        metadata: Dict[str, Any] = None,
    ) -> Dict[str, Any]:
        """添加单个文档"""
        kb = self.get_knowledge_base(kb_id)
        if not kb:
            raise ValueError(f"知识库不存在: {kb_id}")
        
        doc = Document(
            title=title,
            content=content,
            category=category or kb.category,
            metadata=metadata or {},
        )
        
        result = await self._process_documents(kb_id, [doc])
        
        # 更新统计
        kb.document_count += result["added"]
        kb.chunk_count += result["chunks"]
        kb.updated_at = datetime.now()
        self._save_knowledge_bases_meta()
        
        return result
    
    async def add_documents_batch(
        self,
        kb_id: str,
        documents_data: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """批量添加文档"""
        kb = self.get_knowledge_base(kb_id)
        if not kb:
            raise ValueError(f"知识库不存在: {kb_id}")
        
        documents = []
        for data in documents_data:
            doc = self.document_loader.load_from_dict(
                data,
                category=KnowledgeCategory(data.get("category", kb.category.value)),
            )
            documents.append(doc)
        
        result = await self._process_documents(kb_id, documents)
        
        # 更新统计
        kb.document_count += result["added"]
        kb.chunk_count += result["chunks"]
        kb.updated_at = datetime.now()
        self._save_knowledge_bases_meta()
        
        return result
    
    async def _process_documents(
        self,
        kb_id: str,
        documents: List[Document],
    ) -> Dict[str, Any]:
        """处理文档：分块 -> 嵌入 -> 存储"""
        vector_store = self.vector_store_manager.get_store(
            kb_id, self.embedding_service.dimension
        )
        
        total_chunks = 0
        added_docs = 0
        
        for doc in documents:
            # 分块
            chunk_texts = self.document_loader.chunk_document(doc)
            if not chunk_texts:
                continue
            
            # 创建 chunks
            chunks = []
            for idx, text in enumerate(chunk_texts):
                chunk = DocumentChunk(
                    document_id=doc.id,
                    content=text,
                    chunk_index=idx,
                    metadata={
                        "title": doc.title,
                        "category": doc.category.value,
                        "source": doc.source,
                    },
                )
                chunks.append(chunk)
            
            # 批量嵌入
            embeddings = await self.embedding_service.embed_batch(
                [c.content for c in chunks]
            )
            
            # 存储向量
            vector_store.add_batch(chunks, embeddings, doc.category.value)
            
            total_chunks += len(chunks)
            added_docs += 1
        
        logger.info(f"处理了 {added_docs} 个文档，{total_chunks} 个分块")
        return {"added": added_docs, "chunks": total_chunks}
    
    # ==================== 检索与生成 ====================
    
    async def query(
        self,
        query: RAGQuery,
    ) -> RAGResponse:
        """执行 RAG 查询"""
        # 获取或创建会话
        session = None
        if query.session_id:
            session = self.conversation_manager.get_session(query.session_id)
            if session:
                # 添加用户消息
                session = self.conversation_manager.continue_conversation(
                    query.session_id, query.query
                )
        
        if not session and query.divination_type:
            # 创建新会话
            session = self.conversation_manager.start_conversation(
                divination_type=query.divination_type,
                context=query.divination_context,
            )
            session.add_message(MessageRole.USER, query.query)
        
        # 检索相关知识
        retrieval_results = await self._retrieve(query)
        
        # 生成回答
        config = GeneratorConfig(
            include_sources=query.include_sources,
            style="professional",
        )
        
        response = await self.generator.generate(
            query=query,
            retrieval_results=retrieval_results,
            session=session,
            config=config,
        )
        
        # 保存助手回复
        if session:
            self.conversation_manager.add_assistant_response(
                session.id,
                response.answer,
                {"sources_count": len(retrieval_results)},
            )
            response.session_id = session.id
        
        return response
    
    async def _retrieve(self, query: RAGQuery) -> List[RetrievalResult]:
        """执行检索"""
        all_results = []
        
        # 确定检索范围
        kb_ids = list(self._knowledge_bases.keys())
        
        config = RetrievalConfig(
            top_k=query.top_k,
            score_threshold=query.score_threshold,
            use_rerank=query.use_rerank,
            categories=query.categories,
        )
        
        # 从各知识库检索
        for kb_id in kb_ids:
            kb = self._knowledge_bases.get(kb_id)
            if not kb:
                continue
            
            # 分类过滤
            if query.categories:
                if kb.category.value not in query.categories:
                    continue
            
            vector_store = self.vector_store_manager.get_store(kb_id)
            retriever = SemanticRetriever(
                vector_store=vector_store,
                embedding_service=self.embedding_service,
            )
            
            results = await retriever.retrieve(query.query, config)
            all_results.extend(results)
        
        # 按分数排序并截取
        all_results.sort(key=lambda r: r.score, reverse=True)
        return all_results[:query.top_k]
    
    # ==================== 追问对话 ====================
    
    async def follow_up(
        self,
        session_id: str,
        message: str,
        include_sources: bool = True,
    ) -> RAGResponse:
        """追问"""
        session = self.conversation_manager.get_session(session_id)
        if not session:
            raise ValueError(f"会话不存在: {session_id}")
        
        if session.ended_at:
            raise ValueError(f"会话已结束: {session_id}")
        
        # 构建查询
        query = RAGQuery(
            query=message,
            session_id=session_id,
            divination_type=session.divination_type,
            divination_context=session.context,
            include_sources=include_sources,
        )
        
        return await self.query(query)
    
    def end_conversation(self, session_id: str) -> bool:
        """结束对话"""
        return self.conversation_manager.end_conversation(session_id)
    
    def get_conversation_history(self, session_id: str) -> List[Dict[str, Any]]:
        """获取对话历史"""
        session = self.conversation_manager.get_session(session_id)
        if not session:
            return []
        
        return [
            {
                "id": msg.id,
                "role": msg.role.value,
                "content": msg.content,
                "created_at": msg.created_at.isoformat(),
            }
            for msg in session.messages
        ]
    
    # ==================== 统计与管理 ====================
    
    def get_stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        vector_stats = self.vector_store_manager.get_stats()
        
        kb_stats = []
        for kb in self._knowledge_bases.values():
            kb_stat = kb.to_dict()
            kb_stat["vector_stats"] = vector_stats.get(kb.id, {})
            kb_stats.append(kb_stat)
        
        conversations = self.conversation_manager.list_conversations(
            include_ended=False
        )
        
        return {
            "knowledge_bases": kb_stats,
            "total_knowledge_bases": len(self._knowledge_bases),
            "active_conversations": len(conversations),
            "embedding_model": self.embedding_service.model.name,
            "embedding_dimension": self.embedding_service.dimension,
        }
    
    def _load_knowledge_bases_meta(self):
        """加载知识库元数据"""
        import json
        meta_file = self.data_path / "knowledge_bases_meta.json"
        
        if meta_file.exists():
            try:
                with open(meta_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                for kb_data in data.get("knowledge_bases", []):
                    kb = KnowledgeBase(
                        id=kb_data["id"],
                        name=kb_data["name"],
                        description=kb_data.get("description", ""),
                        category=KnowledgeCategory(kb_data.get("category", "general")),
                        document_count=kb_data.get("document_count", 0),
                        chunk_count=kb_data.get("chunk_count", 0),
                        embedding_model=kb_data.get("embedding_model", ""),
                        metadata=kb_data.get("metadata", {}),
                        created_at=datetime.fromisoformat(kb_data["created_at"]) if "created_at" in kb_data else datetime.now(),
                        updated_at=datetime.fromisoformat(kb_data["updated_at"]) if "updated_at" in kb_data else datetime.now(),
                    )
                    self._knowledge_bases[kb.id] = kb
                
                logger.info(f"加载了 {len(self._knowledge_bases)} 个知识库")
            except Exception as e:
                logger.warning(f"加载知识库元数据失败: {e}")
    
    def _save_knowledge_bases_meta(self):
        """保存知识库元数据"""
        import json
        meta_file = self.data_path / "knowledge_bases_meta.json"
        
        try:
            data = {
                "knowledge_bases": [kb.to_dict() for kb in self._knowledge_bases.values()],
                "updated_at": datetime.now().isoformat(),
            }
            with open(meta_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"保存知识库元数据失败: {e}")


# 全局单例
_rag_service: Optional[RAGService] = None


def get_rag_service() -> RAGService:
    """获取 RAG 服务单例"""
    global _rag_service
    if _rag_service is None:
        _rag_service = RAGService()
    return _rag_service


def init_rag_service(**kwargs) -> RAGService:
    """初始化 RAG 服务"""
    global _rag_service
    _rag_service = RAGService(**kwargs)
    return _rag_service

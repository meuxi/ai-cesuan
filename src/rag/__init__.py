"""
RAG (Retrieval-Augmented Generation) 知识库模块

完整的检索增强生成系统，支持：
- 多格式文档加载 (JSON, Markdown, TXT, PDF)
- 向量化存储与语义检索
- 上下文增强生成
- 追问对话与会话管理
- 知识库动态扩展

模块结构:
- models.py: 数据模型定义
- document_loader.py: 文档加载器
- embeddings.py: 向量嵌入服务
- vector_store.py: 向量存储
- retriever.py: 语义检索器
- generator.py: RAG 生成器
- conversation.py: 对话管理
- service.py: 统一服务层
"""

from .models import (
    Document,
    DocumentChunk,
    KnowledgeBase,
    RetrievalResult,
    ConversationMessage,
    ConversationSession,
    RAGQuery,
    RAGResponse,
)
from .service import RAGService, get_rag_service, init_rag_service
from .conversation import ConversationManager

__all__ = [
    # Models
    "Document",
    "DocumentChunk",
    "KnowledgeBase",
    "RetrievalResult",
    "ConversationMessage",
    "ConversationSession",
    "RAGQuery",
    "RAGResponse",
    # Services
    "RAGService",
    "ConversationManager",
    "get_rag_service",
    "init_rag_service",
]

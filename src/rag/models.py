"""
RAG 数据模型定义

定义知识库系统的所有数据结构
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import List, Dict, Any, Optional
import uuid


class DocumentType(Enum):
    """文档类型"""
    JSON = "json"
    MARKDOWN = "markdown"
    TEXT = "text"
    PDF = "pdf"
    HTML = "html"


class KnowledgeCategory(Enum):
    """知识分类"""
    BAZI = "bazi"              # 八字
    LIUYAO = "liuyao"          # 六爻
    TAROT = "tarot"            # 塔罗
    QIMEN = "qimen"            # 奇门遁甲
    ZIWEI = "ziwei"            # 紫微斗数
    MEIHUA = "meihua"          # 梅花易数
    XIAOLIU = "xiaoliu"        # 小六壬
    DALIUREN = "daliuren"      # 大六壬
    FENGSHUI = "fengshui"      # 风水
    WUXING = "wuxing"          # 五行
    TIANGAN_DIZHI = "tiangan_dizhi"  # 天干地支
    ZODIAC = "zodiac"          # 星座
    GENERAL = "general"        # 通用知识
    TERMINOLOGY = "terminology"  # 术语解释


@dataclass
class Document:
    """文档实体"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    title: str = ""
    content: str = ""
    doc_type: DocumentType = DocumentType.TEXT
    category: KnowledgeCategory = KnowledgeCategory.GENERAL
    source: str = ""                    # 来源文件路径
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "doc_type": self.doc_type.value,
            "category": self.category.value,
            "source": self.source,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Document":
        return cls(
            id=data.get("id", str(uuid.uuid4())),
            title=data.get("title", ""),
            content=data.get("content", ""),
            doc_type=DocumentType(data.get("doc_type", "text")),
            category=KnowledgeCategory(data.get("category", "general")),
            source=data.get("source", ""),
            metadata=data.get("metadata", {}),
            created_at=datetime.fromisoformat(data["created_at"]) if "created_at" in data else datetime.now(),
            updated_at=datetime.fromisoformat(data["updated_at"]) if "updated_at" in data else datetime.now(),
        )


@dataclass
class DocumentChunk:
    """文档分块"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    document_id: str = ""
    content: str = ""
    chunk_index: int = 0
    embedding: Optional[List[float]] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "document_id": self.document_id,
            "content": self.content,
            "chunk_index": self.chunk_index,
            "embedding": self.embedding,
            "metadata": self.metadata,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "DocumentChunk":
        return cls(
            id=data.get("id", str(uuid.uuid4())),
            document_id=data.get("document_id", ""),
            content=data.get("content", ""),
            chunk_index=data.get("chunk_index", 0),
            embedding=data.get("embedding"),
            metadata=data.get("metadata", {}),
        )


@dataclass
class KnowledgeBase:
    """知识库"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    description: str = ""
    category: KnowledgeCategory = KnowledgeCategory.GENERAL
    document_count: int = 0
    chunk_count: int = 0
    embedding_model: str = "text-embedding-3-small"
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "category": self.category.value,
            "document_count": self.document_count,
            "chunk_count": self.chunk_count,
            "embedding_model": self.embedding_model,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }


@dataclass
class RetrievalResult:
    """检索结果"""
    chunk: DocumentChunk
    score: float                        # 相似度分数 0-1
    document: Optional[Document] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "chunk_id": self.chunk.id,
            "content": self.chunk.content,
            "score": self.score,
            "document_id": self.chunk.document_id,
            "metadata": self.chunk.metadata,
        }


class MessageRole(Enum):
    """消息角色"""
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


@dataclass
class ConversationMessage:
    """对话消息"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    session_id: str = ""
    role: MessageRole = MessageRole.USER
    content: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "session_id": self.session_id,
            "role": self.role.value,
            "content": self.content,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat(),
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ConversationMessage":
        return cls(
            id=data.get("id", str(uuid.uuid4())),
            session_id=data.get("session_id", ""),
            role=MessageRole(data.get("role", "user")),
            content=data.get("content", ""),
            metadata=data.get("metadata", {}),
            created_at=datetime.fromisoformat(data["created_at"]) if "created_at" in data else datetime.now(),
        )


@dataclass
class ConversationSession:
    """对话会话"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    divination_type: str = ""           # 占卜类型
    divination_id: Optional[str] = None # 关联的占卜记录ID
    context: Dict[str, Any] = field(default_factory=dict)  # 占卜上下文
    messages: List[ConversationMessage] = field(default_factory=list)
    max_history: int = 20               # 最大历史消息数
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    ended_at: Optional[datetime] = None
    
    def add_message(self, role: MessageRole, content: str, metadata: Dict[str, Any] = None) -> ConversationMessage:
        """添加消息"""
        message = ConversationMessage(
            session_id=self.id,
            role=role,
            content=content,
            metadata=metadata or {},
        )
        self.messages.append(message)
        self.updated_at = datetime.now()
        
        # 保持历史消息在限制内
        if len(self.messages) > self.max_history:
            self.messages = self.messages[-self.max_history:]
        
        return message
    
    def get_history_for_prompt(self, include_system: bool = False) -> List[Dict[str, str]]:
        """获取用于提示词的历史消息"""
        history = []
        for msg in self.messages:
            if msg.role == MessageRole.SYSTEM and not include_system:
                continue
            history.append({
                "role": msg.role.value,
                "content": msg.content,
            })
        return history
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "divination_type": self.divination_type,
            "divination_id": self.divination_id,
            "context": self.context,
            "messages": [m.to_dict() for m in self.messages],
            "max_history": self.max_history,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "ended_at": self.ended_at.isoformat() if self.ended_at else None,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ConversationSession":
        session = cls(
            id=data.get("id", str(uuid.uuid4())),
            divination_type=data.get("divination_type", ""),
            divination_id=data.get("divination_id"),
            context=data.get("context", {}),
            max_history=data.get("max_history", 20),
            created_at=datetime.fromisoformat(data["created_at"]) if "created_at" in data else datetime.now(),
            updated_at=datetime.fromisoformat(data["updated_at"]) if "updated_at" in data else datetime.now(),
            ended_at=datetime.fromisoformat(data["ended_at"]) if data.get("ended_at") else None,
        )
        session.messages = [ConversationMessage.from_dict(m) for m in data.get("messages", [])]
        return session


@dataclass
class RAGQuery:
    """RAG 查询请求"""
    query: str                          # 用户问题
    session_id: Optional[str] = None    # 会话ID (追问时必填)
    divination_type: Optional[str] = None  # 占卜类型
    divination_context: Optional[Dict[str, Any]] = None  # 占卜上下文
    categories: Optional[List[str]] = None  # 限定知识分类
    top_k: int = 5                      # 检索数量
    score_threshold: float = 0.5        # 相似度阈值
    use_rerank: bool = True             # 是否使用重排序
    include_sources: bool = True        # 是否返回来源


@dataclass
class RAGResponse:
    """RAG 响应"""
    answer: str                         # AI回答
    session_id: str                     # 会话ID
    sources: List[RetrievalResult] = field(default_factory=list)  # 引用来源
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "answer": self.answer,
            "session_id": self.session_id,
            "sources": [s.to_dict() for s in self.sources] if self.sources else [],
            "metadata": self.metadata,
        }

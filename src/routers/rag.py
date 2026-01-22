"""
RAG 知识库 API 路由

提供知识库管理、文档管理、检索和对话的 RESTful API
"""

from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
import logging

from ..rag import RAGService, get_rag_service, init_rag_service
from ..rag.models import KnowledgeCategory, RAGQuery

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/rag", tags=["RAG知识库"])


# ==================== 请求/响应模型 ====================

class CreateKnowledgeBaseRequest(BaseModel):
    """创建知识库请求"""
    name: str = Field(..., description="知识库名称")
    description: str = Field("", description="知识库描述")
    category: str = Field("general", description="知识分类")


class AddDocumentRequest(BaseModel):
    """添加文档请求"""
    title: str = Field(..., description="文档标题")
    content: str = Field(..., description="文档内容")
    category: Optional[str] = Field(None, description="分类（可选）")
    metadata: Optional[Dict[str, Any]] = Field(None, description="元数据")


class AddDocumentsBatchRequest(BaseModel):
    """批量添加文档请求"""
    documents: List[Dict[str, Any]] = Field(..., description="文档列表")


class AddFromDirectoryRequest(BaseModel):
    """从目录添加文档请求"""
    directory: str = Field(..., description="目录路径")
    recursive: bool = Field(True, description="是否递归")


class QueryRequest(BaseModel):
    """查询请求"""
    query: str = Field(..., description="查询问题")
    session_id: Optional[str] = Field(None, description="会话ID（追问时使用）")
    divination_type: Optional[str] = Field(None, description="占卜类型")
    divination_context: Optional[Dict[str, Any]] = Field(None, description="占卜上下文")
    categories: Optional[List[str]] = Field(None, description="限定知识分类")
    top_k: int = Field(5, description="返回结果数量")
    score_threshold: float = Field(0.5, description="相似度阈值")
    include_sources: bool = Field(True, description="是否返回来源")


class FollowUpRequest(BaseModel):
    """追问请求"""
    message: str = Field(..., description="追问内容")
    include_sources: bool = Field(True, description="是否返回来源")


class EndConversationRequest(BaseModel):
    """结束对话请求"""
    rating: Optional[float] = Field(None, description="评分（可选）")


# ==================== 知识库管理 ====================

@router.post("/knowledge-bases", summary="创建知识库")
async def create_knowledge_base(request: CreateKnowledgeBaseRequest):
    """创建新的知识库"""
    try:
        service = get_rag_service()
        category = KnowledgeCategory(request.category)
        kb = service.create_knowledge_base(
            name=request.name,
            description=request.description,
            category=category,
        )
        return {
            "success": True,
            "data": kb.to_dict(),
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"创建知识库失败: {e}")
        raise HTTPException(status_code=500, detail="创建知识库失败")


@router.get("/knowledge-bases", summary="列出知识库")
async def list_knowledge_bases():
    """获取所有知识库列表"""
    service = get_rag_service()
    kbs = service.list_knowledge_bases()
    return {
        "success": True,
        "data": [kb.to_dict() for kb in kbs],
        "total": len(kbs),
    }


@router.get("/knowledge-bases/{kb_id}", summary="获取知识库详情")
async def get_knowledge_base(kb_id: str):
    """获取指定知识库的详细信息"""
    service = get_rag_service()
    kb = service.get_knowledge_base(kb_id)
    if not kb:
        raise HTTPException(status_code=404, detail="知识库不存在")
    return {
        "success": True,
        "data": kb.to_dict(),
    }


@router.delete("/knowledge-bases/{kb_id}", summary="删除知识库")
async def delete_knowledge_base(kb_id: str):
    """删除指定知识库"""
    service = get_rag_service()
    success = service.delete_knowledge_base(kb_id)
    if not success:
        raise HTTPException(status_code=404, detail="知识库不存在")
    return {
        "success": True,
        "message": "知识库已删除",
    }


# ==================== 文档管理 ====================

@router.post("/knowledge-bases/{kb_id}/documents", summary="添加文档")
async def add_document(kb_id: str, request: AddDocumentRequest):
    """向知识库添加单个文档"""
    try:
        service = get_rag_service()
        category = KnowledgeCategory(request.category) if request.category else None
        result = await service.add_document(
            kb_id=kb_id,
            title=request.title,
            content=request.content,
            category=category,
            metadata=request.metadata,
        )
        return {
            "success": True,
            "data": result,
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"添加文档失败: {e}")
        raise HTTPException(status_code=500, detail="添加文档失败")


@router.post("/knowledge-bases/{kb_id}/documents/batch", summary="批量添加文档")
async def add_documents_batch(kb_id: str, request: AddDocumentsBatchRequest):
    """向知识库批量添加文档"""
    try:
        service = get_rag_service()
        result = await service.add_documents_batch(kb_id, request.documents)
        return {
            "success": True,
            "data": result,
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"批量添加文档失败: {e}")
        raise HTTPException(status_code=500, detail="批量添加文档失败")


@router.post("/knowledge-bases/{kb_id}/documents/from-directory", summary="从目录添加文档")
async def add_documents_from_directory(kb_id: str, request: AddFromDirectoryRequest):
    """从目录加载并添加文档到知识库"""
    try:
        service = get_rag_service()
        result = await service.add_documents_from_directory(
            kb_id=kb_id,
            directory=request.directory,
            recursive=request.recursive,
        )
        return {
            "success": True,
            "data": result,
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="目录不存在")
    except Exception as e:
        logger.error(f"从目录添加文档失败: {e}")
        raise HTTPException(status_code=500, detail="添加文档失败")


# ==================== 检索与生成 ====================

@router.post("/query", summary="RAG查询")
async def rag_query(request: QueryRequest):
    """
    执行 RAG 查询
    
    - 如果提供 session_id，则为追问模式
    - 如果提供 divination_type，会自动创建新会话
    """
    try:
        service = get_rag_service()
        
        query = RAGQuery(
            query=request.query,
            session_id=request.session_id,
            divination_type=request.divination_type,
            divination_context=request.divination_context,
            categories=request.categories,
            top_k=request.top_k,
            score_threshold=request.score_threshold,
            include_sources=request.include_sources,
        )
        
        response = await service.query(query)
        
        return {
            "success": True,
            "data": response.to_dict(),
        }
    except Exception as e:
        logger.error(f"RAG查询失败: {e}")
        raise HTTPException(status_code=500, detail="查询失败")


@router.post("/conversations/{session_id}/follow-up", summary="追问")
async def follow_up(session_id: str, request: FollowUpRequest):
    """在已有会话中追问"""
    try:
        service = get_rag_service()
        response = await service.follow_up(
            session_id=session_id,
            message=request.message,
            include_sources=request.include_sources,
        )
        return {
            "success": True,
            "data": response.to_dict(),
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"追问失败: {e}")
        raise HTTPException(status_code=500, detail="追问失败")


# ==================== 对话管理 ====================

@router.get("/conversations", summary="列出对话")
async def list_conversations(
    divination_type: Optional[str] = None,
    include_ended: bool = False,
):
    """获取对话列表"""
    service = get_rag_service()
    conversations = service.conversation_manager.list_conversations(
        divination_type=divination_type,
        include_ended=include_ended,
    )
    return {
        "success": True,
        "data": conversations,
        "total": len(conversations),
    }


@router.get("/conversations/{session_id}", summary="获取对话详情")
async def get_conversation(session_id: str):
    """获取指定对话的详细信息和历史"""
    service = get_rag_service()
    session = service.conversation_manager.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="对话不存在")
    
    history = service.get_conversation_history(session_id)
    
    return {
        "success": True,
        "data": {
            "session": session.to_dict(),
            "history": history,
        },
    }


@router.post("/conversations/{session_id}/end", summary="结束对话")
async def end_conversation(session_id: str, request: EndConversationRequest = None):
    """结束指定对话"""
    service = get_rag_service()
    success = service.end_conversation(session_id)
    if not success:
        raise HTTPException(status_code=404, detail="对话不存在")
    return {
        "success": True,
        "message": "对话已结束",
    }


@router.delete("/conversations/{session_id}", summary="删除对话")
async def delete_conversation(session_id: str):
    """删除指定对话"""
    service = get_rag_service()
    success = service.conversation_manager.store.delete_session(session_id)
    if not success:
        raise HTTPException(status_code=404, detail="对话不存在")
    return {
        "success": True,
        "message": "对话已删除",
    }


# ==================== 统计信息 ====================

@router.get("/stats", summary="获取统计信息")
async def get_stats():
    """获取 RAG 系统统计信息"""
    service = get_rag_service()
    stats = service.get_stats()
    return {
        "success": True,
        "data": stats,
    }


# ==================== 知识分类 ====================

@router.get("/categories", summary="获取知识分类列表")
async def get_categories():
    """获取所有可用的知识分类"""
    categories = [
        {"value": cat.value, "label": cat.name}
        for cat in KnowledgeCategory
    ]
    return {
        "success": True,
        "data": categories,
    }

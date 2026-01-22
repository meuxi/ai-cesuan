"""
提示词模板 API 路由
参考方案中的路由设计
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict, Any

from ..prompts import (
    PromptTemplate,
    PromptCategory,
    PromptStatus,
    get_prompt_manager,
)

router = APIRouter(prefix="/prompts", tags=["提示词模板"])


class PromptTemplateCreate(BaseModel):
    """创建提示词模板请求"""
    id: str
    name: str
    category: str
    system_prompt: str
    user_prompt_template: str
    description: str = ""


class PromptTemplateUpdate(BaseModel):
    """更新提示词模板请求"""
    name: Optional[str] = None
    system_prompt: Optional[str] = None
    user_prompt_template: Optional[str] = None
    description: Optional[str] = None
    change_log: str = ""


class PromptRenderRequest(BaseModel):
    """渲染模板请求"""
    variables: Dict[str, Any]


class PromptScoreRequest(BaseModel):
    """设置评分请求"""
    score: float


@router.get("/")
async def list_templates(
    category: Optional[str] = None,
    status: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    获取提示词模板列表
    
    - **category**: 按分类筛选
    - **status**: 按状态筛选 (draft/active/deprecated)
    """
    manager = get_prompt_manager()
    templates = manager.list_all()
    
    if category:
        try:
            cat = PromptCategory(category)
            templates = [t for t in templates if t.category == cat]
        except ValueError:
            pass
    
    if status:
        try:
            st = PromptStatus(status)
            templates = [t for t in templates if t.status == st]
        except ValueError:
            pass
    
    return [t.to_dict() for t in templates]


@router.post("/")
async def create_template(request: PromptTemplateCreate) -> Dict[str, Any]:
    """创建新的提示词模板"""
    manager = get_prompt_manager()
    
    try:
        category = PromptCategory(request.category)
    except ValueError:
        raise HTTPException(status_code=400, detail=f"无效的分类: {request.category}")
    
    template = PromptTemplate(
        id=request.id,
        name=request.name,
        category=category,
        system_prompt=request.system_prompt,
        user_prompt_template=request.user_prompt_template,
        description=request.description,
    )
    
    try:
        created = manager.create(template)
        return created.to_dict()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{template_id}")
async def get_template(template_id: str) -> Dict[str, Any]:
    """获取单个提示词模板"""
    manager = get_prompt_manager()
    template = manager.get(template_id)
    
    if not template:
        raise HTTPException(status_code=404, detail=f"模板 {template_id} 不存在")
    
    return template.to_dict()


@router.put("/{template_id}")
async def update_template(
    template_id: str, 
    request: PromptTemplateUpdate
) -> Dict[str, Any]:
    """更新提示词模板"""
    manager = get_prompt_manager()
    
    updates = {k: v for k, v in request.dict().items() if v is not None and k != "change_log"}
    
    try:
        updated = manager.update(template_id, updates, request.change_log)
        return updated.to_dict()
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{template_id}")
async def delete_template(template_id: str) -> Dict[str, str]:
    """删除提示词模板"""
    manager = get_prompt_manager()
    
    if manager.delete(template_id):
        return {"message": f"模板 {template_id} 已删除"}
    else:
        raise HTTPException(status_code=404, detail=f"模板 {template_id} 不存在")


@router.post("/{template_id}/activate")
async def activate_template(template_id: str) -> Dict[str, Any]:
    """激活提示词模板"""
    manager = get_prompt_manager()
    
    try:
        activated = manager.activate(template_id)
        return activated.to_dict()
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/{template_id}/deprecate")
async def deprecate_template(template_id: str) -> Dict[str, Any]:
    """废弃提示词模板"""
    manager = get_prompt_manager()
    
    try:
        deprecated = manager.deprecate(template_id)
        return deprecated.to_dict()
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/{template_id}/versions")
async def get_template_versions(template_id: str) -> List[Dict[str, Any]]:
    """获取模板的版本历史"""
    manager = get_prompt_manager()
    versions = manager.get_versions(template_id)
    
    if not versions:
        raise HTTPException(status_code=404, detail=f"模板 {template_id} 不存在或无版本历史")
    
    return [
        {
            "version": v.version,
            "created_at": v.created_at.isoformat(),
            "change_log": v.change_log,
        }
        for v in versions
    ]


@router.post("/{template_id}/render")
async def render_template(
    template_id: str, 
    request: PromptRenderRequest
) -> Dict[str, str]:
    """
    渲染模板
    
    将变量替换到模板中，返回最终的 system_prompt 和 user_prompt
    """
    manager = get_prompt_manager()
    
    try:
        rendered = manager.render_template(template_id, request.variables)
        return rendered
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/{template_id}/score")
async def set_template_score(
    template_id: str, 
    request: PromptScoreRequest
) -> Dict[str, Any]:
    """设置模板效果评分"""
    manager = get_prompt_manager()
    
    try:
        updated = manager.set_score(template_id, request.score)
        return updated.to_dict()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/category/{category}/best")
async def get_best_template(category: str) -> Dict[str, Any]:
    """获取某分类下效果最好的激活模板"""
    manager = get_prompt_manager()
    
    try:
        cat = PromptCategory(category)
    except ValueError:
        raise HTTPException(status_code=400, detail=f"无效的分类: {category}")
    
    template = manager.get_best(cat)
    
    if not template:
        raise HTTPException(status_code=404, detail=f"分类 {category} 下没有激活的模板")
    
    return template.to_dict()

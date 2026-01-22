"""
提示词模板管理器
参考 zhanwen 的 PromptTemplateService 设计
"""

import json
import logging
from typing import Dict, List, Optional
from pathlib import Path
from datetime import datetime

from .models import PromptTemplate, PromptCategory, PromptStatus, PromptVersion

logger = logging.getLogger(__name__)


class PromptTemplateManager:
    """
    提示词模板管理器
    支持 CRUD、版本控制、分类管理
    """
    
    def __init__(self, storage_path: Optional[str] = None):
        """
        Args:
            storage_path: 存储路径，默认使用内存存储
        """
        self._templates: Dict[str, PromptTemplate] = {}
        self._versions: Dict[str, List[PromptVersion]] = {}
        self._storage_path = Path(storage_path) if storage_path else None
        
        if self._storage_path and self._storage_path.exists():
            self._load_from_file()
    
    def create(self, template: PromptTemplate) -> PromptTemplate:
        """创建模板"""
        if template.id in self._templates:
            raise ValueError(f"模板 {template.id} 已存在")
        
        template.created_at = datetime.now()
        template.updated_at = datetime.now()
        
        self._templates[template.id] = template
        self._versions[template.id] = [
            PromptVersion(
                template_id=template.id,
                version=template.version,
                system_prompt=template.system_prompt,
                user_prompt_template=template.user_prompt_template,
                change_log="初始创建"
            )
        ]
        
        self._save_to_file()
        logger.info(f"创建提示词模板: {template.id}")
        return template
    
    def get(self, template_id: str) -> Optional[PromptTemplate]:
        """获取模板"""
        return self._templates.get(template_id)
    
    def get_template(self, template_id: str) -> Optional[PromptTemplate]:
        """获取模板（get的别名，兼容旧接口调用）"""
        return self.get(template_id)
    
    def get_by_category(self, category: PromptCategory) -> List[PromptTemplate]:
        """按分类获取模板"""
        return [t for t in self._templates.values() if t.category == category]
    
    def get_active(self, category: Optional[PromptCategory] = None) -> List[PromptTemplate]:
        """获取激活的模板"""
        templates = self._templates.values()
        if category:
            templates = [t for t in templates if t.category == category]
        return [t for t in templates if t.status == PromptStatus.ACTIVE]
    
    def get_best(self, category: PromptCategory) -> Optional[PromptTemplate]:
        """获取某分类下效果最好的激活模板"""
        active_templates = self.get_active(category)
        if not active_templates:
            return None
        return max(active_templates, key=lambda t: t.effectiveness_score)
    
    def list_all(self) -> List[PromptTemplate]:
        """列出所有模板"""
        return list(self._templates.values())
    
    def update(
        self, 
        template_id: str, 
        updates: Dict, 
        change_log: str = ""
    ) -> PromptTemplate:
        """
        更新模板
        
        Args:
            template_id: 模板ID
            updates: 更新内容
            change_log: 变更日志
        
        Returns:
            更新后的模板
        """
        template = self._templates.get(template_id)
        if not template:
            raise ValueError(f"模板 {template_id} 不存在")
        
        # 检查是否需要升级版本（system_prompt 或 user_prompt_template 变化）
        need_version_up = (
            "system_prompt" in updates and updates["system_prompt"] != template.system_prompt
        ) or (
            "user_prompt_template" in updates and updates["user_prompt_template"] != template.user_prompt_template
        )
        
        # 更新字段
        for key, value in updates.items():
            if hasattr(template, key):
                setattr(template, key, value)
        
        template.updated_at = datetime.now()
        
        # 版本升级
        if need_version_up:
            template.version += 1
            self._versions[template_id].append(
                PromptVersion(
                    template_id=template_id,
                    version=template.version,
                    system_prompt=template.system_prompt,
                    user_prompt_template=template.user_prompt_template,
                    change_log=change_log or f"更新到版本 {template.version}"
                )
            )
        
        self._save_to_file()
        logger.info(f"更新提示词模板: {template_id}, 版本: {template.version}")
        return template
    
    def delete(self, template_id: str) -> bool:
        """删除模板"""
        if template_id not in self._templates:
            return False
        
        del self._templates[template_id]
        if template_id in self._versions:
            del self._versions[template_id]
        
        self._save_to_file()
        logger.info(f"删除提示词模板: {template_id}")
        return True
    
    def activate(self, template_id: str) -> PromptTemplate:
        """激活模板"""
        return self.update(template_id, {"status": PromptStatus.ACTIVE})
    
    def deprecate(self, template_id: str) -> PromptTemplate:
        """废弃模板"""
        return self.update(template_id, {"status": PromptStatus.DEPRECATED})
    
    def get_versions(self, template_id: str) -> List[PromptVersion]:
        """获取模板的版本历史"""
        return self._versions.get(template_id, [])
    
    def set_score(self, template_id: str, score: float) -> PromptTemplate:
        """设置效果评分"""
        if score < 0 or score > 10:
            raise ValueError("评分必须在 0-10 之间")
        return self.update(template_id, {"effectiveness_score": score})
    
    def render_template(
        self, 
        template_id: str, 
        variables: Dict
    ) -> Dict[str, str]:
        """
        渲染模板
        
        Args:
            template_id: 模板ID
            variables: 变量字典
        
        Returns:
            {"system_prompt": "...", "user_prompt": "..."}
        """
        template = self.get(template_id)
        if not template:
            raise ValueError(f"模板 {template_id} 不存在")
        return template.render(variables)
    
    def _save_to_file(self):
        """保存到文件"""
        if not self._storage_path:
            return
        
        data = {
            "templates": {k: v.to_dict() for k, v in self._templates.items()},
            "versions": {
                k: [
                    {
                        "template_id": v.template_id,
                        "version": v.version,
                        "system_prompt": v.system_prompt,
                        "user_prompt_template": v.user_prompt_template,
                        "created_at": v.created_at.isoformat(),
                        "change_log": v.change_log,
                    }
                    for v in versions
                ]
                for k, versions in self._versions.items()
            }
        }
        
        self._storage_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self._storage_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def _load_from_file(self):
        """从文件加载"""
        if not self._storage_path or not self._storage_path.exists():
            return
        
        try:
            with open(self._storage_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            for template_data in data.get("templates", {}).values():
                template = PromptTemplate.from_dict(template_data)
                self._templates[template.id] = template
            
            for template_id, versions_data in data.get("versions", {}).items():
                self._versions[template_id] = [
                    PromptVersion(
                        template_id=v["template_id"],
                        version=v["version"],
                        system_prompt=v["system_prompt"],
                        user_prompt_template=v["user_prompt_template"],
                        change_log=v.get("change_log", ""),
                    )
                    for v in versions_data
                ]
            
            logger.info(f"从文件加载 {len(self._templates)} 个提示词模板")
        except Exception as e:
            logger.error(f"加载提示词模板失败: {e}")
    
    def import_builtin_templates(self, templates: List[PromptTemplate]):
        """导入内置模板"""
        for template in templates:
            if template.id not in self._templates:
                self.create(template)


# 全局管理器实例
_default_manager: Optional[PromptTemplateManager] = None


def get_prompt_manager() -> PromptTemplateManager:
    """获取全局提示词管理器"""
    global _default_manager
    if _default_manager is None:
        _default_manager = PromptTemplateManager()
        # 导入内置模板
        from .templates import BUILTIN_TEMPLATES
        _default_manager.import_builtin_templates(BUILTIN_TEMPLATES)
    return _default_manager


def set_prompt_manager(manager: PromptTemplateManager):
    """设置全局提示词管理器"""
    global _default_manager
    _default_manager = manager

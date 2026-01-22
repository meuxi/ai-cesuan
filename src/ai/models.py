"""
AI 模型配置管理
参考 zhanwen 项目的数据模型设计
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from enum import Enum


class ModelStatus(Enum):
    """模型状态"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    DEPRECATED = "deprecated"


@dataclass
class AIModel:
    """AI 模型配置"""
    name: str                          # 模型名称
    provider: str                      # Provider 类型
    api_key: str = ""                  # API 密钥
    base_url: Optional[str] = None     # 自定义 API 地址
    status: ModelStatus = ModelStatus.ACTIVE
    is_primary: bool = False           # 是否为主模型
    cost_per_1k_tokens: float = 0.0    # 每千 Token 成本
    parameters: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "provider": self.provider,
            "base_url": self.base_url,
            "status": self.status.value,
            "is_primary": self.is_primary,
            "cost_per_1k_tokens": self.cost_per_1k_tokens,
            "parameters": self.parameters,
        }


@dataclass
class AIModelConfig:
    """AI 模型配置管理器"""
    primary: Optional[AIModel] = None
    backups: List[AIModel] = field(default_factory=list)
    
    def add_model(self, model: AIModel):
        """添加模型"""
        if model.is_primary:
            self.primary = model
        else:
            self.backups.append(model)
    
    def get_active_models(self) -> List[AIModel]:
        """获取所有活跃的模型（按优先级排序）"""
        models = []
        if self.primary and self.primary.status == ModelStatus.ACTIVE:
            models.append(self.primary)
        
        for backup in self.backups:
            if backup.status == ModelStatus.ACTIVE:
                models.append(backup)
        
        return models
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "primary": self.primary.to_dict() if self.primary else None,
            "backups": [m.to_dict() for m in self.backups],
        }


# 预设的模型线路配置（参考 Diviner 项目）
PRESET_ROUTES = {
    # 主线路（ModelScope）
    1: AIModel(
        name="DeepSeek-V3",
        provider="modelscope",
        is_primary=True,
        parameters={"model": "deepseek-ai/DeepSeek-V3.2"}
    ),
    2: AIModel(
        name="Qwen3-80B",
        provider="modelscope",
        parameters={"model": "Qwen/Qwen3-Next-80B-A3B-Instruct"}
    ),
    3: AIModel(
        name="DeepSeek-R1",
        provider="modelscope",
        parameters={"model": "deepseek-ai/DeepSeek-R1-0528"}
    ),
    4: AIModel(
        name="Qwen3-235B",
        provider="modelscope",
        parameters={"model": "Qwen/Qwen3-235B-A22B"}
    ),
    # 备用线路
    5: AIModel(
        name="备用-DeepSeek",
        provider="openai",
        base_url="https://apis.iflow.cn/v1",
        parameters={"model": "deepseek-v3"}
    ),
    6: AIModel(
        name="备用-Qwen3",
        provider="openai",
        base_url="https://apis.iflow.cn/v1",
        parameters={"model": "qwen3-235b"}
    ),
}


def get_route_mapping() -> Dict[int, Dict[str, Any]]:
    """获取线路切换映射（参考 Diviner）"""
    return {
        1: {"backup": 5, "next": 2, "backup_label": "备用1", "next_label": "线路2"},
        5: {"backup": 2, "next": 6, "backup_label": "线路2", "next_label": "备用2"},
        2: {"backup": 6, "next": 3, "backup_label": "备用2", "next_label": "线路3"},
        6: {"backup": 3, "next": 7, "backup_label": "线路3", "next_label": "备用3"},
        3: {"backup": 7, "next": 4, "backup_label": "备用3", "next_label": "线路4"},
        7: {"backup": 4, "next": 8, "backup_label": "线路4", "next_label": "备用4"},
        4: {"backup": 8, "next": 1, "backup_label": "备用4", "next_label": "线路1"},
        8: {"backup": 1, "next": 5, "backup_label": "线路1", "next_label": "备用1"},
    }

"""
提示词模板数据模型
参考 zhanwen 项目的数据模型设计
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
import re


class PromptCategory(Enum):
    """提示词分类"""
    GENERAL = "general"         # 通用
    BAZI = "bazi"               # 八字
    LIUYAO = "liuyao"           # 六爻
    TAROT = "tarot"             # 塔罗
    QIMEN = "qimen"             # 奇门遁甲
    DALIUREN = "daliuren"       # 大六壬
    MEIHUA = "meihua"           # 梅花易数
    ZIWEI = "ziwei"             # 紫微斗数
    XIAOLIU = "xiaoliu"         # 小六壬
    CHOUQIAN = "chouqian"       # 抽签
    LIFE_KLINE = "life_kline"   # 人生K线
    DREAM = "dream"             # 周公解梦
    NAME = "name"               # 姓名测算
    NEW_NAME = "new_name"       # 起名
    FATE = "fate"               # 缘分测算
    ZHUGE = "zhuge"             # 诸葛神算
    HEHUN = "hehun"             # 八字合婚
    FORTUNE = "fortune"         # 运势类（每日/每周/每月）
    ZODIAC = "zodiac"           # 星座运势


class PromptStatus(Enum):
    """提示词状态"""
    DRAFT = "draft"             # 草稿
    ACTIVE = "active"           # 激活
    DEPRECATED = "deprecated"   # 已废弃


@dataclass
class PromptTemplate:
    """提示词模板"""
    id: str                                    # 唯一标识
    name: str                                  # 模板名称
    category: PromptCategory                   # 分类
    system_prompt: str                         # 系统提示词
    user_prompt_template: str                  # 用户提示词模板
    variables: List[str] = field(default_factory=list)  # 变量列表
    version: int = 1                           # 版本号
    status: PromptStatus = PromptStatus.DRAFT  # 状态
    effectiveness_score: float = 0.0           # 效果评分 (0-10)
    description: str = ""                      # 描述
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        # 自动提取变量
        if not self.variables:
            self.variables = self._extract_variables()
    
    def _extract_variables(self) -> List[str]:
        """从模板中提取变量 (格式: {variable_name})"""
        pattern = r'\{(\w+)\}'
        all_vars = set()
        all_vars.update(re.findall(pattern, self.system_prompt))
        all_vars.update(re.findall(pattern, self.user_prompt_template))
        return list(all_vars)
    
    def render(self, variables: Dict[str, Any]) -> Dict[str, str]:
        """
        渲染模板，替换变量
        
        Args:
            variables: 变量字典
        
        Returns:
            {"system_prompt": "...", "user_prompt": "..."}
        """
        system = self.system_prompt
        user = self.user_prompt_template
        
        for key, value in variables.items():
            placeholder = "{" + key + "}"
            system = system.replace(placeholder, str(value))
            user = user.replace(placeholder, str(value))
        
        return {
            "system_prompt": system,
            "user_prompt": user
        }
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category.value,
            "system_prompt": self.system_prompt,
            "user_prompt_template": self.user_prompt_template,
            "variables": self.variables,
            "version": self.version,
            "status": self.status.value,
            "effectiveness_score": self.effectiveness_score,
            "description": self.description,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "metadata": self.metadata,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PromptTemplate":
        """从字典创建"""
        return cls(
            id=data["id"],
            name=data["name"],
            category=PromptCategory(data["category"]),
            system_prompt=data["system_prompt"],
            user_prompt_template=data["user_prompt_template"],
            variables=data.get("variables", []),
            version=data.get("version", 1),
            status=PromptStatus(data.get("status", "draft")),
            effectiveness_score=data.get("effectiveness_score", 0.0),
            description=data.get("description", ""),
            metadata=data.get("metadata", {}),
        )


@dataclass
class PromptVersion:
    """提示词版本记录"""
    template_id: str
    version: int
    system_prompt: str
    user_prompt_template: str
    created_at: datetime = field(default_factory=datetime.now)
    change_log: str = ""

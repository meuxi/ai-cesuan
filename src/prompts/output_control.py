"""
输出长度控制模块
根据不同场景和用户需求控制AI输出的长度和结构
"""
from enum import Enum
from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List
import logging

logger = logging.getLogger(__name__)


class OutputMode(Enum):
    """输出模式"""
    QUICK = "quick"        # 快速模式：简洁回复
    STANDARD = "standard"  # 标准模式：平衡详细度
    DETAILED = "detailed"  # 详细模式：完整分析


@dataclass
class OutputConfig:
    """输出配置"""
    mode: OutputMode = OutputMode.STANDARD
    min_chars: int = 800
    max_chars: int = 1200
    max_tokens: int = 800
    require_sections: List[str] = field(default_factory=list)
    forbid_sections: List[str] = field(default_factory=list)


# 预定义模式配置
MODE_CONFIGS: Dict[OutputMode, OutputConfig] = {
    OutputMode.QUICK: OutputConfig(
        mode=OutputMode.QUICK,
        min_chars=300,
        max_chars=500,
        max_tokens=400,
        require_sections=["核心结论"],
        forbid_sections=["详细分析", "历史背景", "延伸阅读"]
    ),
    OutputMode.STANDARD: OutputConfig(
        mode=OutputMode.STANDARD,
        min_chars=800,
        max_chars=1200,
        max_tokens=800,
        require_sections=["核心结论", "简要分析", "建议"],
        forbid_sections=["延伸阅读"]
    ),
    OutputMode.DETAILED: OutputConfig(
        mode=OutputMode.DETAILED,
        min_chars=2500,
        max_chars=5000,
        max_tokens=4000,
        require_sections=["核心结论", "详细分析", "深度解读", "量化评估", "应期推断", "建议", "注意事项"],
        forbid_sections=[]
    )
}

# 工具特定配置覆盖
TOOL_OUTPUT_OVERRIDES: Dict[str, Dict[OutputMode, Dict[str, Any]]] = {
    "bazi_analysis": {
        OutputMode.QUICK: {"max_chars": 600, "max_tokens": 500},
        OutputMode.DETAILED: {"max_chars": 3000, "max_tokens": 2000}
    },
    "tarot_reading": {
        OutputMode.QUICK: {"max_chars": 400, "max_tokens": 350},
        OutputMode.STANDARD: {"max_chars": 1000, "max_tokens": 700}
    },
    "liuyao_analysis": {
        OutputMode.STANDARD: {"max_chars": 2000, "max_tokens": 1500},
        OutputMode.DETAILED: {"max_chars": 6000, "max_tokens": 5000, 
                              "require_sections": ["卦名与核心数据", "大师断语", "卦象总览", 
                                                   "六爻逐爻分析", "用神深度分析", "神系作用链推演",
                                                   "动爻变化详解", "世应关系深度分析", "应期精准推断",
                                                   "量化评估总表", "综合建议与指导"]}
    },
    "dream_divination": {
        OutputMode.QUICK: {"max_chars": 350, "max_tokens": 300}
    },
    "ziwei": {
        OutputMode.STANDARD: {"max_chars": 2500, "max_tokens": 2000},
        OutputMode.DETAILED: {"max_chars": 5000, "max_tokens": 4000}
    }
}


class OutputLengthController:
    """输出长度控制器"""
    
    def __init__(self):
        self._mode_configs = MODE_CONFIGS.copy()
        self._tool_overrides = TOOL_OUTPUT_OVERRIDES.copy()
    
    def get_config(self, mode: OutputMode, tool_name: str = None) -> OutputConfig:
        """
        获取输出配置
        如果指定了工具名，会应用工具特定的覆盖配置
        """
        base_config = self._mode_configs.get(mode, MODE_CONFIGS[OutputMode.STANDARD])
        
        # 创建新配置以避免修改原配置
        config = OutputConfig(
            mode=base_config.mode,
            min_chars=base_config.min_chars,
            max_chars=base_config.max_chars,
            max_tokens=base_config.max_tokens,
            require_sections=base_config.require_sections.copy(),
            forbid_sections=base_config.forbid_sections.copy()
        )
        
        # 应用工具特定覆盖
        if tool_name and tool_name in self._tool_overrides:
            tool_config = self._tool_overrides[tool_name]
            if mode in tool_config:
                overrides = tool_config[mode]
                for key, value in overrides.items():
                    if hasattr(config, key):
                        setattr(config, key, value)
        
        return config
    
    def build_length_constraint_prompt(self, config: OutputConfig) -> str:
        """构建长度约束提示词"""
        constraints = []
        
        # 字数约束
        constraints.append(
            f"【输出要求】请将回复控制在 {config.min_chars}-{config.max_chars} 字之间。"
        )
        
        # 必须包含的部分
        if config.require_sections:
            sections_str = "、".join(config.require_sections)
            constraints.append(f"必须包含以下部分：{sections_str}。")
        
        # 禁止包含的部分
        if config.forbid_sections:
            sections_str = "、".join(config.forbid_sections)
            constraints.append(f"请勿包含以下内容：{sections_str}。")
        
        # 模式特定指导
        if config.mode == OutputMode.QUICK:
            constraints.append("请直奔主题，给出核心结论和最重要的建议即可。")
        elif config.mode == OutputMode.DETAILED:
            constraints.append("请进行深入全面的分析，提供详尽的解读和具体可行的建议。")
        
        return "\n".join(constraints)
    
    def enhance_prompt(self, original_prompt: str, mode: OutputMode,
                       tool_name: str = None) -> str:
        """
        增强原始提示词，添加输出长度控制
        """
        config = self.get_config(mode, tool_name)
        constraint_prompt = self.build_length_constraint_prompt(config)
        
        # 在原始提示词末尾添加约束
        enhanced = f"{original_prompt}\n\n{constraint_prompt}"
        
        return enhanced
    
    def get_max_tokens(self, mode: OutputMode, tool_name: str = None) -> int:
        """获取最大token数（用于API调用）"""
        config = self.get_config(mode, tool_name)
        return config.max_tokens
    
    def parse_mode(self, mode_str: str) -> OutputMode:
        """解析模式字符串"""
        mode_map = {
            "quick": OutputMode.QUICK,
            "fast": OutputMode.QUICK,
            "简洁": OutputMode.QUICK,
            "standard": OutputMode.STANDARD,
            "normal": OutputMode.STANDARD,
            "标准": OutputMode.STANDARD,
            "detailed": OutputMode.DETAILED,
            "full": OutputMode.DETAILED,
            "详细": OutputMode.DETAILED
        }
        return mode_map.get(mode_str.lower(), OutputMode.STANDARD)
    
    def register_tool_override(self, tool_name: str, mode: OutputMode,
                               overrides: Dict[str, Any]):
        """注册工具特定配置覆盖"""
        if tool_name not in self._tool_overrides:
            self._tool_overrides[tool_name] = {}
        self._tool_overrides[tool_name][mode] = overrides


# 全局单例
output_controller = OutputLengthController()


def enhance_prompt_with_length_control(prompt: str, mode: str = "standard",
                                        tool_name: str = None) -> str:
    """便捷函数：增强提示词"""
    output_mode = output_controller.parse_mode(mode)
    return output_controller.enhance_prompt(prompt, output_mode, tool_name)


def get_output_max_tokens(mode: str = "standard", tool_name: str = None) -> int:
    """便捷函数：获取最大token数"""
    output_mode = output_controller.parse_mode(mode)
    return output_controller.get_max_tokens(output_mode, tool_name)

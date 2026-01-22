"""
Token 计数与成本估算
参考 zhanwen 项目的 estimateTokensFromText 函数
"""

from typing import Optional


def estimate_tokens(text: str) -> int:
    """
    估算文本的 Token 数
    
    算法说明：
    - ASCII 字符：约 4 个字符 = 1 Token
    - CJK 字符（中日韩）：约 1 个字符 = 1 Token
    - 其他字符：约 2 个字符 = 1 Token
    
    Args:
        text: 待估算的文本
    
    Returns:
        估算的 Token 数
    """
    if not text or not isinstance(text, str):
        return 0
    
    text = text.strip()
    if not text:
        return 0
    
    ascii_count = 0
    cjk_count = 0
    other_count = 0
    
    for char in text:
        code = ord(char)
        
        # ASCII 字符
        if code <= 0x7F:
            ascii_count += 1
            continue
        
        # CJK 字符范围检测
        is_cjk = (
            (0x4E00 <= code <= 0x9FFF) or      # CJK 基本区
            (0x3400 <= code <= 0x4DBF) or      # CJK 扩展 A
            (0x20000 <= code <= 0x2A6DF) or    # CJK 扩展 B
            (0x2A700 <= code <= 0x2B73F) or    # CJK 扩展 C
            (0x2B740 <= code <= 0x2B81F) or    # CJK 扩展 D
            (0x2B820 <= code <= 0x2CEAF) or    # CJK 扩展 E
            (0xF900 <= code <= 0xFAFF) or      # CJK 兼容
            (0x2F800 <= code <= 0x2FA1F) or    # CJK 兼容扩展
            (0x3000 <= code <= 0x303F) or      # CJK 标点
            (0xFF00 <= code <= 0xFFEF)         # 全角字符
        )
        
        if is_cjk:
            cjk_count += 1
        else:
            other_count += 1
    
    # Token 估算
    estimated = cjk_count + (ascii_count // 4) + (other_count // 2)
    return max(1, estimated)


def estimate_cost(tokens: int, cost_per_1k: float) -> float:
    """
    估算 Token 成本
    
    Args:
        tokens: Token 数量
        cost_per_1k: 每千 Token 的成本
    
    Returns:
        估算成本（保留 6 位小数）
    """
    if tokens <= 0 or cost_per_1k <= 0:
        return 0.0
    
    cost = (tokens * cost_per_1k) / 1000
    return round(cost, 6)


def estimate_total_tokens(input_text: str, output_text: str) -> Optional[int]:
    """
    估算输入和输出的总 Token 数
    
    Args:
        input_text: 输入文本（包含 system prompt 和 user prompt）
        output_text: AI 输出文本
    
    Returns:
        总 Token 数，如果都为空则返回 None
    """
    input_tokens = estimate_tokens(input_text)
    output_tokens = estimate_tokens(output_text)
    
    total = input_tokens + output_tokens
    return total if total > 0 else None


# 常见模型的成本配置（每千 Token，单位：美元）
MODEL_COSTS = {
    # OpenAI
    "gpt-4": 0.03,
    "gpt-4-turbo": 0.01,
    "gpt-4o": 0.005,
    "gpt-4o-mini": 0.00015,
    "gpt-3.5-turbo": 0.0005,
    
    # Anthropic
    "claude-3-opus": 0.015,
    "claude-3-sonnet": 0.003,
    "claude-3-haiku": 0.00025,
    "claude-3.5-sonnet": 0.003,
    
    # DeepSeek
    "deepseek-chat": 0.00014,
    "deepseek-coder": 0.00014,
    "deepseek-v3": 0.00014,
    "deepseek-r1": 0.00055,
    
    # Gemini
    "gemini-pro": 0.0005,
    "gemini-1.5-pro": 0.00125,
    "gemini-1.5-flash": 0.000075,
    
    # Qwen (阿里通义)
    "qwen-turbo": 0.0008,
    "qwen-plus": 0.004,
    "qwen-max": 0.02,
}


def get_model_cost(model_name: str) -> float:
    """
    获取模型的每千 Token 成本
    
    Args:
        model_name: 模型名称
    
    Returns:
        每千 Token 成本，未知模型返回 0
    """
    model_lower = model_name.lower()
    
    # 精确匹配
    if model_lower in MODEL_COSTS:
        return MODEL_COSTS[model_lower]
    
    # 模糊匹配
    for key, cost in MODEL_COSTS.items():
        if key in model_lower or model_lower in key:
            return cost
    
    return 0.0

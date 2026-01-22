"""
诸葛神算类型定义
"""
from typing import TypedDict, Optional


class ZhugeInput(TypedDict):
    """诸葛神算输入"""
    char1: str              # 第一个字
    char2: str              # 第二个字
    char3: str              # 第三个字
    bihua1: int             # 第一个字笔画
    bihua2: int             # 第二个字笔画
    bihua3: int             # 第三个字笔画


class ZhugeResult(TypedDict):
    """诸葛神算结果"""
    success: bool           # 是否成功
    input: Optional[ZhugeInput]  # 输入信息
    qian_number: int        # 签号
    qian_id: str            # 签号ID（三位数字符串）
    title: str              # 签名
    content: str            # 签文内容

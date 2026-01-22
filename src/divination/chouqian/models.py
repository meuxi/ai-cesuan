"""抽签模型 - 完整移植自ASP源码"""
from pydantic import BaseModel
from typing import Literal, Optional
import random


# 支持的灵签类型
QianType = Literal["guanyin", "guandi", "lvzu", "tianhou", "huangdaxian", "zhuge"]


class ChouqianResult(BaseModel):
    """抽签结果"""
    id: int
    number: int
    title: str
    content: str
    image: str = ""
    type: str
    type_name: str
    # 黄大仙专用字段
    qianshu: str = ""  # 签属(上上签/上签/中签/下签等)
    name: str = ""     # 签名
    shi: str = ""      # 卦语/诗


class ChouqianRequest(BaseModel):
    """抽签请求"""
    type: QianType = "guanyin"
    user_name: str = ""
    question: str = ""


class ShengbeiResult(BaseModel):
    """圣杯结果 - 完整实现源码中的圣杯/笑杯机制
    
    规则(从guanyin.asp等移植)：
    1. 抽签后需连续掷出3次圣杯
    2. 圣杯概率3/4, 笑杯概率1/4
    3. 掷出笑杯此签无效需重新抽签
    4. 连续3次圣杯后才能查看签词
    """
    is_shengbei: bool      # True=圣杯, False=笑杯
    count: int             # 当前已掷圣杯次数
    is_complete: bool      # 是否完成3次圣杯
    is_failed: bool        # 是否失败(掷出笑杯)
    message: str           # 提示信息
    
    @staticmethod
    def throw() -> tuple:
        """掷圣杯
        
        Returns:
            (is_shengbei, message)
        """
        # 1/4概率笑杯(gysmile=4), 3/4概率圣杯
        result = random.randint(1, 4)
        if result == 4:
            return (False, "笑杯")
        return (True, "圣杯")


class ShengbeiSession(BaseModel):
    """圣杯会话状态"""
    qian_number: int           # 抽到的签号
    qian_type: str             # 签类型
    shengbei_count: int = 0    # 已掷圣杯次数
    is_complete: bool = False  # 是否完成
    is_failed: bool = False    # 是否失败
    history: list = []         # 掷杯历史

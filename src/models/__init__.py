"""
数据模型模块
"""
# 基础模型（用户、占卜请求等）
from .base import (
    SettingsInfo,
    OauthBody,
    User,
    NewName,
    PlumFlower,
    Fate,
    DivinationBody,
    BirthdayBody,
    CommonResponse,
)

# 占卜响应模型
from .divination_response import (
    # 基础模型
    TimeInfo,
    GanZhi,
    # 紫微
    ZiweiStar,
    ZiweiPalace,
    ZiweiPaipanResponse,
    # 奇门
    QimenGong,
    QimenPaipanResponse,
    # 大六壬
    DaliurenSike,
    DaliurenSanchuan,
    DaliurenPaipanResponse,
    # 八字
    BaziPillar,
    BaziPaipanResponse,
    # 六爻
    LiuyaoLine,
    LiuyaoPaipanResponse,
    # 梅花
    MeihuaGua,
    MeihuaPaipanResponse,
)

__all__ = [
    # 基础模型
    'SettingsInfo',
    'OauthBody',
    'User',
    'NewName',
    'PlumFlower',
    'Fate',
    'DivinationBody',
    'BirthdayBody',
    'CommonResponse',
    # 占卜响应模型
    'TimeInfo',
    'GanZhi',
    'ZiweiStar',
    'ZiweiPalace',
    'ZiweiPaipanResponse',
    'QimenGong',
    'QimenPaipanResponse',
    'DaliurenSike',
    'DaliurenSanchuan',
    'DaliurenPaipanResponse',
    'BaziPillar',
    'BaziPaipanResponse',
    'LiuyaoLine',
    'LiuyaoPaipanResponse',
    'MeihuaGua',
    'MeihuaPaipanResponse',
]

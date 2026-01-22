from . import base
from .base import DivinationFactory

# 显式导入所有占卜类，确保元类正确注册
from .tarot import TarotDivination
from .birthday import BirthdayFactory
from .name import NameFactory
from .dream import DreamFactory
from .new_name import NewNameFactory
from .plum_flower import PlumFlowerFactory
from .fate import Fate as FateFactory
from .xiaoliu import XiaoLiuRenFactory
from .ziwei_divination import ZiweiFactory
from .zhuge_divination import ZhugeFactory
from .qimen_divination import QimenFactory
from .daliuren_divination import DaliurenFactory
from .hehun_divination import HehunFactory

# 伦理过滤器
from .ethics_filter import (
    EthicsFilter,
    ethics_filter,
    filter_by_age,
    check_minor,
    validate_content,
)

# 星座模块
from .zodiac import (
    get_sun_sign,
    get_moon_sign,
    get_rising_sign,
    get_zodiac_info,
    get_all_zodiacs,
    get_daily_zodiac_fortune,
    get_weekly_zodiac_fortune,
    get_monthly_zodiac_fortune,
    get_zodiac_compatibility,
)

# AI解读服务
from .ai_interpreter import (
    AIInterpreter,
    BaziInterpreter,
    ZiweiInterpreter,
    LiuyaoInterpreter,
    InterpreterFactory,
    DivinationType,
    InterpretationResult,
    interpret_bazi,
    interpret_ziwei,
    interpret_liuyao,
    get_interpreter,
)

import logging

_logger = logging.getLogger("divination factory")
_logger.info(
    f"Loaded divination types: {list(DivinationFactory.divination_map.keys())}"
)

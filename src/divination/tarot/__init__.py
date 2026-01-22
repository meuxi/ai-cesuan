"""
塔罗牌模块
提供78张韦特塔罗牌数据和抽牌功能
"""
from .divination import TarotDivination

from .data import (
    TAROT_CARDS,
    MAJOR_ARCANA,
    TAROT_SPREADS,
    SUIT_NAMES,
    SUIT_ELEMENTS,
    TarotCard,
    DrawnCard,
    TarotSpread,
    draw_cards,
    draw_for_spread,
    get_daily_card,
    get_card_by_id,
)

from .minor_arcana import (
    MINOR_ARCANA,
    WANDS,
    CUPS,
    SWORDS,
    PENTACLES,
    get_all_minor_arcana,
    get_cards_by_suit,
    get_minor_card_by_code,
)

from .cards import (
    CardSuit,
    SPREADS,
    get_all_major_arcana,
    get_card_by_code,
    get_spread_by_code,
    get_all_spreads,
)

__all__ = [
    'TarotDivination',
    'TAROT_CARDS',
    'MAJOR_ARCANA',
    'MINOR_ARCANA',
    'TAROT_SPREADS',
    'SUIT_NAMES',
    'SUIT_ELEMENTS',
    'TarotCard',
    'DrawnCard',
    'TarotSpread',
    'CardSuit',
    'SPREADS',
    'WANDS',
    'CUPS',
    'SWORDS',
    'PENTACLES',
    'draw_cards',
    'draw_for_spread',
    'get_daily_card',
    'get_card_by_id',
    'get_all_major_arcana',
    'get_all_minor_arcana',
    'get_card_by_code',
    'get_minor_card_by_code',
    'get_cards_by_suit',
    'get_spread_by_code',
    'get_all_spreads',
]

"""
通用功能模块

包含跨领域的通用数据和工具：
- MBTI性格测试
- 沟通建议模板
- 黄历宜忌术语
- 精确节气计算
"""

from .mbti import (
    MBTI_TYPES,
    PERSONALITY_BASICS,
    DIMENSION_DESCRIPTIONS,
    get_personality_info,
    get_dimension_description,
    calculate_result,
    is_valid_mbti_type,
    get_compatible_types,
)

from .communication_templates import (
    CONFLICT_TRIGGERS,
    COMMUNICATION_TEMPLATES,
    SEVERITY_ADVICE,
    get_conflict_triggers,
    get_communication_template,
    get_severity_advice,
)

from .huangli_terms import (
    HUANGLI_TERMS,
    HUANGLI_CATEGORIES,
    get_term_meaning,
    get_term_category,
    get_all_terms_by_category,
    search_terms,
)

from .calendar_almanac import (
    CalendarAlmanacData,
    BLACK_DAY_ZHI_SHEN,
    YELLOW_DAY_ZHI_SHEN,
    WEEKDAY_NAMES,
    LUNAR_MONTH_NAMES,
    LUNAR_DAY_NAMES,
    SOLAR_TERMS,
    ZODIAC_ANIMALS,
    LIU_YAO,
    MOON_PHASES,
    is_black_day,
    is_yellow_day,
    get_zhi_shen_desc,
    get_weekday_chinese,
    get_lunar_month_name,
    get_lunar_day_name,
    get_zodiac_animal,
    get_moon_phase,
    format_solar_date_chinese,
    create_empty_almanac,
)

from .solar_terms import (
    SolarTermsCalculator,
    TrueSolarTimeCalculator,
    solar_terms_calculator,
    true_solar_time_calculator,
    get_solar_term_info,
    get_true_solar_time,
    get_bazi_datetime,
)

from .ganzhi import (
    GanZhiCalculator,
    get_bazi,
    get_wuxing,
    get_nayin,
)

__all__ = [
    # MBTI
    'MBTI_TYPES',
    'PERSONALITY_BASICS',
    'DIMENSION_DESCRIPTIONS',
    'get_personality_info',
    'get_dimension_description',
    'calculate_result',
    'is_valid_mbti_type',
    'get_compatible_types',
    # 沟通模板
    'CONFLICT_TRIGGERS',
    'COMMUNICATION_TEMPLATES',
    'SEVERITY_ADVICE',
    'get_conflict_triggers',
    'get_communication_template',
    'get_severity_advice',
    # 黄历术语
    'HUANGLI_TERMS',
    'HUANGLI_CATEGORIES',
    'get_term_meaning',
    'get_term_category',
    'get_all_terms_by_category',
    'search_terms',
    # 黄历日历
    'CalendarAlmanacData',
    'BLACK_DAY_ZHI_SHEN',
    'YELLOW_DAY_ZHI_SHEN',
    'WEEKDAY_NAMES',
    'LUNAR_MONTH_NAMES',
    'LUNAR_DAY_NAMES',
    'SOLAR_TERMS',
    'ZODIAC_ANIMALS',
    'LIU_YAO',
    'MOON_PHASES',
    'is_black_day',
    'is_yellow_day',
    'get_zhi_shen_desc',
    'get_weekday_chinese',
    'get_lunar_month_name',
    'get_lunar_day_name',
    'get_zodiac_animal',
    'get_moon_phase',
    'format_solar_date_chinese',
    'create_empty_almanac',
    # 精确节气计算
    'SolarTermsCalculator',
    'TrueSolarTimeCalculator',
    'solar_terms_calculator',
    'true_solar_time_calculator',
    'get_solar_term_info',
    'get_true_solar_time',
    'get_bazi_datetime',
    # 干支计算
    'GanZhiCalculator',
    'get_bazi',
    'get_wuxing',
    'get_nayin',
]

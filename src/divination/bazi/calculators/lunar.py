"""农历转换封装"""
from lunar_python import Lunar, Solar
from typing import Dict


def solar_to_lunar(year: int, month: int, day: int) -> Dict:
    """公历转农历
    
    Args:
        year: 公历年
        month: 公历月
        day: 公历日
        
    Returns:
        {
            'year': 农历年,
            'month': 农历月,
            'day': 农历日,
            'is_leap': 是否闰月,
            'year_cn': '甲子年',
            'month_cn': '正月',
            'day_cn': '初一',
            'zodiac': '生肖'
        }
    """
    solar = Solar.fromYmd(year, month, day)
    lunar = solar.getLunar()
    
    return {
        'year': lunar.getYear(),
        'month': lunar.getMonth(),
        'day': lunar.getDay(),
        'is_leap': lunar.getMonth() < 0,
        'year_cn': lunar.getYearInGanZhi(),
        'month_cn': lunar.getMonthInChinese(),
        'day_cn': lunar.getDayInChinese(),
        'zodiac': lunar.getYearShengXiao()
    }


def lunar_to_solar(year: int, month: int, day: int, 
                   is_leap: bool = False) -> Dict:
    """农历转公历
    
    Args:
        year: 农历年
        month: 农历月
        day: 农历日
        is_leap: 是否闰月
        
    Returns:
        {
            'year': 公历年,
            'month': 公历月,
            'day': 公历日
        }
    """
    lunar = Lunar.fromYmd(year, month, day, 0 if not is_leap else month)
    solar = lunar.getSolar()
    
    return {
        'year': solar.getYear(),
        'month': solar.getMonth(),
        'day': solar.getDay()
    }

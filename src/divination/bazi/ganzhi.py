"""
天干地支计算模块
转换自 cls_ganzhi.php
"""
from typing import List, Dict


class GanZhi:
    """天干地支计算类"""
    
    # 天干
    TIANGAN = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']
    
    # 地支
    DIZHI = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']
    
    # 月份起始索引（年上起月法）
    MONTH_START = [4, 15, 27, 39, 51, 4, 15, 27, 39, 51]
    
    # 时辰起始索引（日上起时法）
    HOUR_START = [1, 3, 5, 7, 9, 1, 3, 5, 7, 9]
    
    # 五行映射
    WUXING_MAP = {
        '甲': '木', '乙': '木',
        '丙': '火', '丁': '火',
        '戊': '土', '己': '土',
        '庚': '金', '辛': '金',
        '壬': '水', '癸': '水',
        '子': '水', '亥': '水',
        '寅': '木', '卯': '木',
        '巳': '火', '午': '火',
        '申': '金', '酉': '金',
        '辰': '土', '戌': '土', '丑': '土', '未': '土'
    }
    
    # 六十甲子表（缓存）
    _jiazi_table: List[str] = None
    
    @classmethod
    def get_tiangan(cls, index: int) -> str:
        """获取天干
        
        Args:
            index: 1-10
            
        Returns:
            天干字符
        """
        if not (1 <= index <= 10):
            index = 1
        return cls.TIANGAN[index - 1]
    
    @classmethod
    def get_dizhi(cls, index: int) -> str:
        """获取地支
        
        Args:
            index: 1-12
            
        Returns:
            地支字符
        """
        if not (1 <= index <= 12):
            index = 1
        return cls.DIZHI[index - 1]
    
    @classmethod
    def create_jiazi_table(cls) -> List[str]:
        """创建六十甲子表"""
        if cls._jiazi_table is not None:
            return cls._jiazi_table
            
        table = []
        tian_idx = 0
        di_idx = 0
        
        for _ in range(60):
            gz = cls.TIANGAN[tian_idx] + cls.DIZHI[di_idx]
            table.append(gz)
            tian_idx = (tian_idx + 1) % 10
            di_idx = (di_idx + 1) % 12
            
        cls._jiazi_table = table
        return table
    
    @classmethod
    def get_jiazi(cls, index: int) -> str:
        """获取六十甲子
        
        Args:
            index: 1-60
            
        Returns:
            干支组合，如"甲子"
        """
        if cls._jiazi_table is None:
            cls.create_jiazi_table()
            
        if not (1 <= index <= 60):
            index = 1
        return cls._jiazi_table[index - 1]
    
    @classmethod
    def get_year(cls, year: int) -> str:
        """获取干支年
        
        Args:
            year: 公历年份（>= 4年）
            
        Returns:
            干支年，如"甲子"
            
        Example:
            >>> GanZhi.get_year(2024)
            '甲辰'
        """
        # 1911年为辛亥年（第48个甲子）
        diff = (year - 1911) + 48
        remainder = diff % 60
        
        if remainder == 0:
            remainder = 60
            
        return cls.get_jiazi(abs(remainder))
    
    @classmethod
    def get_month(cls, year: int, month: int = None) -> str:
        """获取干支月
        
        Args:
            year: 公历年份
            month: 月份(1-12)，从立春算起
            
        Returns:
            干支月或月份列表
        """
        year_gz = cls.get_year(year)
        
        # 找到年干对应的月份起始索引
        year_tg = year_gz[0]
        tg_idx = cls.TIANGAN.index(year_tg)
        start = cls.MONTH_START[tg_idx]
        
        if month is None:
            # 返回全年12个月
            result = []
            for i in range(12):
                idx = start + i
                if idx > 60:
                    idx -= 60
                result.append(cls.get_jiazi(idx))
            return result
        else:
            # 返回指定月份（从立春开始，2月为第一个月）
            idx = start + (month - 2)
            if idx > 60:
                idx -= 60
            elif idx <= 0:
                idx += 60
            return cls.get_jiazi(idx)
    
    @classmethod
    def get_day(cls, year: int, month: int, day: int) -> str:
        """获取干支日（蔡勒公式）
        
        Args:
            year: 年份
            month: 月份
            day: 日期
            
        Returns:
            干支日
        """
        # 取年份后两位
        y = year % 100
        century = year // 100
        
        # 1月和2月视为上年的13月和14月
        m = month
        if month == 1:
            m = 13
            y -= 1
        elif month == 2:
            m = 14
            y -= 1
        
        # 月份偏移
        i = 6 if m % 2 == 0 else 0
        
        # 天干计算
        tg_idx = (4 * century + century // 4 + 5 * y + y // 4 + 
                  (3 * (m + 1)) // 5 + day - 3) % 10
        
        # 地支计算
        dz_idx = (8 * century + century // 4 + 5 * y + y // 4 + 
                  (3 * (m + 1)) // 5 + day + 7 + i) % 12
        
        return cls.TIANGAN[tg_idx] + cls.DIZHI[dz_idx]
    
    @classmethod
    def get_hour(cls, year: int, month: int, day: int, hour: int) -> str:
        """获取干支时
        
        Args:
            year: 年份
            month: 月份
            day: 日期
            hour: 小时(0-23)
            
        Returns:
            干支时
        """
        day_gz = cls.get_day(year, month, day)
        day_tg = day_gz[0]
        tg_idx = cls.TIANGAN.index(day_tg)
        start = cls.HOUR_START[tg_idx]
        
        # 计算时辰索引（23-1点为子时）
        if hour % 2 == 0:
            hour_before = hour - 1
            offset = (hour_before // 2) + 1
        else:
            offset = (hour // 2) + 1
        
        if offset >= 11:
            offset = 0
        
        # 计算时干
        tg_offset = (start + offset - 1) % 10
        
        return cls.TIANGAN[tg_offset] + cls.DIZHI[offset]
    
    @classmethod
    def get_bazi(cls, year: int, month: int, day: int, hour: int) -> Dict:
        """获取完整八字
        
        Args:
            year: 年份
            month: 月份
            day: 日期
            hour: 小时
            
        Returns:
            {
                'year': '年柱',
                'month': '月柱',
                'day': '日柱',
                'hour': '时柱',
                'full': '完整八字'
            }
        """
        year_gz = cls.get_year(year)
        month_gz = cls.get_month(year, month)
        day_gz = cls.get_day(year, month, day)
        hour_gz = cls.get_hour(year, month, day, hour)
        
        return {
            'year': year_gz,
            'month': month_gz,
            'day': day_gz,
            'hour': hour_gz,
            'full': f"{year_gz} {month_gz} {day_gz} {hour_gz}"
        }
    
    @classmethod
    def get_wuxing(cls, gan_or_zhi: str) -> str:
        """获取天干或地支的五行属性
        
        Args:
            gan_or_zhi: 天干或地支
            
        Returns:
            五行属性
        """
        return cls.WUXING_MAP.get(gan_or_zhi, '')

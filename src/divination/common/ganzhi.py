"""
公共干支计算模块

提供统一的干支计算功能，可被八字、奇门遁甲、六爻等多个模块复用。
支持：
- 天干地支基础数据和映射
- 六十甲子表生成
- 年/月/日/时柱计算
- 五行/纳音计算
- 通过 lunar_python 实现精确的节气交接

使用方式：
    from src.divination.common.ganzhi import GanZhiCalculator
    
    # 获取精确四柱（使用 lunar_python）
    result = GanZhiCalculator.get_bazi_by_lunar(2026, 1, 21, 14, 30)
    
    # 获取简化四柱（不需要 lunar_python）
    result = GanZhiCalculator.get_bazi(2026, 1, 21, 14)
"""
from typing import Dict, List, Optional, Tuple
from datetime import date
import logging

_logger = logging.getLogger(__name__)


class GanZhiCalculator:
    """天干地支计算器（单例模式）"""
    
    # 天干
    TIANGAN = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']
    
    # 地支
    DIZHI = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']
    
    # 天干五行
    TIANGAN_WUXING = {
        '甲': '木', '乙': '木',
        '丙': '火', '丁': '火',
        '戊': '土', '己': '土',
        '庚': '金', '辛': '金',
        '壬': '水', '癸': '水'
    }
    
    # 地支五行
    DIZHI_WUXING = {
        '子': '水', '亥': '水',
        '寅': '木', '卯': '木',
        '巳': '火', '午': '火',
        '申': '金', '酉': '金',
        '辰': '土', '戌': '土', '丑': '土', '未': '土'
    }
    
    # 五行生克关系
    WUXING_SHENGKE = {
        '生': {'木': '火', '火': '土', '土': '金', '金': '水', '水': '木'},
        '克': {'木': '土', '土': '水', '水': '火', '火': '金', '金': '木'}
    }
    
    # 时辰名称
    SHICHEN_NAMES = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']
    
    # 六十甲子表（懒加载）
    _jiazi_table: Optional[List[str]] = None
    
    # 纳音映射表
    NAYIN_TABLE = {
        '甲子': '海中金', '乙丑': '海中金', '丙寅': '炉中火', '丁卯': '炉中火',
        '戊辰': '大林木', '己巳': '大林木', '庚午': '路旁土', '辛未': '路旁土',
        '壬申': '剑锋金', '癸酉': '剑锋金', '甲戌': '山头火', '乙亥': '山头火',
        '丙子': '涧下水', '丁丑': '涧下水', '戊寅': '城头土', '己卯': '城头土',
        '庚辰': '白腊金', '辛巳': '白腊金', '壬午': '杨柳木', '癸未': '杨柳木',
        '甲申': '泉中水', '乙酉': '泉中水', '丙戌': '屋上土', '丁亥': '屋上土',
        '戊子': '霹雳火', '己丑': '霹雳火', '庚寅': '松柏木', '辛卯': '松柏木',
        '壬辰': '长流水', '癸巳': '长流水', '甲午': '沙中金', '乙未': '沙中金',
        '丙申': '山下火', '丁酉': '山下火', '戊戌': '平地木', '己亥': '平地木',
        '庚子': '壁上土', '辛丑': '壁上土', '壬寅': '金箔金', '癸卯': '金箔金',
        '甲辰': '覆灯火', '乙巳': '覆灯火', '丙午': '天河水', '丁未': '天河水',
        '戊申': '大驿土', '己酉': '大驿土', '庚戌': '钗钏金', '辛亥': '钗钏金',
        '壬子': '桑柘木', '癸丑': '桑柘木', '甲寅': '大溪水', '乙卯': '大溪水',
        '丙辰': '沙中土', '丁巳': '沙中土', '戊午': '天上火', '己未': '天上火',
        '庚申': '石榴木', '辛酉': '石榴木', '壬戌': '大海水', '癸亥': '大海水'
    }
    
    @classmethod
    def create_jiazi_table(cls) -> List[str]:
        """创建六十甲子表"""
        if cls._jiazi_table is not None:
            return cls._jiazi_table
        
        table = []
        for i in range(60):
            gz = cls.TIANGAN[i % 10] + cls.DIZHI[i % 12]
            table.append(gz)
        
        cls._jiazi_table = table
        return table
    
    @classmethod
    def get_jiazi(cls, index: int) -> str:
        """获取六十甲子（0-59）"""
        if cls._jiazi_table is None:
            cls.create_jiazi_table()
        return cls._jiazi_table[index % 60]
    
    @classmethod
    def jiazi_index(cls, ganzhi: str) -> int:
        """获取干支在六十甲子中的索引"""
        if cls._jiazi_table is None:
            cls.create_jiazi_table()
        try:
            return cls._jiazi_table.index(ganzhi)
        except ValueError:
            return 0
    
    @classmethod
    def get_wuxing(cls, char: str) -> str:
        """获取天干或地支的五行"""
        return cls.TIANGAN_WUXING.get(char) or cls.DIZHI_WUXING.get(char, '')
    
    @classmethod
    def get_nayin(cls, ganzhi: str) -> str:
        """获取干支的纳音"""
        return cls.NAYIN_TABLE.get(ganzhi, '')
    
    @classmethod
    def hour_to_shichen(cls, hour: int) -> int:
        """小时转时辰索引（0-11）
        
        23:00-00:59 子时(0)
        01:00-02:59 丑时(1)
        ...
        """
        if hour >= 23 or hour < 1:
            return 0
        return (hour + 1) // 2
    
    @classmethod
    def get_bazi_by_lunar(cls, year: int, month: int, day: int, 
                          hour: int = 12, minute: int = 0) -> Dict[str, str]:
        """使用 lunar_python 获取精确四柱
        
        正确处理：
        - 年柱：立春交节换年柱
        - 月柱：节气交节换月柱
        - 日柱：精确计算
        - 时柱：根据日干推时干
        
        Args:
            year, month, day: 公历年月日
            hour: 小时 (0-23)
            minute: 分钟 (0-59)
            
        Returns:
            {'year': '年柱', 'month': '月柱', 'day': '日柱', 'hour': '时柱',
             'full': '完整八字', 'method': 'lunar_python'}
        """
        try:
            from lunar_python import Solar
            
            solar = Solar.fromYmdHms(year, month, day, hour, minute, 0)
            lunar = solar.getLunar()
            bazi = lunar.getEightChar()
            
            return {
                'year': bazi.getYear(),
                'month': bazi.getMonth(),
                'day': bazi.getDay(),
                'hour': bazi.getTime(),
                'full': f"{bazi.getYear()} {bazi.getMonth()} {bazi.getDay()} {bazi.getTime()}",
                'method': 'lunar_python'
            }
        except Exception as e:
            _logger.warning(f"lunar_python 计算失败，回退到简化算法: {e}")
            return cls.get_bazi(year, month, day, hour)
    
    @classmethod
    def get_bazi(cls, year: int, month: int, day: int, hour: int) -> Dict[str, str]:
        """获取四柱（简化算法，不处理节气交接）
        
        Args:
            year, month, day: 公历年月日
            hour: 小时 (0-23)
            
        Returns:
            {'year': '年柱', 'month': '月柱', 'day': '日柱', 'hour': '时柱',
             'full': '完整八字', 'method': 'simplified'}
        """
        year_gz = cls._calc_year_pillar(year)
        month_gz = cls._calc_month_pillar(year_gz[0], month)
        day_gz = cls._calc_day_pillar(year, month, day)
        hour_gz = cls._calc_hour_pillar(day_gz[0], hour)
        
        return {
            'year': year_gz,
            'month': month_gz,
            'day': day_gz,
            'hour': hour_gz,
            'full': f"{year_gz} {month_gz} {day_gz} {hour_gz}",
            'method': 'simplified'
        }
    
    @classmethod
    def _calc_year_pillar(cls, year: int) -> str:
        """计算年柱（简化）"""
        idx = (year - 4) % 60
        return cls.TIANGAN[idx % 10] + cls.DIZHI[idx % 12]
    
    @classmethod
    def _calc_month_pillar(cls, year_gan: str, month: int) -> str:
        """计算月柱（简化，不处理节气）"""
        year_gan_idx = cls.TIANGAN.index(year_gan) if year_gan in cls.TIANGAN else 0
        
        # 年上起月法
        base_gan_idx = (year_gan_idx % 5) * 2 + 2
        gan_idx = (base_gan_idx + month - 1) % 10
        zhi_idx = (month + 1) % 12  # 正月寅
        
        return cls.TIANGAN[gan_idx] + cls.DIZHI[zhi_idx]
    
    @classmethod
    def _calc_day_pillar(cls, year: int, month: int, day: int) -> str:
        """计算日柱"""
        base_date = date(1900, 1, 31)  # 甲子日
        target_date = date(year, month, day)
        diff = (target_date - base_date).days
        
        idx = diff % 60
        return cls.TIANGAN[idx % 10] + cls.DIZHI[idx % 12]
    
    @classmethod
    def _calc_hour_pillar(cls, day_gan: str, hour: int) -> str:
        """计算时柱"""
        day_gan_idx = cls.TIANGAN.index(day_gan) if day_gan in cls.TIANGAN else 0
        shichen_idx = cls.hour_to_shichen(hour)
        
        # 日上起时法
        base_gan_idx = (day_gan_idx % 5) * 2
        gan_idx = (base_gan_idx + shichen_idx) % 10
        
        return cls.TIANGAN[gan_idx] + cls.DIZHI[shichen_idx]
    
    @classmethod
    def get_xun_shou(cls, ganzhi: str) -> str:
        """获取旬首（甲子、甲戌等）"""
        idx = cls.jiazi_index(ganzhi)
        xun_idx = (idx // 10) * 10  # 每10个干支为一旬
        return cls.get_jiazi(xun_idx)
    
    @classmethod
    def get_xun_kong(cls, ganzhi: str) -> Tuple[str, str]:
        """获取旬空（空亡）"""
        xun_shou = cls.get_xun_shou(ganzhi)
        xun_kong_map = {
            '甲子': ('戌', '亥'), '甲戌': ('申', '酉'),
            '甲申': ('午', '未'), '甲午': ('辰', '巳'),
            '甲辰': ('寅', '卯'), '甲寅': ('子', '丑')
        }
        return xun_kong_map.get(xun_shou, ('戌', '亥'))
    
    @classmethod
    def get_liuyi(cls, ganzhi: str) -> str:
        """获取六仪（遁甲用）"""
        xun_shou = cls.get_xun_shou(ganzhi)
        liuyi_map = {
            '甲子': '戊', '甲戌': '己', '甲申': '庚',
            '甲午': '辛', '甲辰': '壬', '甲寅': '癸'
        }
        return liuyi_map.get(xun_shou, '戊')


# 便捷函数
def get_bazi(year: int, month: int, day: int, hour: int, 
             minute: int = 0, precise: bool = True) -> Dict[str, str]:
    """获取四柱八字
    
    Args:
        year, month, day: 公历年月日
        hour: 小时 (0-23)
        minute: 分钟 (0-59)
        precise: 是否使用精确算法（需要 lunar_python）
        
    Returns:
        四柱信息字典
    """
    if precise:
        return GanZhiCalculator.get_bazi_by_lunar(year, month, day, hour, minute)
    return GanZhiCalculator.get_bazi(year, month, day, hour)


def get_wuxing(char: str) -> str:
    """获取天干/地支的五行"""
    return GanZhiCalculator.get_wuxing(char)


def get_nayin(ganzhi: str) -> str:
    """获取干支的纳音"""
    return GanZhiCalculator.get_nayin(ganzhi)

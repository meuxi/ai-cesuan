"""
星曜计算器
计算紫微斗数的星曜安放
"""
from typing import Dict, List


class XingXiuCalculator:
    """星曜计算类"""
    
    # 主星（十四主星）
    ZHU_XING = ['紫微', '天机', '太阳', '武曲', '天同', '廉贞', '天府',
                '太阴', '贪狼', '巨门', '天相', '天梁', '七杀', '破军']
    
    # 辅星
    FU_XING = ['左辅', '右弼', '文昌', '文曲', '天魁', '天钺', '禄存', '天马']
    
    # 煞星
    SHA_XING = ['擎羊', '陀罗', '火星', '铃星', '地空', '地劫']
    
    # 十二地支
    DIZHI = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']
    
    # 紫微星系安星表（根据五行局和农历日）
    ZIWEI_TABLE = {
        # 水二局
        2: {1: '寅', 2: '卯', 3: '辰', 4: '巳', 5: '午', 6: '未',
            7: '申', 8: '酉', 9: '戌', 10: '亥', 11: '子', 12: '丑'},
        # 木三局
        3: {1: '辰', 2: '巳', 3: '巳', 4: '午', 5: '午', 6: '未',
            7: '未', 8: '申', 9: '申', 10: '酉', 11: '酉', 12: '戌'},
        # 金四局
        4: {1: '午', 2: '未', 3: '未', 4: '申', 5: '申', 6: '酉',
            7: '酉', 8: '戌', 9: '戌', 10: '亥', 11: '亥', 12: '子'},
        # 土五局
        5: {1: '申', 2: '酉', 3: '酉', 4: '戌', 5: '戌', 6: '亥',
            7: '亥', 8: '子', 9: '子', 10: '丑', 11: '丑', 12: '寅'},
        # 火六局
        6: {1: '戌', 2: '亥', 3: '亥', 4: '子', 5: '子', 6: '丑',
            7: '丑', 8: '寅', 9: '寅', 10: '卯', 11: '卯', 12: '辰'}
    }
    
    @classmethod
    def calculate_wuxing_ju(cls, ming_gong_zhi: str, year_gan: str) -> int:
        """计算五行局
        
        Args:
            ming_gong_zhi: 命宫地支
            year_gan: 年干
            
        Returns:
            五行局数（2/3/4/5/6）
        """
        # 简化版：根据命宫地支和年干查表
        # 实际应根据纳音五行计算
        tiangan = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']
        gan_idx = tiangan.index(year_gan) if year_gan in tiangan else 0
        zhi_idx = cls.DIZHI.index(ming_gong_zhi) if ming_gong_zhi in cls.DIZHI else 0
        
        # 简化计算
        ju_map = [2, 6, 3, 5, 4, 2, 6, 3, 5, 4]  # 根据年干
        return ju_map[gan_idx]
    
    @classmethod
    def place_ziwei(cls, wuxing_ju: int, lunar_day: int) -> str:
        """安紫微星
        
        Args:
            wuxing_ju: 五行局数
            lunar_day: 农历日
            
        Returns:
            紫微星所在地支
        """
        day_mod = (lunar_day - 1) % 12 + 1
        table = cls.ZIWEI_TABLE.get(wuxing_ju, cls.ZIWEI_TABLE[2])
        return table.get(day_mod, '寅')
    
    @classmethod
    def place_tianfu(cls, ziwei_zhi: str) -> str:
        """安天府星（与紫微星对称）
        
        Args:
            ziwei_zhi: 紫微星地支
            
        Returns:
            天府星所在地支
        """
        ziwei_idx = cls.DIZHI.index(ziwei_zhi) if ziwei_zhi in cls.DIZHI else 0
        # 天府与紫微对称
        tianfu_idx = (4 - ziwei_idx + 12) % 12  # 以寅为轴对称
        return cls.DIZHI[tianfu_idx]
    
    @classmethod
    def calculate_all_stars(cls, wuxing_ju: int, lunar_day: int,
                            lunar_month: int, shi_zhi: str,
                            year_gan: str, year_zhi: str) -> Dict[str, str]:
        """计算所有星曜位置
        
        Args:
            wuxing_ju: 五行局
            lunar_day: 农历日
            lunar_month: 农历月
            shi_zhi: 时支
            year_gan: 年干
            year_zhi: 年支
            
        Returns:
            {星名: 地支}
        """
        stars = {}
        
        # 安紫微
        ziwei_zhi = cls.place_ziwei(wuxing_ju, lunar_day)
        stars['紫微'] = ziwei_zhi
        ziwei_idx = cls.DIZHI.index(ziwei_zhi)
        
        # 紫微星系（逆时针排布）
        ziwei_series = ['紫微', '天机', '空', '太阳', '武曲', '天同', '空', '廉贞']
        for i, star in enumerate(ziwei_series):
            if star != '空':
                idx = (ziwei_idx - i + 12) % 12
                stars[star] = cls.DIZHI[idx]
        
        # 安天府
        tianfu_zhi = cls.place_tianfu(ziwei_zhi)
        stars['天府'] = tianfu_zhi
        tianfu_idx = cls.DIZHI.index(tianfu_zhi)
        
        # 天府星系（顺时针排布）
        tianfu_series = ['天府', '太阴', '贪狼', '巨门', '天相', '天梁', '七杀', '空', '空', '空', '空', '破军']
        for i, star in enumerate(tianfu_series):
            if star != '空':
                idx = (tianfu_idx + i) % 12
                stars[star] = cls.DIZHI[idx]
        
        # 安辅星
        shi_idx = cls.DIZHI.index(shi_zhi) if shi_zhi in cls.DIZHI else 0
        month_idx = lunar_month - 1
        
        # 左辅右弼（根据月支）
        stars['左辅'] = cls.DIZHI[(2 + month_idx) % 12]  # 辰起正月顺行
        stars['右弼'] = cls.DIZHI[(10 - month_idx + 12) % 12]  # 戌起正月逆行
        
        # 文昌文曲（根据时支）
        stars['文昌'] = cls.DIZHI[(10 - shi_idx + 12) % 12]  # 戌起子时逆行
        stars['文曲'] = cls.DIZHI[(4 + shi_idx) % 12]  # 辰起子时顺行
        
        # 天魁天钺（根据年干）
        tiangan = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']
        gan_idx = tiangan.index(year_gan) if year_gan in tiangan else 0
        kui_table = ['丑', '子', '亥', '酉', '丑', '子', '丑', '午', '卯', '卯']
        yue_table = ['未', '申', '酉', '亥', '未', '申', '未', '寅', '巳', '巳']
        stars['天魁'] = kui_table[gan_idx]
        stars['天钺'] = yue_table[gan_idx]
        
        # 禄存（根据年干）
        lucun_table = ['寅', '卯', '巳', '午', '巳', '午', '申', '酉', '亥', '子']
        stars['禄存'] = lucun_table[gan_idx]
        
        # 擎羊陀罗（禄存前后一位）
        lucun_idx = cls.DIZHI.index(lucun_table[gan_idx])
        stars['擎羊'] = cls.DIZHI[(lucun_idx + 1) % 12]
        stars['陀罗'] = cls.DIZHI[(lucun_idx - 1 + 12) % 12]
        
        # 火星铃星（根据年支和时支）
        year_zhi_idx = cls.DIZHI.index(year_zhi) if year_zhi in cls.DIZHI else 0
        if year_zhi in ['寅', '午', '戌']:
            fire_start = 2  # 丑
        elif year_zhi in ['申', '子', '辰']:
            fire_start = 1  # 寅
        elif year_zhi in ['巳', '酉', '丑']:
            fire_start = 3  # 卯
        else:  # 亥卯未
            fire_start = 9  # 酉
        stars['火星'] = cls.DIZHI[(fire_start + shi_idx) % 12]
        
        if year_zhi in ['寅', '午', '戌']:
            bell_start = 3  # 卯
        elif year_zhi in ['申', '子', '辰']:
            bell_start = 10  # 戌
        elif year_zhi in ['巳', '酉', '丑']:
            bell_start = 10  # 戌
        else:  # 亥卯未
            bell_start = 10  # 戌
        stars['铃星'] = cls.DIZHI[(bell_start + shi_idx) % 12]
        
        # 地空地劫（根据时支）
        stars['地空'] = cls.DIZHI[(11 - shi_idx + 12) % 12]  # 亥起子时逆行
        stars['地劫'] = cls.DIZHI[(11 + shi_idx) % 12]  # 亥起子时顺行
        
        return stars

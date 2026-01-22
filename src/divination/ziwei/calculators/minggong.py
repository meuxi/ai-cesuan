"""
命宫计算器
计算紫微斗数的十二宫位置
"""
from typing import Dict, List


class MingGongCalculator:
    """命宫计算类"""
    
    # 十二宫名称
    SHI_ER_GONG = ['命宫', '兄弟宫', '夫妻宫', '子女宫', '财帛宫', '疾厄宫',
                   '迁移宫', '仆役宫', '官禄宫', '田宅宫', '福德宫', '父母宫']
    
    # 十二地支
    DIZHI = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']
    
    @classmethod
    def calculate_ming_gong(cls, lunar_month: int, shi_zhi: str) -> str:
        """计算命宫位置
        
        Args:
            lunar_month: 农历月（1-12）
            shi_zhi: 时支
            
        Returns:
            命宫所在地支
        """
        # 命宫公式：寅起正月，顺数至生月，再逆数至时支
        shi_idx = cls.DIZHI.index(shi_zhi) if shi_zhi in cls.DIZHI else 0
        
        # 从寅开始顺数到生月
        month_gong = (2 + lunar_month - 1) % 12  # 寅=2
        
        # 从生月宫位逆数到时支
        ming_gong_idx = (month_gong - shi_idx + 12) % 12
        
        return cls.DIZHI[ming_gong_idx]
    
    @classmethod
    def calculate_shen_gong(cls, lunar_month: int, shi_zhi: str) -> str:
        """计算身宫位置
        
        Args:
            lunar_month: 农历月
            shi_zhi: 时支
            
        Returns:
            身宫所在地支
        """
        # 身宫公式：寅起正月，顺数至生月，再顺数至时支
        shi_idx = cls.DIZHI.index(shi_zhi) if shi_zhi in cls.DIZHI else 0
        month_gong = (2 + lunar_month - 1) % 12
        shen_gong_idx = (month_gong + shi_idx) % 12
        
        return cls.DIZHI[shen_gong_idx]
    
    @classmethod
    def arrange_twelve_gong(cls, ming_gong_zhi: str) -> Dict[str, str]:
        """安排十二宫
        
        Args:
            ming_gong_zhi: 命宫地支
            
        Returns:
            {宫名: 地支}
        """
        ming_idx = cls.DIZHI.index(ming_gong_zhi) if ming_gong_zhi in cls.DIZHI else 0
        
        gong_layout = {}
        for i, gong_name in enumerate(cls.SHI_ER_GONG):
            zhi_idx = (ming_idx + i) % 12
            gong_layout[gong_name] = cls.DIZHI[zhi_idx]
        
        return gong_layout

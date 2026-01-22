"""
天地盘计算器
计算大六壬的天地盘布局
"""
from typing import Dict, List


class TianPanCalculator:
    """天地盘计算类"""
    
    # 十二地支
    DIZHI = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']
    
    # 地支对应宫位（地盘固定）
    DI_PAN = {
        '子': 1, '丑': 2, '寅': 3, '卯': 4,
        '辰': 5, '巳': 6, '午': 7, '未': 8,
        '申': 9, '酉': 10, '戌': 11, '亥': 12
    }
    
    @classmethod
    def calculate(cls, yue_jiang: str, shi_zhi: str) -> Dict:
        """计算天地盘
        
        Args:
            yue_jiang: 月将（太阳所在宫位对应的地支）
            shi_zhi: 时支
            
        Returns:
            天地盘布局
        """
        # 地盘固定
        di_pan = {i+1: cls.DIZHI[i] for i in range(12)}
        
        # 天盘：月将加时
        yue_jiang_idx = cls.DIZHI.index(yue_jiang) if yue_jiang in cls.DIZHI else 0
        shi_zhi_idx = cls.DIZHI.index(shi_zhi) if shi_zhi in cls.DIZHI else 0
        
        # 月将落在时支宫位
        offset = shi_zhi_idx - yue_jiang_idx
        
        tian_pan = {}
        for i in range(12):
            tian_zhi_idx = (i + offset) % 12
            tian_pan[i+1] = cls.DIZHI[tian_zhi_idx]
        
        return {
            'di_pan': di_pan,
            'tian_pan': tian_pan,
            'yue_jiang': yue_jiang,
            'shi_zhi': shi_zhi
        }
    
    @classmethod
    def get_yue_jiang(cls, month: int, day: int) -> str:
        """获取月将
        
        Args:
            month: 农历月
            day: 农历日
            
        Returns:
            月将地支
        """
        # 简化版：根据月份判断月将
        # 实际应根据节气精确计算
        yue_jiang_map = {
            1: '亥',   # 正月用登明（亥）
            2: '戌',   # 二月用河魁（戌）
            3: '酉',   # 三月用从魁（酉）
            4: '申',   # 四月用传送（申）
            5: '未',   # 五月用小吉（未）
            6: '午',   # 六月用胜光（午）
            7: '巳',   # 七月用太乙（巳）
            8: '辰',   # 八月用天罡（辰）
            9: '卯',   # 九月用太冲（卯）
            10: '寅',  # 十月用功曹（寅）
            11: '丑',  # 十一月用大吉（丑）
            12: '子'   # 十二月用神后（子）
        }
        return yue_jiang_map.get(month, '子')

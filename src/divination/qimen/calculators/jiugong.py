"""
九宫计算器
计算九宫布局、飞宫规则
"""
from typing import Dict, List


class JiuGongCalculator:
    """九宫计算类"""
    
    # 洛书飞宫顺序（1-9）
    LUOSHU_ORDER = [1, 8, 3, 4, 9, 2, 7, 6]  # 不含中宫5
    
    # 物理顺时针顺序（用于转盘式）
    PHYSICAL_CLOCKWISE = [1, 8, 3, 4, 9, 2, 7, 6]
    
    # 物理逆时针顺序
    PHYSICAL_COUNTER_CLOCKWISE = [1, 6, 7, 2, 9, 4, 3, 8]
    
    # 中宫寄坤二
    ZHONG_GONG_JI = 2
    
    # 宫位名称
    GONG_NAMES = {
        1: '坎一宫', 2: '坤二宫', 3: '震三宫', 4: '巽四宫',
        5: '中五宫', 6: '乾六宫', 7: '兑七宫', 8: '艮八宫', 9: '离九宫'
    }
    
    # 宫位五行
    GONG_WUXING = {
        1: '水', 2: '土', 3: '木', 4: '木',
        5: '土', 6: '金', 7: '金', 8: '土', 9: '火'
    }
    
    # 地支与宫位对应
    DIZHI_GONG = {
        '子': 1, '丑': 8, '寅': 8, '卯': 3, '辰': 4, '巳': 4,
        '午': 9, '未': 2, '申': 2, '酉': 7, '戌': 6, '亥': 6
    }
    
    @classmethod
    def fly_forward(cls, start_gong: int, steps: int) -> int:
        """飞盘式顺飞
        
        Args:
            start_gong: 起始宫位
            steps: 飞宫步数
            
        Returns:
            目标宫位
        """
        if start_gong == 5:
            start_gong = cls.ZHONG_GONG_JI
        
        try:
            idx = cls.LUOSHU_ORDER.index(start_gong)
        except ValueError:
            idx = 0
        
        new_idx = (idx + steps) % 8
        return cls.LUOSHU_ORDER[new_idx]
    
    @classmethod
    def fly_backward(cls, start_gong: int, steps: int) -> int:
        """飞盘式逆飞
        
        Args:
            start_gong: 起始宫位
            steps: 飞宫步数
            
        Returns:
            目标宫位
        """
        if start_gong == 5:
            start_gong = cls.ZHONG_GONG_JI
        
        try:
            idx = cls.LUOSHU_ORDER.index(start_gong)
        except ValueError:
            idx = 0
        
        new_idx = (idx - steps) % 8
        return cls.LUOSHU_ORDER[new_idx]
    
    @classmethod
    def rotate(cls, start_gong: int, steps: int, is_yang: bool) -> int:
        """转盘式旋转
        
        Args:
            start_gong: 起始宫位
            steps: 旋转步数
            is_yang: 是否阳遁（顺时针）
            
        Returns:
            目标宫位
        """
        if start_gong == 5:
            start_gong = cls.ZHONG_GONG_JI
        
        order = cls.PHYSICAL_CLOCKWISE if is_yang else cls.PHYSICAL_COUNTER_CLOCKWISE
        
        try:
            idx = order.index(start_gong)
        except ValueError:
            idx = 0
        
        new_idx = (idx + steps) % 8
        return order[new_idx]
    
    @classmethod
    def get_gong_by_dizhi(cls, dizhi: str) -> int:
        """根据地支获取宫位
        
        Args:
            dizhi: 地支
            
        Returns:
            宫位数字
        """
        return cls.DIZHI_GONG.get(dizhi, 1)

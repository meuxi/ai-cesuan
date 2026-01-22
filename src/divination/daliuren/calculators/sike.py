"""
四课计算器
计算大六壬的四课
"""
from typing import Dict, List, Tuple


class SiKeCalculator:
    """四课计算类"""
    
    # 十天干
    TIANGAN = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']
    
    # 十二地支
    DIZHI = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']
    
    # 天干寄宫
    TIANGAN_JI_GONG = {
        '甲': '寅', '乙': '辰', '丙': '巳', '丁': '未',
        '戊': '巳', '己': '未', '庚': '申', '辛': '戌',
        '壬': '亥', '癸': '丑'
    }
    
    @classmethod
    def calculate(cls, ri_gan: str, ri_zhi: str, tian_pan: Dict[int, str]) -> List[Dict]:
        """计算四课
        
        Args:
            ri_gan: 日干
            ri_zhi: 日支
            tian_pan: 天盘布局
            
        Returns:
            四课信息列表
        """
        # 日干寄宫
        gan_gong = cls.TIANGAN_JI_GONG.get(ri_gan, '寅')
        
        # 反转天盘：宫位 -> 天盘地支
        tian_pan_reverse = {v: k for k, v in tian_pan.items()}
        
        # 第一课：日干上神
        # 日干寄宫在天盘上的地支
        gan_gong_idx = cls.DIZHI.index(gan_gong)
        ke1_shang = tian_pan.get(gan_gong_idx + 1, gan_gong)
        ke1 = {'name': '第一课', 'shang': ke1_shang, 'xia': ri_gan}
        
        # 第二课：日干上神的上神
        ke1_shang_idx = cls.DIZHI.index(ke1_shang) if ke1_shang in cls.DIZHI else 0
        ke2_shang = tian_pan.get(ke1_shang_idx + 1, ke1_shang)
        ke2 = {'name': '第二课', 'shang': ke2_shang, 'xia': ke1_shang}
        
        # 第三课：日支上神
        ri_zhi_idx = cls.DIZHI.index(ri_zhi) if ri_zhi in cls.DIZHI else 0
        ke3_shang = tian_pan.get(ri_zhi_idx + 1, ri_zhi)
        ke3 = {'name': '第三课', 'shang': ke3_shang, 'xia': ri_zhi}
        
        # 第四课：日支上神的上神
        ke3_shang_idx = cls.DIZHI.index(ke3_shang) if ke3_shang in cls.DIZHI else 0
        ke4_shang = tian_pan.get(ke3_shang_idx + 1, ke3_shang)
        ke4 = {'name': '第四课', 'shang': ke4_shang, 'xia': ke3_shang}
        
        return [ke1, ke2, ke3, ke4]
    
    @classmethod
    def find_ke_with_relation(cls, si_ke: List[Dict], relation: str) -> List[Dict]:
        """找出有特定关系的课
        
        Args:
            si_ke: 四课列表
            relation: 关系类型（克/生/比等）
            
        Returns:
            符合条件的课列表
        """
        results = []
        for ke in si_ke:
            shang = ke['shang']
            xia = ke['xia']
            # 这里可以添加五行生克判断逻辑
            # 简化版暂不实现
        return results

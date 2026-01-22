"""
三奇六仪计算器
计算三奇六仪的布局
"""
from typing import Dict


class SanQiLiuYiCalculator:
    """三奇六仪计算类"""
    
    # 三奇六仪顺序（戊-己-庚-辛-壬-癸-丁-丙-乙）
    SAN_QI_LIU_YI = ['戊', '己', '庚', '辛', '壬', '癸', '丁', '丙', '乙']
    
    # 旬首对应的六仪
    XUN_SHOU_LIU_YI = {
        '甲子': '戊', '甲戌': '己', '甲申': '庚',
        '甲午': '辛', '甲辰': '壬', '甲寅': '癸'
    }
    
    # 天干
    TIANGAN = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']
    
    # 地支
    DIZHI = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']
    
    @classmethod
    def get_xun_shou(cls, ganzhi: str) -> str:
        """获取旬首
        
        Args:
            ganzhi: 干支，如"甲子"
            
        Returns:
            旬首，如"甲子"
        """
        if len(ganzhi) < 2:
            return '甲子'
        
        gan = ganzhi[0]
        zhi = ganzhi[1]
        
        try:
            gan_idx = cls.TIANGAN.index(gan)
            zhi_idx = cls.DIZHI.index(zhi)
        except ValueError:
            return '甲子'
        
        # 旬首计算
        xun_zhi_idx = (zhi_idx - gan_idx) % 12
        xun_shou_map = {0: '甲子', 2: '甲寅', 4: '甲辰', 
                        6: '甲午', 8: '甲申', 10: '甲戌'}
        return xun_shou_map.get(xun_zhi_idx, '甲子')
    
    @classmethod
    def get_dun_gan(cls, ganzhi: str) -> str:
        """获取遁甲干（甲遁于某仪下）
        
        Args:
            ganzhi: 干支
            
        Returns:
            遁甲干（六仪之一）
        """
        xun_shou = cls.get_xun_shou(ganzhi)
        return cls.XUN_SHOU_LIU_YI.get(xun_shou, '戊')
    
    @classmethod
    def calculate_di_pan(cls, ju_shu: int, is_yang: bool) -> Dict[int, str]:
        """计算地盘三奇六仪布局
        
        Args:
            ju_shu: 局数（1-9）
            is_yang: 是否阳遁
            
        Returns:
            {宫位: 天干}
        """
        from .jiugong import JiuGongCalculator
        
        gong_gan = {}
        start_gong = ju_shu
        
        for i, gan in enumerate(cls.SAN_QI_LIU_YI):
            gong = JiuGongCalculator.rotate(start_gong, i, is_yang)
            gong_gan[gong] = gan
        
        # 中宫继承寄宫
        gong_gan[5] = gong_gan.get(JiuGongCalculator.ZHONG_GONG_JI, '戊')
        
        return gong_gan
    
    @classmethod
    def calculate_tian_pan(cls, di_pan: Dict[int, str], ref_ganzhi: str, 
                           is_yang: bool) -> Dict[int, str]:
        """计算天盘三奇六仪布局
        
        Args:
            di_pan: 地盘布局
            ref_ganzhi: 参考干支（时干支）
            is_yang: 是否阳遁
            
        Returns:
            {宫位: 天干}
        """
        from .jiugong import JiuGongCalculator
        
        # 获取参考干对应的遁甲干
        ref_gan = ref_ganzhi[0] if ref_ganzhi else '戊'
        if ref_gan == '甲':
            ref_gan = cls.get_dun_gan(ref_ganzhi)
        
        # 找到参考干在地盘的位置
        di_pan_reverse = {v: k for k, v in di_pan.items()}
        start_gong = di_pan_reverse.get(ref_gan, 1)
        if start_gong == 5:
            start_gong = JiuGongCalculator.ZHONG_GONG_JI
        
        # 转盘式：整体旋转
        gong_gan = {}
        for i, gan in enumerate(cls.SAN_QI_LIU_YI):
            gong = JiuGongCalculator.rotate(start_gong, i, is_yang)
            gong_gan[gong] = gan
        
        # 中宫继承寄宫
        gong_gan[5] = gong_gan.get(JiuGongCalculator.ZHONG_GONG_JI, '戊')
        
        return gong_gan

"""
三传计算器
计算大六壬的三传（初传、中传、末传）
"""
from typing import Dict, List, Tuple


class SanChuanCalculator:
    """三传计算类"""
    
    # 十二地支
    DIZHI = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']
    
    # 地支五行
    DIZHI_WUXING = {
        '子': '水', '丑': '土', '寅': '木', '卯': '木',
        '辰': '土', '巳': '火', '午': '火', '未': '土',
        '申': '金', '酉': '金', '戌': '土', '亥': '水'
    }
    
    # 五行相克
    KE_MAP = {
        '木': '土', '土': '水', '水': '火', '火': '金', '金': '木'
    }
    
    @classmethod
    def calculate(cls, si_ke: List[Dict], tian_pan: Dict[int, str],
                  ri_gan: str, ri_zhi: str) -> Dict:
        """计算三传
        
        Args:
            si_ke: 四课
            tian_pan: 天盘
            ri_gan: 日干
            ri_zhi: 日支
            
        Returns:
            三传信息
        """
        # 发用（初传）的确定遵循九宗门规则
        # 1. 贼克：下克上用下，上克下用上
        # 2. 比用：无克取比
        # 3. 涉害：多克取涉害深者
        # ... 其他规则
        
        # 简化版：取第一课上神为初传
        chu_chuan = si_ke[0]['shang'] if si_ke else '子'
        
        # 中传：初传的上神
        chu_idx = cls.DIZHI.index(chu_chuan) if chu_chuan in cls.DIZHI else 0
        zhong_chuan = tian_pan.get(chu_idx + 1, chu_chuan)
        
        # 末传：中传的上神
        zhong_idx = cls.DIZHI.index(zhong_chuan) if zhong_chuan in cls.DIZHI else 0
        mo_chuan = tian_pan.get(zhong_idx + 1, zhong_chuan)
        
        # 判断三传类型
        chuan_type = cls._get_chuan_type(chu_chuan, zhong_chuan, mo_chuan)
        
        return {
            'chu_chuan': chu_chuan,
            'zhong_chuan': zhong_chuan,
            'mo_chuan': mo_chuan,
            'type': chuan_type,
            'interpretation': cls._get_interpretation(chuan_type)
        }
    
    @classmethod
    def _get_chuan_type(cls, chu: str, zhong: str, mo: str) -> str:
        """判断三传类型"""
        # 三传顺序判断
        chu_idx = cls.DIZHI.index(chu) if chu in cls.DIZHI else 0
        zhong_idx = cls.DIZHI.index(zhong) if zhong in cls.DIZHI else 0
        mo_idx = cls.DIZHI.index(mo) if mo in cls.DIZHI else 0
        
        # 顺传
        if (zhong_idx - chu_idx) % 12 == (mo_idx - zhong_idx) % 12:
            diff = (zhong_idx - chu_idx) % 12
            if diff == 2:
                return '进茹'
            elif diff == 10:  # -2 mod 12
                return '退茹'
        
        # 三传相同
        if chu == zhong == mo:
            return '三刑'
        
        return '普通'
    
    @classmethod
    def _get_interpretation(cls, chuan_type: str) -> str:
        """获取三传解释"""
        interpretations = {
            '进茹': '事情进展顺利，步步高升',
            '退茹': '事情有阻滞，需要退让',
            '三刑': '反复多变，需要谨慎',
            '普通': '正常发展，按部就班'
        }
        return interpretations.get(chuan_type, '待分析')

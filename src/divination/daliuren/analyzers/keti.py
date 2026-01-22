"""
课体分析器
分析大六壬的课体类型
"""
from typing import Dict, List


class KetiAnalyzer:
    """课体分析类"""
    
    # 课体类型定义
    KETI_TYPES = {
        '贼克': {'meaning': '有冲突、争斗之象'},
        '比用': {'meaning': '平和、协调之象'},
        '涉害': {'meaning': '复杂、多变之象'},
        '遥克': {'meaning': '远方、间接影响'},
        '昴星': {'meaning': '隐秘、暗中进行'},
        '别责': {'meaning': '特殊、例外情况'},
        '八专': {'meaning': '专一、集中力量'},
        '伏吟': {'meaning': '停滞、等待时机'},
        '反吟': {'meaning': '反复、变化无常'}
    }
    
    @classmethod
    def analyze(cls, si_ke: List[Dict], san_chuan: Dict) -> Dict:
        """分析课体
        
        Args:
            si_ke: 四课
            san_chuan: 三传
            
        Returns:
            课体分析结果
        """
        keti = cls._determine_keti(si_ke)
        
        return {
            'type': keti,
            'meaning': cls.KETI_TYPES.get(keti, {}).get('meaning', ''),
            'details': cls._get_details(keti, si_ke, san_chuan)
        }
    
    @classmethod
    def _determine_keti(cls, si_ke: List[Dict]) -> str:
        """确定课体类型"""
        # 简化版：检查四课中是否有克关系
        # 实际需要根据复杂的规则判断
        
        has_ke = False
        for ke in si_ke:
            shang = ke.get('shang', '')
            xia = ke.get('xia', '')
            if cls._check_ke(shang, xia):
                has_ke = True
                break
        
        if has_ke:
            return '贼克'
        return '比用'
    
    @classmethod
    def _check_ke(cls, shang: str, xia: str) -> bool:
        """检查是否有克关系"""
        # 简化版
        dizhi_wuxing = {
            '子': '水', '丑': '土', '寅': '木', '卯': '木',
            '辰': '土', '巳': '火', '午': '火', '未': '土',
            '申': '金', '酉': '金', '戌': '土', '亥': '水'
        }
        ke_map = {
            '木': '土', '土': '水', '水': '火', '火': '金', '金': '木'
        }
        
        shang_wx = dizhi_wuxing.get(shang, '')
        xia_wx = dizhi_wuxing.get(xia, '')
        
        if shang_wx and xia_wx:
            return ke_map.get(shang_wx) == xia_wx or ke_map.get(xia_wx) == shang_wx
        return False
    
    @classmethod
    def _get_details(cls, keti: str, si_ke: List[Dict], san_chuan: Dict) -> str:
        """获取详细分析"""
        details = f"课体为{keti}。"
        
        if keti == '贼克':
            details += "四课中有克关系，主事情有冲突、竞争之象。"
        elif keti == '比用':
            details += "四课和谐，主事情平稳发展。"
        
        return details

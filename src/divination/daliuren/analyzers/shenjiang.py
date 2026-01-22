"""
神将分析器
分析大六壬的十二天将
"""
from typing import Dict, List


class ShenJiangAnalyzer:
    """神将分析类"""
    
    # 十二天将
    TIAN_JIANG = ['贵人', '腾蛇', '朱雀', '六合', '勾陈', '青龙',
                  '天空', '白虎', '太常', '玄武', '太阴', '天后']
    
    # 十二天将属性
    TIAN_JIANG_ATTR = {
        '贵人': {'nature': '吉', 'wuxing': '土', 'meaning': '贵人星，主尊贵、权威'},
        '腾蛇': {'nature': '凶', 'wuxing': '火', 'meaning': '虚惊怪异，主惊恐、虚假'},
        '朱雀': {'nature': '凶', 'wuxing': '火', 'meaning': '口舌是非，主文书、争论'},
        '六合': {'nature': '吉', 'wuxing': '木', 'meaning': '和合之神，主婚姻、合作'},
        '勾陈': {'nature': '凶', 'wuxing': '土', 'meaning': '争斗之神，主官讼、牢狱'},
        '青龙': {'nature': '吉', 'wuxing': '木', 'meaning': '吉庆之神，主财喜、升迁'},
        '天空': {'nature': '凶', 'wuxing': '土', 'meaning': '虚空之神，主欺诈、落空'},
        '白虎': {'nature': '凶', 'wuxing': '金', 'meaning': '凶煞之神，主血光、疾病'},
        '太常': {'nature': '吉', 'wuxing': '土', 'meaning': '宴会之神，主饮食、衣禄'},
        '玄武': {'nature': '凶', 'wuxing': '水', 'meaning': '盗贼之神，主偷盗、欺诈'},
        '太阴': {'nature': '吉', 'wuxing': '金', 'meaning': '阴私之神，主隐秘、策划'},
        '天后': {'nature': '吉', 'wuxing': '水', 'meaning': '阴贵之神，主妇女、阴私'}
    }
    
    # 天将落宫（根据日干确定贵人位置）
    GUI_REN_YANG = {
        '甲': '丑', '戊': '丑', '庚': '丑',
        '乙': '子', '己': '子',
        '丙': '亥', '丁': '亥',
        '壬': '巳', '癸': '巳',
        '辛': '午'
    }
    
    GUI_REN_YIN = {
        '甲': '未', '戊': '未', '庚': '未',
        '乙': '申', '己': '申',
        '丙': '酉', '丁': '酉',
        '壬': '卯', '癸': '卯',
        '辛': '寅'
    }
    
    @classmethod
    def calculate(cls, ri_gan: str, shi_zhi: str) -> Dict[str, str]:
        """计算十二天将布局
        
        Args:
            ri_gan: 日干
            shi_zhi: 时支
            
        Returns:
            天将布局 {地支: 天将}
        """
        dizhi = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']
        
        # 判断用昼贵还是夜贵
        shi_idx = dizhi.index(shi_zhi) if shi_zhi in dizhi else 0
        is_day = 3 <= shi_idx <= 8  # 寅到未为昼
        
        # 获取贵人位置
        gui_ren_zhi = cls.GUI_REN_YANG.get(ri_gan, '丑') if is_day else cls.GUI_REN_YIN.get(ri_gan, '未')
        gui_ren_idx = dizhi.index(gui_ren_zhi) if gui_ren_zhi in dizhi else 0
        
        # 布十二天将
        jiang_layout = {}
        for i, jiang in enumerate(cls.TIAN_JIANG):
            zhi_idx = (gui_ren_idx + i) % 12
            jiang_layout[dizhi[zhi_idx]] = jiang
        
        return jiang_layout
    
    @classmethod
    def analyze(cls, jiang_layout: Dict[str, str], san_chuan: Dict) -> List[Dict]:
        """分析天将
        
        Args:
            jiang_layout: 天将布局
            san_chuan: 三传
            
        Returns:
            天将分析结果
        """
        results = []
        
        # 分析三传落在的天将
        for chuan_name, chuan_zhi in [('初传', san_chuan.get('chu_chuan', '')),
                                       ('中传', san_chuan.get('zhong_chuan', '')),
                                       ('末传', san_chuan.get('mo_chuan', ''))]:
            jiang = jiang_layout.get(chuan_zhi, '')
            if jiang and jiang in cls.TIAN_JIANG_ATTR:
                attr = cls.TIAN_JIANG_ATTR[jiang]
                results.append({
                    'position': chuan_name,
                    'dizhi': chuan_zhi,
                    'jiang': jiang,
                    'nature': attr['nature'],
                    'meaning': attr['meaning']
                })
        
        return results

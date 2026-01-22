"""
神煞分析器
分析奇门遁甲中的神煞
"""
from typing import Dict, List


class ShenShaAnalyzer:
    """神煞分析类"""
    
    # 八神定义
    BA_SHEN = ['值符', '腾蛇', '太阴', '六合', '白虎', '玄武', '九地', '九天']
    
    # 八神属性
    BA_SHEN_ATTR = {
        '值符': {'nature': '吉', 'meaning': '贵人星，主尊贵、权威'},
        '腾蛇': {'nature': '凶', 'meaning': '虚惊怪异，主惊恐、虚假'},
        '太阴': {'nature': '吉', 'meaning': '阴私暗昧，主隐秘、策划'},
        '六合': {'nature': '吉', 'meaning': '和合之神，主婚姻、合作'},
        '白虎': {'nature': '凶', 'meaning': '凶煞之神，主血光、疾病'},
        '玄武': {'nature': '凶', 'meaning': '盗贼之神，主偷盗、欺诈'},
        '九地': {'nature': '吉', 'meaning': '坤顺之神，主稳固、守成'},
        '九天': {'nature': '吉', 'meaning': '乾健之神，主刚强、进取'}
    }
    
    # 九星定义
    JIU_XING = ['蓬', '芮', '冲', '辅', '禽', '心', '柱', '任', '英']
    
    # 九星属性
    JIU_XING_ATTR = {
        '蓬': {'nature': '凶', 'wuxing': '水', 'meaning': '天蓬星，主盗贼'},
        '芮': {'nature': '凶', 'wuxing': '土', 'meaning': '天芮星，主疾病'},
        '冲': {'nature': '吉', 'wuxing': '木', 'meaning': '天冲星，主武勇'},
        '辅': {'nature': '吉', 'wuxing': '木', 'meaning': '天辅星，主文昌'},
        '禽': {'nature': '中', 'wuxing': '土', 'meaning': '天禽星，主中和'},
        '心': {'nature': '吉', 'wuxing': '火', 'meaning': '天心星，主医药'},
        '柱': {'nature': '中', 'wuxing': '金', 'meaning': '天柱星，主隐遁'},
        '任': {'nature': '吉', 'wuxing': '土', 'meaning': '天任星，主慈善'},
        '英': {'nature': '中', 'wuxing': '火', 'meaning': '天英星，主血光'}
    }
    
    # 八门定义
    BA_MEN = ['休', '生', '伤', '杜', '景', '死', '惊', '开']
    
    # 八门属性
    BA_MEN_ATTR = {
        '休': {'nature': '吉', 'wuxing': '水', 'meaning': '休门，主休息、求财'},
        '生': {'nature': '吉', 'wuxing': '土', 'meaning': '生门，主生发、营造'},
        '伤': {'nature': '凶', 'wuxing': '木', 'meaning': '伤门，主伤害、捕捉'},
        '杜': {'nature': '中', 'wuxing': '木', 'meaning': '杜门，主堵塞、躲藏'},
        '景': {'nature': '中', 'wuxing': '火', 'meaning': '景门，主光明、文书'},
        '死': {'nature': '凶', 'wuxing': '土', 'meaning': '死门，主死亡、哭泣'},
        '惊': {'nature': '凶', 'wuxing': '金', 'meaning': '惊门，主惊恐、官讼'},
        '开': {'nature': '吉', 'wuxing': '金', 'meaning': '开门，主开张、出行'}
    }
    
    @classmethod
    def analyze_ba_shen(cls, ba_shen: Dict[int, str]) -> List[Dict]:
        """分析八神
        
        Args:
            ba_shen: 八神布局 {宫位: 神}
            
        Returns:
            八神分析结果
        """
        results = []
        for gong, shen in ba_shen.items():
            if shen in cls.BA_SHEN_ATTR:
                attr = cls.BA_SHEN_ATTR[shen]
                results.append({
                    'gong': gong,
                    'shen': shen,
                    'nature': attr['nature'],
                    'meaning': attr['meaning']
                })
        return results
    
    @classmethod
    def analyze_jiu_xing(cls, jiu_xing: Dict[int, str]) -> List[Dict]:
        """分析九星
        
        Args:
            jiu_xing: 九星布局 {宫位: 星}
            
        Returns:
            九星分析结果
        """
        results = []
        for gong, xing in jiu_xing.items():
            if xing in cls.JIU_XING_ATTR:
                attr = cls.JIU_XING_ATTR[xing]
                results.append({
                    'gong': gong,
                    'xing': xing,
                    'nature': attr['nature'],
                    'wuxing': attr['wuxing'],
                    'meaning': attr['meaning']
                })
        return results
    
    @classmethod
    def analyze_ba_men(cls, ba_men: Dict[int, str]) -> List[Dict]:
        """分析八门
        
        Args:
            ba_men: 八门布局 {宫位: 门}
            
        Returns:
            八门分析结果
        """
        results = []
        for gong, men in ba_men.items():
            if men in cls.BA_MEN_ATTR:
                attr = cls.BA_MEN_ATTR[men]
                results.append({
                    'gong': gong,
                    'men': men,
                    'nature': attr['nature'],
                    'wuxing': attr['wuxing'],
                    'meaning': attr['meaning']
                })
        return results
    
    @classmethod
    def get_ji_men(cls) -> List[str]:
        """获取吉门列表"""
        return [men for men, attr in cls.BA_MEN_ATTR.items() if attr['nature'] == '吉']
    
    @classmethod
    def get_xiong_men(cls) -> List[str]:
        """获取凶门列表"""
        return [men for men, attr in cls.BA_MEN_ATTR.items() if attr['nature'] == '凶']

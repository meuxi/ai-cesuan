"""
五行分析器
分析八字中的五行力量、生克关系
"""
from typing import Dict, List


class WuXingAnalyzer:
    """五行分析类"""
    
    # 五行
    WUXING = ['木', '火', '土', '金', '水']
    
    # 天干五行
    TIANGAN_WUXING = {
        '甲': '木', '乙': '木',
        '丙': '火', '丁': '火',
        '戊': '土', '己': '土',
        '庚': '金', '辛': '金',
        '壬': '水', '癸': '水'
    }
    
    # 地支五行
    DIZHI_WUXING = {
        '子': '水', '丑': '土', '寅': '木', '卯': '木',
        '辰': '土', '巳': '火', '午': '火', '未': '土',
        '申': '金', '酉': '金', '戌': '土', '亥': '水'
    }
    
    # 五行相生
    SHENG_MAP = {
        '木': '火', '火': '土', '土': '金', '金': '水', '水': '木'
    }
    
    # 五行相克
    KE_MAP = {
        '木': '土', '土': '水', '水': '火', '火': '金', '金': '木'
    }
    
    @classmethod
    def analyze(cls, sizhu: Dict[str, str]) -> Dict:
        """分析八字五行
        
        Args:
            sizhu: 四柱信息 {'year': '甲子', 'month': '乙丑', ...}
            
        Returns:
            五行分析结果
        """
        # 统计五行数量
        wuxing_count = {wx: 0 for wx in cls.WUXING}
        
        for pillar_name, pillar in sizhu.items():
            if len(pillar) >= 2:
                gan = pillar[0]
                zhi = pillar[1]
                
                # 天干五行
                gan_wx = cls.TIANGAN_WUXING.get(gan)
                if gan_wx:
                    wuxing_count[gan_wx] += 1
                
                # 地支五行
                zhi_wx = cls.DIZHI_WUXING.get(zhi)
                if zhi_wx:
                    wuxing_count[zhi_wx] += 1
        
        # 分析结果
        total = sum(wuxing_count.values())
        
        # 找出最多和最少的五行
        max_wx = max(wuxing_count.items(), key=lambda x: x[1])
        min_wx = min(wuxing_count.items(), key=lambda x: x[1])
        
        # 缺失的五行
        missing = [wx for wx, count in wuxing_count.items() if count == 0]
        
        return {
            'distribution': wuxing_count,
            'dominant': max_wx[0] if max_wx[1] > 0 else None,
            'weak': min_wx[0] if min_wx[1] < total / 5 else None,
            'missing': missing,
            'balance': cls._evaluate_balance(wuxing_count),
            'suggestions': cls._generate_suggestions(wuxing_count, missing)
        }
    
    @classmethod
    def _evaluate_balance(cls, wuxing_count: Dict[str, int]) -> str:
        """评估五行平衡度"""
        values = list(wuxing_count.values())
        avg = sum(values) / len(values)
        variance = sum((v - avg) ** 2 for v in values) / len(values)
        
        if variance < 0.5:
            return '五行平衡'
        elif variance < 1.5:
            return '五行较平衡'
        elif variance < 3:
            return '五行略有偏颇'
        else:
            return '五行偏颇较重'
    
    @classmethod
    def _generate_suggestions(cls, wuxing_count: Dict[str, int], 
                             missing: List[str]) -> List[str]:
        """生成五行调理建议"""
        suggestions = []
        
        if missing:
            for wx in missing:
                if wx == '木':
                    suggestions.append('命中缺木，宜从事木业、绿色事业，多穿绿色')
                elif wx == '火':
                    suggestions.append('命中缺火，宜从事火业、光电事业，多穿红色')
                elif wx == '土':
                    suggestions.append('命中缺土，宜从事土业、建筑地产，多穿黄色')
                elif wx == '金':
                    suggestions.append('命中缺金，宜从事金融、机械行业，多穿白色')
                elif wx == '水':
                    suggestions.append('命中缺水，宜从事水利、运输行业，多穿黑色')
        
        # 五行过旺的建议
        for wx, count in wuxing_count.items():
            if count >= 4:
                ke_wx = cls.KE_MAP.get(wx)
                if ke_wx:
                    suggestions.append(f'{wx}过旺，宜用{ke_wx}来制约')
        
        return suggestions if suggestions else ['五行调和，顺其自然']

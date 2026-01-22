"""
局数计算器
计算奇门遁甲的局数（1-9局）
"""
from typing import Dict, Tuple


class JuShuCalculator:
    """局数计算类"""
    
    # 节气对应的局数表（阳遁）
    JIEQI_YANG_JU = {
        '冬至': [1, 7, 4], '小寒': [2, 8, 5], '大寒': [3, 9, 6],
        '立春': [8, 5, 2], '雨水': [9, 6, 3], '惊蛰': [1, 7, 4],
        '春分': [3, 9, 6], '清明': [4, 1, 7], '谷雨': [5, 2, 8],
        '立夏': [4, 1, 7], '小满': [5, 2, 8], '芒种': [6, 3, 9]
    }
    
    # 节气对应的局数表（阴遁）
    JIEQI_YIN_JU = {
        '夏至': [9, 3, 6], '小暑': [8, 2, 5], '大暑': [7, 1, 4],
        '立秋': [2, 5, 8], '处暑': [1, 4, 7], '白露': [9, 3, 6],
        '秋分': [7, 1, 4], '寒露': [6, 9, 3], '霜降': [5, 8, 2],
        '立冬': [6, 9, 3], '小雪': [5, 8, 2], '大雪': [4, 7, 1]
    }
    
    # 阳遁节气列表
    YANG_JIEQI = ['冬至', '小寒', '大寒', '立春', '雨水', '惊蛰',
                  '春分', '清明', '谷雨', '立夏', '小满', '芒种']
    
    # 阴遁节气列表
    YIN_JIEQI = ['夏至', '小暑', '大暑', '立秋', '处暑', '白露',
                 '秋分', '寒露', '霜降', '立冬', '小雪', '大雪']
    
    @classmethod
    def calculate(cls, jieqi: str, yuan: str) -> Tuple[int, bool]:
        """计算局数
        
        Args:
            jieqi: 节气名称
            yuan: 上中下元（'上', '中', '下'）
            
        Returns:
            (局数, 是否阳遁)
        """
        yuan_idx = {'上': 0, '中': 1, '下': 2}.get(yuan, 0)
        
        # 判断阴阳遁
        if jieqi in cls.YANG_JIEQI:
            ju_list = cls.JIEQI_YANG_JU.get(jieqi, [1, 7, 4])
            is_yang = True
        elif jieqi in cls.YIN_JIEQI:
            ju_list = cls.JIEQI_YIN_JU.get(jieqi, [9, 3, 6])
            is_yang = False
        else:
            return 1, True
        
        return ju_list[yuan_idx], is_yang
    
    @classmethod
    def get_yuan(cls, day_ganzhi: str) -> str:
        """根据日干支判断上中下元
        
        Args:
            day_ganzhi: 日干支，如"甲子"
            
        Returns:
            '上', '中', '下'
        """
        # 六十甲子中的位置
        jiazi_60 = [
            '甲子', '乙丑', '丙寅', '丁卯', '戊辰', '己巳', '庚午', '辛未', '壬申', '癸酉',
            '甲戌', '乙亥', '丙子', '丁丑', '戊寅', '己卯', '庚辰', '辛巳', '壬午', '癸未',
            '甲申', '乙酉', '丙戌', '丁亥', '戊子', '己丑', '庚寅', '辛卯', '壬辰', '癸巳',
            '甲午', '乙未', '丙申', '丁酉', '戊戌', '己亥', '庚子', '辛丑', '壬寅', '癸卯',
            '甲辰', '乙巳', '丙午', '丁未', '戊申', '己酉', '庚戌', '辛亥', '壬子', '癸丑',
            '甲寅', '乙卯', '丙辰', '丁巳', '戊午', '己未', '庚申', '辛酉', '壬戌', '癸亥'
        ]
        
        try:
            idx = jiazi_60.index(day_ganzhi)
            # 每旬10天，分上中下三元
            xun_idx = idx // 10
            if xun_idx % 3 == 0:
                return '上'
            elif xun_idx % 3 == 1:
                return '中'
            else:
                return '下'
        except ValueError:
            return '上'

# -*- coding: utf-8 -*-
"""
梅花易数计算服务
来源：mingpan项目 MeihuaService.ts
提供时间起卦和数字起卦功能
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime

# 八卦数据（先天八卦序）
BAGUA = {
    1: {'name': '乾', 'wuxing': '金', 'yao': [1, 1, 1], 'nature': '天'},
    2: {'name': '兑', 'wuxing': '金', 'yao': [1, 1, 0], 'nature': '泽'},
    3: {'name': '离', 'wuxing': '火', 'yao': [1, 0, 1], 'nature': '火'},
    4: {'name': '震', 'wuxing': '木', 'yao': [0, 0, 1], 'nature': '雷'},
    5: {'name': '巽', 'wuxing': '木', 'yao': [0, 1, 1], 'nature': '风'},
    6: {'name': '坎', 'wuxing': '水', 'yao': [0, 1, 0], 'nature': '水'},
    7: {'name': '艮', 'wuxing': '土', 'yao': [1, 0, 0], 'nature': '山'},
    8: {'name': '坤', 'wuxing': '土', 'yao': [0, 0, 0], 'nature': '地'}
}

# 卦名反查
BAGUA_NAME_TO_NUM = {v['name']: k for k, v in BAGUA.items()}

# 64卦名称（上卦-下卦）
GUA64_NAMES = {
    ('乾', '乾'): '乾为天', ('乾', '兑'): '天泽履', ('乾', '离'): '天火同人', ('乾', '震'): '天雷无妄',
    ('乾', '巽'): '天风姤', ('乾', '坎'): '天水讼', ('乾', '艮'): '天山遁', ('乾', '坤'): '天地否',
    ('兑', '乾'): '泽天夬', ('兑', '兑'): '兑为泽', ('兑', '离'): '泽火革', ('兑', '震'): '泽雷随',
    ('兑', '巽'): '泽风大过', ('兑', '坎'): '泽水困', ('兑', '艮'): '泽山咸', ('兑', '坤'): '泽地萃',
    ('离', '乾'): '火天大有', ('离', '兑'): '火泽睽', ('离', '离'): '离为火', ('离', '震'): '火雷噬嗑',
    ('离', '巽'): '火风鼎', ('离', '坎'): '火水未济', ('离', '艮'): '火山旅', ('离', '坤'): '火地晋',
    ('震', '乾'): '雷天大壮', ('震', '兑'): '雷泽归妹', ('震', '离'): '雷火丰', ('震', '震'): '震为雷',
    ('震', '巽'): '雷风恒', ('震', '坎'): '雷水解', ('震', '艮'): '雷山小过', ('震', '坤'): '雷地豫',
    ('巽', '乾'): '风天小畜', ('巽', '兑'): '风泽中孚', ('巽', '离'): '风火家人', ('巽', '震'): '风雷益',
    ('巽', '巽'): '巽为风', ('巽', '坎'): '风水涣', ('巽', '艮'): '风山渐', ('巽', '坤'): '风地观',
    ('坎', '乾'): '水天需', ('坎', '兑'): '水泽节', ('坎', '离'): '水火既济', ('坎', '震'): '水雷屯',
    ('坎', '巽'): '水风井', ('坎', '坎'): '坎为水', ('坎', '艮'): '水山蹇', ('坎', '坤'): '水地比',
    ('艮', '乾'): '山天大畜', ('艮', '兑'): '山泽损', ('艮', '离'): '山火贲', ('艮', '震'): '山雷颐',
    ('艮', '巽'): '山风蛊', ('艮', '坎'): '山水蒙', ('艮', '艮'): '艮为山', ('艮', '坤'): '山地剥',
    ('坤', '乾'): '地天泰', ('坤', '兑'): '地泽临', ('坤', '离'): '地火明夷', ('坤', '震'): '地雷复',
    ('坤', '巽'): '地风升', ('坤', '坎'): '地水师', ('坤', '艮'): '地山谦', ('坤', '坤'): '坤为地'
}

# 五行生克
WUXING_SHENG = {'木': '火', '火': '土', '土': '金', '金': '水', '水': '木'}
WUXING_KE = {'木': '土', '土': '水', '水': '火', '火': '金', '金': '木'}


@dataclass
class GuaXiang:
    """卦象"""
    name: str
    upper_gua: Dict[str, Any]
    lower_gua: Dict[str, Any]


@dataclass
class MeihuaResult:
    """梅花易数结果"""
    method: str  # 'time' or 'number'
    qigua_data: Dict[str, Any]
    time_info: Optional[Dict[str, str]]
    ben_gua: GuaXiang  # 本卦
    bian_gua: GuaXiang  # 变卦
    hu_gua: GuaXiang  # 互卦
    moving_yao: int  # 动爻（1-6）
    ti_yong: Dict[str, Any]  # 体用关系


class MeihuaCalculator:
    """梅花易数计算器"""
    
    @classmethod
    def calculate_by_number(cls, num1: int, num2: int, 
                            yao_num: Optional[int] = None) -> MeihuaResult:
        """
        数字起卦
        
        Args:
            num1: 第一个数（上卦）
            num2: 第二个数（下卦）
            yao_num: 动爻数（可选，默认为num1+num2）
        """
        # 计算上下卦
        upper_index = ((num1 - 1) % 8) + 1
        lower_index = ((num2 - 1) % 8) + 1
        
        # 计算动爻
        total = num1 + num2
        if yao_num is not None:
            moving_yao = ((yao_num - 1) % 6) + 1
        else:
            moving_yao = ((total - 1) % 6) + 1
        
        qigua_data = {
            'upper_index': upper_index,
            'lower_index': lower_index,
            'moving_yao': moving_yao,
            'method': 'number',
            'input': {'num1': num1, 'num2': num2}
        }
        
        return cls._build_result('number', qigua_data, None)
    
    @classmethod
    def calculate_by_time(cls, year: int, month: int, day: int, 
                          hour: int, is_lunar: bool = False) -> MeihuaResult:
        """
        时间起卦
        
        传统方法：年数+月数+日数 除8余数为上卦
                 年数+月数+日数+时数 除8余数为下卦
                 总数 除6余数为动爻
        """
        # 简化处理：使用公历
        # 年数取地支序数（子1丑2...亥12）
        year_num = ((year - 4) % 12) + 1  # 简化：年份对12取余
        
        # 上卦数 = 年+月+日
        upper_num = year_num + month + day
        upper_index = ((upper_num - 1) % 8) + 1
        
        # 下卦数 = 年+月+日+时
        lower_num = upper_num + hour
        lower_index = ((lower_num - 1) % 8) + 1
        
        # 动爻 = 总数 mod 6
        total = lower_num
        moving_yao = ((total - 1) % 6) + 1
        
        qigua_data = {
            'upper_index': upper_index,
            'lower_index': lower_index,
            'moving_yao': moving_yao,
            'method': 'time',
            'input': {'year': year, 'month': month, 'day': day, 'hour': hour}
        }
        
        time_info = {
            'solar_date': f'{year}年{month}月{day}日',
            'hour': f'{hour}时'
        }
        
        return cls._build_result('time', qigua_data, time_info)
    
    @classmethod
    def _build_result(cls, method: str, qigua_data: Dict, 
                      time_info: Optional[Dict]) -> MeihuaResult:
        """构建结果"""
        upper_index = qigua_data['upper_index']
        lower_index = qigua_data['lower_index']
        moving_yao = qigua_data['moving_yao']
        
        # 获取上下卦信息
        upper_gua = BAGUA[upper_index]
        lower_gua = BAGUA[lower_index]
        
        # 本卦
        ben_gua_name = GUA64_NAMES.get(
            (upper_gua['name'], lower_gua['name']), 
            f"{upper_gua['name']}{lower_gua['name']}"
        )
        ben_gua = GuaXiang(
            name=ben_gua_name,
            upper_gua=upper_gua,
            lower_gua=lower_gua
        )
        
        # 变卦（动爻变）
        bian_upper, bian_lower = cls._calculate_bian_gua(
            upper_gua['name'], lower_gua['name'], moving_yao
        )
        bian_upper_info = BAGUA[BAGUA_NAME_TO_NUM[bian_upper]]
        bian_lower_info = BAGUA[BAGUA_NAME_TO_NUM[bian_lower]]
        bian_gua_name = GUA64_NAMES.get(
            (bian_upper, bian_lower),
            f"{bian_upper}{bian_lower}"
        )
        bian_gua = GuaXiang(
            name=bian_gua_name,
            upper_gua=bian_upper_info,
            lower_gua=bian_lower_info
        )
        
        # 互卦
        hu_upper, hu_lower = cls._calculate_hu_gua(
            upper_gua['name'], lower_gua['name']
        )
        hu_upper_info = BAGUA[BAGUA_NAME_TO_NUM[hu_upper]]
        hu_lower_info = BAGUA[BAGUA_NAME_TO_NUM[hu_lower]]
        hu_gua_name = GUA64_NAMES.get(
            (hu_upper, hu_lower),
            f"{hu_upper}{hu_lower}"
        )
        hu_gua = GuaXiang(
            name=hu_gua_name,
            upper_gua=hu_upper_info,
            lower_gua=hu_lower_info
        )
        
        # 体用关系
        ti_yong = cls._calculate_ti_yong(
            upper_gua['wuxing'], lower_gua['wuxing'], moving_yao
        )
        
        return MeihuaResult(
            method=method,
            qigua_data=qigua_data,
            time_info=time_info,
            ben_gua=ben_gua,
            bian_gua=bian_gua,
            hu_gua=hu_gua,
            moving_yao=moving_yao,
            ti_yong=ti_yong
        )
    
    @classmethod
    def _calculate_bian_gua(cls, upper_name: str, lower_name: str, 
                            moving_yao: int) -> tuple:
        """计算变卦"""
        upper_yao = list(BAGUA[BAGUA_NAME_TO_NUM[upper_name]]['yao'])
        lower_yao = list(BAGUA[BAGUA_NAME_TO_NUM[lower_name]]['yao'])
        
        # 六爻组合（下卦在下，上卦在上）
        all_yao = lower_yao + upper_yao  # [1,2,3,4,5,6] 对应位置
        
        # 动爻变（0变1，1变0）
        yao_index = moving_yao - 1
        all_yao[yao_index] = 1 - all_yao[yao_index]
        
        # 分离上下卦
        new_lower_yao = all_yao[:3]
        new_upper_yao = all_yao[3:]
        
        # 根据爻组合找卦名
        new_upper = cls._yao_to_gua_name(new_upper_yao)
        new_lower = cls._yao_to_gua_name(new_lower_yao)
        
        return new_upper, new_lower
    
    @classmethod
    def _calculate_hu_gua(cls, upper_name: str, lower_name: str) -> tuple:
        """计算互卦（取2-3-4爻为下互，3-4-5爻为上互）"""
        upper_yao = BAGUA[BAGUA_NAME_TO_NUM[upper_name]]['yao']
        lower_yao = BAGUA[BAGUA_NAME_TO_NUM[lower_name]]['yao']
        
        # 六爻组合
        all_yao = list(lower_yao) + list(upper_yao)
        
        # 下互卦：2-3-4爻
        hu_lower_yao = all_yao[1:4]
        # 上互卦：3-4-5爻
        hu_upper_yao = all_yao[2:5]
        
        hu_upper = cls._yao_to_gua_name(hu_upper_yao)
        hu_lower = cls._yao_to_gua_name(hu_lower_yao)
        
        return hu_upper, hu_lower
    
    @classmethod
    def _yao_to_gua_name(cls, yao: List[int]) -> str:
        """根据爻组合找卦名"""
        for num, info in BAGUA.items():
            if info['yao'] == yao:
                return info['name']
        return '坤'  # 默认
    
    @classmethod
    def _calculate_ti_yong(cls, upper_wuxing: str, lower_wuxing: str,
                           moving_yao: int) -> Dict[str, Any]:
        """
        计算体用关系
        动爻在上卦（4-6爻），上卦为用，下卦为体
        动爻在下卦（1-3爻），下卦为用，上卦为体
        """
        if moving_yao <= 3:
            ti = upper_wuxing
            yong = lower_wuxing
            ti_position = '上卦'
            yong_position = '下卦'
        else:
            ti = lower_wuxing
            yong = upper_wuxing
            ti_position = '下卦'
            yong_position = '上卦'
        
        # 判断体用生克关系
        if WUXING_SHENG.get(yong) == ti:
            relation = '用生体'
            judgment = '吉'
        elif WUXING_SHENG.get(ti) == yong:
            relation = '体生用'
            judgment = '泄'
        elif WUXING_KE.get(yong) == ti:
            relation = '用克体'
            judgment = '凶'
        elif WUXING_KE.get(ti) == yong:
            relation = '体克用'
            judgment = '小吉'
        elif ti == yong:
            relation = '体用比和'
            judgment = '平'
        else:
            relation = '无直接生克'
            judgment = '平'
        
        return {
            'ti': ti,
            'yong': yong,
            'ti_position': ti_position,
            'yong_position': yong_position,
            'relation': relation,
            'judgment': judgment
        }

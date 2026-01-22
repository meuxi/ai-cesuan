"""
梅花易数完整计算服务
支持：
1. 数字起卦
2. 时间起卦（含真太阳时校正）
3. 体用关系分析
4. 互卦计算
5. 变卦计算
"""
from datetime import datetime
from typing import Dict, Any, Optional, Tuple, List
from lunar_python import Lunar, Solar
import math


# 八卦数据
BAGUA = {
    1: {'name': '乾', 'nature': '天', 'wuxing': '金', 'symbol': '☰', 'binary': '111'},
    2: {'name': '兑', 'nature': '泽', 'wuxing': '金', 'symbol': '☱', 'binary': '110'},
    3: {'name': '离', 'nature': '火', 'wuxing': '火', 'symbol': '☲', 'binary': '101'},
    4: {'name': '震', 'nature': '雷', 'wuxing': '木', 'symbol': '☳', 'binary': '100'},
    5: {'name': '巽', 'nature': '风', 'wuxing': '木', 'symbol': '☴', 'binary': '011'},
    6: {'name': '坎', 'nature': '水', 'wuxing': '水', 'symbol': '☵', 'binary': '010'},
    7: {'name': '艮', 'nature': '山', 'wuxing': '土', 'symbol': '☶', 'binary': '001'},
    8: {'name': '坤', 'nature': '地', 'wuxing': '土', 'symbol': '☷', 'binary': '000'},
}

# 五行生克
WUXING_SHENGKE = {
    '金': {'生': '水', '克': '木', '被生': '土', '被克': '火'},
    '木': {'生': '火', '克': '土', '被生': '水', '被克': '金'},
    '水': {'生': '木', '克': '火', '被生': '金', '被克': '土'},
    '火': {'生': '土', '克': '金', '被生': '木', '被克': '水'},
    '土': {'生': '金', '克': '水', '被生': '火', '被克': '木'},
}

# 六十四卦名称映射
GUA_64_NAMES = {
    (1, 1): '乾为天', (1, 2): '天泽履', (1, 3): '天火同人', (1, 4): '天雷无妄',
    (1, 5): '天风姤', (1, 6): '天水讼', (1, 7): '天山遁', (1, 8): '天地否',
    (2, 1): '泽天夬', (2, 2): '兑为泽', (2, 3): '泽火革', (2, 4): '泽雷随',
    (2, 5): '泽风大过', (2, 6): '泽水困', (2, 7): '泽山咸', (2, 8): '泽地萃',
    (3, 1): '火天大有', (3, 2): '火泽睽', (3, 3): '离为火', (3, 4): '火雷噬嗑',
    (3, 5): '火风鼎', (3, 6): '火水未济', (3, 7): '火山旅', (3, 8): '火地晋',
    (4, 1): '雷天大壮', (4, 2): '雷泽归妹', (4, 3): '雷火丰', (4, 4): '震为雷',
    (4, 5): '雷风恒', (4, 6): '雷水解', (4, 7): '雷山小过', (4, 8): '雷地豫',
    (5, 1): '风天小畜', (5, 2): '风泽中孚', (5, 3): '风火家人', (5, 4): '风雷益',
    (5, 5): '巽为风', (5, 6): '风水涣', (5, 7): '风山渐', (5, 8): '风地观',
    (6, 1): '水天需', (6, 2): '水泽节', (6, 3): '水火既济', (6, 4): '水雷屯',
    (6, 5): '水风井', (6, 6): '坎为水', (6, 7): '水山蹇', (6, 8): '水地比',
    (7, 1): '山天大畜', (7, 2): '山泽损', (7, 3): '山火贲', (7, 4): '山雷颐',
    (7, 5): '山风蛊', (7, 6): '山水蒙', (7, 7): '艮为山', (7, 8): '山地剥',
    (8, 1): '地天泰', (8, 2): '地泽临', (8, 3): '地火明夷', (8, 4): '地雷复',
    (8, 5): '地风升', (8, 6): '地水师', (8, 7): '地山谦', (8, 8): '坤为地',
}


class PlumFlowerService:
    """梅花易数完整计算服务"""
    
    # 经度时区对应表（用于真太阳时计算）
    TIMEZONE_OFFSET = {
        'Beijing': (116.4, 8),  # 北京：东经116.4度，东八区
        'Shanghai': (121.5, 8),
        'Guangzhou': (113.3, 8),
        'Chengdu': (104.1, 8),
        'Xian': (108.9, 8),
    }
    
    @classmethod
    def number_to_gua(cls, num: int) -> int:
        """数字转卦数（1-8）"""
        result = num % 8
        return 8 if result == 0 else result
    
    @classmethod
    def calculate_true_solar_time(
        cls,
        dt: datetime,
        longitude: float = 116.4,
        timezone: int = 8
    ) -> datetime:
        """
        计算真太阳时
        
        Args:
            dt: 标准时间（北京时间）
            longitude: 所在地经度
            timezone: 时区
            
        Returns:
            真太阳时
        """
        # 1. 计算时差（每度4分钟）
        standard_longitude = timezone * 15  # 标准时区经度
        time_diff_minutes = (longitude - standard_longitude) * 4
        
        # 2. 计算时差方程（简化版，考虑地球公转轨道椭圆性）
        day_of_year = dt.timetuple().tm_yday
        b = 2 * math.pi * (day_of_year - 81) / 364
        equation_of_time = 9.87 * math.sin(2 * b) - 7.53 * math.cos(b) - 1.5 * math.sin(b)
        
        # 3. 总时差
        total_minutes = time_diff_minutes + equation_of_time
        
        # 4. 应用时差
        from datetime import timedelta
        return dt + timedelta(minutes=total_minutes)
    
    @classmethod
    def get_lunar_hour_number(cls, hour: int) -> int:
        """获取时辰数（子时为1）"""
        # 子(23-1)=1, 丑(1-3)=2, ..., 亥(21-23)=12
        hour_map = {
            23: 1, 0: 1,
            1: 2, 2: 2,
            3: 3, 4: 3,
            5: 4, 6: 4,
            7: 5, 8: 5,
            9: 6, 10: 6,
            11: 7, 12: 7,
            13: 8, 14: 8,
            15: 9, 16: 9,
            17: 10, 18: 10,
            19: 11, 20: 11,
            21: 12, 22: 12,
        }
        return hour_map.get(hour, 1)
    
    @classmethod
    def calculate_by_number(cls, num1: int, num2: int) -> Dict[str, Any]:
        """
        数字起卦
        
        Args:
            num1: 第一个数字（用于上卦）
            num2: 第二个数字（用于下卦和动爻）
            
        Returns:
            卦象结果
        """
        # 上卦
        upper = cls.number_to_gua(num1)
        # 下卦
        lower = cls.number_to_gua(num2)
        # 动爻 (1-6)
        dong_yao = ((num1 + num2) % 6) or 6
        
        return cls._build_hexagram_result(upper, lower, dong_yao, 'number', {
            'num1': num1,
            'num2': num2
        })
    
    @classmethod
    def calculate_by_time(
        cls,
        year: Optional[int] = None,
        month: Optional[int] = None,
        day: Optional[int] = None,
        hour: Optional[int] = None,
        use_true_solar_time: bool = False,
        longitude: float = 116.4
    ) -> Dict[str, Any]:
        """
        时间起卦
        
        Args:
            year, month, day, hour: 时间，不传则使用当前时间
            use_true_solar_time: 是否使用真太阳时
            longitude: 经度（用于真太阳时计算）
            
        Returns:
            卦象结果
        """
        # 获取时间
        now = datetime.now()
        dt = datetime(
            year or now.year,
            month or now.month,
            day or now.day,
            hour if hour is not None else now.hour,
            now.minute
        )
        
        # 是否使用真太阳时
        if use_true_solar_time:
            dt = cls.calculate_true_solar_time(dt, longitude)
        
        # 转换为农历
        solar = Solar.fromYmdHms(dt.year, dt.month, dt.day, dt.hour, dt.minute, 0)
        lunar = solar.getLunar()
        
        lunar_year = lunar.getYear()
        lunar_month = lunar.getMonth()
        lunar_day = lunar.getDay()
        hour_number = cls.get_lunar_hour_number(dt.hour)
        
        # 上卦：(年+月+日) / 8
        upper_sum = lunar_year + lunar_month + lunar_day
        upper = cls.number_to_gua(upper_sum)
        
        # 下卦：(年+月+日+时) / 8
        lower_sum = upper_sum + hour_number
        lower = cls.number_to_gua(lower_sum)
        
        # 动爻：(年+月+日+时) / 6
        dong_yao = (lower_sum % 6) or 6
        
        return cls._build_hexagram_result(upper, lower, dong_yao, 'time', {
            'solar': f"{dt.year}-{dt.month:02d}-{dt.day:02d} {dt.hour:02d}:{dt.minute:02d}",
            'lunar': f"{lunar_year}年{lunar_month}月{lunar_day}日",
            'hour_number': hour_number,
            'use_true_solar_time': use_true_solar_time,
            'longitude': longitude if use_true_solar_time else None
        })
    
    @classmethod
    def _get_gua_name(cls, upper: int, lower: int) -> str:
        """获取六十四卦名称"""
        return GUA_64_NAMES.get((upper, lower), f'{BAGUA[upper]["name"]}{BAGUA[lower]["name"]}')
    
    @classmethod
    def _calculate_bian_gua(cls, upper: int, lower: int, dong_yao: int) -> Tuple[int, int]:
        """
        计算变卦
        动爻1-3在下卦，4-6在上卦
        """
        upper_binary = list(BAGUA[upper]['binary'])
        lower_binary = list(BAGUA[lower]['binary'])
        
        if dong_yao <= 3:
            # 动爻在下卦
            idx = 3 - dong_yao  # 转换为列表索引
            lower_binary[idx] = '0' if lower_binary[idx] == '1' else '1'
        else:
            # 动爻在上卦
            idx = 6 - dong_yao
            upper_binary[idx] = '0' if upper_binary[idx] == '1' else '1'
        
        # 二进制转卦数
        def binary_to_gua(binary_list: List[str]) -> int:
            binary_str = ''.join(binary_list)
            for num, data in BAGUA.items():
                if data['binary'] == binary_str:
                    return num
            return 1
        
        return binary_to_gua(upper_binary), binary_to_gua(lower_binary)
    
    @classmethod
    def _calculate_hu_gua(cls, upper: int, lower: int) -> Tuple[int, int]:
        """
        计算互卦
        上互：2,3,4爻
        下互：3,4,5爻
        """
        # 组合六爻（上卦在上，下卦在下）
        upper_binary = BAGUA[upper]['binary']
        lower_binary = BAGUA[lower]['binary']
        six_yao = lower_binary + upper_binary  # "下下下上上上"
        
        # 互卦
        # 上互：取2,3,4爻（索引1,2,3）
        hu_upper_binary = six_yao[1:4]
        # 下互：取3,4,5爻（索引2,3,4）
        hu_lower_binary = six_yao[2:5]
        
        def binary_to_gua(binary_str: str) -> int:
            for num, data in BAGUA.items():
                if data['binary'] == binary_str:
                    return num
            return 1
        
        return binary_to_gua(hu_upper_binary), binary_to_gua(hu_lower_binary)
    
    @classmethod
    def _analyze_ti_yong(cls, upper: int, lower: int, dong_yao: int) -> Dict[str, Any]:
        """
        分析体用关系
        体卦：不动之卦
        用卦：动爻所在之卦
        """
        if dong_yao <= 3:
            # 动爻在下卦，下卦为用，上卦为体
            ti_gua = upper
            yong_gua = lower
            ti_position = 'upper'
        else:
            # 动爻在上卦，上卦为用，下卦为体
            ti_gua = lower
            yong_gua = upper
            ti_position = 'lower'
        
        ti_wuxing = BAGUA[ti_gua]['wuxing']
        yong_wuxing = BAGUA[yong_gua]['wuxing']
        
        # 分析生克关系
        relation = cls._analyze_wuxing_relation(ti_wuxing, yong_wuxing)
        
        return {
            'ti': {
                'position': ti_position,
                'gua_num': ti_gua,
                'gua_name': BAGUA[ti_gua]['name'],
                'wuxing': ti_wuxing,
                'nature': BAGUA[ti_gua]['nature'],
                'symbol': BAGUA[ti_gua]['symbol'],
            },
            'yong': {
                'position': 'lower' if ti_position == 'upper' else 'upper',
                'gua_num': yong_gua,
                'gua_name': BAGUA[yong_gua]['name'],
                'wuxing': yong_wuxing,
                'nature': BAGUA[yong_gua]['nature'],
                'symbol': BAGUA[yong_gua]['symbol'],
            },
            'relation': relation,
        }
    
    @classmethod
    def _analyze_wuxing_relation(cls, ti_wuxing: str, yong_wuxing: str) -> Dict[str, Any]:
        """分析五行生克关系"""
        if ti_wuxing == yong_wuxing:
            return {
                'type': '比和',
                'description': f'体用同属{ti_wuxing}，为比和之象',
                'fortune': '平',
                'suggestion': '事情平稳，无大波折'
            }
        
        ti_data = WUXING_SHENGKE[ti_wuxing]
        
        if ti_data['生'] == yong_wuxing:
            return {
                'type': '体生用',
                'description': f'体卦{ti_wuxing}生用卦{yong_wuxing}',
                'fortune': '泄',
                'suggestion': '有所付出，需防耗泄'
            }
        elif ti_data['克'] == yong_wuxing:
            return {
                'type': '体克用',
                'description': f'体卦{ti_wuxing}克用卦{yong_wuxing}',
                'fortune': '吉',
                'suggestion': '能够掌控局面，事可成'
            }
        elif ti_data['被生'] == yong_wuxing:
            return {
                'type': '用生体',
                'description': f'用卦{yong_wuxing}生体卦{ti_wuxing}',
                'fortune': '大吉',
                'suggestion': '得外力相助，事业顺遂'
            }
        elif ti_data['被克'] == yong_wuxing:
            return {
                'type': '用克体',
                'description': f'用卦{yong_wuxing}克体卦{ti_wuxing}',
                'fortune': '凶',
                'suggestion': '受外力压制，需谨慎行事'
            }
        
        return {'type': '未知', 'description': '', 'fortune': '平', 'suggestion': ''}
    
    @classmethod
    def _build_hexagram_result(
        cls,
        upper: int,
        lower: int,
        dong_yao: int,
        method: str,
        input_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """构建完整卦象结果"""
        
        # 本卦
        ben_gua_name = cls._get_gua_name(upper, lower)
        
        # 变卦
        bian_upper, bian_lower = cls._calculate_bian_gua(upper, lower, dong_yao)
        bian_gua_name = cls._get_gua_name(bian_upper, bian_lower)
        
        # 互卦
        hu_upper, hu_lower = cls._calculate_hu_gua(upper, lower)
        hu_gua_name = cls._get_gua_name(hu_upper, hu_lower)
        
        # 体用分析
        ti_yong = cls._analyze_ti_yong(upper, lower, dong_yao)
        
        return {
            'method': method,
            'input': input_data,
            'ben_gua': {
                'name': ben_gua_name,
                'upper': {
                    'num': upper,
                    'name': BAGUA[upper]['name'],
                    'nature': BAGUA[upper]['nature'],
                    'wuxing': BAGUA[upper]['wuxing'],
                    'symbol': BAGUA[upper]['symbol'],
                },
                'lower': {
                    'num': lower,
                    'name': BAGUA[lower]['name'],
                    'nature': BAGUA[lower]['nature'],
                    'wuxing': BAGUA[lower]['wuxing'],
                    'symbol': BAGUA[lower]['symbol'],
                },
                'dong_yao': dong_yao,
                'dong_yao_position': '下卦' if dong_yao <= 3 else '上卦',
            },
            'bian_gua': {
                'name': bian_gua_name,
                'upper': {
                    'num': bian_upper,
                    'name': BAGUA[bian_upper]['name'],
                    'nature': BAGUA[bian_upper]['nature'],
                    'wuxing': BAGUA[bian_upper]['wuxing'],
                    'symbol': BAGUA[bian_upper]['symbol'],
                },
                'lower': {
                    'num': bian_lower,
                    'name': BAGUA[bian_lower]['name'],
                    'nature': BAGUA[bian_lower]['nature'],
                    'wuxing': BAGUA[bian_lower]['wuxing'],
                    'symbol': BAGUA[bian_lower]['symbol'],
                },
            },
            'hu_gua': {
                'name': hu_gua_name,
                'upper': {
                    'num': hu_upper,
                    'name': BAGUA[hu_upper]['name'],
                    'nature': BAGUA[hu_upper]['nature'],
                    'wuxing': BAGUA[hu_upper]['wuxing'],
                    'symbol': BAGUA[hu_upper]['symbol'],
                },
                'lower': {
                    'num': hu_lower,
                    'name': BAGUA[hu_lower]['name'],
                    'nature': BAGUA[hu_lower]['nature'],
                    'wuxing': BAGUA[hu_lower]['wuxing'],
                    'symbol': BAGUA[hu_lower]['symbol'],
                },
            },
            'ti_yong': ti_yong,
            'summary': {
                'ben': ben_gua_name,
                'hu': hu_gua_name,
                'bian': bian_gua_name,
                'dong_yao': f'第{dong_yao}爻动',
                'ti_yong_relation': ti_yong['relation']['type'],
                'fortune': ti_yong['relation']['fortune'],
            }
        }

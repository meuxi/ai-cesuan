"""
八字大运计算模块
计算大运起运年龄、大运序列、流年运势

理论依据：
- 阳男阴女顺排，阴男阳女逆排
- 起运年龄 = 出生日到节气日的天数 / 3
- 每步大运管10年
"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from datetime import date, datetime, timedelta


# 天干地支
TIANGAN = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']
DIZHI = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']

# 阳干阴干
YANG_GAN = ['甲', '丙', '戊', '庚', '壬']
YIN_GAN = ['乙', '丁', '己', '辛', '癸']

# 天干五行
GAN_WUXING = {
    '甲': '木', '乙': '木', '丙': '火', '丁': '火', '戊': '土',
    '己': '土', '庚': '金', '辛': '金', '壬': '水', '癸': '水'
}

# 地支五行
ZHI_WUXING = {
    '子': '水', '丑': '土', '寅': '木', '卯': '木', '辰': '土', '巳': '火',
    '午': '火', '未': '土', '申': '金', '酉': '金', '戌': '土', '亥': '水'
}


@dataclass
class DayunInfo:
    """大运信息"""
    index: int              # 大运序号（从1开始）
    ganzhi: str             # 干支
    gan: str                # 天干
    zhi: str                # 地支
    start_age: int          # 起始年龄
    end_age: int            # 结束年龄
    start_year: int         # 起始公历年份
    end_year: int           # 结束公历年份
    wuxing: str             # 五行
    ten_god: str            # 十神（相对日主）
    is_current: bool        # 是否当前大运
    description: str        # 大运解读


@dataclass
class LiunianInfo:
    """流年信息"""
    year: int               # 公历年份
    ganzhi: str             # 干支
    gan: str                # 天干
    zhi: str                # 地支
    age: int                # 虚岁年龄
    ten_god: str            # 十神
    description: str        # 流年解读


class DayunCalculator:
    """大运计算器"""
    
    # 十神计算表
    SHISHEN_TABLE = {
        '甲': {'甲': '比肩', '乙': '劫财', '丙': '食神', '丁': '伤官', '戊': '偏财',
               '己': '正财', '庚': '七杀', '辛': '正官', '壬': '偏印', '癸': '正印'},
        '乙': {'甲': '劫财', '乙': '比肩', '丙': '伤官', '丁': '食神', '戊': '正财',
               '己': '偏财', '庚': '正官', '辛': '七杀', '壬': '正印', '癸': '偏印'},
        '丙': {'甲': '偏印', '乙': '正印', '丙': '比肩', '丁': '劫财', '戊': '食神',
               '己': '伤官', '庚': '偏财', '辛': '正财', '壬': '七杀', '癸': '正官'},
        '丁': {'甲': '正印', '乙': '偏印', '丙': '劫财', '丁': '比肩', '戊': '伤官',
               '己': '食神', '庚': '正财', '辛': '偏财', '壬': '正官', '癸': '七杀'},
        '戊': {'甲': '七杀', '乙': '正官', '丙': '偏印', '丁': '正印', '戊': '比肩',
               '己': '劫财', '庚': '食神', '辛': '伤官', '壬': '偏财', '癸': '正财'},
        '己': {'甲': '正官', '乙': '七杀', '丙': '正印', '丁': '偏印', '戊': '劫财',
               '己': '比肩', '庚': '伤官', '辛': '食神', '壬': '正财', '癸': '偏财'},
        '庚': {'甲': '偏财', '乙': '正财', '丙': '七杀', '丁': '正官', '戊': '偏印',
               '己': '正印', '庚': '比肩', '辛': '劫财', '壬': '食神', '癸': '伤官'},
        '辛': {'甲': '正财', '乙': '偏财', '丙': '正官', '丁': '七杀', '戊': '正印',
               '己': '偏印', '庚': '劫财', '辛': '比肩', '壬': '伤官', '癸': '食神'},
        '壬': {'甲': '食神', '乙': '伤官', '丙': '偏财', '丁': '正财', '戊': '七杀',
               '己': '正官', '庚': '偏印', '辛': '正印', '壬': '比肩', '癸': '劫财'},
        '癸': {'甲': '伤官', '乙': '食神', '丙': '正财', '丁': '偏财', '戊': '正官',
               '己': '七杀', '庚': '正印', '辛': '偏印', '壬': '劫财', '癸': '比肩'},
    }
    
    # 十神运势解读
    SHISHEN_DAYUN_DESC = {
        '比肩': '竞争与合作并存，适合拓展人脉，但需防破财',
        '劫财': '财运波动较大，不宜投资冒险，守成为上',
        '食神': '才华显露期，适合创作、表达，身体健康',
        '伤官': '思维活跃但易生是非，适合技术创新，避免口舌',
        '偏财': '财运活跃，有意外收获，适合投资理财',
        '正财': '财运稳定，工作顺利，适合置业积累',
        '七杀': '压力与机遇并存，适合突破瓶颈，需防小人',
        '正官': '事业上升期，有升迁机会，贵人相助',
        '偏印': '学业进步期，适合进修学习，偏业有成',
        '正印': '贵人运旺，长辈提携，适合文教工作',
    }
    
    @classmethod
    def is_yang_gan(cls, gan: str) -> bool:
        """判断是否阳干"""
        return gan in YANG_GAN
    
    @classmethod
    def calculate_shishen(cls, day_master: str, target_gan: str) -> str:
        """计算十神"""
        if day_master not in cls.SHISHEN_TABLE:
            return '未知'
        return cls.SHISHEN_TABLE[day_master].get(target_gan, '未知')
    
    @classmethod
    def calculate_qiyun_age(
        cls,
        birth_date: date,
        birth_hour: int,
        gender: str,
        year_gan: str,
        month_jieqi_date: Optional[date] = None,
        next_jieqi_date: Optional[date] = None
    ) -> Tuple[int, str]:
        """
        计算起运年龄
        
        Args:
            birth_date: 出生日期
            birth_hour: 出生时辰（0-23）
            gender: 性别（男/女）
            year_gan: 年干
            month_jieqi_date: 本月节气日期（可选）
            next_jieqi_date: 下月节气日期（可选）
            
        Returns:
            (起运年龄, 顺逆方向)
        """
        is_yang = cls.is_yang_gan(year_gan)
        is_male = gender in ['男', 'male', 'M', 'm']
        
        # 阳男阴女顺排，阴男阳女逆排
        is_forward = (is_yang and is_male) or (not is_yang and not is_male)
        direction = '顺' if is_forward else '逆'
        
        # 如果没有提供节气日期，使用简化计算
        if month_jieqi_date is None or next_jieqi_date is None:
            # 简化计算：假设节气在月初和月中
            day_of_month = birth_date.day
            if is_forward:
                days_to_jieqi = 30 - day_of_month  # 到下一个节气的天数
            else:
                days_to_jieqi = day_of_month  # 到上一个节气的天数
        else:
            if is_forward:
                days_to_jieqi = (next_jieqi_date - birth_date).days
            else:
                days_to_jieqi = (birth_date - month_jieqi_date).days
        
        # 三天折一年
        qiyun_age = max(1, round(days_to_jieqi / 3))
        
        return qiyun_age, direction
    
    @classmethod
    def calculate_dayun_sequence(
        cls,
        month_gan: str,
        month_zhi: str,
        day_master: str,
        birth_year: int,
        qiyun_age: int,
        direction: str,
        count: int = 8
    ) -> List[DayunInfo]:
        """
        计算大运序列
        
        Args:
            month_gan: 月干
            month_zhi: 月支
            day_master: 日主
            birth_year: 出生年份
            qiyun_age: 起运年龄
            direction: 顺逆方向（顺/逆）
            count: 大运数量
            
        Returns:
            大运列表
        """
        dayun_list = []
        
        gan_idx = TIANGAN.index(month_gan)
        zhi_idx = DIZHI.index(month_zhi)
        
        is_forward = direction == '顺'
        
        current_year = datetime.now().year
        current_age = current_year - birth_year + 1  # 虚岁
        
        for i in range(count):
            # 计算大运干支
            if is_forward:
                new_gan_idx = (gan_idx + i + 1) % 10
                new_zhi_idx = (zhi_idx + i + 1) % 12
            else:
                new_gan_idx = (gan_idx - i - 1) % 10
                new_zhi_idx = (zhi_idx - i - 1) % 12
            
            gan = TIANGAN[new_gan_idx]
            zhi = DIZHI[new_zhi_idx]
            ganzhi = gan + zhi
            
            # 计算年龄范围
            start_age = qiyun_age + i * 10
            end_age = start_age + 9
            start_year = birth_year + start_age - 1
            end_year = birth_year + end_age - 1
            
            # 计算五行
            wuxing = GAN_WUXING[gan]
            
            # 计算十神
            ten_god = cls.calculate_shishen(day_master, gan)
            
            # 判断是否当前大运
            is_current = start_age <= current_age <= end_age
            
            # 获取解读
            description = cls.SHISHEN_DAYUN_DESC.get(ten_god, '运势平稳')
            
            dayun_list.append(DayunInfo(
                index=i + 1,
                ganzhi=ganzhi,
                gan=gan,
                zhi=zhi,
                start_age=start_age,
                end_age=end_age,
                start_year=start_year,
                end_year=end_year,
                wuxing=wuxing,
                ten_god=ten_god,
                is_current=is_current,
                description=description
            ))
        
        return dayun_list
    
    @classmethod
    def calculate_liunian(
        cls,
        day_master: str,
        birth_year: int,
        start_year: int,
        end_year: int
    ) -> List[LiunianInfo]:
        """
        计算流年序列
        
        Args:
            day_master: 日主
            birth_year: 出生年份
            start_year: 起始年份
            end_year: 结束年份
            
        Returns:
            流年列表
        """
        liunian_list = []
        
        for year in range(start_year, end_year + 1):
            # 计算年干支
            gan_idx = (year - 4) % 10
            zhi_idx = (year - 4) % 12
            
            gan = TIANGAN[gan_idx]
            zhi = DIZHI[zhi_idx]
            ganzhi = gan + zhi
            
            # 计算虚岁
            age = year - birth_year + 1
            
            # 计算十神
            ten_god = cls.calculate_shishen(day_master, gan)
            
            # 获取解读
            description = cls._get_liunian_description(ten_god, age)
            
            liunian_list.append(LiunianInfo(
                year=year,
                ganzhi=ganzhi,
                gan=gan,
                zhi=zhi,
                age=age,
                ten_god=ten_god,
                description=description
            ))
        
        return liunian_list
    
    @classmethod
    def _get_liunian_description(cls, ten_god: str, age: int) -> str:
        """获取流年解读"""
        base_desc = {
            '比肩': '朋友助力，竞争加剧',
            '劫财': '破财风险，谨慎理财',
            '食神': '口福财运，身心愉悦',
            '伤官': '才华显露，防口舌是非',
            '偏财': '意外收获，投资有利',
            '正财': '正财稳定，工作顺利',
            '七杀': '压力机遇，突破瓶颈',
            '正官': '升迁有望，贵人相助',
            '偏印': '学业进步，偏业有成',
            '正印': '长辈提携，学业顺利',
        }
        
        return base_desc.get(ten_god, '运势平稳')
    
    @classmethod
    def get_current_dayun(
        cls,
        dayun_list: List[DayunInfo],
        current_age: int
    ) -> Optional[DayunInfo]:
        """获取当前大运"""
        for dayun in dayun_list:
            if dayun.start_age <= current_age <= dayun.end_age:
                return dayun
        return None
    
    @classmethod
    def analyze_dayun_trend(
        cls,
        dayun_list: List[DayunInfo],
        day_master: str
    ) -> Dict[str, any]:
        """
        分析大运整体走势
        
        Returns:
            走势分析结果
        """
        # 统计十神分布
        shishen_count = {}
        for dayun in dayun_list:
            shishen_count[dayun.ten_god] = shishen_count.get(dayun.ten_god, 0) + 1
        
        # 找出主要运势
        main_shishen = max(shishen_count.items(), key=lambda x: x[1])[0] if shishen_count else None
        
        # 分析吉凶
        ji_shishen = ['食神', '正财', '正官', '正印']  # 吉神
        xiong_shishen = ['劫财', '伤官', '七杀']  # 凶神
        
        ji_count = sum(1 for d in dayun_list if d.ten_god in ji_shishen)
        xiong_count = sum(1 for d in dayun_list if d.ten_god in xiong_shishen)
        
        if ji_count > xiong_count:
            overall_trend = '整体运势向好，多有贵人相助'
        elif xiong_count > ji_count:
            overall_trend = '整体运势有波折，需谨慎应对'
        else:
            overall_trend = '整体运势平稳，稳中求进'
        
        return {
            'shishen_distribution': shishen_count,
            'main_shishen': main_shishen,
            'ji_count': ji_count,
            'xiong_count': xiong_count,
            'overall_trend': overall_trend
        }


# 便捷函数
def calculate_dayun(
    month_gan: str,
    month_zhi: str,
    day_master: str,
    birth_year: int,
    birth_date: date,
    birth_hour: int,
    gender: str,
    year_gan: str
) -> Dict[str, any]:
    """
    计算完整大运信息
    
    Returns:
        包含起运年龄、大运序列、流年信息的完整结果
    """
    # 计算起运年龄
    qiyun_age, direction = DayunCalculator.calculate_qiyun_age(
        birth_date, birth_hour, gender, year_gan
    )
    
    # 计算大运序列
    dayun_list = DayunCalculator.calculate_dayun_sequence(
        month_gan, month_zhi, day_master, birth_year, qiyun_age, direction
    )
    
    # 获取当前大运
    current_year = datetime.now().year
    current_age = current_year - birth_year + 1
    current_dayun = DayunCalculator.get_current_dayun(dayun_list, current_age)
    
    # 计算近10年流年
    liunian_list = DayunCalculator.calculate_liunian(
        day_master, birth_year, current_year, current_year + 9
    )
    
    # 分析大运走势
    trend_analysis = DayunCalculator.analyze_dayun_trend(dayun_list, day_master)
    
    return {
        'qiyun_age': qiyun_age,
        'direction': direction,
        'dayun_list': [d.__dict__ for d in dayun_list],
        'current_dayun': current_dayun.__dict__ if current_dayun else None,
        'liunian_list': [l.__dict__ for l in liunian_list],
        'trend_analysis': trend_analysis
    }


def get_liunian_info(day_master: str, birth_year: int, target_year: int) -> Dict:
    """获取指定年份的流年信息"""
    liunian_list = DayunCalculator.calculate_liunian(
        day_master, birth_year, target_year, target_year
    )
    return liunian_list[0].__dict__ if liunian_list else None


class EnhancedDayunAnalyzer:
    """增强版大运分析器 - 结合大运流年"""
    
    # 地支藏干
    ZHI_CANGGAN = {
        '子': ['癸'], '丑': ['己', '癸', '辛'], '寅': ['甲', '丙', '戊'],
        '卯': ['乙'], '辰': ['戊', '乙', '癸'], '巳': ['丙', '庚', '戊'],
        '午': ['丁', '己'], '未': ['己', '丁', '乙'], '申': ['庚', '壬', '戊'],
        '酉': ['辛'], '戌': ['戊', '辛', '丁'], '亥': ['壬', '甲']
    }
    
    # 地支相冲
    ZHI_CHONG = {
        '子': '午', '午': '子', '丑': '未', '未': '丑',
        '寅': '申', '申': '寅', '卯': '酉', '酉': '卯',
        '辰': '戌', '戌': '辰', '巳': '亥', '亥': '巳'
    }
    
    # 地支三合
    ZHI_SANHE = {
        '子': ('申', '辰', '水'), '丑': ('巳', '酉', '金'), 
        '寅': ('午', '戌', '火'), '卯': ('亥', '未', '木'),
        '辰': ('申', '子', '水'), '巳': ('丑', '酉', '金'),
        '午': ('寅', '戌', '火'), '未': ('亥', '卯', '木'),
        '申': ('子', '辰', '水'), '酉': ('丑', '巳', '金'),
        '戌': ('寅', '午', '火'), '亥': ('卯', '未', '木')
    }
    
    # 运势评分
    SHISHEN_SCORE = {
        '比肩': 60, '劫财': 40, '食神': 80, '伤官': 55,
        '偏财': 75, '正财': 80, '七杀': 50, '正官': 85,
        '偏印': 65, '正印': 85
    }
    
    @classmethod
    def analyze_combined_fortune(
        cls,
        dayun: DayunInfo,
        liunian: LiunianInfo,
        day_master: str,
        day_branch: str,
        yong_shen: List[str] = None
    ) -> Dict[str, any]:
        """
        分析大运流年组合运势
        
        Args:
            dayun: 大运信息
            liunian: 流年信息
            day_master: 日主
            day_branch: 日支
            yong_shen: 用神列表
        """
        result = {
            'overall_score': 0,
            'career': {'score': 0, 'description': ''},
            'wealth': {'score': 0, 'description': ''},
            'relationship': {'score': 0, 'description': ''},
            'health': {'score': 0, 'description': ''},
            'highlights': [],
            'warnings': [],
            'suggestions': []
        }
        
        # 基础分数
        dayun_score = cls.SHISHEN_SCORE.get(dayun.ten_god, 60)
        liunian_score = cls.SHISHEN_SCORE.get(liunian.ten_god, 60)
        base_score = (dayun_score + liunian_score) / 2
        
        # 用神加分
        if yong_shen:
            dayun_wuxing = GAN_WUXING.get(dayun.gan, '')
            liunian_wuxing = GAN_WUXING.get(liunian.gan, '')
            
            if dayun_wuxing in yong_shen:
                base_score += 10
                result['highlights'].append(f'大运{dayun.gan}({dayun_wuxing})为用神，运势加持')
            
            if liunian_wuxing in yong_shen:
                base_score += 5
                result['highlights'].append(f'流年{liunian.gan}({liunian_wuxing})为用神，有利')
        
        # 检查大运流年组合
        
        # 1. 天干组合分析
        gan_combo = cls._analyze_gan_combination(dayun.gan, liunian.gan, day_master)
        base_score += gan_combo['score_adj']
        if gan_combo['description']:
            if gan_combo['score_adj'] > 0:
                result['highlights'].append(gan_combo['description'])
            else:
                result['warnings'].append(gan_combo['description'])
        
        # 2. 地支组合分析
        zhi_combo = cls._analyze_zhi_combination(
            dayun.zhi, liunian.zhi, day_branch
        )
        base_score += zhi_combo['score_adj']
        if zhi_combo['description']:
            if zhi_combo['score_adj'] > 0:
                result['highlights'].append(zhi_combo['description'])
            else:
                result['warnings'].append(zhi_combo['description'])
        
        # 3. 十神组合分析
        shishen_combo = cls._analyze_shishen_combination(
            dayun.ten_god, liunian.ten_god
        )
        result['career']['score'] = shishen_combo['career']
        result['career']['description'] = shishen_combo['career_desc']
        result['wealth']['score'] = shishen_combo['wealth']
        result['wealth']['description'] = shishen_combo['wealth_desc']
        result['relationship']['score'] = shishen_combo['relationship']
        result['relationship']['description'] = shishen_combo['relationship_desc']
        result['health']['score'] = shishen_combo['health']
        result['health']['description'] = shishen_combo['health_desc']
        
        # 计算总分
        result['overall_score'] = min(100, max(0, round(base_score)))
        
        # 生成建议
        result['suggestions'] = cls._generate_fortune_suggestions(
            dayun.ten_god, liunian.ten_god, result['overall_score']
        )
        
        return result
    
    @classmethod
    def _analyze_gan_combination(
        cls, dayun_gan: str, liunian_gan: str, day_master: str
    ) -> Dict:
        """分析天干组合"""
        result = {'score_adj': 0, 'description': ''}
        
        # 天干五合
        gan_he = {
            ('甲', '己'): '土', ('乙', '庚'): '金', ('丙', '辛'): '水',
            ('丁', '壬'): '木', ('戊', '癸'): '火'
        }
        
        combo = (dayun_gan, liunian_gan)
        reverse_combo = (liunian_gan, dayun_gan)
        
        if combo in gan_he or reverse_combo in gan_he:
            element = gan_he.get(combo) or gan_he.get(reverse_combo)
            result['score_adj'] = 10
            result['description'] = f'大运{dayun_gan}与流年{liunian_gan}相合化{element}，运势和谐'
        
        # 天干相冲（甲庚、乙辛、丙壬、丁癸）
        gan_chong = [('甲', '庚'), ('乙', '辛'), ('丙', '壬'), ('丁', '癸')]
        if combo in gan_chong or reverse_combo in gan_chong:
            result['score_adj'] = -10
            result['description'] = f'大运{dayun_gan}与流年{liunian_gan}相冲，变动较大'
        
        return result
    
    @classmethod
    def _analyze_zhi_combination(
        cls, dayun_zhi: str, liunian_zhi: str, day_branch: str
    ) -> Dict:
        """分析地支组合"""
        result = {'score_adj': 0, 'description': ''}
        
        # 地支相冲
        if cls.ZHI_CHONG.get(dayun_zhi) == liunian_zhi:
            result['score_adj'] = -15
            result['description'] = f'大运{dayun_zhi}与流年{liunian_zhi}相冲，易有动荡'
        
        # 流年冲日支
        if cls.ZHI_CHONG.get(liunian_zhi) == day_branch:
            result['score_adj'] -= 10
            result['description'] = f'流年{liunian_zhi}冲日支{day_branch}，注意健康和感情'
        
        # 检查三合
        sanhe_info = cls.ZHI_SANHE.get(dayun_zhi)
        if sanhe_info and liunian_zhi in sanhe_info[:2]:
            result['score_adj'] = 8
            result['description'] = f'大运{dayun_zhi}与流年{liunian_zhi}形成{sanhe_info[2]}局半合，有助力'
        
        return result
    
    @classmethod
    def _analyze_shishen_combination(
        cls, dayun_shishen: str, liunian_shishen: str
    ) -> Dict:
        """分析十神组合"""
        result = {
            'career': 60, 'career_desc': '事业平稳',
            'wealth': 60, 'wealth_desc': '财运平稳',
            'relationship': 60, 'relationship_desc': '感情平稳',
            'health': 70, 'health_desc': '健康尚可'
        }
        
        # 事业评分
        career_good = ['正官', '正印', '偏印', '食神']
        if dayun_shishen in career_good or liunian_shishen in career_good:
            result['career'] = 80
            result['career_desc'] = '事业运上升，有贵人相助'
        if dayun_shishen == '正官' and liunian_shishen in ['正印', '正财']:
            result['career'] = 90
            result['career_desc'] = '事业大吉，升职有望'
        if dayun_shishen == '七杀' and liunian_shishen == '伤官':
            result['career'] = 50
            result['career_desc'] = '事业压力大，需谨慎处理人际关系'
        
        # 财运评分
        wealth_good = ['正财', '偏财', '食神']
        if dayun_shishen in wealth_good or liunian_shishen in wealth_good:
            result['wealth'] = 80
            result['wealth_desc'] = '财运亨通，收入增加'
        if dayun_shishen == '劫财' or liunian_shishen == '劫财':
            result['wealth'] = 50
            result['wealth_desc'] = '财运波动，防破财'
        if dayun_shishen == '偏财' and liunian_shishen == '食神':
            result['wealth'] = 90
            result['wealth_desc'] = '财运大旺，有意外收获'
        
        # 感情评分
        if dayun_shishen in ['正财', '正官'] or liunian_shishen in ['正财', '正官']:
            result['relationship'] = 75
            result['relationship_desc'] = '感情稳定，有桃花运'
        if dayun_shishen == '伤官' or liunian_shishen == '伤官':
            result['relationship'] = 55
            result['relationship_desc'] = '感情易有波折，需多沟通'
        
        # 健康评分
        if dayun_shishen == '七杀' and liunian_shishen == '七杀':
            result['health'] = 50
            result['health_desc'] = '注意身体健康，防意外'
        if dayun_shishen == '食神' or liunian_shishen == '正印':
            result['health'] = 85
            result['health_desc'] = '身体康健，精力充沛'
        
        return result
    
    @classmethod
    def _generate_fortune_suggestions(
        cls, dayun_shishen: str, liunian_shishen: str, score: int
    ) -> List[str]:
        """生成运势建议"""
        suggestions = []
        
        # 根据十神组合给建议
        if dayun_shishen in ['正官', '七杀'] or liunian_shishen in ['正官', '七杀']:
            suggestions.append('事业上可积极进取，把握升迁机会')
        
        if dayun_shishen in ['正财', '偏财'] or liunian_shishen in ['正财', '偏财']:
            suggestions.append('财运较好，可适当投资理财')
        
        if dayun_shishen == '劫财' or liunian_shishen == '劫财':
            suggestions.append('注意理财，避免大额投资和借贷')
        
        if dayun_shishen == '伤官' or liunian_shishen == '伤官':
            suggestions.append('说话谨慎，避免口舌是非')
        
        if dayun_shishen in ['正印', '偏印'] or liunian_shishen in ['正印', '偏印']:
            suggestions.append('适合学习进修，考取证书')
        
        if dayun_shishen == '食神' or liunian_shishen == '食神':
            suggestions.append('发挥才华，创意工作有利')
        
        # 根据总分给建议
        if score >= 80:
            suggestions.append('整体运势向好，可大胆开拓')
        elif score >= 60:
            suggestions.append('运势平稳，稳中求进为宜')
        else:
            suggestions.append('运势有波折，宜守不宜攻')
        
        return suggestions
    
    @classmethod
    def analyze_yearly_fortune(
        cls,
        dayun_list: List[DayunInfo],
        day_master: str,
        day_branch: str,
        birth_year: int,
        target_year: int,
        yong_shen: List[str] = None
    ) -> Dict:
        """
        分析指定年份的综合运势
        """
        # 获取当前大运
        current_age = target_year - birth_year + 1
        current_dayun = None
        for dayun in dayun_list:
            if dayun.start_age <= current_age <= dayun.end_age:
                current_dayun = dayun
                break
        
        if not current_dayun:
            return {'error': '无法确定当前大运'}
        
        # 获取流年信息
        liunian_list = DayunCalculator.calculate_liunian(
            day_master, birth_year, target_year, target_year
        )
        if not liunian_list:
            return {'error': '无法计算流年信息'}
        
        liunian = liunian_list[0]
        
        # 综合分析
        combined_analysis = cls.analyze_combined_fortune(
            current_dayun, liunian, day_master, day_branch, yong_shen
        )
        
        return {
            'year': target_year,
            'age': current_age,
            'dayun': current_dayun.__dict__,
            'liunian': liunian.__dict__,
            'analysis': combined_analysis
        }

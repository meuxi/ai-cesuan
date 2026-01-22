"""
紫微斗数四化计算器
计算本命四化、大限四化、流年四化

四化：化禄、化权、化科、化忌
"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass


@dataclass
class SihuaInfo:
    """四化信息"""
    lu: str       # 化禄
    quan: str     # 化权
    ke: str       # 化科
    ji: str       # 化忌


class SihuaCalculator:
    """四化计算器"""
    
    # 天干对应的四化星
    SIHUA_TABLE: Dict[str, SihuaInfo] = {
        '甲': SihuaInfo(lu='廉贞', quan='破军', ke='武曲', ji='太阳'),
        '乙': SihuaInfo(lu='天机', quan='天梁', ke='紫微', ji='太阴'),
        '丙': SihuaInfo(lu='天同', quan='天机', ke='文昌', ji='廉贞'),
        '丁': SihuaInfo(lu='太阴', quan='天同', ke='天机', ji='巨门'),
        '戊': SihuaInfo(lu='贪狼', quan='太阴', ke='右弼', ji='天机'),
        '己': SihuaInfo(lu='武曲', quan='贪狼', ke='天梁', ji='文曲'),
        '庚': SihuaInfo(lu='太阳', quan='武曲', ke='太阴', ji='天同'),
        '辛': SihuaInfo(lu='巨门', quan='太阳', ke='文曲', ji='文昌'),
        '壬': SihuaInfo(lu='天梁', quan='紫微', ke='左辅', ji='武曲'),
        '癸': SihuaInfo(lu='破军', quan='巨门', ke='太阴', ji='贪狼'),
    }
    
    # 十四主星列表
    MAIN_STARS = [
        '紫微', '天机', '太阳', '武曲', '天同', '廉贞', '天府',
        '太阴', '贪狼', '巨门', '天相', '天梁', '七杀', '破军'
    ]
    
    # 辅星列表
    MINOR_STARS = [
        '文昌', '文曲', '左辅', '右弼', '天魁', '天钺',
        '禄存', '天马', '擎羊', '陀罗', '火星', '铃星',
        '地空', '地劫'
    ]
    
    # 星曜名称变体映射（简繁体）
    STAR_NAME_VARIANTS = {
        '天機': '天机', '太陽': '太阳', '廉貞': '廉贞',
        '太陰': '太阴', '貪狼': '贪狼', '巨門': '巨门',
        '七殺': '七杀', '破軍': '破军', '左輔': '左辅',
        '天鉞': '天钺', '祿存': '禄存', '天馬': '天马',
        '陀羅': '陀罗', '鈴星': '铃星',
    }
    
    @classmethod
    def get_sihua(cls, tiangan: str) -> Optional[SihuaInfo]:
        """
        获取天干对应的四化星
        
        Args:
            tiangan: 天干
            
        Returns:
            四化信息
        """
        return cls.SIHUA_TABLE.get(tiangan)
    
    @classmethod
    def normalize_star_name(cls, name: str) -> str:
        """
        标准化星曜名称（繁体转简体）
        """
        return cls.STAR_NAME_VARIANTS.get(name, name)
    
    @classmethod
    def get_star_sihua_type(
        cls, 
        tiangan: str, 
        star_name: str
    ) -> Optional[str]:
        """
        获取某颗星的四化类型
        
        Args:
            tiangan: 天干
            star_name: 星曜名称
            
        Returns:
            四化类型（禄/权/科/忌）或 None
        """
        sihua = cls.get_sihua(tiangan)
        if not sihua:
            return None
        
        normalized_star = cls.normalize_star_name(star_name)
        
        if cls.normalize_star_name(sihua.lu) == normalized_star:
            return '禄'
        if cls.normalize_star_name(sihua.quan) == normalized_star:
            return '权'
        if cls.normalize_star_name(sihua.ke) == normalized_star:
            return '科'
        if cls.normalize_star_name(sihua.ji) == normalized_star:
            return '忌'
        
        return None
    
    @classmethod
    def get_complete_sihua(
        cls,
        natal_stem: str,
        decade_stem: Optional[str] = None,
        yearly_stem: Optional[str] = None
    ) -> Dict[str, Optional[SihuaInfo]]:
        """
        获取完整的四化信息（本命、大限、流年）
        
        Args:
            natal_stem: 本命天干（年干）
            decade_stem: 大限天干
            yearly_stem: 流年天干
            
        Returns:
            完整的四化信息字典
        """
        result = {
            'natal': cls.get_sihua(natal_stem),
            'decade': cls.get_sihua(decade_stem) if decade_stem else None,
            'yearly': cls.get_sihua(yearly_stem) if yearly_stem else None,
        }
        return result
    
    @classmethod
    def get_star_all_sihua(
        cls,
        star_name: str,
        natal_stem: str,
        decade_stem: Optional[str] = None,
        yearly_stem: Optional[str] = None
    ) -> List[str]:
        """
        获取某颗星在本命、大限、流年的所有四化
        
        Args:
            star_name: 星曜名称
            natal_stem: 本命天干
            decade_stem: 大限天干
            yearly_stem: 流年天干
            
        Returns:
            四化列表，如 ['本禄', '限忌']
        """
        sihua_list = []
        
        # 本命四化
        natal_type = cls.get_star_sihua_type(natal_stem, star_name)
        if natal_type:
            sihua_list.append(f'本{natal_type}')
        
        # 大限四化
        if decade_stem:
            decade_type = cls.get_star_sihua_type(decade_stem, star_name)
            if decade_type:
                sihua_list.append(f'限{decade_type}')
        
        # 流年四化
        if yearly_stem:
            yearly_type = cls.get_star_sihua_type(yearly_stem, star_name)
            if yearly_type:
                sihua_list.append(f'年{yearly_type}')
        
        return sihua_list
    
    @classmethod
    def analyze_sihua_combinations(
        cls,
        natal_stem: str,
        decade_stem: Optional[str] = None,
        yearly_stem: Optional[str] = None
    ) -> Dict[str, List[str]]:
        """
        分析四化组合（双禄、禄忌同宫等）
        
        Returns:
            组合分析结果
        """
        combinations = {
            'double_lu': [],      # 双禄
            'double_ji': [],      # 双忌
            'lu_ji_clash': [],    # 禄忌冲
            'quan_ke_meet': [],   # 权科会
        }
        
        all_sihua = cls.get_complete_sihua(natal_stem, decade_stem, yearly_stem)
        
        # 收集所有禄星
        lu_stars = []
        ji_stars = []
        quan_stars = []
        ke_stars = []
        
        for level, info in all_sihua.items():
            if info:
                lu_stars.append((level, info.lu))
                ji_stars.append((level, info.ji))
                quan_stars.append((level, info.quan))
                ke_stars.append((level, info.ke))
        
        # 检查双禄
        lu_names = [s[1] for s in lu_stars]
        for star in set(lu_names):
            if lu_names.count(star) >= 2:
                combinations['double_lu'].append(star)
        
        # 检查双忌
        ji_names = [s[1] for s in ji_stars]
        for star in set(ji_names):
            if ji_names.count(star) >= 2:
                combinations['double_ji'].append(star)
        
        # 检查禄忌同宫（同一颗星既化禄又化忌）
        for lu_star in lu_names:
            if lu_star in ji_names:
                combinations['lu_ji_clash'].append(lu_star)
        
        return combinations
    
    @classmethod
    def get_sihua_description(cls, sihua_type: str) -> str:
        """
        获取四化的解释
        """
        descriptions = {
            '禄': '化禄主财禄、顺利、增益，是最吉利的四化。代表该星曜能量增强，带来好运和财富。',
            '权': '化权主权力、能力、掌控，是功名利禄的象征。代表该星曜展现主导力量。',
            '科': '化科主名声、学业、贵人，是文名声誉的象征。代表该星曜带来好名声和贵人缘。',
            '忌': '化忌主阻碍、损失、纠缠，是最需注意的四化。代表该星曜能量受阻，需要谨慎应对。',
        }
        return descriptions.get(sihua_type, '未知四化类型')


class DayunCalculator:
    """大运（大限）计算器"""
    
    # 五行局数
    WUXING_JU = {
        '水二局': 2,
        '木三局': 3,
        '金四局': 4,
        '土五局': 5,
        '火六局': 6,
    }
    
    @classmethod
    def calculate_dayun_start_age(
        cls,
        wuxing_ju: str,
        gender: str,
        year_stem: str
    ) -> int:
        """
        计算大运起始年龄
        
        Args:
            wuxing_ju: 五行局（如"水二局"）
            gender: 性别（男/女）
            year_stem: 年干
            
        Returns:
            大运起始年龄
        """
        ju_num = cls.WUXING_JU.get(wuxing_ju, 5)
        
        # 阳年生男、阴年生女顺行
        # 阴年生男、阳年生女逆行
        yang_stems = ['甲', '丙', '戊', '庚', '壬']
        is_yang = year_stem in yang_stems
        is_male = gender in ['男', 'male', 'M']
        
        # 顺逆判断
        is_clockwise = (is_yang and is_male) or (not is_yang and not is_male)
        
        # 起运年龄 = 局数
        start_age = ju_num
        
        return start_age
    
    @classmethod
    def calculate_dayun_sequence(
        cls,
        ming_gong_index: int,
        wuxing_ju: str,
        gender: str,
        year_stem: str,
        max_age: int = 100
    ) -> List[Dict]:
        """
        计算大运序列
        
        Args:
            ming_gong_index: 命宫地支索引（0-11）
            wuxing_ju: 五行局
            gender: 性别
            year_stem: 年干
            max_age: 最大年龄
            
        Returns:
            大运列表
        """
        dizhi = ['子', '丑', '寅', '卯', '辰', '巳', 
                 '午', '未', '申', '酉', '戌', '亥']
        tiangan = ['甲', '乙', '丙', '丁', '戊', 
                   '己', '庚', '辛', '壬', '癸']
        
        start_age = cls.calculate_dayun_start_age(wuxing_ju, gender, year_stem)
        
        # 判断顺逆
        yang_stems = ['甲', '丙', '戊', '庚', '壬']
        is_yang = year_stem in yang_stems
        is_male = gender in ['男', 'male', 'M']
        is_clockwise = (is_yang and is_male) or (not is_yang and not is_male)
        
        dayun_list = []
        current_age = start_age
        gong_index = ming_gong_index
        
        # 计算起始天干（根据命宫地支和年干推算）
        # 简化处理：使用宫干
        
        decade_count = 0
        while current_age <= max_age:
            end_age = current_age + 9
            
            # 大限宫位
            dayun_gong = dizhi[gong_index]
            
            # 大限天干（根据五虎遁推算）
            # 简化：使用地支对应的天干
            stem_index = (gong_index + tiangan.index(year_stem) * 2) % 10
            dayun_stem = tiangan[stem_index]
            
            dayun_list.append({
                'index': decade_count,
                'start_age': current_age,
                'end_age': end_age,
                'gong_zhi': dayun_gong,
                'gong_gan': dayun_stem,
                'ganzhi': dayun_stem + dayun_gong,
                'is_current': False,  # 需要外部设置
            })
            
            # 移动到下一个宫位
            if is_clockwise:
                gong_index = (gong_index + 1) % 12
            else:
                gong_index = (gong_index - 1) % 12
            
            current_age = end_age + 1
            decade_count += 1
        
        return dayun_list
    
    @classmethod
    def get_current_dayun(
        cls,
        dayun_list: List[Dict],
        current_age: int
    ) -> Optional[Dict]:
        """
        获取当前大运
        """
        for dayun in dayun_list:
            if dayun['start_age'] <= current_age <= dayun['end_age']:
                return dayun
        return None


class LiunianCalculator:
    """流年计算器"""
    
    TIANGAN = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']
    DIZHI = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']
    
    @classmethod
    def get_year_ganzhi(cls, year: int) -> Tuple[str, str]:
        """
        获取年干支
        
        Args:
            year: 公历年份
            
        Returns:
            (年干, 年支)
        """
        gan_index = (year - 4) % 10
        zhi_index = (year - 4) % 12
        return cls.TIANGAN[gan_index], cls.DIZHI[zhi_index]
    
    @classmethod
    def calculate_liunian(
        cls,
        birth_year: int,
        target_year: int
    ) -> Dict:
        """
        计算流年信息
        
        Args:
            birth_year: 出生年份
            target_year: 目标年份
            
        Returns:
            流年信息
        """
        year_gan, year_zhi = cls.get_year_ganzhi(target_year)
        age = target_year - birth_year + 1  # 虚岁
        
        # 流年四化
        sihua = SihuaCalculator.get_sihua(year_gan)
        
        return {
            'year': target_year,
            'ganzhi': year_gan + year_zhi,
            'gan': year_gan,
            'zhi': year_zhi,
            'age': age,
            'sihua': {
                'lu': sihua.lu if sihua else None,
                'quan': sihua.quan if sihua else None,
                'ke': sihua.ke if sihua else None,
                'ji': sihua.ji if sihua else None,
            }
        }
    
    @classmethod
    def calculate_liunian_range(
        cls,
        birth_year: int,
        start_year: int,
        end_year: int
    ) -> List[Dict]:
        """
        计算流年范围
        """
        return [
            cls.calculate_liunian(birth_year, year)
            for year in range(start_year, end_year + 1)
        ]


# 便捷函数
def get_sihua(tiangan: str) -> Optional[SihuaInfo]:
    """获取四化"""
    return SihuaCalculator.get_sihua(tiangan)


def calculate_dayun(
    ming_gong_index: int,
    wuxing_ju: str,
    gender: str,
    year_stem: str
) -> List[Dict]:
    """计算大运"""
    return DayunCalculator.calculate_dayun_sequence(
        ming_gong_index, wuxing_ju, gender, year_stem
    )


def calculate_liunian(birth_year: int, target_year: int) -> Dict:
    """计算流年"""
    return LiunianCalculator.calculate_liunian(birth_year, target_year)

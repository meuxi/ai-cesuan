"""
紫微斗数配置模块
支持全书派、中州派等不同派别的四化配置
参考 py-iztro 的 ConfigModel 实现
"""

from enum import Enum
from typing import Dict, List, Optional
from pydantic import BaseModel, Field


class YearDivideType(str, Enum):
    """年分割点类型"""
    NORMAL = "normal"      # 正月初一分界
    EXACT = "exact"        # 立春分界


class AgeDivideType(str, Enum):
    """小限分割点类型"""
    NORMAL = "normal"      # 只考虑年份，不考虑生日
    BIRTHDAY = "birthday"  # 以生日为分界点


class AlgorithmType(str, Enum):
    """紫微派别"""
    DEFAULT = "default"        # 以《紫微斗数全书》为基础安星
    ZHONGZHOU = "zhongzhou"    # 以中州派安星法为基础安星


# 全书派四化表（默认）
MUTAGEN_TABLE_DEFAULT: Dict[str, List[str]] = {
    '甲': ['廉贞', '破军', '武曲', '太阳'],
    '乙': ['天机', '天梁', '紫微', '太阴'],
    '丙': ['天同', '天机', '文昌', '廉贞'],
    '丁': ['太阴', '天同', '天机', '巨门'],
    '戊': ['贪狼', '太阴', '右弼', '天机'],
    '己': ['武曲', '贪狼', '天梁', '文曲'],
    '庚': ['太阳', '武曲', '太阴', '天同'],
    '辛': ['巨门', '太阳', '文曲', '文昌'],
    '壬': ['天梁', '紫微', '左辅', '武曲'],
    '癸': ['破军', '巨门', '太阴', '贪狼'],
}

# 中州派四化表（部分差异）
MUTAGEN_TABLE_ZHONGZHOU: Dict[str, List[str]] = {
    '甲': ['廉贞', '破军', '武曲', '太阳'],
    '乙': ['天机', '天梁', '紫微', '太阴'],
    '丙': ['天同', '天机', '文昌', '廉贞'],
    '丁': ['太阴', '天同', '天机', '巨门'],
    '戊': ['贪狼', '太阴', '右弼', '天机'],
    '己': ['武曲', '贪狼', '天梁', '文曲'],
    '庚': ['太阳', '武曲', '天同', '天相'],  # 中州派差异：天同化忌，天相替代太阴化科
    '辛': ['巨门', '太阳', '文曲', '文昌'],
    '壬': ['天梁', '紫微', '左辅', '武曲'],
    '癸': ['破军', '巨门', '太阴', '贪狼'],
}

# 星曜亮度表（完整12宫亮度配置）
# 格式：{星名: [子, 丑, 寅, 卯, 辰, 巳, 午, 未, 申, 酉, 戌, 亥]}
BRIGHTNESS_TABLE_DEFAULT: Dict[str, List[str]] = {
    '紫微': ['旺', '得', '得', '得', '旺', '得', '旺', '得', '得', '得', '旺', '得'],
    '天机': ['庙', '陷', '得', '旺', '得', '得', '陷', '得', '旺', '庙', '得', '得'],
    '太阳': ['陷', '陷', '旺', '庙', '庙', '庙', '旺', '得', '得', '陷', '陷', '陷'],
    '武曲': ['旺', '得', '庙', '利', '平', '庙', '旺', '得', '庙', '利', '平', '庙'],
    '天同': ['得', '平', '陷', '庙', '不', '不', '得', '庙', '陷', '得', '不', '不'],
    '廉贞': ['平', '旺', '庙', '平', '陷', '旺', '庙', '旺', '庙', '平', '陷', '旺'],
    '天府': ['庙', '得', '庙', '得', '旺', '得', '庙', '得', '庙', '得', '旺', '得'],
    '太阴': ['旺', '庙', '庙', '得', '得', '陷', '陷', '陷', '陷', '得', '庙', '旺'],
    '贪狼': ['旺', '旺', '庙', '旺', '旺', '平', '旺', '旺', '庙', '旺', '旺', '平'],
    '巨门': ['旺', '庙', '得', '陷', '得', '庙', '旺', '庙', '得', '陷', '得', '庙'],
    '天相': ['庙', '旺', '陷', '庙', '得', '平', '庙', '旺', '陷', '庙', '得', '平'],
    '天梁': ['旺', '得', '庙', '庙', '陷', '得', '旺', '得', '旺', '旺', '陷', '得'],
    '七杀': ['庙', '旺', '庙', '旺', '平', '旺', '庙', '旺', '庙', '旺', '平', '旺'],
    '破军': ['旺', '平', '得', '旺', '旺', '平', '旺', '平', '得', '旺', '旺', '平'],
    '左辅': ['庙', '庙', '庙', '庙', '庙', '庙', '庙', '庙', '庙', '庙', '庙', '庙'],
    '右弼': ['庙', '庙', '庙', '庙', '庙', '庙', '庙', '庙', '庙', '庙', '庙', '庙'],
    '文昌': ['陷', '利', '庙', '平', '平', '利', '庙', '利', '庙', '平', '平', '利'],
    '文曲': ['陷', '利', '平', '庙', '利', '平', '陷', '利', '平', '庙', '利', '平'],
    '天魁': ['庙', '庙', '庙', '庙', '庙', '庙', '庙', '庙', '庙', '庙', '庙', '庙'],
    '天钺': ['庙', '庙', '庙', '庙', '庙', '庙', '庙', '庙', '庙', '庙', '庙', '庙'],
    '禄存': ['庙', '庙', '庙', '庙', '庙', '庙', '庙', '庙', '庙', '庙', '庙', '庙'],
    '天马': ['旺', '得', '旺', '得', '旺', '得', '旺', '得', '旺', '得', '旺', '得'],
    '擎羊': ['陷', '得', '庙', '陷', '得', '庙', '陷', '得', '庙', '陷', '得', '庙'],
    '陀罗': ['庙', '陷', '得', '庙', '陷', '得', '庙', '陷', '得', '庙', '陷', '得'],
    '火星': ['庙', '陷', '庙', '陷', '陷', '庙', '庙', '陷', '庙', '陷', '陷', '庙'],
    '铃星': ['陷', '庙', '陷', '庙', '庙', '陷', '陷', '庙', '陷', '庙', '庙', '陷'],
    '地空': ['', '', '', '', '', '', '', '', '', '', '', ''],
    '地劫': ['', '', '', '', '', '', '', '', '', '', '', ''],
}


class ZiweiConfig(BaseModel):
    """紫微斗数配置"""
    
    # 四化表配置
    mutagens: Optional[Dict[str, List[str]]] = Field(
        default=None,
        description="四化表配置，格式：{天干: [化禄星, 化权星, 化科星, 化忌星]}"
    )
    
    # 星曜亮度配置
    brightness: Optional[Dict[str, List[str]]] = Field(
        default=None,
        description="星曜亮度配置，格式：{星名: [子宫亮度, 丑宫亮度, ...]}"
    )
    
    # 年分割点
    year_divide: YearDivideType = Field(
        default=YearDivideType.NORMAL,
        description="年分割点：normal=正月初一分界, exact=立春分界"
    )
    
    # 小限分割点
    age_divide: AgeDivideType = Field(
        default=AgeDivideType.NORMAL,
        description="小限分割点：normal=只考虑年份, birthday=以生日为分界点"
    )
    
    # 运限分割点
    horoscope_divide: YearDivideType = Field(
        default=YearDivideType.NORMAL,
        description="运限分割点：normal=正月初一分界, exact=立春分界"
    )
    
    # 安星派别
    algorithm: AlgorithmType = Field(
        default=AlgorithmType.DEFAULT,
        description="紫微派别：default=全书派, zhongzhou=中州派"
    )
    
    def get_mutagen_table(self) -> Dict[str, List[str]]:
        """获取当前四化表"""
        if self.mutagens:
            # 合并自定义配置和默认配置
            base_table = MUTAGEN_TABLE_ZHONGZHOU.copy() if self.algorithm == AlgorithmType.ZHONGZHOU else MUTAGEN_TABLE_DEFAULT.copy()
            base_table.update(self.mutagens)
            return base_table
        
        if self.algorithm == AlgorithmType.ZHONGZHOU:
            return MUTAGEN_TABLE_ZHONGZHOU
        return MUTAGEN_TABLE_DEFAULT
    
    def get_brightness_table(self) -> Dict[str, List[str]]:
        """获取当前亮度表"""
        if self.brightness:
            base_table = BRIGHTNESS_TABLE_DEFAULT.copy()
            base_table.update(self.brightness)
            return base_table
        return BRIGHTNESS_TABLE_DEFAULT
    
    def get_mutagen_by_stem(self, stem: str) -> Dict[str, str]:
        """根据天干获取四化"""
        table = self.get_mutagen_table()
        stars = table.get(stem, ['', '', '', ''])
        return {
            'lu': stars[0] if len(stars) > 0 else '',
            'quan': stars[1] if len(stars) > 1 else '',
            'ke': stars[2] if len(stars) > 2 else '',
            'ji': stars[3] if len(stars) > 3 else '',
        }


# 全局默认配置
_global_config = ZiweiConfig()


def get_config() -> ZiweiConfig:
    """获取当前全局配置"""
    return _global_config


def set_config(config: ZiweiConfig) -> None:
    """设置全局配置"""
    global _global_config
    _global_config = config


def reset_config() -> None:
    """重置为默认配置"""
    global _global_config
    _global_config = ZiweiConfig()

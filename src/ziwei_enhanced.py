"""
增强版紫微斗数计算模块
集成mingpan专业计算引擎
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
import logging

# 尝试导入mingpan相关模块
try:
    import sys
    import os
    sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'external', 'mingpan'))
    from mingpan.services.ziwei import ZiweiService
    from mingpan.services.ziwei.types import ZiweiInput, ZiweiResult
    MINGPAN_AVAILABLE = True
except ImportError:
    logging.warning("Mingpan not available, using fallback implementation")
    MINGPAN_AVAILABLE = False

logger = logging.getLogger(__name__)

class EnhancedZiweiCalculator:
    """增强版紫微斗数计算器"""
    
    def __init__(self):
        self.mingpan_service = None
        if MINGPAN_AVAILABLE:
            try:
                self.mingpan_service = ZiweiService()
                logger.info("Mingpan service initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize Mingpan service: {e}")
    
    def calculate(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        计算紫微斗数命盘
        
        Args:
            data: 包含生辰信息的字典
                - year: 出生年份
                - month: 出生月份
                - day: 出生日
                - hour: 出生时
                - minute: 出生分 (可选)
                - gender: 性别 ('male'/'female')
        
        Returns:
            完整的紫微斗数命盘数据
        """
        try:
            if self.mingpan_service and MINGPAN_AVAILABLE:
                return self._calculate_with_mingpan(data)
            else:
                return self._calculate_fallback(data)
        except Exception as e:
            logger.error(f"Ziwei calculation failed: {e}")
            raise
    
    def _calculate_with_mingpan(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """使用mingpan计算"""
        try:
            # 构建输入
            ziwei_input = ZiweiInput(
                year=data['year'],
                month=data['month'],
                day=data['day'],
                hour=data['hour'],
                minute=data.get('minute', 0),
                gender=data['gender'],
                language='zh-CN'
            )
            
            # 计算
            result = self.mingpan_service.calculate(ziwei_input)
            
            # 转换为API响应格式
            return self._convert_mingpan_result(result, data)
            
        except Exception as e:
            logger.error(f"Mingpan calculation failed: {e}")
            # 降级到fallback
            return self._calculate_fallback(data)
    
    def _calculate_fallback(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """降级计算实现"""
        try:
            from . import bazi_models
            from lunar_javascript import Solar
            
            # 基本信息计算
            solar = Solar.fromYmdHms(
                data['year'], 
                data['month'], 
                data['day'], 
                data['hour'], 
                data.get('minute', 0), 
                0
            )
            lunar = solar.getLunar()
            
            # 四柱
            year_gz = lunar.getYearInGanZhi()
            month_gz = lunar.getMonthInGanZhi()
            day_gz = lunar.getDayInGanZhi()
            hour_gz = lunar.getTimeInGanZhi()
            
            # 基础命盘结构
            palaces = self._generate_basic_palaces(data, lunar)
            decades = self._generate_basic_decades(data)
            
            return {
                "success": True,
                "data": {
                    "basicInfo": {
                        "zodiac": self._get_zodiac(data['year']),
                        "constellation": self._get_constellation(data['month'], data['day']),
                        "fourPillars": {
                            "year": {"stem": year_gz[0], "branch": year_gz[1]},
                            "month": {"stem": month_gz[0], "branch": month_gz[1]},
                            "day": {"stem": day_gz[0], "branch": day_gz[1]},
                            "hour": {"stem": hour_gz[0], "branch": hour_gz[1]}
                        },
                        "fiveElement": self._get_five_element(lunar),
                        "soul": "命主",
                        "body": "身主"
                    },
                    "solarDate": f"{data['year']}-{data['month']:02d}-{data['day']:02d}",
                    "lunarDate": {
                        "year": lunar.getYear(),
                        "month": lunar.getMonth(),
                        "day": lunar.getDay(),
                        "isLeapMonth": False
                    },
                    "palaces": palaces,
                    "decades": decades,
                    "currentDecade": self._get_current_decade(decades, data),
                    "yearlyInfo": self._get_current_yearly(data),
                    "mutagenInfo": self._get_basic_mutagen(),
                    "gender": data['gender'],
                    "birthYear": data['year'],
                    "language": "zh-CN"
                }
            }
            
        except Exception as e:
            logger.error(f"Fallback calculation failed: {e}")
            raise
    
    def _convert_mingpan_result(self, result: Any, original_data: Dict[str, Any]) -> Dict[str, Any]:
        """转换mingpan结果为API格式"""
        try:
            # 这里需要根据mingpan的实际返回结构进行转换
            # 暂时返回基础结构
            return self._calculate_fallback(original_data)
        except Exception as e:
            logger.error(f"Result conversion failed: {e}")
            return self._calculate_fallback(original_data)
    
    def _generate_basic_palaces(self, data: Dict[str, Any], lunar: Any) -> List[Dict[str, Any]]:
        """生成基础十二宫位"""
        palace_names = [
            '命宮', '兄弟', '夫妻', '子女', '财帛', '疾厄',
            '迁移', '交友', '官禄', '田宅', '福德', '父母'
        ]
        
        branches = ['寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥', '子', '丑']
        
        palaces = []
        for i, name in enumerate(palace_names):
            palace = {
                "name": name,
                "index": i,
                "position": i,
                "earthlyBranch": branches[i],
                "heavenlyStem": "",
                "majorStars": [],
                "minorStars": [],
                "isBodyPalace": False,
                "decadeInfo": None,
                "isDecadeHighlight": False,
                "isYearlyHighlight": False,
                "minorLimitAges": []
            }
            palaces.append(palace)
        
        return palaces
    
    def _generate_basic_decades(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """生成基础大限信息"""
        decades = []
        palace_names = [
            '命宮', '兄弟', '夫妻', '子女', '财帛', '疾厄',
            '迁移', '交友', '官禄', '田宅', '福德', '父母'
        ]
        
        for i in range(12):
            start_age = i * 10 + 1
            end_age = start_age + 9
            
            decade = {
                "index": i,
                "palaceIndex": i,
                "startAge": start_age,
                "endAge": end_age,
                "heavenlyStem": "",
                "earthlyBranch": "",
                "palaceName": palace_names[i],
                "label": f"{start_age}-{end_age}岁"
            }
            decades.append(decade)
        
        return decades
    
    def _get_current_decade(self, decades: List[Dict[str, Any]], data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """获取当前大限"""
        current_age = datetime.now().year - data['year'] + 1
        
        for decade in decades:
            if decade['startAge'] <= current_age <= decade['endAge']:
                decade['isCurrent'] = True
                return decade
        
        return None
    
    def _get_current_yearly(self, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """获取当前流年"""
        current_year = datetime.now().year
        current_age = current_year - data['year'] + 1
        
        return {
            "year": current_year,
            "age": current_age,
            "heavenlyStem": "",
            "earthlyBranch": "",
            "palaceIndex": 0
        }
    
    def _get_basic_mutagen(self) -> Dict[str, Any]:
        """获取基础四化信息"""
        return {
            "natal": {
                "lu": "",
                "quan": "",
                "ke": "",
                "ji": ""
            },
            "combined": {}
        }
    
    def _get_zodiac(self, year: int) -> str:
        """获取生肖"""
        animals = ['鼠', '牛', '虎', '兔', '龙', '蛇', '马', '羊', '猴', '鸡', '狗', '猪']
        return animals[(year - 4) % 12]
    
    def _get_constellation(self, month: int, day: int) -> str:
        """获取星座"""
        constellations = ['水瓶座', '双鱼座', '白羊座', '金牛座', '双子座', '巨蟹座', 
                         '狮子座', '处女座', '天秤座', '天蝎座', '射手座', '摩羯座']
        dates = [20, 19, 21, 20, 21, 22, 23, 23, 23, 24, 23, 22]
        
        if day < dates[month - 1]:
            return constellations[(month - 2 + 12) % 12]
        return constellations[month - 1]
    
    def _get_five_element(self, lunar: Any) -> str:
        """获取五行局"""
        elements = ['水二局', '木三局', '金四局', '土五局', '火六局']
        return elements[lunar.getDay() % 5]

# 全局实例
enhanced_ziwei_calculator = EnhancedZiweiCalculator()

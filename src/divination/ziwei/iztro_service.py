"""
紫微斗数计算服务 - 使用iztro-py纯Python库
核心算法在后端执行，前端只负责展示
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
import logging
import re

from iztro_py import by_solar
from iztro_py.i18n import t, set_language
from lunar_python import Solar
from .adjective_stars import apply_adjective_stars_to_palaces

logger = logging.getLogger(__name__)

# 初始化时设置中文语言
try:
    set_language('zh-CN')
    logger.info("iztro-py语言已设置为中文(zh-CN)")
except Exception as e:
    logger.warning(f"设置iztro-py语言失败: {e}")

# 中文翻译映射表 - 确保所有输出都是中文
CHINESE_TRANSLATIONS = {
    # 宫位名称 - 英文key到中文
    "lifePalace": "命宫", "siblingsPalace": "兄弟宫", "spousePalace": "夫妻宫",
    "childrenPalace": "子女宫", "wealthPalace": "财帛宫", "healthPalace": "疾厄宫",
    "surfacePalace": "迁移宫", "friendsPalace": "仆役宫", "careerPalace": "官禄宫",
    "propertyPalace": "田宅宫", "spiritPalace": "福德宫", "parentsPalace": "父母宫",
    # 宫位名称 - 简体中文直接映射
    "命宫": "命宫", "兄弟宫": "兄弟宫", "夫妻宫": "夫妻宫", "子女宫": "子女宫",
    "财帛宫": "财帛宫", "疾厄宫": "疾厄宫", "迁移宫": "迁移宫", "仆役宫": "仆役宫",
    "官禄宫": "官禄宫", "田宅宫": "田宅宫", "福德宫": "福德宫", "父母宫": "父母宫",
    # 繁体中文宫位名称映射到简体
    "命宮": "命宫", "兄弟": "兄弟宫", "夫妻": "夫妻宫", "子女": "子女宫",
    "财帛": "财帛宫", "疾厄": "疾厄宫", "迁移": "迁移宫", "交友": "仆役宫",
    "官禄": "官禄宫", "田宅": "田宅宫", "福德": "福德宫", "父母": "父母宫",
    
    # 主星
    "ziweiStar": "紫微", "tianjiStar": "天机", "taiyangStar": "太阳",
    "wuquStar": "武曲", "tiantongStar": "天同", "lianzhenStar": "廉贞",
    "tianfuStar": "天府", "taiyinStar": "太阴", "tanlangStar": "贪狼",
    "jumenStar": "巨门", "tianxiangStar": "天相", "tianlangStar": "天梁",
    "qishaStar": "七杀", "pojunStar": "破军",
    "紫微": "紫微", "天机": "天机", "太阳": "太阳", "武曲": "武曲",
    "天同": "天同", "廉贞": "廉贞", "天府": "天府", "太阴": "太阴",
    "贪狼": "贪狼", "巨门": "巨门", "天相": "天相", "天梁": "天梁",
    "七杀": "七杀", "破军": "破军",
    
    # 辅星
    "zuofuStar": "左辅", "youbiStar": "右弼", "wenchangStar": "文昌",
    "wenquStar": "文曲", "lucunStar": "禄存", "tianmaStar": "天马",
    "qingyangStar": "擎羊", "tuoluoStar": "陀罗", "huoxingStar": "火星",
    "lingxingStar": "铃星", "dikongStar": "地空", "dijieStar": "地劫",
    "tiankuiStar": "天魁", "tianyueStar": "天钺", "huagaiStar": "华盖",
    "tianguanStar": "天官", "tianfuStar2": "天福", "tianxingStar": "天刑",
    "tianyaoStar": "天姚", "tiankuStar": "天哭", "tianxuStar": "天虚",
    "左辅": "左辅", "右弼": "右弼", "文昌": "文昌", "文曲": "文曲",
    "禄存": "禄存", "天马": "天马", "擎羊": "擎羊", "陀罗": "陀罗",
    "火星": "火星", "铃星": "铃星", "地空": "地空", "地劫": "地劫",
    "天魁": "天魁", "天钺": "天钺", "华盖": "华盖", "天官": "天官",
    "天福": "天福", "天刑": "天刑", "天姚": "天姚", "天哭": "天哭", "天虚": "天虚",
    
    # 亮度
    "temple": "庙", "prosperous": "旺", "gain": "得", "benefit": "利",
    "average": "平", "notBenefit": "不", "fallen": "陷",
    "庙": "庙", "旺": "旺", "得": "得", "利": "利", "平": "平", "不": "不", "陷": "陷",
    
    # 地支 (各种格式)
    "zi": "子", "chou": "丑", "yin": "寅", "mao": "卯", "chen": "辰", "si": "巳",
    "wu": "午", "wei": "未", "shen": "申", "you": "酉", "xu": "戌", "hai": "亥",
    "子": "子", "丑": "丑", "寅": "寅", "卯": "卯", "辰": "辰", "巳": "巳",
    "午": "午", "未": "未", "申": "申", "酉": "酉", "戌": "戌", "亥": "亥",
    # 地支带Earthly后缀格式
    "ziEarthly": "子", "chouEarthly": "丑", "yinEarthly": "寅", "maoEarthly": "卯", "chenEarthly": "辰", "siEarthly": "巳",
    "wuEarthly": "午", "weiEarthly": "未", "shenEarthly": "申", "youEarthly": "酉", "xuEarthly": "戌", "haiEarthly": "亥",
    # 地支带Branch后缀格式
    "ziBranch": "子", "chouBranch": "丑", "yinBranch": "寅", "maoBranch": "卯", "chenBranch": "辰", "siBranch": "巳",
    "wuBranch": "午", "weiBranch": "未", "shenBranch": "申", "youBranch": "酉", "xuBranch": "戌", "haiBranch": "亥",
    
    # 天干 (各种格式)
    "jia": "甲", "yi": "乙", "bing": "丙", "ding": "丁", "wu2": "戊",
    "ji": "己", "geng": "庚", "xin": "辛", "ren": "壬", "gui": "癸",
    "甲": "甲", "乙": "乙", "丙": "丙", "丁": "丁", "戊": "戊",
    "己": "己", "庚": "庚", "辛": "辛", "壬": "壬", "癸": "癸",
    # 天干带Heavenly后缀格式
    "jiaHeavenly": "甲", "yiHeavenly": "乙", "bingHeavenly": "丙", "dingHeavenly": "丁", "wuHeavenly": "戊",
    "jiHeavenly": "己", "gengHeavenly": "庚", "xinHeavenly": "辛", "renHeavenly": "壬", "guiHeavenly": "癸",
    # 天干带Stem后缀格式
    "jiaStem": "甲", "yiStem": "乙", "bingStem": "丙", "dingStem": "丁", "wuStem": "戊",
    "jiStem": "己", "gengStem": "庚", "xinStem": "辛", "renStem": "壬", "guiStem": "癸",
    
    # 四化
    "lu": "禄", "quan": "权", "ke": "科", "ji2": "忌",
    "禄": "禄", "权": "权", "科": "科", "忌": "忌",
    
    # 命主身主
    "soul": "命主", "body": "身主",
    
    # 五行局
    "waterTwo": "水二局", "woodThree": "木三局", "goldFour": "金四局",
    "earthFive": "土五局", "fireSix": "火六局",
    "水二局": "水二局", "木三局": "木三局", "金四局": "金四局",
    "土五局": "土五局", "火六局": "火六局",
    
    # 生肖
    "rat": "鼠", "ox": "牛", "tiger": "虎", "rabbit": "兔",
    "dragon": "龙", "snake": "蛇", "horse": "马", "goat": "羊",
    "monkey": "猴", "rooster": "鸡", "dog": "狗", "pig": "猪",
    "鼠": "鼠", "牛": "牛", "虎": "虎", "兔": "兔",
    "龙": "龙", "蛇": "蛇", "马": "马", "羊": "羊",
    "猴": "猴", "鸡": "鸡", "狗": "狗", "猪": "猪",
    
    # 星座
    "aries": "白羊座", "taurus": "金牛座", "gemini": "双子座", "cancer": "巨蟹座",
    "leo": "狮子座", "virgo": "处女座", "libra": "天秤座", "scorpio": "天蝎座",
    "sagittarius": "射手座", "capricorn": "摩羯座", "aquarius": "水瓶座", "pisces": "双鱼座",
    "白羊座": "白羊座", "金牛座": "金牛座", "双子座": "双子座", "巨蟹座": "巨蟹座",
    "狮子座": "狮子座", "处女座": "处女座", "天秤座": "天秤座", "天蝎座": "天蝎座",
    "射手座": "射手座", "摩羯座": "摩羯座", "水瓶座": "水瓶座", "双鱼座": "双鱼座",
    
    # 更多星曜 (iztro-py可能返回的英文名)
    "ziwei": "紫微", "tianji": "天机", "taiyang": "太阳", "wuqu": "武曲",
    "tiantong": "天同", "lianzhen": "廉贞", "tianfu": "天府", "taiyin": "太阴",
    "tanlang": "贪狼", "jumen": "巨门", "tianxiang": "天相", "tianliang": "天梁",
    "qisha": "七杀", "pojun": "破军",
    "zuofu": "左辅", "youbi": "右弼", "wenchang": "文昌", "wenqu": "文曲",
    "lucun": "禄存", "tianma": "天马", "qingyang": "擎羊", "tuoluo": "陀罗",
    "huoxing": "火星", "lingxing": "铃星", "dikong": "地空", "dijie": "地劫",
    "tiankui": "天魁", "tianyue": "天钺",
    
    # 命主身主英文名
    "greedy wolf": "贪狼", "giant gate": "巨门", "lucun": "禄存", "wenqu": "文曲",
    "lianzhen": "廉贞", "wuqu": "武曲", "pojun": "破军",
    "火星": "火星", "天相": "天相", "天梁": "天梁", "天同": "天同", "文昌": "文昌",
    
    # 长生12神
    "changsheng": "长生", "muyu": "沐浴", "guandai": "冠带", "linguan": "临官",
    "diwang": "帝旺", "shuai": "衰", "bing": "病", "si": "死",
    "mu": "墓", "jue": "绝", "tai": "胎", "yang": "养",
    "长生": "长生", "沐浴": "沐浴", "冠带": "冠带", "临官": "临官",
    "帝旺": "帝旺", "衰": "衰", "病": "病", "死": "死",
    "墓": "墓", "绝": "绝", "胎": "胎", "养": "养",
    
    # 博士12神
    "boshi": "博士", "lishi": "力士", "qinglong": "青龙", "xiaohao": "小耗",
    "jiangjun": "将军", "zhoushu": "奏书", "faylian": "飞廉", "xishen": "喜神",
    "bingfu": "病符", "dahao": "大耗", "fubing": "伏兵", "guanfu": "官府",
    "博士": "博士", "力士": "力士", "青龙": "青龙", "小耗": "小耗",
    "将军": "将军", "奏书": "奏书", "飞廉": "飞廉", "喜神": "喜神",
    "病符": "病符", "大耗": "大耗", "伏兵": "伏兵", "官府": "官府",
    
    # 将前12神
    "jiangxing": "将星", "panao": "攀鞍", "suiyi": "岁驿", "xifu": "息神",
    "huagai": "华盖", "jiesha": "劫煞", "zaifu": "灾煞", "tianha": "天煞",
    "zhifu": "指背", "xianchi": "咸池", "yuejian": "月煞", "wangshen": "亡神",
    
    # 岁前12神  
    "suijian": "岁建", "huiqi": "晦气", "sangshen": "丧门", "guansuo": "贯索",
    "guanfu2": "官符", "xiaohao2": "小耗", "dahao2": "大耗", "longde": "龙德",
    "baihufei": "白虎", "tiande": "天德", "diaoke": "吊客", "bingfu2": "病符",
}


def translate_name(key: str, category: str = '') -> str:
    """翻译英文key为中文"""
    if not key:
        return key
    
    # 如果已经是中文，直接返回
    if len(key) == 1 and '\u4e00' <= key <= '\u9fff':
        return key
    
    # 先检查本地翻译表
    if key in CHINESE_TRANSLATIONS:
        return CHINESE_TRANSLATIONS[key]
    
    # 处理带后缀的key (如 xxxStar, xxxPalace, xxxHeavenly, xxxEarthly)
    suffixes = ['Star', 'Palace', 'Heavenly', 'Earthly', 'Stem', 'Branch']
    clean_key = key
    for suffix in suffixes:
        clean_key = clean_key.replace(suffix, '')
    
    if clean_key in CHINESE_TRANSLATIONS:
        return CHINESE_TRANSLATIONS[clean_key]
    
    # 处理驼峰命名的复合key（如 jiHeavenly -> ji -> 己）
    # 提取首部小写部分
    match = re.match(r'^([a-z]+)', key)
    if match:
        prefix = match.group(1)
        if prefix in CHINESE_TRANSLATIONS:
            return CHINESE_TRANSLATIONS[prefix]
    
    # 尝试 iztro 翻译
    paths = [
        f"palaces.{key}",
        f"stars.major.{key}",
        f"stars.minor.{key}",
        f"earthlyBranch.{key}",
        f"heavenlyStem.{key}",
        f"brightness.{key}",
        key
    ]
    for path in paths:
        try:
            result = t(path)
            if result != path and result != key:
                return result
        except:
            pass
    
    # 最后尝试记录未翻译的key以便调试
    logger.debug(f"未翻译的key: {key}")
    return key


class IztroService:
    """紫微斗数计算服务"""
    
    def calculate(
        self,
        year: int,
        month: int,
        day: int,
        hour: int,
        minute: int = 0,
        gender: str = "male",
        language: str = "zh-CN"
    ) -> Dict[str, Any]:
        """
        计算紫微斗数命盘
        
        Args:
            year: 出生年份
            month: 出生月份
            day: 出生日
            hour: 出生时
            minute: 出生分
            gender: 性别 ('male'/'female')
            language: 语言 ('zh-CN'/'zh-TW'/'en-US'/'ko-KR'/'ja-JP')
        
        Returns:
            完整的紫微斗数命盘数据
        """
        try:
            # 构建日期字符串
            date_str = f"{year}-{month}-{day}"
            
            # 计算时辰索引 (0-12)
            time_index = self._hour_to_time_index(hour)
            
            # 性别转换为中文
            gender_cn = "男" if gender == "male" else "女"
            
            # 使用iztro-py计算命盘
            astrolabe = by_solar(
                solar_date=date_str,
                time_index=time_index,
                gender=gender_cn,
                fix_leap=True,
                language=language
            )
            
            if not astrolabe:
                raise ValueError("创建命盘失败")
            
            # 转换为API响应格式
            return self._convert_to_response(astrolabe, year, month, day, hour, minute, gender, language)
            
        except Exception as e:
            logger.error(f"紫微斗数计算失败: {e}")
            raise
    
    def _hour_to_time_index(self, hour: int) -> int:
        """
        将小时转换为时辰索引（0-12）
        0: 早子时 (00:00-01:00)
        1: 丑时 (01:00-03:00)
        2: 寅时 (03:00-05:00)
        ...
        12: 晚子时 (23:00-24:00)
        """
        if hour >= 23:
            return 12  # 晚子时
        if hour >= 0 and hour < 1:
            return 0  # 早子时
        return (hour + 1) // 2
    
    def _convert_to_response(
        self,
        astrolabe: Any,
        year: int,
        month: int,
        day: int,
        hour: int,
        minute: int,
        gender: str,
        language: str
    ) -> Dict[str, Any]:
        """转换命盘数据为API响应格式"""
        
        # 提取基本信息
        basic_info = self._extract_basic_info(astrolabe, year, month, day, hour)
        
        # 获取农历月份用于杂曜计算
        lunar_date_info = self._get_lunar_date(astrolabe)
        lunar_month = lunar_date_info.get('month', month) if isinstance(lunar_date_info, dict) else month
        
        # 提取宫位信息
        palaces = self._extract_palaces(astrolabe)
        
        # 应用杂曜和12神（补充iztro-py缺失的功能）
        year_stem = basic_info.get('fourPillars', {}).get('year', {}).get('stem', '')
        year_branch = basic_info.get('fourPillars', {}).get('year', {}).get('branch', '')
        five_element = basic_info.get('fiveElement', '')
        if year_stem and year_branch:
            palaces = apply_adjective_stars_to_palaces(
                palaces, year_stem, year_branch, abs(lunar_month), five_element
            )
        
        # 计算大限信息
        decades = self._calculate_decades(astrolabe, year, gender)
        
        # 当前大限
        current_decade = self._get_current_decade(decades, year)
        
        # 流年信息
        yearly_info = self._calculate_yearly(year)
        
        # 四化信息
        mutagen_info = self._extract_mutagen(astrolabe)
        
        # 农历日期
        lunar_date = self._get_lunar_date(astrolabe)
        
        return {
            "success": True,
            "basicInfo": basic_info,
            "solarDate": f"{year}-{month:02d}-{day:02d}",
            "lunarDate": lunar_date,
            "palaces": palaces,
            "decades": decades,
            "currentDecade": current_decade,
            "yearlyInfo": yearly_info,
            "mutagenInfo": mutagen_info,
            "gender": gender,
            "birthYear": year,
            "language": language
        }
    
    def _extract_basic_info(self, astrolabe: Any, year: int, month: int, day: int, hour: int) -> Dict[str, Any]:
        """提取基本信息"""
        try:
            # 使用lunar_python计算正确的四柱（iztro-py日柱算法有bug）
            four_pillars = self._calculate_four_pillars(year, month, day, hour)
            
            # 翻译可能是英文的字段
            zodiac = str(getattr(astrolabe, 'zodiac', self._get_zodiac(year)))
            sign = str(getattr(astrolabe, 'sign', self._get_constellation(month, day)))
            five_elem = str(getattr(astrolabe, 'five_elements_class', '水二局'))
            soul = str(getattr(astrolabe, 'soul', '命主'))
            body = str(getattr(astrolabe, 'body', '身主'))
            
            return {
                "zodiac": translate_name(zodiac),
                "constellation": translate_name(sign),
                "fourPillars": four_pillars,
                "fiveElement": translate_name(five_elem),
                "soul": translate_name(soul),
                "body": translate_name(body)
            }
        except Exception as e:
            logger.warning(f"提取基本信息失败: {e}")
            return {
                "zodiac": self._get_zodiac(year),
                "constellation": self._get_constellation(month, day),
                "fourPillars": {
                    "year": {"stem": "", "branch": ""},
                    "month": {"stem": "", "branch": ""},
                    "day": {"stem": "", "branch": ""},
                    "hour": {"stem": "", "branch": ""}
                },
                "fiveElement": "水二局",
                "soul": "命主",
                "body": "身主"
            }
    
    def _calculate_four_pillars(self, year: int, month: int, day: int, hour: int) -> Dict[str, Any]:
        """使用lunar_python计算正确的四柱（iztro-py的日柱算法有bug）"""
        four_pillars = {
            "year": {"stem": "", "branch": ""},
            "month": {"stem": "", "branch": ""},
            "day": {"stem": "", "branch": ""},
            "hour": {"stem": "", "branch": ""}
        }
        
        try:
            solar = Solar.fromYmdHms(year, month, day, hour, 0, 0)
            lunar = solar.getLunar()
            bazi = lunar.getEightChar()
            
            # 年柱
            year_gz = bazi.getYear()
            four_pillars["year"] = {"stem": year_gz[0], "branch": year_gz[1]}
            
            # 月柱
            month_gz = bazi.getMonth()
            four_pillars["month"] = {"stem": month_gz[0], "branch": month_gz[1]}
            
            # 日柱
            day_gz = bazi.getDay()
            four_pillars["day"] = {"stem": day_gz[0], "branch": day_gz[1]}
            
            # 时柱
            hour_gz = bazi.getTime()
            four_pillars["hour"] = {"stem": hour_gz[0], "branch": hour_gz[1]}
            
        except Exception as e:
            logger.error(f"lunar_python计算四柱失败: {e}")
        
        return four_pillars
    
    def _parse_chinese_date(self, chinese_date: str) -> Dict[str, Any]:
        """解析四柱字符串 (如: '庚辰年甲申月乙卯日 壬午时')"""
        four_pillars = {
            "year": {"stem": "", "branch": ""},
            "month": {"stem": "", "branch": ""},
            "day": {"stem": "", "branch": ""},
            "hour": {"stem": "", "branch": ""}
        }
        try:
            if not chinese_date:
                return four_pillars
            # 去除空格
            parts = chinese_date.replace(' ', '')
            # 解析年月日时
            if '年' in parts:
                idx = parts.index('年')
                if idx >= 2:
                    four_pillars["year"] = {"stem": parts[idx-2], "branch": parts[idx-1]}
            if '月' in parts:
                idx = parts.index('月')
                if idx >= 2:
                    four_pillars["month"] = {"stem": parts[idx-2], "branch": parts[idx-1]}
            if '日' in parts:
                idx = parts.index('日')
                if idx >= 2:
                    four_pillars["day"] = {"stem": parts[idx-2], "branch": parts[idx-1]}
            if '时' in parts:
                idx = parts.index('时')
                if idx >= 2:
                    four_pillars["hour"] = {"stem": parts[idx-2], "branch": parts[idx-1]}
        except Exception as e:
            logger.warning(f"解析四柱失败: {e}")
        return four_pillars
    
    def _extract_palaces(self, astrolabe: Any) -> List[Dict[str, Any]]:
        """提取宫位信息"""
        palaces = []
        
        try:
            if hasattr(astrolabe, 'palaces') and astrolabe.palaces:
                for i, palace in enumerate(astrolabe.palaces):
                    # 提取主星（翻译名称）
                    major_stars = []
                    if hasattr(palace, 'major_stars'):
                        for star in palace.major_stars:
                            star_name = str(getattr(star, 'name', star))
                            brightness = str(getattr(star, 'brightness', ''))
                            major_stars.append({
                                "name": translate_name(star_name),
                                "type": "major",
                                "brightness": translate_name(brightness),
                                "mutagen": [str(getattr(star, 'mutagen', ''))] if hasattr(star, 'mutagen') and star.mutagen else None
                            })
                    
                    # 提取辅星（翻译名称）
                    minor_stars = []
                    if hasattr(palace, 'minor_stars'):
                        for star in palace.minor_stars:
                            star_name = str(getattr(star, 'name', star))
                            minor_stars.append({
                                "name": translate_name(star_name),
                                "type": "minor",
                                "brightness": "",
                                "mutagen": None
                            })
                    
                    # 提取杂曜
                    if hasattr(palace, 'adjective_stars'):
                        for star in palace.adjective_stars:
                            star_name = str(getattr(star, 'name', star))
                            minor_stars.append({
                                "name": translate_name(star_name),
                                "type": "auxiliary",
                                "brightness": "",
                                "mutagen": None
                            })
                    
                    # 翻译宫位名和地支
                    palace_name = str(getattr(palace, 'name', f'宫位{i}'))
                    earthly_branch = str(getattr(palace, 'earthly_branch', ''))
                    
                    # 翻译天干
                    heavenly_stem = str(getattr(palace, 'heavenly_stem', ''))
                    
                    # 提取12神数据
                    extras = {}
                    if hasattr(palace, 'changsheng12') and palace.changsheng12:
                        extras['changsheng12'] = translate_name(str(palace.changsheng12))
                    if hasattr(palace, 'boshi12') and palace.boshi12:
                        extras['boshi12'] = translate_name(str(palace.boshi12))
                    if hasattr(palace, 'jiangqian12') and palace.jiangqian12:
                        extras['jiangqian12'] = translate_name(str(palace.jiangqian12))
                    if hasattr(palace, 'suiqian12') and palace.suiqian12:
                        extras['suiqian12'] = translate_name(str(palace.suiqian12))
                    if hasattr(palace, 'ages') and palace.ages:
                        extras['ages'] = list(palace.ages) if hasattr(palace.ages, '__iter__') else []
                    
                    # 提取大限信息
                    decade_info = None
                    if hasattr(palace, 'decadal') and palace.decadal:
                        decadal = palace.decadal
                        decade_info = {
                            "startAge": decadal.range[0] if hasattr(decadal, 'range') and decadal.range else 0,
                            "endAge": decadal.range[1] if hasattr(decadal, 'range') and len(decadal.range) > 1 else 0,
                            "heavenlyStem": translate_name(str(getattr(decadal, 'heavenly_stem', ''))),
                            "earthlyBranch": translate_name(str(getattr(decadal, 'earthly_branch', '')))
                        }
                    
                    palaces.append({
                        "name": translate_name(palace_name),
                        "index": i,
                        "position": i,
                        "earthlyBranch": translate_name(earthly_branch),
                        "heavenlyStem": translate_name(heavenly_stem),
                        "majorStars": major_stars,
                        "minorStars": minor_stars,
                        "isBodyPalace": bool(getattr(palace, 'is_body_palace', False)),
                        "decadeInfo": decade_info,
                        "extras": extras
                    })
            else:
                # 返回基础宫位结构
                palace_names = ['命宮', '兄弟', '夫妻', '子女', '财帛', '疾厄',
                               '迁移', '交友', '官禄', '田宅', '福德', '父母']
                branches = ['寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥', '子', '丑']
                
                for i, name in enumerate(palace_names):
                    palaces.append({
                        "name": name,
                        "index": i,
                        "position": i,
                        "earthlyBranch": branches[i],
                        "heavenlyStem": "",
                        "majorStars": [],
                        "minorStars": [],
                        "isBodyPalace": False,
                        "decadeInfo": None,
                        "extras": {}
                    })
                    
        except Exception as e:
            logger.error(f"提取宫位信息失败: {e}")
        
        return palaces
    
    def _calculate_decades(self, astrolabe: Any, birth_year: int, gender: str) -> List[Dict[str, Any]]:
        """计算大限信息"""
        decades = []
        palace_names = ['命宮', '兄弟', '夫妻', '子女', '财帛', '疾厄',
                       '迁移', '交友', '官禄', '田宅', '福德', '父母']
        
        try:
            # 尝试从astrolabe获取大限信息
            if hasattr(astrolabe, 'decades') and astrolabe.decades:
                for i, decade in enumerate(astrolabe.decades):
                    # 翻译天干地支
                    hs = translate_name(str(getattr(decade, 'heavenly_stem', '')))
                    eb = translate_name(str(getattr(decade, 'earthly_branch', '')))
                    pn = translate_name(str(getattr(decade, 'palace_name', palace_names[i % 12])))
                    decades.append({
                        "index": i,
                        "palaceIndex": i,
                        "startAge": getattr(decade, 'start_age', i * 10 + 1),
                        "endAge": getattr(decade, 'end_age', i * 10 + 10),
                        "heavenlyStem": hs,
                        "earthlyBranch": eb,
                        "palaceName": pn,
                        "label": f"{getattr(decade, 'start_age', i * 10 + 1)}-{getattr(decade, 'end_age', i * 10 + 10)}岁"
                    })
            else:
                # 生成基础大限
                for i in range(12):
                    start_age = i * 10 + 1
                    end_age = start_age + 9
                    decades.append({
                        "index": i,
                        "palaceIndex": i,
                        "startAge": start_age,
                        "endAge": end_age,
                        "heavenlyStem": "",
                        "earthlyBranch": "",
                        "palaceName": palace_names[i],
                        "label": f"{start_age}-{end_age}岁"
                    })
        except Exception as e:
            logger.warning(f"计算大限失败: {e}")
            # 返回基础大限
            for i in range(12):
                start_age = i * 10 + 1
                end_age = start_age + 9
                decades.append({
                    "index": i,
                    "palaceIndex": i,
                    "startAge": start_age,
                    "endAge": end_age,
                    "heavenlyStem": "",
                    "earthlyBranch": "",
                    "palaceName": palace_names[i],
                    "label": f"{start_age}-{end_age}岁"
                })
        
        return decades
    
    def _get_current_decade(self, decades: List[Dict[str, Any]], birth_year: int) -> Optional[Dict[str, Any]]:
        """获取当前大限"""
        current_age = datetime.now().year - birth_year + 1
        
        for decade in decades:
            if decade['startAge'] <= current_age <= decade['endAge']:
                decade['isCurrent'] = True
                return decade
        
        return None
    
    def _calculate_yearly(self, birth_year: int) -> Dict[str, Any]:
        """计算流年信息"""
        current_year = datetime.now().year
        current_age = current_year - birth_year + 1
        
        stems = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']
        branches = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']
        
        return {
            "year": current_year,
            "age": current_age,
            "heavenlyStem": stems[(current_year - 4) % 10],
            "earthlyBranch": branches[(current_year - 4) % 12],
            "palaceIndex": 0
        }
    
    def _extract_mutagen(self, astrolabe: Any) -> Dict[str, Any]:
        """提取四化信息"""
        try:
            if hasattr(astrolabe, 'mutagen') and astrolabe.mutagen:
                return {
                    "natal": {
                        "lu": str(getattr(astrolabe.mutagen, 'lu', '')),
                        "quan": str(getattr(astrolabe.mutagen, 'quan', '')),
                        "ke": str(getattr(astrolabe.mutagen, 'ke', '')),
                        "ji": str(getattr(astrolabe.mutagen, 'ji', ''))
                    },
                    "combined": {}
                }
        except Exception as e:
            logger.warning(f"提取四化信息失败: {e}")
        
        return {
            "natal": {"lu": "", "quan": "", "ke": "", "ji": ""},
            "combined": {}
        }
    
    def _get_lunar_date(self, astrolabe: Any) -> Dict[str, Any]:
        """获取农历日期"""
        try:
            # iztro-py使用raw_lunar_date属性
            if hasattr(astrolabe, 'raw_lunar_date') and astrolabe.raw_lunar_date:
                lunar = astrolabe.raw_lunar_date
                return {
                    "year": getattr(lunar, 'year', 0),
                    "month": getattr(lunar, 'month', 0),
                    "day": getattr(lunar, 'day', 0),
                    "isLeapMonth": getattr(lunar, 'is_leap_month', False)
                }
        except Exception as e:
            logger.warning(f"获取农历日期失败: {e}")
        
        return {"year": 0, "month": 0, "day": 0, "isLeapMonth": False}
    
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


# 全局单例
iztro_service = IztroService()

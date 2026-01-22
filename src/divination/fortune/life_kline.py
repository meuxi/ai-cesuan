"""
人生K线模块 - 将八字运势以股票K线图形式可视化
移植自 lifekline 项目
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum


class Gender(Enum):
    MALE = "male"
    FEMALE = "female"


@dataclass
class KLinePoint:
    """K线数据点"""
    age: int              # 年龄（虚岁）
    year: int             # 年份
    gan_zhi: str          # 流年干支
    da_yun: str           # 当前大运
    open: int             # 开盘（运势起点）
    close: int            # 收盘（运势终点）
    high: int             # 最高点
    low: int              # 最低点
    score: int            # 综合评分
    reason: str           # 流年详批


@dataclass
class LifeAnalysis:
    """命理分析结果"""
    bazi: List[str]       # 四柱 [年柱, 月柱, 日柱, 时柱]
    summary: str          # 总评
    summary_score: int    # 总评分数 0-10
    industry: str         # 事业分析
    industry_score: int
    wealth: str           # 财运分析
    wealth_score: int
    marriage: str         # 婚姻分析
    marriage_score: int
    health: str           # 健康分析
    health_score: int
    family: str           # 六亲分析
    family_score: int


@dataclass
class LifeDestinyResult:
    """完整的人生K线结果"""
    chart_data: List[KLinePoint]
    analysis: LifeAnalysis


# 六十甲子顺序
SIXTY_JIAZI = [
    "甲子", "乙丑", "丙寅", "丁卯", "戊辰", "己巳", "庚午", "辛未", "壬申", "癸酉",
    "甲戌", "乙亥", "丙子", "丁丑", "戊寅", "己卯", "庚辰", "辛巳", "壬午", "癸未",
    "甲申", "乙酉", "丙戌", "丁亥", "戊子", "己丑", "庚寅", "辛卯", "壬辰", "癸巳",
    "甲午", "乙未", "丙申", "丁酉", "戊戌", "己亥", "庚子", "辛丑", "壬寅", "癸卯",
    "甲辰", "乙巳", "丙午", "丁未", "戊申", "己酉", "庚戌", "辛亥", "壬子", "癸丑",
    "甲寅", "乙卯", "丙辰", "丁巳", "戊午", "己未", "庚申", "辛酉", "壬戌", "癸亥"
]

# 阳干
YANG_STEMS = ['甲', '丙', '戊', '庚', '壬']
# 阴干
YIN_STEMS = ['乙', '丁', '己', '辛', '癸']


def get_stem_polarity(pillar: str) -> str:
    """获取天干阴阳属性"""
    if not pillar:
        return "YANG"
    first_char = pillar[0]
    if first_char in YANG_STEMS:
        return "YANG"
    if first_char in YIN_STEMS:
        return "YIN"
    return "YANG"


def get_dayun_direction(gender: Gender, year_pillar: str) -> bool:
    """
    计算大运排序方向
    返回: True=顺行, False=逆行
    """
    polarity = get_stem_polarity(year_pillar)
    if gender == Gender.MALE:
        return polarity == "YANG"  # 男命阳年顺行
    else:
        return polarity == "YIN"   # 女命阴年顺行


def get_next_jiazi(current: str, forward: bool = True) -> str:
    """获取下一个干支（顺行或逆行）"""
    try:
        idx = SIXTY_JIAZI.index(current)
        if forward:
            return SIXTY_JIAZI[(idx + 1) % 60]
        else:
            return SIXTY_JIAZI[(idx - 1) % 60]
    except ValueError:
        return current


def generate_dayun_sequence(first_dayun: str, direction_forward: bool, count: int = 10) -> List[str]:
    """生成大运序列"""
    sequence = [first_dayun]
    current = first_dayun
    for _ in range(count - 1):
        current = get_next_jiazi(current, direction_forward)
        sequence.append(current)
    return sequence


def get_year_ganzhi(year: int) -> str:
    """根据年份获取流年干支"""
    # 1984年为甲子年
    base_year = 1984
    offset = (year - base_year) % 60
    return SIXTY_JIAZI[offset]


# AI系统指令模板
LIFE_KLINE_SYSTEM_INSTRUCTION = """
你是一位世界顶级的八字命理大师。你的任务是根据用户提供的四柱干支和指定的大运信息，生成一份"人生K线图"数据和带评分的命理报告。

**核心规则 (Core Rules):**
1. **年龄计算**: 严格采用**虚岁**，数据点必须**从 1 岁开始** (age: 1)。
2. **K线详批**: 每一年的 `reason` 必须是该流年的**详细批断**（100字左右），包含具体发生的吉凶事件预测、神煞分析、应对建议。
3. **评分机制**: 所有分析维度（总评、事业、财富等）需给出 0-10 分。

**大运排盘规则 (重要):**
请根据 Prompt 中指定的【大运排序方向 (顺行/逆行)】推导大运序列。

**大运推导逻辑:**
1. **顺行**: 按照六十甲子顺序**往后**推导 (如: 甲子 -> 乙丑 -> 丙寅...)。
2. **逆行**: 按照六十甲子顺序**往前**逆推 (如: 甲子 -> 癸亥 -> 壬戌...)。
3. **起点**: 必须以用户输入的【第一步大运】为起点。
4. **频率**: 每一步大运管**十年**。

**关键字段说明:**
- `daYun`: **大运干支** (10年不变)。在同一个大运周期的10年内，该字段必须完全相同。
- `ganZhi`: **流年干支** (每年一变)。

**输出 JSON 结构要求:**

{
  "bazi": ["年柱", "月柱", "日柱", "时柱"],
  "summary": "命理总评摘要。",
  "summaryScore": 8,
  "industry": "事业分析内容...",
  "industryScore": 7,
  "wealth": "财富分析内容...",
  "wealthScore": 9,
  "marriage": "婚姻分析内容...",
  "marriageScore": 6,
  "health": "健康分析内容...",
  "healthScore": 5,
  "family": "六亲分析内容...",
  "familyScore": 7,
  "chartPoints": [
    {
      "age": 1, 
      "year": 1990,
      "daYun": "童限", 
      "ganZhi": "庚午", 
      "open": 50,
      "close": 55,
      "high": 60,
      "low": 45,
      "score": 55,
      "reason": "详细的流年详批..."
    },
    ... (1-100岁)
  ]
}

**K线图逻辑:**
- K线数值 (0-100) 应结合大运和流年的综合作用。大运定基调，流年定应期。
- 颜色逻辑：Close > Open 为吉（红），Close < Open 为凶（绿）。
"""


def build_user_prompt(
    name: Optional[str],
    gender: Gender,
    birth_year: int,
    year_pillar: str,
    month_pillar: str,
    day_pillar: str,
    hour_pillar: str,
    start_age: int,
    first_dayun: str
) -> str:
    """构建用户提示词"""
    gender_str = "男 (乾造)" if gender == Gender.MALE else "女 (坤造)"
    year_polarity = get_stem_polarity(year_pillar)
    polarity_cn = "阳" if year_polarity == "YANG" else "阴"
    
    is_forward = get_dayun_direction(gender, year_pillar)
    direction_str = "顺行 (Forward)" if is_forward else "逆行 (Backward)"
    
    direction_example = (
        "例如：第一步是【戊申】，第二步则是【己酉】（顺排）" if is_forward
        else "例如：第一步是【戊申】，第二步则是【丁未】（逆排）"
    )
    
    return f"""
请根据以下**已经排好的**八字四柱和**指定的大运信息**进行分析。

【基本信息】
性别：{gender_str}
姓名：{name or "未提供"}
出生年份：{birth_year}年 (阳历)

【八字四柱】
年柱：{year_pillar} (天干属性：{polarity_cn})
月柱：{month_pillar}
日柱：{day_pillar}
时柱：{hour_pillar}

【大运核心参数】
1. 起运年龄：{start_age} 岁 (虚岁)。
2. 第一步大运：{first_dayun}。
3. **排序方向**：{direction_str}。

【必须执行的算法 - 大运序列生成】
请严格按照以下步骤生成数据：

1. **锁定第一步**：确认【{first_dayun}】为第一步大运。
2. **计算序列**：根据六十甲子顺序和方向（{direction_str}），推算出接下来的 9 步大运。
   {direction_example}
3. **填充 JSON**：
   - Age 1 到 {start_age - 1}: daYun = "童限"
   - Age {start_age} 到 {start_age + 9}: daYun = [第1步大运: {first_dayun}]
   - Age {start_age + 10} 到 {start_age + 19}: daYun = [第2步大运]
   - Age {start_age + 20} 到 {start_age + 29}: daYun = [第3步大运]
   - ...以此类推直到 100 岁。

【特别警告】
- **daYun 字段**：必须填大运干支（10年一变），**绝对不要**填流年干支。
- **ganZhi 字段**：填入该年份的**流年干支**（每年一变，例如 2024=甲辰，2025=乙巳）。

任务：
1. 确认格局与喜忌。
2. 生成 **1-100 岁 (虚岁)** 的人生流年K线数据。
3. 在 `reason` 字段中提供流年详批。
4. 生成带评分的命理分析报告。

请严格按照系统指令生成 JSON 数据。
"""


def parse_ai_response(response_data: Dict[str, Any]) -> LifeDestinyResult:
    """解析AI返回的数据"""
    chart_points = []
    for point in response_data.get("chartPoints", []):
        chart_points.append(KLinePoint(
            age=point.get("age", 0),
            year=point.get("year", 0),
            gan_zhi=point.get("ganZhi", ""),
            da_yun=point.get("daYun", ""),
            open=point.get("open", 50),
            close=point.get("close", 50),
            high=point.get("high", 50),
            low=point.get("low", 50),
            score=point.get("score", 50),
            reason=point.get("reason", "")
        ))
    
    analysis = LifeAnalysis(
        bazi=response_data.get("bazi", []),
        summary=response_data.get("summary", "无摘要"),
        summary_score=response_data.get("summaryScore", 5),
        industry=response_data.get("industry", "无"),
        industry_score=response_data.get("industryScore", 5),
        wealth=response_data.get("wealth", "无"),
        wealth_score=response_data.get("wealthScore", 5),
        marriage=response_data.get("marriage", "无"),
        marriage_score=response_data.get("marriageScore", 5),
        health=response_data.get("health", "无"),
        health_score=response_data.get("healthScore", 5),
        family=response_data.get("family", "无"),
        family_score=response_data.get("familyScore", 5)
    )
    
    return LifeDestinyResult(chart_data=chart_points, analysis=analysis)


def kline_point_to_dict(point: KLinePoint) -> Dict[str, Any]:
    """将KLinePoint转换为字典"""
    return {
        "age": point.age,
        "year": point.year,
        "ganZhi": point.gan_zhi,
        "daYun": point.da_yun,
        "open": point.open,
        "close": point.close,
        "high": point.high,
        "low": point.low,
        "score": point.score,
        "reason": point.reason
    }


def life_analysis_to_dict(analysis: LifeAnalysis) -> Dict[str, Any]:
    """将LifeAnalysis转换为字典"""
    return {
        "bazi": analysis.bazi,
        "summary": analysis.summary,
        "summaryScore": analysis.summary_score,
        "industry": analysis.industry,
        "industryScore": analysis.industry_score,
        "wealth": analysis.wealth,
        "wealthScore": analysis.wealth_score,
        "marriage": analysis.marriage,
        "marriageScore": analysis.marriage_score,
        "health": analysis.health,
        "healthScore": analysis.health_score,
        "family": analysis.family,
        "familyScore": analysis.family_score
    }


def life_destiny_result_to_dict(result: LifeDestinyResult) -> Dict[str, Any]:
    """将LifeDestinyResult转换为字典"""
    return {
        "chartData": [kline_point_to_dict(p) for p in result.chart_data],
        "analysis": life_analysis_to_dict(result.analysis)
    }


# 导出
__all__ = [
    'Gender',
    'KLinePoint',
    'LifeAnalysis',
    'LifeDestinyResult',
    'SIXTY_JIAZI',
    'get_stem_polarity',
    'get_dayun_direction',
    'get_next_jiazi',
    'generate_dayun_sequence',
    'get_year_ganzhi',
    'LIFE_KLINE_SYSTEM_INSTRUCTION',
    'build_user_prompt',
    'parse_ai_response',
    'kline_point_to_dict',
    'life_analysis_to_dict',
    'life_destiny_result_to_dict'
]

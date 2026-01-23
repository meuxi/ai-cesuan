"""
人生K线图分析模块
参考 lifekline3 项目移植
生成1-100岁的人生运势K线图数据
"""

import json
import logging
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field, asdict
from enum import Enum

logger = logging.getLogger(__name__)


class Gender(Enum):
    """性别"""
    MALE = "male"
    FEMALE = "female"


@dataclass
class KLinePoint:
    """K线数据点"""
    age: int              # 虚岁
    year: int             # 公历年份
    ganZhi: str           # 流年干支
    daYun: str            # 大运干支
    open: int             # 开盘值
    close: int            # 收盘值
    high: int             # 最高值
    low: int              # 最低值
    score: int            # 综合评分
    reason: str           # 流年详批(20-30字)


@dataclass
class LifeKLineInput:
    """人生K线图输入参数"""
    name: str = ""                    # 姓名
    gender: Gender = Gender.MALE      # 性别
    birth_year: int = 1990            # 出生年份
    year_pillar: str = ""             # 年柱
    month_pillar: str = ""            # 月柱
    day_pillar: str = ""              # 日柱
    hour_pillar: str = ""             # 时柱
    start_age: int = 1                # 起运年龄
    first_dayun: str = ""             # 第一步大运
    is_forward: bool = True           # 大运是否顺行


@dataclass
class LifeKLineAnalysis:
    """人生K线分析结果"""
    bazi: List[str] = field(default_factory=list)
    summary: str = ""
    summaryScore: int = 5
    personality: str = ""
    personalityScore: int = 5
    industry: str = ""
    industryScore: int = 5
    fengShui: str = ""
    fengShuiScore: int = 5
    wealth: str = ""
    wealthScore: int = 5
    marriage: str = ""
    marriageScore: int = 5
    health: str = ""
    healthScore: int = 5
    family: str = ""
    familyScore: int = 5


@dataclass
class LifeKLineResult:
    """人生K线图完整结果"""
    chart_data: List[KLinePoint] = field(default_factory=list)
    analysis: LifeKLineAnalysis = field(default_factory=LifeKLineAnalysis)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "chartData": [asdict(p) for p in self.chart_data],
            "analysis": asdict(self.analysis),
        }


# 六十甲子表
JIAZI_60 = [
    "甲子", "乙丑", "丙寅", "丁卯", "戊辰", "己巳", "庚午", "辛未", "壬申", "癸酉",
    "甲戌", "乙亥", "丙子", "丁丑", "戊寅", "己卯", "庚辰", "辛巳", "壬午", "癸未",
    "甲申", "乙酉", "丙戌", "丁亥", "戊子", "己丑", "庚寅", "辛卯", "壬辰", "癸巳",
    "甲午", "乙未", "丙申", "丁酉", "戊戌", "己亥", "庚子", "辛丑", "壬寅", "癸卯",
    "甲辰", "乙巳", "丙午", "丁未", "戊申", "己酉", "庚戌", "辛亥", "壬子", "癸丑",
    "甲寅", "乙卯", "丙辰", "丁巳", "戊午", "己未", "庚申", "辛酉", "壬戌", "癸亥",
]


def get_stem_polarity(pillar: str) -> str:
    """获取天干阴阳属性"""
    if not pillar:
        return "YANG"
    
    first_char = pillar.strip()[0] if pillar.strip() else ""
    yang_stems = ["甲", "丙", "戊", "庚", "壬"]
    yin_stems = ["乙", "丁", "己", "辛", "癸"]
    
    if first_char in yang_stems:
        return "YANG"
    elif first_char in yin_stems:
        return "YIN"
    return "YANG"


def calculate_dayun_direction(year_pillar: str, gender: Gender) -> bool:
    """
    计算大运顺逆
    
    规则：
    - 阳年男命、阴年女命：顺行
    - 阴年男命、阳年女命：逆行
    """
    polarity = get_stem_polarity(year_pillar)
    is_yang = polarity == "YANG"
    
    if gender == Gender.MALE:
        return is_yang  # 阳男顺行
    else:
        return not is_yang  # 阴女顺行


def calculate_dayun_sequence(first_dayun: str, is_forward: bool, count: int = 10) -> List[str]:
    """
    计算大运序列
    
    Args:
        first_dayun: 第一步大运
        is_forward: 是否顺行
        count: 计算步数
    
    Returns:
        大运序列列表
    """
    if first_dayun not in JIAZI_60:
        return [first_dayun] * count
    
    start_idx = JIAZI_60.index(first_dayun)
    result = []
    
    for i in range(count):
        if is_forward:
            idx = (start_idx + i) % 60
        else:
            idx = (start_idx - i) % 60
        result.append(JIAZI_60[idx])
    
    return result


def get_liunian_ganzhi(birth_year: int, age: int) -> str:
    """
    计算流年干支
    
    Args:
        birth_year: 出生年份
        age: 虚岁
    
    Returns:
        流年干支
    """
    year = birth_year + age - 1
    # 1984年为甲子年
    idx = (year - 1984) % 60
    return JIAZI_60[idx]


class LifeKLineAnalyzer:
    """人生K线分析器"""
    
    def __init__(self, ai_service=None):
        """
        Args:
            ai_service: AI服务（可选，用于生成AI解读）
        """
        self.ai_service = ai_service
    
    def build_prompt(self, input_data: LifeKLineInput) -> Dict[str, str]:
        """构建AI提示词"""
        from ..prompts import get_prompt_manager
        
        manager = get_prompt_manager()
        
        # 计算大运方向
        direction_str = "顺行 (Forward)" if input_data.is_forward else "逆行 (Backward)"
        gender_str = "男 (乾造)" if input_data.gender == Gender.MALE else "女 (坤造)"
        
        variables = {
            "gender": gender_str,
            "name": input_data.name or "未提供",
            "birth_year": input_data.birth_year,
            "year_pillar": input_data.year_pillar,
            "month_pillar": input_data.month_pillar,
            "day_pillar": input_data.day_pillar,
            "hour_pillar": input_data.hour_pillar,
            "start_age": input_data.start_age,
            "first_dayun": input_data.first_dayun,
            "dayun_direction": direction_str,
        }
        
        try:
            rendered = manager.render_template("life_kline_analysis", variables)
            return rendered
        except Exception as e:
            logger.warning(f"渲染模板失败: {e}, 使用默认提示词")
            return self._build_default_prompt(input_data, variables)
    
    def _build_default_prompt(self, input_data: LifeKLineInput, variables: Dict) -> Dict[str, str]:
        """构建默认提示词"""
        system_prompt = """你是一位八字命理大师。根据用户提供的四柱干支和大运信息，生成"人生K线图"数据。
核心规则:
1. 年龄采用虚岁，从1岁开始
2. 每年的reason字段提供专业的命理分析（30-50字），体现干支生克关系
3. 所有维度给出0-10分
4. 让评分呈现明显波动，体现"牛市"和"熊市"
5. daYun是大运干支(10年不变)，ganZhi是流年干支(每年一变)
6. summary、personality、industry等文字字段请提供深度专业的解析，充分展开分析"""
        
        user_prompt = f"""请分析以下八字：

性别：{variables['gender']}
出生年份：{variables['birth_year']}年

八字四柱：
年柱：{variables['year_pillar']}
月柱：{variables['month_pillar']}
日柱：{variables['day_pillar']}
时柱：{variables['hour_pillar']}

大运参数：
起运年龄：{variables['start_age']}岁
第一步大运：{variables['first_dayun']}
排序方向：{variables['dayun_direction']}

请生成1-100岁的人生K线数据，输出纯JSON格式。"""
        
        return {"system_prompt": system_prompt, "user_prompt": user_prompt}
    
    async def generate_with_ai(self, input_data: LifeKLineInput) -> LifeKLineResult:
        """使用AI生成人生K线图"""
        if not self.ai_service:
            raise ValueError("AI服务未配置")
        
        prompts = self.build_prompt(input_data)
        
        from ..ai.provider import ChatMessage
        
        messages = [
            ChatMessage(role="system", content=prompts["system_prompt"]),
            ChatMessage(role="user", content=prompts["user_prompt"]),
        ]
        
        response = await self.ai_service.chat(messages, temperature=0.7, max_tokens=32000)  # 用户体验优先：无限制输出
        
        # 解析JSON响应
        return self._parse_ai_response(response.content)
    
    def _parse_ai_response(self, content: str) -> LifeKLineResult:
        """解析AI响应"""
        # 提取JSON
        json_content = content
        
        # 尝试提取 ```json ... ``` 中的内容
        import re
        json_match = re.search(r'```(?:json)?\s*([\s\S]*?)```', content)
        if json_match:
            json_content = json_match.group(1).strip()
        else:
            # 查找JSON对象
            start = content.find('{')
            end = content.rfind('}')
            if start != -1 and end != -1:
                json_content = content[start:end + 1]
        
        try:
            data = json.loads(json_content)
        except json.JSONDecodeError as e:
            logger.error(f"JSON解析失败: {e}")
            raise ValueError(f"AI返回的数据格式不正确: {e}")
        
        # 构建结果
        chart_points = []
        for point in data.get("chartPoints", []):
            chart_points.append(KLinePoint(
                age=point.get("age", 0),
                year=point.get("year", 0),
                ganZhi=point.get("ganZhi", ""),
                daYun=point.get("daYun", ""),
                open=point.get("open", 50),
                close=point.get("close", 50),
                high=point.get("high", 50),
                low=point.get("low", 50),
                score=point.get("score", 50),
                reason=point.get("reason", ""),
            ))
        
        analysis = LifeKLineAnalysis(
            bazi=data.get("bazi", []),
            summary=data.get("summary", ""),
            summaryScore=data.get("summaryScore", 5),
            personality=data.get("personality", ""),
            personalityScore=data.get("personalityScore", 5),
            industry=data.get("industry", ""),
            industryScore=data.get("industryScore", 5),
            fengShui=data.get("fengShui", ""),
            fengShuiScore=data.get("fengShuiScore", 5),
            wealth=data.get("wealth", ""),
            wealthScore=data.get("wealthScore", 5),
            marriage=data.get("marriage", ""),
            marriageScore=data.get("marriageScore", 5),
            health=data.get("health", ""),
            healthScore=data.get("healthScore", 5),
            family=data.get("family", ""),
            familyScore=data.get("familyScore", 5),
        )
        
        return LifeKLineResult(chart_data=chart_points, analysis=analysis)
    
    def generate_basic_chart(self, input_data: LifeKLineInput) -> LifeKLineResult:
        """
        生成基础K线图数据（不使用AI，仅基于命理规则）
        
        用于演示或API Key未配置的情况
        """
        import random
        
        chart_points = []
        dayun_sequence = calculate_dayun_sequence(
            input_data.first_dayun, 
            input_data.is_forward, 
            count=12
        )
        
        # 基础运势波动
        base_score = 50
        trend = 0
        
        for age in range(1, 101):
            year = input_data.birth_year + age - 1
            ganzhi = get_liunian_ganzhi(input_data.birth_year, age)
            
            # 计算大运
            if age < input_data.start_age:
                dayun = "童限"
            else:
                dayun_idx = (age - input_data.start_age) // 10
                dayun = dayun_sequence[min(dayun_idx, len(dayun_sequence) - 1)]
            
            # 模拟运势波动
            trend += random.uniform(-5, 5)
            trend = max(-20, min(20, trend))  # 限制趋势范围
            
            noise = random.uniform(-10, 10)
            score = int(base_score + trend + noise)
            score = max(20, min(95, score))
            
            # K线数据
            open_val = score + random.randint(-5, 5)
            close_val = score + random.randint(-5, 5)
            high_val = max(open_val, close_val) + random.randint(2, 8)
            low_val = min(open_val, close_val) - random.randint(2, 8)
            
            # 限制范围
            open_val = max(10, min(100, open_val))
            close_val = max(10, min(100, close_val))
            high_val = max(open_val, min(100, high_val))
            low_val = max(10, min(close_val, low_val))
            
            # 生成简短原因
            if close_val > open_val:
                reasons = ["运势上扬，贵人相助", "事业有成，财运亨通", "机遇来临，把握时机", "顺风顺水，心想事成"]
            else:
                reasons = ["运势平淡，宜守不宜攻", "小有波折，谨慎行事", "暂时蛰伏，等待时机", "调整期，蓄势待发"]
            
            chart_points.append(KLinePoint(
                age=age,
                year=year,
                ganZhi=ganzhi,
                daYun=dayun,
                open=open_val,
                close=close_val,
                high=high_val,
                low=low_val,
                score=score,
                reason=random.choice(reasons),
            ))
        
        # 基础分析
        analysis = LifeKLineAnalysis(
            bazi=[input_data.year_pillar, input_data.month_pillar, 
                  input_data.day_pillar, input_data.hour_pillar],
            summary="命局整体平稳，把握机遇可获成功。建议保持积极心态，顺势而为。",
            summaryScore=7,
            personality="性格稳重，为人踏实，具有较强的适应能力和抗压能力。",
            personalityScore=7,
            industry="适合从事稳定性较强的行业，如金融、教育、技术等领域。",
            industryScore=6,
            fengShui="建议居住环境保持明亮通风，办公桌朝向东南方有利。",
            fengShuiScore=7,
            wealth="财运中等偏上，正财为主，适合稳健投资。",
            wealthScore=6,
            marriage="感情运势平稳，真诚待人可遇良缘。",
            marriageScore=7,
            health="整体健康良好，注意劳逸结合，定期体检。",
            healthScore=7,
            family="六亲关系和睦，家庭运势稳定。",
            familyScore=7,
        )
        
        return LifeKLineResult(chart_data=chart_points, analysis=analysis)

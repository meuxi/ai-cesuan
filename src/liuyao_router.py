"""
六爻起卦API路由
独立路由模块，包含高级分析功能
"""
import json
import logging
from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field

from fastapi import APIRouter, HTTPException, Request, status
from fastapi.responses import StreamingResponse

from src.liuyao import (
    LineType, 
    coin_cast_full, 
    number_method, 
    time_method,
    calculate_hexagram,
    hexagram_to_dict,
    get_line_name
)
from src.liuyao_service import LiuYaoAIService, build_interpretation_prompt
from src.chatgpt_router import get_ai_manager
from src.ai.provider import ChatMessage
from src.config import settings
from openai import AsyncOpenAI
from src.divination.liuyao_advanced import (
    LiuyaoAdvancedAnalyzer, 
    calculate_time_recommendations,
    time_recommendations_to_dict,
    DIZHI_WUXING
)
from src.divination.liuyao.advanced_analysis import perform_advanced_analysis as perform_full_analysis

router = APIRouter()
_logger = logging.getLogger(__name__)

def get_current_ganzhi() -> dict:
    """获取当前时间的干支信息（简化版）"""
    now = datetime.now()
    
    # 简化算法：基于2000年1月1日为戊午日
    base_date = datetime(2000, 1, 1)
    days_diff = (now - base_date).days
    
    # 天干地支循环
    tian_gan = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']
    di_zhi = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']
    
    # 日干支（2000-1-1 为戊午日，戊=4，午=6）
    day_gan_idx = (4 + days_diff) % 10
    day_zhi_idx = (6 + days_diff) % 12
    
    # 月支简化计算（农历月份，这里用公历月份近似）
    month = now.month
    # 正月寅月，依次类推
    month_zhi_map = {1: '寅', 2: '卯', 3: '辰', 4: '巳', 5: '午', 6: '未',
                     7: '申', 8: '酉', 9: '戌', 10: '亥', 11: '子', 12: '丑'}
    month_zhi = month_zhi_map.get(month, '子')
    
    return {
        'day_gan': tian_gan[day_gan_idx],
        'day_zhi': di_zhi[day_zhi_idx],
        'month_zhi': month_zhi
    }


# ========== 请求/响应模型 ==========

class CoinCastRequest(BaseModel):
    """摇钱卦请求"""
    question: Optional[str] = Field(default="", description="用户问题")


class CoinCastLineResult(BaseModel):
    """单爻摇卦结果"""
    line_type: int = Field(description="爻类型 0-3")
    line_name: str = Field(description="爻名称")
    backs: int = Field(description="背面数量")


class NumberMethodRequest(BaseModel):
    """数理卦请求"""
    upper_num: int = Field(ge=1, description="上卦数字")
    lower_num: int = Field(ge=1, description="下卦数字")
    moving_num: int = Field(ge=1, description="动爻数字")
    question: Optional[str] = Field(default="", description="用户问题")


class TimeMethodRequest(BaseModel):
    """时空卦请求"""
    question: Optional[str] = Field(default="", description="用户问题")


class ManualLinesRequest(BaseModel):
    """手动输入爻请求"""
    lines: List[int] = Field(min_length=6, max_length=6, description="六爻列表 [0-3]*6")
    question: Optional[str] = Field(default="", description="用户问题")


class InterpretRequest(BaseModel):
    """AI解卦请求"""
    hexagram_data: dict = Field(description="卦象数据")
    question: Optional[str] = Field(default="", description="用户问题")
    style: Optional[str] = Field(default="detailed", description="解卦风格: concise/detailed/philosophical")


class AdvancedAnalysisRequest(BaseModel):
    """高级分析请求"""
    hexagram_data: dict = Field(description="卦象数据（来自起卦接口）")
    month_zhi: str = Field(description="月支，如：子、丑、寅...")
    day_gan: str = Field(description="日干，如：甲、乙、丙...")
    day_zhi: str = Field(description="日支，如：子、丑、寅...")
    yong_shen_element: Optional[str] = Field(default=None, description="用神五行（可选）")


class HexagramResponse(BaseModel):
    """卦象响应"""
    success: bool = True
    hexagram: dict = Field(description="卦象详情")
    cast_results: Optional[List[CoinCastLineResult]] = Field(default=None, description="摇卦结果(仅摇钱法)")


class InterpretResponse(BaseModel):
    """解卦响应"""
    success: bool = True
    interpretation: str = Field(description="AI解卦结果")
    provider: str = Field(description="AI提供商")


# ========== API端点 ==========

@router.post("/coin", response_model=HexagramResponse, tags=["六爻"])
async def coin_cast(request: Request, body: CoinCastRequest):
    """
    摇钱卦 - 模拟三枚铜钱摇六次
    
    返回完整卦象信息和每次摇卦的结果
    """
    _logger.info(f"摇钱卦请求: question={body.question}")
    
    try:
        # 摇卦
        cast_results = coin_cast_full()
        lines = [result[0] for result in cast_results]
        
        # 计算卦象
        hexagram = calculate_hexagram(lines)
        hexagram_dict = hexagram_to_dict(hexagram)
        
        # 构建摇卦结果
        cast_result_list = [
            CoinCastLineResult(
                line_type=int(result[0]),
                line_name=get_line_name(result[0]),
                backs=result[1]
            )
            for result in cast_results
        ]
        
        return HexagramResponse(
            success=True,
            hexagram=hexagram_dict,
            cast_results=cast_result_list
        )
    except Exception as e:
        _logger.error(f"摇钱卦失败: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"摇钱卦失败: {str(e)}"
        )


@router.post("/number", response_model=HexagramResponse, tags=["六爻"])
async def number_cast(request: Request, body: NumberMethodRequest):
    """
    数理卦 - 根据三个数字起卦
    
    - upper_num: 上卦数字 (取模8得卦)
    - lower_num: 下卦数字 (取模8得卦)
    - moving_num: 动爻数字 (取模6得动爻位置)
    """
    _logger.info(f"数理卦请求: upper={body.upper_num}, lower={body.lower_num}, moving={body.moving_num}")
    
    try:
        # 起卦
        lines = number_method(body.upper_num, body.lower_num, body.moving_num)
        
        # 计算卦象
        hexagram = calculate_hexagram(lines)
        hexagram_dict = hexagram_to_dict(hexagram)
        
        return HexagramResponse(
            success=True,
            hexagram=hexagram_dict
        )
    except Exception as e:
        _logger.error(f"数理卦失败: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"数理卦失败: {str(e)}"
        )


@router.post("/time", response_model=HexagramResponse, tags=["六爻"])
async def time_cast(request: Request, body: TimeMethodRequest):
    """
    时空卦 - 根据当前时间起卦
    
    使用年月日时自动计算上下卦和动爻
    """
    _logger.info(f"时空卦请求: question={body.question}")
    
    try:
        # 起卦
        lines = time_method()
        
        # 计算卦象
        hexagram = calculate_hexagram(lines)
        hexagram_dict = hexagram_to_dict(hexagram)
        
        return HexagramResponse(
            success=True,
            hexagram=hexagram_dict
        )
    except Exception as e:
        _logger.error(f"时空卦失败: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"时空卦失败: {str(e)}"
        )


@router.post("/manual", response_model=HexagramResponse, tags=["六爻"])
async def manual_cast(request: Request, body: ManualLinesRequest):
    """
    手动输入爻 - 直接传入六爻数据
    
    lines: 六爻列表，每个值0-3
    - 0: 少阳 (静阳)
    - 1: 少阴 (静阴)
    - 2: 老阳 (动阳→阴)
    - 3: 老阴 (动阴→阳)
    """
    _logger.info(f"手动输入爻请求: lines={body.lines}")
    
    # 验证爻值
    for i, line in enumerate(body.lines):
        if line not in [0, 1, 2, 3]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"爻{i+1}的值无效: {line}，应为0-3"
            )
    
    try:
        # 转换为LineType
        lines = [LineType(l) for l in body.lines]
        
        # 计算卦象
        hexagram = calculate_hexagram(lines)
        hexagram_dict = hexagram_to_dict(hexagram)
        
        return HexagramResponse(
            success=True,
            hexagram=hexagram_dict
        )
    except Exception as e:
        _logger.error(f"手动输入爻失败: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"计算卦象失败: {str(e)}"
        )


@router.post("/interpret", response_model=InterpretResponse, tags=["六爻"])
async def interpret_hexagram(request: Request, body: InterpretRequest):
    """
    AI解卦（增强版） - 根据卦象数据生成专业解读
    
    自动集成高级分析：空亡、旺衰、神系、三合六冲等
    
    - hexagram_data: 卦象数据 (来自起卦接口)
    - question: 用户问题
    - style: 解卦风格
      - concise: 直断吉凶
      - detailed: 详细分析
      - philosophical: 哲理解读
    
    后端自动判断AI：优先使用Gemini，未配置则使用OpenAI
    """
    _logger.info(f"AI解卦请求: style={body.style}, question={body.question}")
    
    # 获取自定义API配置 (从请求头)
    custom_api_key = request.headers.get("x-api-key")
    custom_api_base = request.headers.get("x-api-url")
    custom_model = request.headers.get("x-api-model")
    
    try:
        # 自动执行高级分析
        advanced_analysis = None
        try:
            ganzhi = get_current_ganzhi()
            analyzer = LiuyaoAdvancedAnalyzer(
                month_zhi=ganzhi['month_zhi'],
                day_gan=ganzhi['day_gan'],
                day_zhi=ganzhi['day_zhi']
            )
            
            # 从卦象数据提取爻信息
            lines = body.hexagram_data.get('lines', [])
            yaos = []
            for line in lines:
                yao_info = {
                    'index': line.get('index', 0),
                    'branch': line.get('branch', ''),
                    'element': line.get('element', ''),
                    'liu_qin': line.get('six_relation', ''),
                    'is_moving': line.get('is_moving', False),
                }
                if line.get('is_moving') and line.get('changed_branch'):
                    from src.divination.liuyao_advanced import DIZHI_WUXING
                    yao_info['changed_branch'] = line.get('changed_branch')
                    yao_info['changed_element'] = DIZHI_WUXING.get(line.get('changed_branch', ''), '')
                yaos.append(yao_info)
            
            # 根据问题推断用神五行
            yong_shen_element = _infer_yong_shen_element(body.question or "")
            advanced_analysis = analyzer.analyze_hexagram(yaos=yaos, yong_shen_element=yong_shen_element)
            _logger.info("高级分析完成")
        except Exception as e:
            _logger.warning(f"高级分析失败，将使用基础解读: {e}")
        
        # 使用AI故障转移系统（流式输出）
        prompt = build_interpretation_prompt(body.hexagram_data, body.question or "", body.style or "detailed", advanced_analysis)
        system_prompt = "你是一位精通《周易》的资深易学大师，深谙《增删卜易》《卜筮正宗》之精髓。请根据用户提供的卦象进行专业解读。"
        
        ai_manager = get_ai_manager()
        messages = [
            ChatMessage(role="system", content=system_prompt),
            ChatMessage(role="user", content=prompt)
        ]
        
        result = await ai_manager.chat_with_failover(
            messages=messages,
            temperature=0.8,
            max_tokens=32000,  # 用户体验优先：无限制输出
        )
        _logger.info(f"六爻解卦使用模型: {result.model_used.name}")
        
        return InterpretResponse(
            success=True,
            interpretation=result.response.content,
            provider=result.model_used.name
        )
    except Exception as e:
        _logger.error(f"AI解卦失败: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"AI解卦失败: {str(e)}"
        )


@router.post("/interpret/stream", tags=["六爻"])
async def interpret_hexagram_stream(request: Request, body: InterpretRequest):
    """
    AI解卦（真正流式输出版） - 根据卦象数据生成专业解读
    
    返回SSE流式响应，适合前端实时显示
    """
    _logger.info(f"AI流式解卦请求: style={body.style}, question={body.question}")
    
    # 自动执行高级分析
    advanced_analysis = None
    try:
        ganzhi = get_current_ganzhi()
        analyzer = LiuyaoAdvancedAnalyzer(
            month_zhi=ganzhi['month_zhi'],
            day_gan=ganzhi['day_gan'],
            day_zhi=ganzhi['day_zhi']
        )
        
        lines = body.hexagram_data.get('lines', [])
        yaos = []
        for line in lines:
            yao_info = {
                'index': line.get('index', 0),
                'branch': line.get('branch', ''),
                'element': line.get('element', ''),
                'liu_qin': line.get('six_relation', ''),
                'is_moving': line.get('is_moving', False),
            }
            if line.get('is_moving') and line.get('changed_branch'):
                yao_info['changed_branch'] = line.get('changed_branch')
                yao_info['changed_element'] = DIZHI_WUXING.get(line.get('changed_branch', ''), '')
            yaos.append(yao_info)
        
        yong_shen_element = _infer_yong_shen_element(body.question or "")
        advanced_analysis = analyzer.analyze_hexagram(yaos=yaos, yong_shen_element=yong_shen_element)
    except Exception as e:
        _logger.warning(f"高级分析失败: {e}")
    
    # 构建prompt
    prompt = build_interpretation_prompt(body.hexagram_data, body.question or "", body.style or "detailed", advanced_analysis)
    system_prompt = "你是一位精通《周易》的资深易学大师，深谙《增删卜易》《卜筮正宗》之精髓。请根据用户提供的卦象进行专业解读。"
    
    # 使用DashScope进行真正的流式调用
    api_key = settings.dashscope_api_key
    api_base = settings.dashscope_api_base
    model = settings.dashscope_model
    
    if not api_key:
        # 降级到其他可用的API
        api_key = settings.deepseek_api_key or settings.zhipu_api_key or settings.api_key
        api_base = settings.deepseek_api_base if settings.deepseek_api_key else (
            settings.zhipu_api_base if settings.zhipu_api_key else settings.api_base
        )
        model = settings.deepseek_model if settings.deepseek_api_key else (
            settings.zhipu_model if settings.zhipu_api_key else settings.model
        )
    
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="未配置任何AI API密钥"
        )
    
    _logger.info(f"六爻流式解卦使用: {api_base}, 模型: {model}")
    
    async def generate_stream():
        try:
            client = AsyncOpenAI(
                api_key=api_key,
                base_url=api_base,
                timeout=120.0,
                max_retries=0
            )
            
            stream = await client.chat.completions.create(
                model=model,
                max_tokens=32000,  # 用户体验优先：无限制输出
                temperature=0.8,
                stream=True,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ]
            )
            
            async for event in stream:
                if event.choices and event.choices[0].delta and event.choices[0].delta.content:
                    chunk = event.choices[0].delta.content
                    yield f"data: {json.dumps(chunk)}\n\n"
                    
        except Exception as e:
            _logger.error(f"流式调用失败: {e}")
            yield f"data: {json.dumps({'error': str(e)})}\n\n"
    
    return StreamingResponse(generate_stream(), media_type='text/event-stream')


def _infer_yong_shen_element(question: str) -> str:
    """根据问题推断用神五行"""
    # 问财运 → 妻财 → 看被我克的五行
    # 问事业 → 官鬼 → 看克我的五行
    # 问考试 → 父母 → 看生我的五行
    # 问婚姻 → 妻财/官鬼
    # 问子女 → 子孙 → 看我生的五行
    
    question_lower = question.lower()
    
    if any(kw in question_lower for kw in ['财', '钱', '投资', '生意', '买卖', '收入']):
        return '土'  # 妻财（假设世爻为木）
    elif any(kw in question_lower for kw in ['工作', '事业', '官', '升职', '面试', '职位']):
        return '金'  # 官鬼
    elif any(kw in question_lower for kw in ['考试', '学习', '文书', '合同', '证书']):
        return '水'  # 父母
    elif any(kw in question_lower for kw in ['孩子', '子女', '怀孕', '生育']):
        return '火'  # 子孙
    elif any(kw in question_lower for kw in ['健康', '疾病', '身体', '病']):
        return '金'  # 官鬼（官鬼代表疾病）
    
    return None  # 默认不指定


@router.get("/hexagram-names", tags=["六爻"])
async def get_hexagram_names():
    """
    获取64卦名列表
    """
    from src.liuyao import HEXAGRAM_NAMES, TRIGRAMS
    
    result = []
    for upper_idx in range(1, 9):
        for lower_idx in range(1, 9):
            name = HEXAGRAM_NAMES[upper_idx][lower_idx]
            upper_trigram = TRIGRAMS[upper_idx].chinese_name
            lower_trigram = TRIGRAMS[lower_idx].chinese_name
            result.append({
                'name': name,
                'upper': upper_trigram,
                'lower': lower_trigram,
                'upper_idx': upper_idx,
                'lower_idx': lower_idx
            })
    
    return {'hexagrams': result, 'total': len(result)}


@router.post("/advanced-analysis", tags=["六爻"])
async def advanced_analysis(request: Request, body: AdvancedAnalysisRequest):
    """
    六爻高级分析 - 空亡、旺衰、神系等专业分析
    
    功能包含：
    1. 空亡体系（真空/动空/冲空/临建）
    2. 旺衰五态（旺相休囚死）
    3. 月建日辰作用判定
    4. 十二长生阶段
    5. 三合局/半合分析
    6. 六冲卦判定
    7. 原神/忌神/仇神体系
    8. 动爻变化分析（化进/化退/回头生克/化空/化墓/伏吟/反吟）
    9. 伏神系统（用神不上卦时）
    
    请求参数：
    - hexagram_data: 卦象数据（来自起卦接口）
    - month_zhi: 月支（子丑寅卯辰巳午未申酉戌亥）
    - day_gan: 日干（甲乙丙丁戊己庚辛壬癸）
    - day_zhi: 日支（子丑寅卯辰巳午未申酉戌亥）
    - yong_shen_element: 用神五行（可选，木火土金水）
    """
    _logger.info(f"高级分析请求: month={body.month_zhi}, day={body.day_gan}{body.day_zhi}")
    
    try:
        # 从卦象数据中提取爻信息
        hexagram_data = body.hexagram_data
        
        # 使用新的完整高级分析模块
        full_analysis = perform_full_analysis(
            hexagram_data=hexagram_data,
            question=hexagram_data.get('question', ''),
            date=datetime.now()
        )
        
        # 同时使用旧的分析器获取兼容性数据
        analyzer = LiuyaoAdvancedAnalyzer(
            month_zhi=body.month_zhi,
            day_gan=body.day_gan,
            day_zhi=body.day_zhi
        )
        
        lines = hexagram_data.get('lines', [])
        yaos = []
        for line in lines:
            yao_info = {
                'index': line.get('index', 0),
                'branch': line.get('branch', ''),
                'element': line.get('element', ''),
                'liu_qin': line.get('six_relation', ''),
                'is_moving': line.get('is_moving', False),
            }
            if line.get('is_moving') and line.get('changed_branch'):
                from src.divination.liuyao_advanced import DIZHI_WUXING
                yao_info['changed_branch'] = line.get('changed_branch')
                yao_info['changed_element'] = DIZHI_WUXING.get(line.get('changed_branch', ''), '')
            yaos.append(yao_info)
        
        analysis_result = analyzer.analyze_hexagram(
            yaos=yaos,
            yong_shen_element=body.yong_shen_element
        )
        
        # 计算应期推断
        moving_yaos = [y for y in yaos if y.get('is_moving')]
        yong_shen_branch = ''
        if body.yong_shen_element:
            for y in yaos:
                if y.get('element') == body.yong_shen_element:
                    yong_shen_branch = y.get('branch', '')
                    break
        
        time_recs = calculate_time_recommendations(
            yong_shen_element=body.yong_shen_element or '',
            yong_shen_branch=yong_shen_branch,
            moving_yaos=moving_yaos
        )
        analysis_result['time_recommendations'] = time_recommendations_to_dict(time_recs)
        
        # 合并完整分析结果
        analysis_result['full_analysis'] = full_analysis
        
        return {
            'success': True,
            'hexagram_name': hexagram_data.get('name', ''),
            'analysis': analysis_result
        }
        
    except Exception as e:
        _logger.error(f"高级分析失败: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"高级分析失败: {str(e)}"
        )

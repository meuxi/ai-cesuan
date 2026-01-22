"""诸葛神算API路由 - 使用AI计算笔画和解签"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

router = APIRouter(prefix="/zhuge", tags=["诸葛神算"])


class ZhugeRequest(BaseModel):
    """诸葛神算请求"""
    text: str  # 三个汉字
    bihua1: Optional[int] = None  # 第一个字笔画(可由AI提供)
    bihua2: Optional[int] = None  # 第二个字笔画
    bihua3: Optional[int] = None  # 第三个字笔画


class ZhugeResponse(BaseModel):
    """诸葛神算响应"""
    success: bool
    input_chars: list = []
    bihua_list: list = []
    qian_number: int = 0
    qian_id: str = ""
    title: str = ""
    content: str = ""
    ai_interpretation: str = ""  # AI解签内容
    error: str = ""


def calculate_qian_number(b1: int, b2: int, b3: int) -> int:
    """根据三个笔画计算签号
    
    算法(从zgss.asp移植)：
    1. 取每个笔画的个位（0改为1）
    2. 组成三位数
    3. 若>=384则减384，循环直到<384
    4. 若结果为0则改为384
    """
    # 取个位，0改为1
    d1 = b1 % 10
    d2 = b2 % 10
    d3 = b3 % 10
    if d1 == 0: d1 = 1
    if d2 == 0: d2 = 1
    if d3 == 0: d3 = 1
    
    # 组成三位数
    number = int(f"{d1}{d2}{d3}")
    
    # 若>=384则减384
    while number >= 384:
        number -= 384
    
    # 若结果为0则改为384
    if number == 0:
        number = 384
    
    return number


@router.post("/divine", response_model=ZhugeResponse, summary="诸葛神算占卜")
async def divine(request: ZhugeRequest):
    """
    诸葛神算占卜接口 - 完整移植自zgss.asp
    
    - **text**: 输入三个汉字进行占卜
    - **bihua1/2/3**: 可选，由前端通过AI获取笔画数后传入
    
    算法说明(从zgss.asp移植)：
    1. 用户输入三个汉字
    2. 通过AI获取每个汉字的笔画数
    3. 取每个笔画数的个位（0改为1）
    4. 三个个位数组成三位数
    5. 若>=384则减384
    6. 根据签号结合AI生成解签
    
    注意：笔画计算和解签内容由前端调用AI服务完成
    """
    try:
        # 提取三个汉字
        chars = list(request.text.replace(" ", ""))[:3]
        if len(chars) < 3:
            return ZhugeResponse(
                success=False,
                error="请输入三个汉字"
            )
        
        # 检查是否提供了笔画数
        if request.bihua1 is None or request.bihua2 is None or request.bihua3 is None:
            return ZhugeResponse(
                success=False,
                input_chars=chars,
                error="请先通过AI获取汉字笔画数，然后提供bihua1/bihua2/bihua3参数"
            )
        
        # 计算签号
        qian_number = calculate_qian_number(request.bihua1, request.bihua2, request.bihua3)
        qian_id = str(qian_number).zfill(3)
        
        return ZhugeResponse(
            success=True,
            input_chars=chars,
            bihua_list=[request.bihua1, request.bihua2, request.bihua3],
            qian_number=qian_number,
            qian_id=qian_id,
            title=f"第{qian_number}签",
            content="请结合AI生成详细解签内容",
            ai_interpretation=""  # 由前端调用AI服务填充
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/info", summary="诸葛神算说明")
async def get_info():
    """获取诸葛神算说明"""
    return {
        "name": "诸葛神算",
        "total": 384,
        "description": """诸葛神数相传是三国时代刘备的军师诸葛亮所作。
根据历史记载，诸葛亮上懂天文，下晓地理，料事如神，用兵用人，皆恰到好处。
诸葛亮每遇难题，必暗自用一种独到的占卜法。心要诚，手要净，焚香向天祷告，然后，在纸上写三个字。
这三个字，即是天灵与人心灵交流，也就是说，你的心事已得上天了解，而上天会对你作出指示。
所以万万不可存"玩一玩"的心态。""",
        "algorithm": """1. 输入三个汉字
2. 通过AI获取每个汉字的笔画数
3. 取每个笔画数的个位（0改为1）
4. 三个个位数组成三位数
5. 若>=384则减384
6. 根据签号结合AI生成解签""",
        "usage": "请先输入三个汉字，系统会通过AI计算笔画并生成解签"
    }

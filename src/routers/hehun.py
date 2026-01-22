"""
八字合婚路由
支持完整八字（年月日时）的合婚分析
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from src.divination.bazi.hepan import (
    BirthInfo, analyze_compatibility, calculate_bazi,
    get_compatibility_level, TIAN_GAN, DI_ZHI
)

router = APIRouter(prefix="/hehun", tags=["合婚"])


class PersonInput(BaseModel):
    """单人输入"""
    name: str = "甲方"
    year: int
    month: int
    day: int
    hour: int
    gender: Optional[str] = None


class HehunRequest(BaseModel):
    """完整八字合婚请求"""
    male: PersonInput
    female: PersonInput
    hepan_type: str = "love"


class SimpleHehunRequest(BaseModel):
    """简化版合婚请求（仅年份，向后兼容）"""
    male_year: int
    female_year: int


@router.post("/analyze")
async def analyze_hehun(request: HehunRequest):
    """
    完整八字合婚分析
    需要双方的年月日时信息
    """
    try:
        # 构建出生信息
        male_birth: BirthInfo = {
            'name': request.male.name or '男方',
            'year': request.male.year,
            'month': request.male.month,
            'day': request.male.day,
            'hour': request.male.hour,
            'gender': request.male.gender or '男',
        }
        
        female_birth: BirthInfo = {
            'name': request.female.name or '女方',
            'year': request.female.year,
            'month': request.female.month,
            'day': request.female.day,
            'hour': request.female.hour,
            'gender': request.female.gender or '女',
        }
        
        # 计算八字
        male_bazi = calculate_bazi(male_birth)
        female_bazi = calculate_bazi(female_birth)
        
        # 分析合盘
        result = analyze_compatibility(male_birth, female_birth, request.hepan_type)
        
        # 获取兼容性等级
        level_info = get_compatibility_level(result['overall_score'])
        
        # 格式化八字显示
        def format_bazi(bazi):
            return {
                'year': f"{bazi['year_gan']}{bazi['year_zhi']}",
                'month': f"{bazi['month_gan']}{bazi['month_zhi']}",
                'day': f"{bazi['day_gan']}{bazi['day_zhi']}",
                'hour': f"{bazi['hour_gan']}{bazi['hour_zhi']}",
                'full': f"{bazi['year_gan']}{bazi['year_zhi']} {bazi['month_gan']}{bazi['month_zhi']} {bazi['day_gan']}{bazi['day_zhi']} {bazi['hour_gan']}{bazi['hour_zhi']}",
                'wuxing_count': bazi['wuxing_count'],
                'dominant_wuxing': bazi['dominant_wuxing'],
            }
        
        return {
            'success': True,
            'male': {
                'name': male_birth['name'],
                'birth': f"{male_birth['year']}-{male_birth['month']:02d}-{male_birth['day']:02d} {male_birth['hour']:02d}:00",
                'bazi': format_bazi(male_bazi),
            },
            'female': {
                'name': female_birth['name'],
                'birth': f"{female_birth['year']}-{female_birth['month']:02d}-{female_birth['day']:02d} {female_birth['hour']:02d}:00",
                'bazi': format_bazi(female_bazi),
            },
            'overall_score': result['overall_score'],
            'level': level_info['level'],
            'level_color': level_info['color'],
            'dimensions': result['dimensions'],
            'conflicts': result['conflicts'],
            'hepan_type': request.hepan_type,
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"合婚分析失败: {str(e)}")


@router.post("/simple")
async def simple_hehun(request: SimpleHehunRequest):
    """
    简化版合婚（仅年份）
    向后兼容旧API
    """
    from src.divination.hehun import analyze_hehun as simple_analyze
    
    try:
        result = simple_analyze(request.male_year, request.female_year)
        return {
            'success': True,
            **result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"合婚计算失败: {str(e)}")

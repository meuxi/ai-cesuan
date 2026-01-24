"""
占卜模块参数验证器

提供统一的参数验证装饰器和验证函数，确保输入数据的有效性。

使用方式：
    from src.divination.common.validators import validate_datetime, validate_gender
    
    @validate_datetime
    def calculate_bazi(year: int, month: int, day: int, hour: int):
        ...
"""
import logging
from functools import wraps
from typing import Callable, Any, Optional
from datetime import datetime

_logger = logging.getLogger(__name__)


class ValidationError(ValueError):
    """参数验证错误"""
    
    def __init__(self, field: str, message: str, value: Any = None):
        self.field = field
        self.message = message
        self.value = value
        super().__init__(f"参数 '{field}' 验证失败: {message}")


# ============= 验证函数 =============

def validate_year(year: int, min_year: int = 1900, max_year: int = 2100) -> int:
    """验证年份"""
    if not isinstance(year, int):
        raise ValidationError("year", f"必须为整数，实际类型: {type(year).__name__}", year)
    if year < min_year or year > max_year:
        raise ValidationError("year", f"必须在 {min_year}-{max_year} 范围内", year)
    return year


def validate_month(month: int) -> int:
    """验证月份（1-12）"""
    if not isinstance(month, int):
        raise ValidationError("month", f"必须为整数，实际类型: {type(month).__name__}", month)
    if month < 1 or month > 12:
        raise ValidationError("month", "必须在 1-12 范围内", month)
    return month


def validate_day(day: int, year: int = None, month: int = None) -> int:
    """验证日期（1-31，可选择根据年月校验）"""
    if not isinstance(day, int):
        raise ValidationError("day", f"必须为整数，实际类型: {type(day).__name__}", day)
    if day < 1 or day > 31:
        raise ValidationError("day", "必须在 1-31 范围内", day)
    
    # 如果提供了年月，校验日期有效性
    if year is not None and month is not None:
        try:
            datetime(year, month, day)
        except ValueError:
            raise ValidationError("day", f"{year}年{month}月没有第{day}天", day)
    
    return day


def validate_hour(hour: int) -> int:
    """验证小时（0-23）"""
    if not isinstance(hour, int):
        raise ValidationError("hour", f"必须为整数，实际类型: {type(hour).__name__}", hour)
    if hour < 0 or hour > 23:
        raise ValidationError("hour", "必须在 0-23 范围内", hour)
    return hour


def validate_minute(minute: int) -> int:
    """验证分钟（0-59）"""
    if not isinstance(minute, int):
        raise ValidationError("minute", f"必须为整数，实际类型: {type(minute).__name__}", minute)
    if minute < 0 or minute > 59:
        raise ValidationError("minute", "必须在 0-59 范围内", minute)
    return minute


def validate_gender(gender: str) -> str:
    """验证性别"""
    valid_genders = {'男', '女', '乾', '坤', 'male', 'female', 'm', 'f', '1', '0'}
    if not isinstance(gender, str):
        raise ValidationError("gender", f"必须为字符串，实际类型: {type(gender).__name__}", gender)
    
    gender_lower = gender.lower().strip()
    if gender_lower not in {g.lower() for g in valid_genders}:
        raise ValidationError("gender", f"必须为 男/女 或 male/female，实际值: {gender}", gender)
    
    # 标准化返回值
    if gender_lower in {'男', 'male', 'm', '乾', '1'}:
        return '男'
    return '女'


def validate_birthday_string(birthday: str) -> datetime:
    """
    验证并解析生日字符串
    
    支持格式：
    - YYYY-MM-DD HH:MM:SS
    - YYYY-MM-DD HH:MM
    - YYYY-MM-DD
    - YYYY/MM/DD HH:MM:SS
    """
    if not isinstance(birthday, str):
        raise ValidationError("birthday", f"必须为字符串，实际类型: {type(birthday).__name__}", birthday)
    
    birthday = birthday.strip()
    if not birthday:
        raise ValidationError("birthday", "不能为空", birthday)
    
    # 尝试多种格式解析
    formats = [
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d %H:%M",
        "%Y-%m-%d",
        "%Y/%m/%d %H:%M:%S",
        "%Y/%m/%d %H:%M",
        "%Y/%m/%d",
    ]
    
    for fmt in formats:
        try:
            return datetime.strptime(birthday, fmt)
        except ValueError:
            continue
    
    raise ValidationError(
        "birthday", 
        f"日期格式无效，支持格式: YYYY-MM-DD HH:MM:SS, YYYY-MM-DD 等", 
        birthday
    )


def validate_positive_int(value: int, field_name: str, max_value: int = None) -> int:
    """验证正整数"""
    if not isinstance(value, int):
        raise ValidationError(field_name, f"必须为整数，实际类型: {type(value).__name__}", value)
    if value < 1:
        raise ValidationError(field_name, "必须为正整数", value)
    if max_value and value > max_value:
        raise ValidationError(field_name, f"不能超过 {max_value}", value)
    return value


def validate_range_int(value: int, field_name: str, min_val: int, max_val: int) -> int:
    """验证范围内的整数"""
    if not isinstance(value, int):
        raise ValidationError(field_name, f"必须为整数，实际类型: {type(value).__name__}", value)
    if value < min_val or value > max_val:
        raise ValidationError(field_name, f"必须在 {min_val}-{max_val} 范围内", value)
    return value


def validate_pan_type(pan_type: str) -> str:
    """验证奇门盘类型"""
    valid_types = ['时盘', '日盘', '月盘', '年盘']
    if pan_type not in valid_types:
        raise ValidationError("pan_type", f"无效的盘类型，应为：{', '.join(valid_types)}", pan_type)
    return pan_type


def validate_pan_style(pan_style: str) -> str:
    """验证奇门盘式"""
    valid_styles = ['转盘', '飞盘']
    if pan_style not in valid_styles:
        raise ValidationError("pan_style", f"无效的盘式，应为：{', '.join(valid_styles)}", pan_style)
    return pan_style


def validate_wuxing(wuxing: str) -> str:
    """验证五行"""
    valid_wuxing = ['木', '火', '土', '金', '水']
    if wuxing not in valid_wuxing:
        raise ValidationError("wuxing", f"无效的五行，应为：{', '.join(valid_wuxing)}", wuxing)
    return wuxing


def validate_gong_position(gong: int, field_name: str = "gong") -> int:
    """验证宫位（1-9）"""
    if not isinstance(gong, int):
        raise ValidationError(field_name, f"必须为整数，实际类型: {type(gong).__name__}", gong)
    if gong < 1 or gong > 9:
        raise ValidationError(field_name, "必须在 1-9 范围内", gong)
    return gong


# ============= 装饰器 =============

def validate_datetime_params(
    year_param: str = 'year',
    month_param: str = 'month', 
    day_param: str = 'day',
    hour_param: str = 'hour',
    minute_param: str = 'minute',
    require_time: bool = False
) -> Callable:
    """
    日期时间参数验证装饰器
    
    Args:
        year_param: 年份参数名
        month_param: 月份参数名
        day_param: 日期参数名
        hour_param: 小时参数名
        minute_param: 分钟参数名
        require_time: 是否要求时间参数
        
    Example:
        @validate_datetime_params()
        def calculate_bazi(year: int, month: int, day: int, hour: int = 12):
            ...
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            # 获取函数签名
            import inspect
            sig = inspect.signature(func)
            params = list(sig.parameters.keys())
            
            # 合并 args 和 kwargs
            bound_args = {}
            for i, arg in enumerate(args):
                if i < len(params):
                    bound_args[params[i]] = arg
            bound_args.update(kwargs)
            
            # 验证年份
            if year_param in bound_args:
                bound_args[year_param] = validate_year(bound_args[year_param])
            
            # 验证月份
            if month_param in bound_args:
                bound_args[month_param] = validate_month(bound_args[month_param])
            
            # 验证日期
            if day_param in bound_args:
                year_val = bound_args.get(year_param)
                month_val = bound_args.get(month_param)
                bound_args[day_param] = validate_day(
                    bound_args[day_param], 
                    year_val, 
                    month_val
                )
            
            # 验证小时
            if hour_param in bound_args and bound_args[hour_param] is not None:
                bound_args[hour_param] = validate_hour(bound_args[hour_param])
            elif require_time and hour_param not in bound_args:
                raise ValidationError(hour_param, "时间参数是必需的")
            
            # 验证分钟
            if minute_param in bound_args and bound_args[minute_param] is not None:
                bound_args[minute_param] = validate_minute(bound_args[minute_param])
            
            # 重新构建参数
            new_args = []
            for i, param in enumerate(params):
                if i < len(args) and param in bound_args:
                    new_args.append(bound_args[param])
                elif i < len(args):
                    new_args.append(args[i])
            
            new_kwargs = {k: v for k, v in bound_args.items() if k not in params[:len(args)]}
            
            return func(*new_args, **new_kwargs)
        
        return wrapper
    return decorator


def validate_gender_param(gender_param: str = 'gender') -> Callable:
    """
    性别参数验证装饰器
    
    Example:
        @validate_gender_param()
        def calculate_dayun(gender: str, ...):
            ...
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            import inspect
            sig = inspect.signature(func)
            params = list(sig.parameters.keys())
            
            # 合并参数
            bound_args = {}
            for i, arg in enumerate(args):
                if i < len(params):
                    bound_args[params[i]] = arg
            bound_args.update(kwargs)
            
            # 验证性别
            if gender_param in bound_args:
                bound_args[gender_param] = validate_gender(bound_args[gender_param])
            
            # 重新构建参数
            new_args = list(args)
            for i, param in enumerate(params):
                if i < len(args) and param in bound_args:
                    new_args[i] = bound_args[param]
            
            new_kwargs = {k: v for k, v in bound_args.items() if k not in params[:len(args)]}
            
            return func(*new_args, **new_kwargs)
        
        return wrapper
    return decorator


# ============= 导出 =============

__all__ = [
    # 异常类
    'ValidationError',
    # 验证函数
    'validate_year',
    'validate_month',
    'validate_day',
    'validate_hour',
    'validate_minute',
    'validate_gender',
    'validate_birthday_string',
    'validate_positive_int',
    'validate_range_int',
    # 奇门验证
    'validate_pan_type',
    'validate_pan_style',
    'validate_wuxing',
    'validate_gong_position',
    # 装饰器
    'validate_datetime_params',
    'validate_gender_param',
]

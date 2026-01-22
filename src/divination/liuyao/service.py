# -*- coding: utf-8 -*-
"""
六爻统一服务入口
整合所有六爻相关功能模块

模块功能：
- 排盘计算
- 纳甲计算
- 伏神计算
- 旺衰分析
- 高级分析（暗动/日破/三合/六冲等）
- AI解卦
"""

from typing import Dict, List, Optional, Any
from datetime import datetime
import logging

from .najia import najia_calculate, EIGHT_PALACES
from .advanced_analysis import LiuyaoAdvancedAnalyzer, calculate_time_recommendations
from .data.hexagram_texts import get_hexagram_texts, get_yao_texts
from ..liuyao_enhanced import (
    FushenCalculator,
    WangshuaiCalculator,
    JintuishenCalculator,
    LiuyaoEnhanced,
    enhance_liuyao_analysis
)

_logger = logging.getLogger(__name__)


class LiuyaoService:
    """
    六爻统一服务类
    提供完整的六爻排盘、分析、解读功能
    """
    
    def __init__(self):
        pass  # 分析器按需创建
    
    def calculate_hexagram(
        self,
        lines: List[int],
        question: str = "",
        method: str = "coin"
    ) -> Dict[str, Any]:
        """
        计算卦象
        
        Args:
            lines: 六爻数据 [0-3]*6, 0=少阳, 1=少阴, 2=老阳, 3=老阴
            question: 所问事项
            method: 起卦方式 coin/number/time
            
        Returns:
            完整卦象数据
        """
        try:
            # 基础纳甲计算
            hexagram_data = najia_calculate(lines)
            
            # 增强分析（伏神、旺衰等）
            if hexagram_data:
                hexagram_data = enhance_liuyao_analysis(hexagram_data)
            
            # 添加卦辞爻辞
            if hexagram_data and hexagram_data.get('hexagram_name'):
                texts = get_hexagram_texts(hexagram_data['hexagram_name'])
                if texts:
                    hexagram_data['guaci'] = texts.get('guaci', '')
                    hexagram_data['tuanci'] = texts.get('tuanci', '')
                    hexagram_data['xiangci'] = texts.get('xiangci', '')
                
                # 添加爻辞
                yao_texts = get_yao_texts(hexagram_data['hexagram_name'])
                if yao_texts and 'lines' in hexagram_data:
                    for i, line in enumerate(hexagram_data['lines']):
                        if i < len(yao_texts):
                            line['yaoci'] = yao_texts[i]
            
            hexagram_data['question'] = question
            hexagram_data['method'] = method
            hexagram_data['timestamp'] = datetime.now().isoformat()
            
            return hexagram_data
            
        except Exception as e:
            _logger.error(f"卦象计算失败: {e}")
            raise
    
    def advanced_analysis(
        self,
        hexagram_data: Dict[str, Any],
        yong_shen: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        执行高级分析
        
        Args:
            hexagram_data: 基础卦象数据
            yong_shen: 用神六亲 (可选，自动推断)
            
        Returns:
            高级分析结果
        """
        try:
            # 创建分析器并执行分析
            question = hexagram_data.get('question', '')
            analyzer = LiuyaoAdvancedAnalyzer(hexagram_data, question)
            analysis = analyzer.analyze()
            
            # 时间推荐
            time_rec = calculate_time_recommendations(hexagram_data, question)
            analysis['timeRecommendations'] = time_rec
            
            return analysis
            
        except Exception as e:
            _logger.error(f"高级分析失败: {e}")
            raise
    
    def full_analysis(
        self,
        lines: List[int],
        question: str = "",
        method: str = "coin",
        yong_shen: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        完整分析（排盘+高级分析）
        
        Args:
            lines: 六爻数据
            question: 所问事项
            method: 起卦方式
            yong_shen: 用神六亲
            
        Returns:
            包含所有分析结果的完整数据
        """
        # 基础排盘
        hexagram_data = self.calculate_hexagram(lines, question, method)
        
        # 高级分析
        advanced_result = self.advanced_analysis(hexagram_data, yong_shen)
        
        return {
            'hexagram': hexagram_data,
            'advanced': advanced_result,
            'question': question,
            'method': method,
            'timestamp': datetime.now().isoformat()
        }
    
    @staticmethod
    def generate_coin_lines() -> List[int]:
        """
        模拟摇钱起卦，生成六爻
        
        Returns:
            六爻数据列表 [0-3]*6
        """
        import random
        lines = []
        for _ in range(6):
            # 模拟三枚铜钱
            coins = [random.choice([0, 1]) for _ in range(3)]  # 0=背, 1=字
            backs = sum(1 for c in coins if c == 0)
            
            # 0背=老阴(3), 1背=少阳(0), 2背=少阴(1), 3背=老阳(2)
            if backs == 0:
                lines.append(3)  # 老阴
            elif backs == 1:
                lines.append(0)  # 少阳
            elif backs == 2:
                lines.append(1)  # 少阴
            else:  # backs == 3
                lines.append(2)  # 老阳
        
        return lines
    
    @staticmethod
    def generate_number_lines(num1: int, num2: int) -> List[int]:
        """
        数字起卦
        
        Args:
            num1: 第一个数字（上卦）
            num2: 第二个数字（下卦）
            
        Returns:
            六爻数据列表
        """
        # 确定上下卦和动爻
        upper = ((num1 - 1) % 8) + 1
        lower = ((num2 - 1) % 8) + 1
        moving = ((num1 + num2 - 1) % 6)  # 动爻位置 0-5
        
        # 八卦对应的爻（从下到上）
        BAGUA_LINES = {
            1: [1, 1, 1],  # 乾
            2: [1, 1, 0],  # 兑
            3: [1, 0, 1],  # 离
            4: [1, 0, 0],  # 震
            5: [0, 1, 1],  # 巽
            6: [0, 1, 0],  # 坎
            7: [0, 0, 1],  # 艮
            8: [0, 0, 0],  # 坤
        }
        
        lower_lines = BAGUA_LINES[lower]
        upper_lines = BAGUA_LINES[upper]
        
        # 组合六爻
        lines = []
        all_lines = lower_lines + upper_lines
        for i, line in enumerate(all_lines):
            if i == moving:
                # 动爻：阳变老阳，阴变老阴
                lines.append(2 if line == 1 else 3)
            else:
                # 静爻
                lines.append(0 if line == 1 else 1)
        
        return lines
    
    @staticmethod
    def generate_time_lines(dt: Optional[datetime] = None) -> List[int]:
        """
        时间起卦
        
        Args:
            dt: 指定时间，默认当前时间
            
        Returns:
            六爻数据列表
        """
        if dt is None:
            dt = datetime.now()
        
        # 农历计算（简化版，实际应用lunar_python）
        month = dt.month
        day = dt.day
        hour = (dt.hour + 1) // 2 % 12  # 地支时辰
        
        upper = ((month + day - 1) % 8) + 1
        lower = ((month + day + hour - 1) % 8) + 1
        moving = ((month + day + hour - 1) % 6)
        
        return LiuyaoService.generate_number_lines(upper * 10 + lower, moving + 1)


# 创建单例服务
liuyao_service = LiuyaoService()


# 便捷函数
def calculate_hexagram(lines: List[int], question: str = "", method: str = "coin") -> Dict[str, Any]:
    """便捷函数：计算卦象"""
    return liuyao_service.calculate_hexagram(lines, question, method)


def full_analysis(lines: List[int], question: str = "", method: str = "coin", 
                  yong_shen: Optional[str] = None) -> Dict[str, Any]:
    """便捷函数：完整分析"""
    return liuyao_service.full_analysis(lines, question, method, yong_shen)


def coin_cast(question: str = "") -> Dict[str, Any]:
    """便捷函数：摇钱起卦"""
    lines = LiuyaoService.generate_coin_lines()
    return liuyao_service.full_analysis(lines, question, "coin")


def number_cast(num1: int, num2: int, question: str = "") -> Dict[str, Any]:
    """便捷函数：数字起卦"""
    lines = LiuyaoService.generate_number_lines(num1, num2)
    return liuyao_service.full_analysis(lines, question, "number")


def time_cast(dt: Optional[datetime] = None, question: str = "") -> Dict[str, Any]:
    """便捷函数：时间起卦"""
    lines = LiuyaoService.generate_time_lines(dt)
    return liuyao_service.full_analysis(lines, question, "time")

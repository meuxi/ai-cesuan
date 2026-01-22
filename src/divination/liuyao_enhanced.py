"""
六爻算法增强模块
参考 mingpan 增加伏神计算、旺衰分析、进退神等功能
"""
from typing import Dict, List, Optional
from datetime import datetime


class FushenCalculator:
    """伏神计算器"""
    
    # 八宫伏神表（宫位 -> 完整六亲列表）
    GONG_LIUQIN = {
        '乾': ['父母', '兄弟', '官鬼', '父母', '妻财', '子孙'],
        '兑': ['兄弟', '子孙', '父母', '兄弟', '官鬼', '妻财'],
        '离': ['官鬼', '父母', '兄弟', '官鬼', '妻财', '子孙'],
        '震': ['妻财', '官鬼', '父母', '妻财', '子孙', '兄弟'],
        '巽': ['兄弟', '父母', '官鬼', '兄弟', '妻财', '子孙'],
        '坎': ['子孙', '妻财', '兄弟', '子孙', '父母', '官鬼'],
        '艮': ['官鬼', '父母', '兄弟', '官鬼', '妻财', '子孙'],
        '坤': ['子孙', '妻财', '兄弟', '子孙', '父母', '官鬼']
    }
    
    @staticmethod
    def calculate(gong_name: str, present_liuqin: List[str]) -> List[Optional[Dict]]:
        """计算伏神
        
        Args:
            gong_name: 宫名（乾、兑、离、震、巽、坎、艮、坤）
            present_liuqin: 本卦六爻的六亲列表（从初爻到上爻）
            
        Returns:
            伏神列表，若某爻无伏神则为None
        """
        if gong_name not in FushenCalculator.GONG_LIUQIN:
            return [None] * 6
        
        gong_liuqin_full = FushenCalculator.GONG_LIUQIN[gong_name]
        fushen_list = []
        
        for i in range(6):
            # 检查本宫六亲是否在本卦中出现
            gong_qin = gong_liuqin_full[i]
            
            # 如果本卦中没有这个六亲，则为伏神
            if gong_qin not in present_liuqin:
                fushen_list.append({
                    'position': i + 1,
                    'liuqin': gong_qin,
                    'type': 'hidden'
                })
            else:
                fushen_list.append(None)
        
        return fushen_list


class WangshuaiCalculator:
    """旺衰计算器"""
    
    # 月令旺衰表（地支月令 -> 五行旺衰）
    MONTHLY_STRENGTH = {
        '寅': {'木': '旺', '火': '相', '水': '休', '金': '囚', '土': '死'},
        '卯': {'木': '旺', '火': '相', '水': '休', '金': '囚', '土': '死'},
        '辰': {'土': '旺', '金': '相', '火': '休', '木': '囚', '水': '死'},
        '巳': {'火': '旺', '土': '相', '木': '休', '水': '囚', '金': '死'},
        '午': {'火': '旺', '土': '相', '木': '休', '水': '囚', '金': '死'},
        '未': {'土': '旺', '火': '相', '金': '休', '水': '囚', '木': '死'},
        '申': {'金': '旺', '水': '相', '土': '休', '火': '囚', '木': '死'},
        '酉': {'金': '旺', '水': '相', '土': '休', '火': '囚', '木': '死'},
        '戌': {'土': '旺', '金': '相', '水': '休', '木': '囚', '火': '死'},
        '亥': {'水': '旺', '木': '相', '金': '休', '土': '囚', '火': '死'},
        '子': {'水': '旺', '木': '相', '金': '休', '土': '囚', '火': '死'},
        '丑': {'土': '旺', '水': '相', '火': '休', '金': '囚', '木': '死'}
    }
    
    # 日辰生克关系
    DAILY_RELATION = {
        '生': '日生',  # 日辰生爻
        '克': '日克',  # 日辰克爻
        '比': '日比',  # 日辰与爻同类
        '被生': '生日',  # 爻生日辰
        '被克': '克日'   # 爻克日辰
    }
    
    @staticmethod
    def calculate_monthly_strength(yao_element: str, month_branch: str) -> str:
        """计算月令旺衰
        
        Args:
            yao_element: 爻的五行
            month_branch: 月支
            
        Returns:
            旺衰状态（旺、相、休、囚、死）
        """
        if month_branch in WangshuaiCalculator.MONTHLY_STRENGTH:
            strength_map = WangshuaiCalculator.MONTHLY_STRENGTH[month_branch]
            return strength_map.get(yao_element, '休')
        return '休'
    
    @staticmethod
    def calculate_daily_relation(yao_element: str, day_element: str) -> str:
        """计算日辰关系
        
        Args:
            yao_element: 爻的五行
            day_element: 日辰五行
            
        Returns:
            日辰关系
        """
        # 五行生克关系
        sheng_map = {
            '木': '火', '火': '土', '土': '金', '金': '水', '水': '木'
        }
        ke_map = {
            '木': '土', '土': '水', '水': '火', '火': '金', '金': '木'
        }
        
        if yao_element == day_element:
            return '日比'
        elif sheng_map.get(day_element) == yao_element:
            return '日生'
        elif ke_map.get(day_element) == yao_element:
            return '日克'
        elif sheng_map.get(yao_element) == day_element:
            return '生日'
        elif ke_map.get(yao_element) == day_element:
            return '克日'
        return '平'


class JintuishenCalculator:
    """进退神计算器"""
    
    @staticmethod
    def calculate(ben_yao_element: str, bian_yao_element: str) -> Optional[str]:
        """计算进退神
        
        Args:
            ben_yao_element: 本卦爻的五行
            bian_yao_element: 变卦爻的五行（动爻才有）
            
        Returns:
            进退神类型（进神、退神、None）
        """
        if not bian_yao_element:
            return None
        
        # 五行强度排序
        strength_order = ['长生', '帝旺', '临官', '冠带', '沐浴', '养', '胎', '绝', '墓', '死', '病', '衰']
        
        # 简化判断：变爻生本爻为进神，变爻克本爻为退神
        sheng_map = {
            '木': '火', '火': '土', '土': '金', '金': '水', '水': '木'
        }
        ke_map = {
            '木': '土', '土': '水', '水': '火', '火': '金', '金': '木'
        }
        
        if sheng_map.get(bian_yao_element) == ben_yao_element:
            return '进神'
        elif ke_map.get(bian_yao_element) == ben_yao_element:
            return '退神'
        
        return None


class LiuyaoEnhanced:
    """六爻增强分析"""
    
    def __init__(self):
        self.fushen_calc = FushenCalculator()
        self.wangshuai_calc = WangshuaiCalculator()
        self.jintui_calc = JintuishenCalculator()
    
    def enhance_liuyao_result(self, basic_result: Dict, 
                              time_info: Optional[Dict] = None) -> Dict:
        """增强六爻分析结果
        
        Args:
            basic_result: 基础六爻排盘结果
            time_info: 时间信息（年月日时的干支）
            
        Returns:
            增强后的结果，包含伏神、旺衰、进退神等
        """
        enhanced = basic_result.copy()
        
        # 提取基础信息
        ben_gua = basic_result.get('ben_gua', {})
        gong_name = ben_gua.get('palace_name', '乾')
        lines = basic_result.get('lines', [])
        
        if not lines:
            return enhanced
        
        # 提取六亲列表
        present_liuqin = [line.get('six_relation', '兄弟') for line in lines]
        
        # 1. 计算伏神
        fushen_list = self.fushen_calc.calculate(gong_name, present_liuqin)
        
        # 2. 计算旺衰和日辰关系
        if time_info:
            month_branch = time_info.get('month_branch', '子')
            day_element = time_info.get('day_element', '木')
            
            for i, line in enumerate(lines):
                yao_element = line.get('element', '木')
                
                # 月令旺衰
                monthly_strength = self.wangshuai_calc.calculate_monthly_strength(
                    yao_element, month_branch
                )
                lines[i]['monthly_strength'] = monthly_strength
                
                # 日辰关系
                daily_relation = self.wangshuai_calc.calculate_daily_relation(
                    yao_element, day_element
                )
                lines[i]['daily_relation'] = daily_relation
                
                # 伏神
                if fushen_list[i]:
                    lines[i]['fushen'] = fushen_list[i]
                
                # 进退神（仅动爻）
                if line.get('is_moving'):
                    bian_yao = line.get('changed_branch')
                    if bian_yao:
                        bian_element = line.get('changed_element', '')
                        jintui = self.jintui_calc.calculate(yao_element, bian_element)
                        if jintui:
                            lines[i]['jintui_shen'] = jintui
        
        enhanced['lines'] = lines
        enhanced['enhanced'] = True
        
        # 3. 生成分析建议
        enhanced['analysis_hints'] = self._generate_analysis_hints(lines)
        
        return enhanced
    
    def _generate_analysis_hints(self, lines: List[Dict]) -> List[str]:
        """生成分析提示"""
        hints = []
        
        # 统计动爻数量
        moving_count = sum(1 for line in lines if line.get('is_moving'))
        if moving_count == 0:
            hints.append('静卦无动爻，以本卦断')
        elif moving_count == 1:
            hints.append('一爻动，以动爻断吉凶')
        elif moving_count > 3:
            hints.append('多爻动，事态复杂多变')
        
        # 检查世应
        for line in lines:
            if line.get('is_shi'):
                shi_strength = line.get('monthly_strength', '')
                if shi_strength == '旺':
                    hints.append('世爻旺相，利于己方')
                elif shi_strength in ['囚', '死']:
                    hints.append('世爻衰弱，不利己方')
        
        # 检查用神
        for line in lines:
            if line.get('six_relation') in ['妻财', '官鬼', '子孙']:
                strength = line.get('monthly_strength', '')
                if strength == '旺':
                    hints.append(f"{line['six_relation']}旺相，所求有望")
        
        return hints if hints else ['请结合卦象具体分析']


def enhance_liuyao_analysis(basic_result: Dict, 
                           year: int, month: int, day: int, hour: int) -> Dict:
    """便捷函数：增强六爻分析
    
    Args:
        basic_result: 基础六爻排盘结果
        year, month, day, hour: 起卦时间
        
    Returns:
        增强后的分析结果
    """
    from ..bazi.ganzhi import GanZhi
    from ..bazi.lunar import solar_to_lunar
    
    # 获取时间干支
    lunar_info = solar_to_lunar(year, month, day)
    month_branch = GanZhi.get_month(year, month)[1]  # 月支
    day_gz = GanZhi.get_day(year, month, day)
    day_element = GanZhi.get_wuxing(day_gz[0])
    
    time_info = {
        'month_branch': month_branch,
        'day_element': day_element,
        'lunar_month': lunar_info['month'],
        'lunar_day': lunar_info['day']
    }
    
    enhancer = LiuyaoEnhanced()
    return enhancer.enhance_liuyao_result(basic_result, time_info)

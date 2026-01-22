"""
奇门遁甲服务入口
整合计算器和分析器，提供统一的奇门服务接口
参考 mingpan 的 QimenService.ts 实现

修复记录：
- 2026-01: 使用 lunar_python 精确计算节气，修复局数判断问题
"""
from typing import Dict, Optional, List
from datetime import datetime
import logging

from lunar_python import Solar

from .calculators.jushu import JuShuCalculator
from .calculators.jiugong import JiuGongCalculator
from .calculators.sanqi import SanQiLiuYiCalculator
from .analyzers.geju import GeJuAnalyzer
from .analyzers.shensha import ShenShaAnalyzer

_logger = logging.getLogger(__name__)


class QimenService:
    """奇门遁甲服务类"""
    
    # 八门原始宫位
    BA_MEN_GONG = {
        '休': 1, '生': 8, '伤': 3, '杜': 4,
        '景': 9, '死': 2, '惊': 7, '开': 6
    }
    
    # 九星原始宫位
    JIU_XING_GONG = {
        '蓬': 1, '芮': 2, '冲': 3, '辅': 4,
        '禽': 5, '心': 6, '柱': 7, '任': 8, '英': 9
    }
    
    def __init__(self):
        """初始化服务"""
        self.jushu_calc = JuShuCalculator
        self.jiugong_calc = JiuGongCalculator
        self.sanqi_calc = SanQiLiuYiCalculator
        self.geju_analyzer = GeJuAnalyzer
        self.shensha_analyzer = ShenShaAnalyzer
    
    def paipan(self, year: int, month: int, day: int, hour: int,
               minute: int = 0, pan_style: str = '时盘',
               pan_type: str = '转盘') -> Dict:
        """排盘
        
        Args:
            year, month, day, hour, minute: 时间
            pan_style: 盘式（时盘/日盘/月盘/年盘）
            pan_type: 盘型（转盘/飞盘）
            
        Returns:
            完整的奇门盘信息
        """
        # 1. 获取干支（优先使用 lunar_python 精确计算）
        ganzhi_data = self._get_ganzhi_by_lunar(year, month, day, hour)
        
        if ganzhi_data:
            year_gz = ganzhi_data['year']
            month_gz = ganzhi_data['month']
            day_gz = ganzhi_data['day']
            hour_gz = ganzhi_data['hour']
        else:
            # 回退到简化计算
            year_gz = self._get_year_ganzhi(year)
            month_gz = self._get_month_ganzhi(year, month)
            day_gz = self._get_day_ganzhi(year, month, day)
            hour_gz = self._get_hour_ganzhi(day_gz, hour)
        
        # 2. 获取节气和三元
        jieqi = self._get_jieqi(year, month, day)
        yuan = self.jushu_calc.get_yuan(day_gz)
        
        # 3. 计算局数
        ju_shu, is_yang = self.jushu_calc.calculate(jieqi, yuan)
        
        # 4. 计算地盘
        di_pan = self.sanqi_calc.calculate_di_pan(ju_shu, is_yang)
        
        # 5. 计算天盘
        ref_gz = hour_gz if pan_style == '时盘' else day_gz
        tian_pan = self.sanqi_calc.calculate_tian_pan(di_pan, ref_gz, is_yang)
        
        # 6. 计算旬首和值符
        xun_shou = self.sanqi_calc.get_xun_shou(ref_gz)
        liu_yi = self.sanqi_calc.XUN_SHOU_LIU_YI.get(xun_shou, '戊')
        
        # 值符星原始宫位
        di_pan_reverse = {v: k for k, v in di_pan.items()}
        zhi_fu_gong = di_pan_reverse.get(liu_yi, 1)
        
        # 7. 计算八门九星八神
        hour_num = (hour + 1) // 2 % 12
        ba_men = self._calculate_ba_men(zhi_fu_gong, hour_num, is_yang)
        jiu_xing = self._calculate_jiu_xing(zhi_fu_gong, hour_num, is_yang)
        ba_shen = self._calculate_ba_shen(zhi_fu_gong, hour_num, is_yang)
        
        # 8. 组装九宫信息
        jiu_gong = self._assemble_jiugong(tian_pan, di_pan, ba_men, jiu_xing, ba_shen)
        
        # 9. 分析格局
        ge_ju = self.geju_analyzer.analyze(tian_pan, di_pan, ba_men, jiu_xing)
        
        return {
            'datetime': f"{year}-{month:02d}-{day:02d} {hour:02d}:{minute:02d}",
            'pan_style': pan_style,
            'pan_type': pan_type,
            'ju_shu': ju_shu,
            'is_yang': is_yang,
            'yuan': yuan,
            'jieqi': jieqi,
            'year_gz': year_gz,
            'month_gz': month_gz,
            'day_gz': day_gz,
            'hour_gz': hour_gz,
            'xun_shou': {
                'xun_shou': xun_shou,
                'liu_yi': liu_yi,
                'xun_kong': self._get_xun_kong(xun_shou)
            },
            'zhi_fu_gong': zhi_fu_gong,
            'tian_pan': tian_pan,
            'di_pan': di_pan,
            'ba_men': ba_men,
            'jiu_xing': jiu_xing,
            'ba_shen': ba_shen,
            'jiu_gong': jiu_gong,
            'ge_ju': ge_ju
        }
    
    def _get_ganzhi_by_lunar(self, year: int, month: int, day: int, hour: int = 12) -> Dict[str, str]:
        """使用 lunar_python 获取精确的四柱干支
        
        Args:
            year, month, day, hour: 公历日期时间
            
        Returns:
            包含年、月、日、时干支的字典
        """
        try:
            solar = Solar.fromYmdHms(year, month, day, hour, 0, 0)
            lunar = solar.getLunar()
            bazi = lunar.getEightChar()
            
            return {
                'year': bazi.getYear(),
                'month': bazi.getMonth(),
                'day': bazi.getDay(),
                'hour': bazi.getTime()
            }
        except Exception as e:
            _logger.warning(f"lunar_python 干支计算失败: {e}")
            return None
    
    def _get_year_ganzhi(self, year: int) -> str:
        """获取年干支（简化计算）"""
        idx = (year - 4) % 60
        tiangan = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']
        dizhi = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']
        return tiangan[idx % 10] + dizhi[idx % 12]
    
    def _get_month_ganzhi(self, year: int, month: int) -> str:
        """获取月干支（简化计算，建议使用 _get_ganzhi_by_lunar）"""
        tiangan = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']
        dizhi = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']
        year_gan_idx = (year - 4) % 10
        base_gan_idx = (year_gan_idx % 5) * 2 + 2
        gan_idx = (base_gan_idx + month - 1) % 10
        zhi_idx = (month + 1) % 12
        return tiangan[gan_idx] + dizhi[zhi_idx]
    
    def _get_day_ganzhi(self, year: int, month: int, day: int) -> str:
        """获取日干支（简化计算）"""
        from datetime import date
        tiangan = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']
        dizhi = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']
        base_date = date(1900, 1, 31)
        target_date = date(year, month, day)
        diff = (target_date - base_date).days
        idx = diff % 60
        return tiangan[idx % 10] + dizhi[idx % 12]
    
    def _get_hour_ganzhi(self, day_gz: str, hour: int) -> str:
        """获取时干支"""
        tiangan = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']
        dizhi = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']
        day_gan_idx = tiangan.index(day_gz[0]) if day_gz[0] in tiangan else 0
        shichen_idx = (hour + 1) // 2 % 12
        base_gan_idx = (day_gan_idx % 5) * 2
        gan_idx = (base_gan_idx + shichen_idx) % 10
        return tiangan[gan_idx] + dizhi[shichen_idx]
    
    def _get_jieqi(self, year: int, month: int, day: int) -> str:
        """获取当前日期所在的节气
        
        使用 lunar_python 精确计算节气，奇门遁甲用"节"不用"气"：
        - 节：立春、惊蛰、清明、立夏、芒种、小暑、立秋、白露、寒露、立冬、大雪、小寒
        - 气：雨水、春分、谷雨、小满、夏至、大暑、处暑、秋分、霜降、小雪、冬至、大寒
        
        Returns:
            当前所在的节气名称
        """
        try:
            solar = Solar.fromYmd(year, month, day)
            lunar = solar.getLunar()
            
            # 获取上一个节（不是气）
            prev_jie = lunar.getPrevJie()
            if prev_jie:
                jie_name = prev_jie.getName()
                _logger.debug(f"日期 {year}-{month}-{day} 所在节气: {jie_name}")
                return jie_name
            
            # 如果没有找到，尝试获取当前节气
            current_jieqi = lunar.getJieQi()
            if current_jieqi:
                return current_jieqi
            
            # 回退到简化计算
            return self._get_jieqi_fallback(month, day)
            
        except Exception as e:
            _logger.warning(f"lunar_python 节气计算失败，回退到简化算法: {e}")
            return self._get_jieqi_fallback(month, day)
    
    def _get_jieqi_fallback(self, month: int, day: int) -> str:
        """节气简化计算（回退方案）
        
        根据月份和日期大致判断节气
        注意：这是近似计算，可能有1-2天偏差
        """
        # 24节气对应的大致日期（每月两个节气）
        # 格式: (月份, 日期界限, 节气名)
        jieqi_boundaries = [
            (1, 6, '小寒'), (1, 20, '大寒'),
            (2, 4, '立春'), (2, 19, '雨水'),
            (3, 6, '惊蛰'), (3, 21, '春分'),
            (4, 5, '清明'), (4, 20, '谷雨'),
            (5, 6, '立夏'), (5, 21, '小满'),
            (6, 6, '芒种'), (6, 21, '夏至'),
            (7, 7, '小暑'), (7, 23, '大暑'),
            (8, 7, '立秋'), (8, 23, '处暑'),
            (9, 8, '白露'), (9, 23, '秋分'),
            (10, 8, '寒露'), (10, 23, '霜降'),
            (11, 7, '立冬'), (11, 22, '小雪'),
            (12, 7, '大雪'), (12, 22, '冬至'),
        ]
        
        # 奇门遁甲只用"节"，过滤掉"气"
        jie_names = {'立春', '惊蛰', '清明', '立夏', '芒种', '小暑', 
                     '立秋', '白露', '寒露', '立冬', '大雪', '小寒'}
        
        # 查找当前日期所在的节气
        current_jieqi = '立春'  # 默认值
        for m, d, name in jieqi_boundaries:
            if month > m or (month == m and day >= d):
                if name in jie_names:
                    current_jieqi = name
        
        return current_jieqi
    
    def _get_xun_kong(self, xun_shou: str) -> List[str]:
        """获取旬空"""
        xun_kong_map = {
            '甲子': ['戌', '亥'], '甲戌': ['申', '酉'],
            '甲申': ['午', '未'], '甲午': ['辰', '巳'],
            '甲辰': ['寅', '卯'], '甲寅': ['子', '丑']
        }
        return xun_kong_map.get(xun_shou, ['戌', '亥'])
    
    def _calculate_ba_men(self, zhi_fu_gong: int, hour_num: int, is_yang: bool) -> Dict[int, str]:
        """计算八门布局"""
        ba_men = ['休', '生', '伤', '杜', '景', '死', '惊', '开']
        gong_men = {}
        
        zhi_shi_men = self._get_men_by_gong(zhi_fu_gong)
        zhi_shi_men_idx = ba_men.index(zhi_shi_men) if zhi_shi_men in ba_men else 0
        zhi_shi_luo_gong = self.jiugong_calc.rotate(zhi_fu_gong, hour_num, is_yang)
        
        for i in range(8):
            men_idx = (zhi_shi_men_idx + i) % 8
            men = ba_men[men_idx]
            gong = self.jiugong_calc.rotate(zhi_shi_luo_gong, i, is_yang)
            gong_men[gong] = men
        
        gong_men[5] = gong_men.get(self.jiugong_calc.ZHONG_GONG_JI, '死')
        return gong_men
    
    def _calculate_jiu_xing(self, zhi_fu_gong: int, hour_num: int, is_yang: bool) -> Dict[int, str]:
        """计算九星布局"""
        xing_order = ['蓬', '任', '冲', '辅', '英', '芮', '柱', '心']
        gong_xing = {}
        
        zhi_fu_xing = self._get_xing_by_gong(zhi_fu_gong)
        xing_idx = xing_order.index(zhi_fu_xing) if zhi_fu_xing in xing_order else 0
        zhi_fu_luo_gong = self.jiugong_calc.rotate(zhi_fu_gong, hour_num, is_yang)
        
        for i in range(8):
            idx = (xing_idx + i) % 8
            xing = xing_order[idx]
            gong = self.jiugong_calc.rotate(zhi_fu_luo_gong, i, is_yang)
            gong_xing[gong] = xing
        
        gong_xing[5] = '禽'
        return gong_xing
    
    def _calculate_ba_shen(self, zhi_fu_gong: int, hour_num: int, is_yang: bool) -> Dict[int, str]:
        """计算八神布局"""
        ba_shen = ['值符', '腾蛇', '太阴', '六合', '白虎', '玄武', '九地', '九天']
        gong_shen = {}
        
        zhi_fu_luo_gong = self.jiugong_calc.rotate(zhi_fu_gong, hour_num, is_yang)
        
        for i in range(8):
            shen = ba_shen[i]
            gong = self.jiugong_calc.rotate(zhi_fu_luo_gong, i, is_yang)
            gong_shen[gong] = shen
        
        gong_shen[5] = gong_shen.get(self.jiugong_calc.ZHONG_GONG_JI, '值符')
        return gong_shen
    
    def _get_men_by_gong(self, gong: int) -> str:
        """根据宫位获取对应的门"""
        gong_men = {1: '休', 2: '死', 3: '伤', 4: '杜', 6: '开', 7: '惊', 8: '生', 9: '景'}
        return gong_men.get(gong, '休')
    
    def _get_xing_by_gong(self, gong: int) -> str:
        """根据宫位获取对应的星"""
        gong_xing = {1: '蓬', 2: '芮', 3: '冲', 4: '辅', 6: '心', 7: '柱', 8: '任', 9: '英'}
        return gong_xing.get(gong, '蓬')
    
    def _assemble_jiugong(self, tian_pan: Dict, di_pan: Dict, 
                          ba_men: Dict, jiu_xing: Dict, ba_shen: Dict) -> List[Dict]:
        """组装九宫信息"""
        jiu_gong = []
        gong_names = {
            1: '坎一宫', 2: '坤二宫', 3: '震三宫', 4: '巽四宫',
            5: '中五宫', 6: '乾六宫', 7: '兑七宫', 8: '艮八宫', 9: '离九宫'
        }
        gong_wuxing = {
            1: '水', 2: '土', 3: '木', 4: '木',
            5: '土', 6: '金', 7: '金', 8: '土', 9: '火'
        }
        
        for gong in range(1, 10):
            jiu_gong.append({
                'gong': gong,
                'gong_name': gong_names.get(gong, ''),
                'tian_gan': tian_pan.get(gong, ''),
                'di_gan': di_pan.get(gong, ''),
                'men': ba_men.get(gong, ''),
                'xing': jiu_xing.get(gong, ''),
                'shen': ba_shen.get(gong, ''),
                'wuxing': gong_wuxing.get(gong, '')
            })
        
        return jiu_gong


# 便捷函数
def qimen_paipan(year: int, month: int, day: int, hour: int,
                 minute: int = 0, pan_style: str = '时盘',
                 pan_type: str = '转盘') -> Dict:
    """快速排盘"""
    service = QimenService()
    return service.paipan(year, month, day, hour, minute, pan_style, pan_type)

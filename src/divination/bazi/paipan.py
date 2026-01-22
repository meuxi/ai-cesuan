"""
八字排盘核心算法
转换自 cls_paipan.php
增加十神分析功能
"""
from typing import Dict, List
from datetime import datetime, timedelta
import os
from lunar_python import Solar, Lunar
from .ganzhi import GanZhi
from .shishen import TenGodsAnalyzer


class BaziPaipan:
    """八字排盘类"""
    
    # 六十甲子纳音表
    NAYIN_TABLE = {
        '甲子': '海中金', '乙丑': '海中金',
        '丙寅': '炉中火', '丁卯': '炉中火',
        '戊辰': '大林木', '己巳': '大林木',
        '庚午': '路旁土', '辛未': '路旁土',
        '壬申': '剑锋金', '癸酉': '剑锋金',
        '甲戌': '山头火', '乙亥': '山头火',
        '丙子': '涧下水', '丁丑': '涧下水',
        '戊寅': '城头土', '己卯': '城头土',
        '庚辰': '白腊金', '辛巳': '白腊金',
        '壬午': '杨柳木', '癸未': '杨柳木',
        '甲申': '泉中水', '乙酉': '泉中水',
        '丙戌': '屋上土', '丁亥': '屋上土',
        '戊子': '霹雳火', '己丑': '霹雳火',
        '庚寅': '松柏木', '辛卯': '松柏木',
        '壬辰': '长流水', '癸巳': '长流水',
        '甲午': '砂石金', '乙未': '砂石金',
        '丙申': '山下火', '丁酉': '山下火',
        '戊戌': '平地木', '己亥': '平地木',
        '庚子': '壁上土', '辛丑': '壁上土',
        '壬寅': '金薄金', '癸卯': '金薄金',
        '甲辰': '覆灯火', '乙巳': '覆灯火',
        '丙午': '天河水', '丁未': '天河水',
        '戊申': '大驿土', '己酉': '大驿土',
        '庚戌': '钗环金', '辛亥': '钗环金',
        '壬子': '桑柘木', '癸丑': '桑柘木',
        '甲寅': '大溪水', '乙卯': '大溪水',
        '丙辰': '沙中土', '丁巳': '沙中土',
        '戊午': '天上火', '己未': '天上火',
        '庚申': '石榴木', '辛酉': '石榴木',
        '壬戌': '大海水', '癸亥': '大海水'
    }
    
    # 地支藏干表
    DIZHI_CANG = {
        '子': ['癸'],
        '丑': ['己', '癸', '辛'],
        '寅': ['甲', '丙', '戊'],
        '卯': ['乙'],
        '辰': ['戊', '乙', '癸'],
        '巳': ['丙', '戊', '庚'],
        '午': ['丁', '己'],
        '未': ['己', '丁', '乙'],
        '申': ['庚', '壬', '戊'],
        '酉': ['辛'],
        '戌': ['戊', '辛', '丁'],
        '亥': ['壬', '甲']
    }
    
    # 旬空表
    XUNKONG_TABLE = [
        ['甲子', '乙丑', '丙寅', '丁卯', '戊辰', '己巳', 
         '庚午', '辛未', '壬申', '癸酉', '戌亥'],
        ['甲戌', '乙亥', '丙子', '丁丑', '戊寅', '己卯', 
         '庚辰', '辛巳', '壬午', '癸未', '申酉'],
        ['甲申', '乙酉', '丙戌', '丁亥', '戊子', '己丑', 
         '庚寅', '辛卯', '壬辰', '癸巳', '午未'],
        ['甲午', '乙未', '丙申', '丁酉', '戊戌', '己亥', 
         '庚子', '辛丑', '壬寅', '癸卯', '辰巳'],
        ['甲辰', '乙巳', '丙午', '丁未', '戊申', '己酉', 
         '庚戌', '辛亥', '壬子', '癸丑', '寅卯'],
        ['甲寅', '乙卯', '丙辰', '丁巳', '戊午', '己未', 
         '庚申', '辛酉', '壬戌', '癸亥', '子丑']
    ]
    
    def __init__(self):
        """初始化"""
        self.gz = GanZhi()
        self.stime_data = self._load_stime_data()
        self.shishen_analyzer = TenGodsAnalyzer()
    
    def _load_stime_data(self) -> Dict:
        """加载真太阳时数据"""
        data = {}
        stime_path = os.path.join(
            os.path.dirname(__file__),
            '../data/stime.txt'
        )
        
        try:
            with open(stime_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    parts = line.replace(':', ' ').split()
                    if len(parts) >= 4:
                        m, d, minute, second = parts[0], parts[1], parts[2], parts[3]
                        key = f"{m}:{d}"
                        data[key] = (int(minute), int(second))
        except FileNotFoundError:
            pass
        
        return data
    
    def get_true_solar_time(self, dt: datetime, longitude: float, 
                            latitude: float = 0) -> datetime:
        """计算真太阳时
        
        Args:
            dt: 当地时间
            longitude: 经度（东经为正）
            latitude: 纬度
            
        Returns:
            真太阳时
        """
        # 1. 时区修正（东经120度为标准）
        zone_offset = (longitude - 120) * 4  # 分钟
        
        # 2. 均时差修正
        key = f"{dt.month}:{dt.day}"
        if key in self.stime_data:
            minute, second = self.stime_data[key]
            if minute < 0:
                eq_time = -(abs(minute) * 60 + second)
            else:
                eq_time = minute * 60 + second
        else:
            eq_time = 0
        
        # 3. 计算真太阳时
        total_seconds = zone_offset * 60 + eq_time
        true_time = dt + timedelta(seconds=total_seconds)
        
        return true_time
    
    def get_nayin(self, ganzhi: str) -> str:
        """获取纳音
        
        Args:
            ganzhi: 干支组合
            
        Returns:
            纳音
        """
        return self.NAYIN_TABLE.get(ganzhi, '')
    
    def get_dizhi_cang(self, dizhi: str) -> List[str]:
        """获取地支藏干
        
        Args:
            dizhi: 地支
            
        Returns:
            藏干列表
        """
        return self.DIZHI_CANG.get(dizhi, [])
    
    def get_xunkong(self, ganzhi: str) -> str:
        """计算旬空
        
        Args:
            ganzhi: 干支
            
        Returns:
            空亡地支
        """
        for xun in self.XUNKONG_TABLE:
            if ganzhi in xun:
                return xun[-1]
        return ''
    
    def get_minggong(self, month_dz_idx: int, hour_dz_idx: int,
                      year_tg_idx: int) -> str:
        """计算命宫
        
        Args:
            month_dz_idx: 月支索引(0-11)
            hour_dz_idx: 时支索引(0-11)
            year_tg_idx: 年干索引(0-9)
            
        Returns:
            命宫干支
        """
        # 命宫地支 = 26 - 月支 - 时支
        ming_dz = (26 - month_dz_idx - hour_dz_idx - 1) % 12
        
        # 命宫天干 = 年干*2 + 命宫地支
        ming_tg = (year_tg_idx * 2 + ming_dz) % 10
        
        return GanZhi.TIANGAN[ming_tg] + GanZhi.DIZHI[ming_dz]
    
    def get_taiyuan(self, month_tg_idx: int, month_dz_idx: int) -> str:
        """计算胎元
        
        Args:
            month_tg_idx: 月干索引
            month_dz_idx: 月支索引
            
        Returns:
            胎元干支
        """
        tai_tg = (month_tg_idx + 1) % 10
        tai_dz = (month_dz_idx + 3) % 12
        
        return GanZhi.TIANGAN[tai_tg] + GanZhi.DIZHI[tai_dz]
    
    def paipan(self, birth_info: dict, use_true_solar: bool = False) -> Dict:
        """完整八字排盘
        
        Args:
            birth_info: {
                'year': 年,
                'month': 月,
                'day': 日,
                'hour': 时,
                'minute': 分(可选),
                'longitude': 经度(可选),
                'latitude': 纬度(可选)
            }
            use_true_solar: 是否使用真太阳时
            
        Returns:
            完整排盘结果
        """
        # 提取信息
        year = birth_info['year']
        month = birth_info['month']
        day = birth_info['day']
        hour = birth_info['hour']
        minute = birth_info.get('minute', 0)
        
        # 真太阳时处理
        if use_true_solar and 'longitude' in birth_info:
            dt = datetime(year, month, day, hour, minute)
            true_dt = self.get_true_solar_time(
                dt, 
                birth_info['longitude'],
                birth_info.get('latitude', 0)
            )
            hour = true_dt.hour
            minute = true_dt.minute
        
        # 使用lunar_python库获取正确的八字四柱（基于节气划分）
        solar = Solar.fromYmdHms(year, month, day, hour, minute, 0)
        lunar = solar.getLunar()
        bazi_obj = lunar.getEightChar()
        
        # 提取各柱
        year_gz = bazi_obj.getYear()
        month_gz = bazi_obj.getMonth()
        day_gz = bazi_obj.getDay()
        hour_gz = bazi_obj.getTime()
        
        bazi = {
            'year': year_gz,
            'month': month_gz,
            'day': day_gz,
            'hour': hour_gz,
            'full': f"{year_gz} {month_gz} {day_gz} {hour_gz}"
        }
        
        # 计算附加信息
        result = {
            'sizhu': bazi,
            'nayin': {
                'year': self.get_nayin(year_gz),
                'month': self.get_nayin(month_gz),
                'day': self.get_nayin(day_gz),
                'hour': self.get_nayin(hour_gz)
            },
            'xunkong': {
                'year': self.get_xunkong(year_gz),
                'month': self.get_xunkong(month_gz),
                'day': self.get_xunkong(day_gz),
                'hour': self.get_xunkong(hour_gz)
            },
            'dizhi_cang': {
                'year': self.get_dizhi_cang(year_gz[1]),
                'month': self.get_dizhi_cang(month_gz[1]),
                'day': self.get_dizhi_cang(day_gz[1]),
                'hour': self.get_dizhi_cang(hour_gz[1])
            }
        }
        
        # 添加十神分析
        try:
            shishen_result = self.shishen_analyzer.analyze_chart(result)
            result['shishen'] = shishen_result
        except Exception as e:
            result['shishen'] = {'error': str(e)}
        
        return result

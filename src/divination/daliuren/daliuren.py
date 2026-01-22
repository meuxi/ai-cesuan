"""
大六壬排盘核心算法
三式之首，包含天地盘、四课、三传、十二天将、神煞
"""
from typing import Dict, List, Optional, Tuple
from datetime import datetime
from lunar_python import Lunar, Solar


class DaliurenPaipan:
    """大六壬排盘类"""
    
    # 天干
    TIANGAN = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']
    
    # 地支
    DIZHI = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']
    
    # 十二天将
    TIAN_JIANG = ['贵人', '腾蛇', '朱雀', '六合', '勾陈', '青龙', 
                  '天空', '白虎', '太常', '玄武', '太阴', '天后']
    
    # 地支对应的天将（从贵人起）
    # 日干为阳干时，从丑起贵人；日干为阴干时，从未起贵人
    GUIREN_YANG = {  # 阳干贵人位置
        '甲': '丑', '丙': '亥', '戊': '丑', '庚': '丑', '壬': '巳'
    }
    
    GUIREN_YIN = {  # 阴干贵人位置
        '乙': '子', '丁': '亥', '己': '子', '辛': '午', '癸': '巳'
    }
    
    # 地支五行
    DIZHI_WUXING = {
        '子': '水', '丑': '土', '寅': '木', '卯': '木',
        '辰': '土', '巳': '火', '午': '火', '未': '土',
        '申': '金', '酉': '金', '戌': '土', '亥': '水'
    }
    
    # 地支方位
    DIZHI_FANGWEI = {
        '子': '北', '丑': '东北', '寅': '东北', '卯': '东',
        '辰': '东南', '巳': '东南', '午': '南', '未': '西南',
        '申': '西南', '酉': '西', '戌': '西北', '亥': '西北'
    }
    
    def __init__(self):
        """初始化"""
        pass
    
    def get_guiren_position(self, day_gan: str) -> str:
        """获取贵人位置
        
        Args:
            day_gan: 日干
            
        Returns:
            贵人所在地支
        """
        # 阳干用阳贵人，阴干用阴贵人
        yang_gan = ['甲', '丙', '戊', '庚', '壬']
        
        if day_gan in yang_gan:
            return self.GUIREN_YANG.get(day_gan, '丑')
        else:
            return self.GUIREN_YIN.get(day_gan, '子')
    
    def get_tianpan(self, month_zhi: str, day_zhi: str) -> Dict[str, str]:
        """获取天盘（月将加时）
        
        Args:
            month_zhi: 月支
            day_zhi: 日支
            
        Returns:
            天盘映射 {地支: 天盘地支}
        """
        # 月将（正月建寅）
        yue_jiang_idx = self.DIZHI.index(month_zhi)
        
        # 从卯位起月将
        mao_idx = 3  # 卯的索引
        
        tianpan = {}
        for i in range(12):
            di_zhi = self.DIZHI[i]
            # 计算天盘对应的地支
            offset = (yue_jiang_idx - mao_idx + i) % 12
            tian_zhi = self.DIZHI[offset]
            tianpan[di_zhi] = tian_zhi
        
        return tianpan
    
    def get_sike(self, day_gan: str, day_zhi: str, hour_zhi: str, 
                 tianpan: Dict[str, str]) -> List[Dict]:
        """获取四课
        
        Args:
            day_gan: 日干
            day_zhi: 日支
            hour_zhi: 时支
            tianpan: 天盘
            
        Returns:
            四课列表
        """
        sike = []
        
        # 一课：日干寄宫的地盘（初课）
        # 日干寄宫规则
        gan_gong = {
            '甲': '寅', '乙': '卯', '丙': '巳', '丁': '午', '戊': '巳',
            '己': '午', '庚': '申', '辛': '酉', '壬': '亥', '癸': '子'
        }
        
        yi_ke_di = gan_gong.get(day_gan, '子')
        yi_ke_tian = tianpan.get(yi_ke_di, yi_ke_di)
        
        sike.append({
            'name': '一课（初课）',
            'di': yi_ke_di,
            'tian': yi_ke_tian,
            'description': f'日干{day_gan}寄{yi_ke_di}宫'
        })
        
        # 二课：一课的天盘地支对应的天盘（二课）
        er_ke_di = yi_ke_tian
        er_ke_tian = tianpan.get(er_ke_di, er_ke_di)
        
        sike.append({
            'name': '二课',
            'di': er_ke_di,
            'tian': er_ke_tian,
            'description': f'一课天盘{yi_ke_tian}之上'
        })
        
        # 三课：日支的地盘（三课）
        san_ke_di = day_zhi
        san_ke_tian = tianpan.get(san_ke_di, san_ke_di)
        
        sike.append({
            'name': '三课',
            'di': san_ke_di,
            'tian': san_ke_tian,
            'description': f'日支{day_zhi}之上'
        })
        
        # 四课：三课的天盘地支对应的天盘（四课）
        si_ke_di = san_ke_tian
        si_ke_tian = tianpan.get(si_ke_di, si_ke_di)
        
        sike.append({
            'name': '四课（末课）',
            'di': si_ke_di,
            'tian': si_ke_tian,
            'description': f'三课天盘{san_ke_tian}之上'
        })
        
        return sike
    
    def get_sanchuan(self, sike: List[Dict], day_gan: str) -> List[Dict]:
        """获取三传
        
        Args:
            sike: 四课
            day_gan: 日干
            
        Returns:
            三传列表（初传、中传、末传）
        """
        # 简化算法：取四课中不重复的三个
        # 实际算法需要根据发用规则（贼克、比用、涉害等）
        
        sanchuan = []
        seen = set()
        
        for ke in sike:
            tian = ke['tian']
            if tian not in seen:
                seen.add(tian)
                chuan_name = ''
                if len(sanchuan) == 0:
                    chuan_name = '初传'
                elif len(sanchuan) == 1:
                    chuan_name = '中传'
                elif len(sanchuan) == 2:
                    chuan_name = '末传'
                
                if chuan_name:
                    sanchuan.append({
                        'name': chuan_name,
                        'zhi': tian,
                        'wuxing': self.DIZHI_WUXING.get(tian, ''),
                        'fangwei': self.DIZHI_FANGWEI.get(tian, '')
                    })
                
                if len(sanchuan) >= 3:
                    break
        
        # 如果不足三个，补充
        while len(sanchuan) < 3:
            sanchuan.append({
                'name': f'第{len(sanchuan)+1}传',
                'zhi': '子',
                'wuxing': '水',
                'fangwei': '北'
            })
        
        return sanchuan[:3]
    
    def get_tianjiang(self, hour_zhi: str, day_gan: str) -> List[Dict]:
        """获取十二天将
        
        Args:
            hour_zhi: 时支
            day_gan: 日干
            
        Returns:
            十二天将列表
        """
        # 从贵人位置起天将
        guiren_pos = self.get_guiren_position(day_gan)
        guiren_idx = self.DIZHI.index(guiren_pos)
        
        # 判断顺逆（白天顺行，夜晚逆行）
        # 简化：阳干顺行，阴干逆行
        yang_gan = ['甲', '丙', '戊', '庚', '壬']
        shun_xing = day_gan in yang_gan
        
        tianjiang = []
        for i in range(12):
            if shun_xing:
                zhi_idx = (guiren_idx + i) % 12
            else:
                zhi_idx = (guiren_idx - i) % 12
            
            zhi = self.DIZHI[zhi_idx]
            jiang = self.TIAN_JIANG[i]
            
            tianjiang.append({
                'zhi': zhi,
                'jiang': jiang,
                'wuxing': self.DIZHI_WUXING.get(zhi, ''),
                'fangwei': self.DIZHI_FANGWEI.get(zhi, '')
            })
        
        return tianjiang
    
    def paipan(self, year: int, month: int, day: int, hour: int,
               minute: int = 0) -> Dict:
        """大六壬排盘
        
        Args:
            year, month, day, hour, minute: 起盘时间
            
        Returns:
            排盘结果
        """
        # 1. 获取干支
        solar = Solar.fromYmd(year, month, day)
        lunar = solar.getLunar()
        
        year_gz = lunar.getYearInGanZhi()
        month_gz = lunar.getMonthInGanZhi()
        day_gz = lunar.getDayInGanZhi()
        
        # 时辰
        shi_chen_idx = (hour + 1) // 2 % 12
        hour_zhi = self.DIZHI[shi_chen_idx]
        
        # 日干日支
        day_gan = day_gz[0]
        day_zhi = day_gz[1]
        
        # 月支
        month_zhi = month_gz[1]
        
        # 2. 天地盘
        tianpan = self.get_tianpan(month_zhi, day_zhi)
        
        # 3. 四课
        sike = self.get_sike(day_gan, day_zhi, hour_zhi, tianpan)
        
        # 4. 三传
        sanchuan = self.get_sanchuan(sike, day_gan)
        
        # 5. 十二天将
        tianjiang = self.get_tianjiang(hour_zhi, day_gan)
        
        # 6. 组装结果
        result = {
            'time_info': {
                'solar_date': f"{year}年{month}月{day}日{hour}时",
                'lunar_date': f"{lunar.getYearInChinese()}年{lunar.getMonthInChinese()}{lunar.getDayInChinese()}",
                'sizhu': {
                    'year': year_gz,
                    'month': month_gz,
                    'day': day_gz,
                    'hour': f'{day_gan}{hour_zhi}'  # 时干需要从日干推算
                },
                'jie_qi': lunar.getJieQi() or lunar.getPrevJieQi().getName()
            },
            'tianpan': tianpan,
            'sike': sike,
            'sanchuan': sanchuan,
            'tianjiang': tianjiang,
            'summary': f"起盘时间：{year}年{month}月{day}日{hour}时，日干{day_gan}，月将{month_zhi}"
        }
        
        return result


# 便捷函数
def daliuren_paipan(year: int, month: int, day: int, hour: int,
                    minute: int = 0) -> Dict:
    """快速大六壬排盘
    
    Args:
        year, month, day, hour, minute: 起盘时间
        
    Returns:
        排盘结果
    """
    paipan = DaliurenPaipan()
    return paipan.paipan(year, month, day, hour, minute)

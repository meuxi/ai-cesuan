"""
奇门遁甲排盘核心算法
支持时盘/日盘排盘、转盘/飞盘、九宫布局、八门九星八神、格局计算
参考mingpan专业实现
"""
from typing import Dict, List, Optional, Tuple
from datetime import datetime
from lunar_python import Lunar, Solar


class QimenPaipan:
    """奇门遁甲排盘类（增强版）"""
    
    # 天干
    TIANGAN = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']
    
    # 地支
    DIZHI = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']
    
    # 三奇六仪（按布局顺序）
    SAN_QI_LIU_YI = ['戊', '己', '庚', '辛', '壬', '癸', '丁', '丙', '乙']
    
    # 八门（按布局顺序）
    BA_MEN = ['休', '生', '伤', '杜', '景', '死', '惊', '开']
    BA_MEN_FULL = ['休门', '生门', '伤门', '杜门', '景门', '死门', '惊门', '开门']
    
    # 八门原始宫位（休门在坎1，生门在艮8...）
    BA_MEN_GONG = {'休': 1, '生': 8, '伤': 3, '杜': 4, '景': 9, '死': 2, '惊': 7, '开': 6}
    
    # 九星（按布局顺序）
    JIU_XING = ['蓬', '任', '冲', '辅', '英', '芮', '柱', '心', '禽']
    JIU_XING_FULL = ['天蓬', '天任', '天冲', '天辅', '天英', '天芮', '天柱', '天心', '天禽']
    
    # 九星原始宫位
    JIU_XING_GONG = {'蓬': 1, '任': 8, '冲': 3, '辅': 4, '英': 9, '芮': 2, '柱': 7, '心': 6, '禽': 5}
    
    # 八神（按布局顺序）
    BA_SHEN = ['符', '蛇', '阴', '合', '虎', '武', '地', '天']
    BA_SHEN_FULL = ['值符', '腾蛇', '太阴', '六合', '白虎', '玄武', '九地', '九天']
    
    # 九宫位置名称
    GONG_NAMES = ['坎一宫', '坤二宫', '震三宫', '巽四宫', '中五宫', '乾六宫', '兑七宫', '艮八宫', '离九宫']
    GONG_NAMES_SHORT = ['坎', '坤', '震', '巽', '中', '乾', '兑', '艮', '离']
    
    # 九宫五行
    GONG_WUXING = {
        1: '水', 2: '土', 3: '木', 4: '木', 5: '土', 6: '金', 7: '金', 8: '土', 9: '火',
        '坎一宫': '水', '坤二宫': '土', '震三宫': '木',
        '巽四宫': '木', '中五宫': '土', '乾六宫': '金',
        '兑七宫': '金', '艮八宫': '土', '离九宫': '火'
    }
    
    # 旬首与六仪对应
    XUN_SHOU_LIU_YI = {
        '甲子': '戊', '甲戌': '己', '甲申': '庚',
        '甲午': '辛', '甲辰': '壬', '甲寅': '癸'
    }
    
    # 转盘式物理方向旋转顺序（顺时针：1→8→3→4→9→2→7→6）
    ZHUAN_PAN_CLOCKWISE = [1, 8, 3, 4, 9, 2, 7, 6]
    # 逆时针：1→6→7→2→9→4→3→8
    ZHUAN_PAN_COUNTER_CLOCKWISE = [1, 6, 7, 2, 9, 4, 3, 8]
    
    # 宫位对冲映射
    CHONG_GONG_MAP = {1: 9, 2: 8, 3: 7, 4: 6, 6: 4, 7: 3, 8: 2, 9: 1}
    
    # 天干相合
    GAN_HE_MAP = {'甲': '己', '乙': '庚', '丙': '辛', '丁': '壬', '戊': '癸',
                  '己': '甲', '庚': '乙', '辛': '丙', '壬': '丁', '癸': '戊'}
    
    # 中宫寄坤二
    ZHONG_GONG_JI = 2
    
    # 阳遁局数（冬至后、夏至前）
    YANG_JU = {
        '冬至': [1, 7, 4, 1, 7, 4, 1, 7, 4],
        '小寒': [2, 8, 5, 2, 8, 5, 2, 8, 5],
        '大寒': [3, 9, 6, 3, 9, 6, 3, 9, 6],
        '立春': [4, 1, 7, 4, 1, 7, 4, 1, 7],
        '雨水': [5, 2, 8, 5, 2, 8, 5, 2, 8],
        '惊蛰': [6, 3, 9, 6, 3, 9, 6, 3, 9],
        '春分': [7, 4, 1, 7, 4, 1, 7, 4, 1],
        '清明': [8, 5, 2, 8, 5, 2, 8, 5, 2],
        '谷雨': [9, 6, 3, 9, 6, 3, 9, 6, 3],
        '立夏': [1, 7, 4, 1, 7, 4, 1, 7, 4],
        '小满': [2, 8, 5, 2, 8, 5, 2, 8, 5],
        '芒种': [3, 9, 6, 3, 9, 6, 3, 9, 6],
    }
    
    # 阴遁局数（夏至后、冬至前）
    YIN_JU = {
        '夏至': [9, 3, 6, 9, 3, 6, 9, 3, 6],
        '小暑': [8, 2, 5, 8, 2, 5, 8, 2, 5],
        '大暑': [7, 1, 4, 7, 1, 4, 7, 1, 4],
        '立秋': [6, 9, 3, 6, 9, 3, 6, 9, 3],
        '处暑': [5, 8, 2, 5, 8, 2, 5, 8, 2],
        '白露': [4, 7, 1, 4, 7, 1, 4, 7, 1],
        '秋分': [3, 6, 9, 3, 6, 9, 3, 6, 9],
        '寒露': [2, 5, 8, 2, 5, 8, 2, 5, 8],
        '霜降': [1, 4, 7, 1, 4, 7, 1, 4, 7],
        '立冬': [9, 3, 6, 9, 3, 6, 9, 3, 6],
        '小雪': [8, 2, 5, 8, 2, 5, 8, 2, 5],
        '大雪': [7, 1, 4, 7, 1, 4, 7, 1, 4],
    }
    
    def __init__(self):
        """初始化"""
        self.pan_style = '转盘'  # 转盘/飞盘
    
    def get_jie_qi(self, year: int, month: int, day: int) -> str:
        """获取当前节气
        
        Args:
            year: 年份
            month: 月份
            day: 日期
            
        Returns:
            节气名称
        """
        solar = Solar.fromYmd(year, month, day)
        lunar = solar.getLunar()
        jie_qi = lunar.getJieQi()
        
        if jie_qi:
            return jie_qi
        
        # 如果当天不是节气，找最近的前一个节气
        jie_qi_table = lunar.getJieQiTable()
        current_date = solar.toYmd()
        
        latest_jq = '立春'
        for jq_name, jq_solar in jie_qi_table.items():
            if jq_solar.toYmd() <= current_date:
                latest_jq = jq_name
        
        return latest_jq
    
    def get_ju_shu(self, year: int, month: int, day: int, hour: int) -> Tuple[int, str]:
        """获取局数
        
        Args:
            year, month, day, hour: 起盘时间
            
        Returns:
            (局数, 阴阳遁)
        """
        jie_qi = self.get_jie_qi(year, month, day)
        
        # 判断阴遁还是阳遁（简化：冬至到夏至为阳遁，夏至到冬至为阴遁）
        yang_jie_qi = ['冬至', '小寒', '大寒', '立春', '雨水', '惊蛰', '春分', '清明', '谷雨', '立夏', '小满', '芒种']
        
        if jie_qi in yang_jie_qi:
            dun_type = '阳遁'
            ju_list = self.YANG_JU.get(jie_qi, [1, 7, 4, 1, 7, 4, 1, 7, 4])
        else:
            dun_type = '阴遁'
            ju_list = self.YIN_JU.get(jie_qi, [9, 3, 6, 9, 3, 6, 9, 3, 6])
        
        # 根据日期确定上中下元
        solar = Solar.fromYmd(year, month, day)
        lunar = solar.getLunar()
        day_num = lunar.getDay()
        
        if day_num <= 5:
            yuan_idx = 0  # 上元
        elif day_num <= 10:
            yuan_idx = 1
        elif day_num <= 15:
            yuan_idx = 2  # 中元
        elif day_num <= 20:
            yuan_idx = 3
        elif day_num <= 25:
            yuan_idx = 4
        else:
            yuan_idx = 5  # 下元
        
        ju_shu = ju_list[yuan_idx % len(ju_list)]
        
        return ju_shu, dun_type
    
    def get_shi_gan(self, year: int, month: int, day: int, hour: int) -> str:
        """获取时干
        
        Args:
            year, month, day, hour: 时间
            
        Returns:
            时干
        """
        # 获取日干
        solar = Solar.fromYmd(year, month, day)
        lunar = solar.getLunar()
        day_gan_zhi = lunar.getDayInGanZhi()
        day_gan = day_gan_zhi[0]
        
        # 时干起法：日上起时
        day_gan_idx = self.TIANGAN.index(day_gan)
        
        # 时辰索引（子时=0）
        shi_chen_idx = (hour + 1) // 2 % 12
        
        # 时干计算口诀
        shi_gan_start = {
            0: 0, 1: 2, 2: 4, 3: 6, 4: 8,  # 甲己日
            5: 0, 6: 2, 7: 4, 8: 6, 9: 8   # 对应规律
        }
        
        base = shi_gan_start.get(day_gan_idx % 5, 0)
        shi_gan_idx = (base + shi_chen_idx * 2) % 10
        
        return self.TIANGAN[shi_gan_idx]
    
    def paipan(self, year: int, month: int, day: int, hour: int,
               minute: int = 0, pan_type: str = '时盘', 
               pan_style: str = '转盘') -> Dict:
        """奇门遁甲排盘（增强版）
        
        Args:
            year, month, day, hour, minute: 起盘时间
            pan_type: 盘类型（时盘/日盘/月盘/年盘）
            pan_style: 盘式（转盘/飞盘）
            
        Returns:
            排盘结果
        """
        self.pan_style = pan_style
        
        # 1. 获取局数
        ju_shu, dun_type = self.get_ju_shu(year, month, day, hour)
        is_yang = dun_type == '阳遁'
        
        # 2. 获取四柱干支
        solar = Solar.fromYmd(year, month, day)
        lunar = solar.getLunar()
        
        year_gz = lunar.getYearInGanZhi()
        month_gz = lunar.getMonthInGanZhi()
        day_gz = lunar.getDayInGanZhi()
        
        # 时辰
        shi_chen_idx = (hour + 1) // 2 % 12
        shi_zhi = self.DIZHI[shi_chen_idx]
        shi_gan = self.get_shi_gan(year, month, day, hour)
        hour_gz = shi_gan + shi_zhi
        
        # 根据盘类型选择参考干支
        if pan_type == '时盘':
            ref_gz = hour_gz
        elif pan_type == '日盘':
            ref_gz = day_gz
        elif pan_type == '月盘':
            ref_gz = month_gz
        elif pan_type == '年盘':
            ref_gz = year_gz
        else:
            ref_gz = hour_gz  # 默认时盘
        
        # 3. 计算旬首信息
        xun_shou = self._get_xun_shou(ref_gz)
        liu_yi_gan = self.XUN_SHOU_LIU_YI.get(xun_shou, '戊')
        
        # 4. 计算地盘布局
        di_pan = self._calculate_di_pan(ju_shu, is_yang)
        
        # 5. 计算天盘布局
        tian_pan = self._calculate_tian_pan(di_pan, ref_gz, is_yang)
        
        # 6. 计算八门布局
        zhi_fu_gong = di_pan['gan_gong'].get(liu_yi_gan, 1)
        if zhi_fu_gong == 5:
            zhi_fu_gong = self.ZHONG_GONG_JI
        ba_men = self._calculate_ba_men(zhi_fu_gong, shi_chen_idx, is_yang)
        
        # 7. 计算九星布局
        jiu_xing = self._calculate_jiu_xing(zhi_fu_gong, shi_chen_idx, is_yang)
        
        # 8. 计算八神布局
        ba_shen = self._calculate_ba_shen(zhi_fu_gong, is_yang)
        
        # 9. 组装九宫信息
        jiugong = self._assemble_jiugong(di_pan, tian_pan, ba_men, jiu_xing, ba_shen)
        
        # 10. 计算格局
        ge_ju = self._calculate_ge_ju(jiugong, day_gz[0], hour_gz[0], is_yang)
        
        # 基本信息
        jie_qi = self.get_jie_qi(year, month, day)
        
        result = {
            'time_info': {
                'solar_date': f"{year}年{month}月{day}日{hour}时",
                'lunar_date': f"{lunar.getYearInChinese()}年{lunar.getMonthInChinese()}{lunar.getDayInChinese()}",
                'sizhu': {
                    'year': year_gz,
                    'month': month_gz,
                    'day': day_gz,
                    'hour': hour_gz
                },
                'jie_qi': jie_qi
            },
            'pan_info': {
                'pan_type': pan_type,
                'pan_style': pan_style,
                'ju_shu': ju_shu,
                'dun_type': dun_type,
                'xun_shou': xun_shou,
                'zhi_fu_gan': liu_yi_gan,
                'description': f"{dun_type}{ju_shu}局（{pan_style}）"
            },
            'jiugong': jiugong,
            'ge_ju': ge_ju,
            'summary': f"起盘时间：{year}年{month}月{day}日{hour}时，{jie_qi}，{dun_type}{ju_shu}局"
        }
        
        return result
    
    def _get_xun_shou(self, gan_zhi: str) -> str:
        """获取旬首"""
        if len(gan_zhi) < 2:
            return '甲子'
        gan = gan_zhi[0]
        zhi = gan_zhi[1]
        gan_idx = self.TIANGAN.index(gan) if gan in self.TIANGAN else 0
        zhi_idx = self.DIZHI.index(zhi) if zhi in self.DIZHI else 0
        
        # 旬首计算：地支索引 - 天干索引（取模12）
        xun_zhi_idx = (zhi_idx - gan_idx) % 12
        xun_shou_map = {0: '甲子', 2: '甲寅', 4: '甲辰', 6: '甲午', 8: '甲申', 10: '甲戌'}
        return xun_shou_map.get(xun_zhi_idx, '甲子')
    
    def _calculate_di_pan(self, ju_shu: int, is_yang: bool) -> Dict:
        """计算地盘布局"""
        gong_gan = {}  # 宫位 -> 天干
        gan_gong = {}  # 天干 -> 宫位
        
        # 从局数对应的宫位开始布三奇六仪
        start_gong = ju_shu
        
        for i, gan in enumerate(self.SAN_QI_LIU_YI):
            gong = self._rotate_gong(start_gong, i, is_yang)
            gong_gan[gong] = gan
            gan_gong[gan] = gong
        
        return {'gong_gan': gong_gan, 'gan_gong': gan_gong}
    
    def _calculate_tian_pan(self, di_pan: Dict, ref_gz: str, is_yang: bool) -> Dict:
        """计算天盘布局"""
        gong_gan = {}
        gan_gong = {}
        
        # 获取参考干对应的遁甲干
        ref_gan = ref_gz[0] if ref_gz else '戊'
        if ref_gan == '甲':
            xun_shou = self._get_xun_shou(ref_gz)
            ref_gan = self.XUN_SHOU_LIU_YI.get(xun_shou, '戊')
        
        # 找到参考干在地盘的位置
        start_gong = di_pan['gan_gong'].get(ref_gan, 1)
        if start_gong == 5:
            start_gong = self.ZHONG_GONG_JI
        
        # 转盘式：整体旋转
        for i, gan in enumerate(self.SAN_QI_LIU_YI):
            gong = self._rotate_gong(start_gong, i, is_yang)
            gong_gan[gong] = gan
            gan_gong[gan] = gong
        
        return {'gong_gan': gong_gan, 'gan_gong': gan_gong}
    
    def _calculate_ba_men(self, zhi_fu_gong: int, hour_num: int, is_yang: bool) -> Dict:
        """计算八门布局"""
        gong_men = {}
        
        # 值使门 = 值符星原始宫位对应的门
        zhi_shi_men = self._get_men_by_gong(zhi_fu_gong)
        zhi_shi_men_idx = self.BA_MEN.index(zhi_shi_men) if zhi_shi_men in self.BA_MEN else 0
        
        # 值使门落宫 = 从值符宫起旋转时辰数
        zhi_shi_luo_gong = self._rotate_gong(zhi_fu_gong, hour_num, is_yang)
        
        # 布八门
        for i in range(8):
            men_idx = (zhi_shi_men_idx + i) % 8
            men = self.BA_MEN[men_idx]
            gong = self._rotate_gong(zhi_shi_luo_gong, i, is_yang)
            gong_men[gong] = men
        
        # 中宫继承坤二
        gong_men[5] = gong_men.get(self.ZHONG_GONG_JI, '死')
        
        return gong_men
    
    def _calculate_jiu_xing(self, zhi_fu_gong: int, hour_num: int, is_yang: bool) -> Dict:
        """计算九星布局"""
        gong_xing = {}
        
        # 值符星 = 旬首遁干地盘宫位对应的星
        zhi_fu_xing = self._get_xing_by_gong(zhi_fu_gong)
        xing_order = ['蓬', '任', '冲', '辅', '英', '芮', '柱', '心']  # 不含天禽
        zhi_fu_xing_idx = xing_order.index(zhi_fu_xing) if zhi_fu_xing in xing_order else 0
        
        # 值符星落宫
        zhi_fu_luo_gong = self._rotate_gong(zhi_fu_gong, hour_num, is_yang)
        
        # 布九星
        for i in range(8):
            xing_idx = (zhi_fu_xing_idx + i) % 8
            xing = xing_order[xing_idx]
            gong = self._rotate_gong(zhi_fu_luo_gong, i, is_yang)
            gong_xing[gong] = xing
        
        # 天禽寄中宫
        gong_xing[5] = '禽'
        
        return gong_xing
    
    def _calculate_ba_shen(self, zhi_fu_gong: int, is_yang: bool) -> Dict:
        """计算八神布局"""
        gong_shen = {}
        
        # 值符始终在值符宫
        start_gong = zhi_fu_gong if zhi_fu_gong != 5 else self.ZHONG_GONG_JI
        
        # 布八神
        for i, shen in enumerate(self.BA_SHEN):
            gong = self._rotate_gong(start_gong, i, is_yang)
            gong_shen[gong] = shen
        
        gong_shen[5] = gong_shen.get(self.ZHONG_GONG_JI, '符')
        
        return gong_shen
    
    def _rotate_gong(self, start: int, steps: int, is_yang: bool) -> int:
        """转盘式宫位旋转"""
        if start == 5:
            start = self.ZHONG_GONG_JI
        
        # 第5步到中宫
        if steps == 4:
            return 5
        
        adjusted_steps = steps - 1 if steps > 4 else steps
        
        order = self.ZHUAN_PAN_CLOCKWISE if is_yang else self.ZHUAN_PAN_COUNTER_CLOCKWISE
        try:
            start_idx = order.index(start)
        except ValueError:
            start_idx = 0
        
        result_idx = (start_idx + adjusted_steps) % 8
        return order[result_idx]
    
    def _get_men_by_gong(self, gong: int) -> str:
        """根据宫位获取原始门"""
        actual_gong = gong if gong != 5 else self.ZHONG_GONG_JI
        for men, men_gong in self.BA_MEN_GONG.items():
            if men_gong == actual_gong:
                return men
        return '死'
    
    def _get_xing_by_gong(self, gong: int) -> str:
        """根据宫位获取原始星"""
        if gong == 5:
            return '禽'
        for xing, xing_gong in self.JIU_XING_GONG.items():
            if xing_gong == gong:
                return xing
        return '芮'
    
    def _assemble_jiugong(self, di_pan: Dict, tian_pan: Dict, ba_men: Dict, 
                          jiu_xing: Dict, ba_shen: Dict) -> List[Dict]:
        """组装九宫信息"""
        jiugong = []
        for i in range(9):
            gong = i + 1
            gong_name = self.GONG_NAMES[i]
            
            gong_info = {
                'position': gong,
                'gong_name': gong_name,
                'gong_wuxing': self.GONG_WUXING.get(gong_name, '土'),
                'di_pan_gan': di_pan['gong_gan'].get(gong, '戊'),
                'tian_pan_gan': tian_pan['gong_gan'].get(gong, '戊'),
                'ba_men': self.BA_MEN_FULL[self.BA_MEN.index(ba_men.get(gong, '死'))] if ba_men.get(gong) in self.BA_MEN else '死门',
                'jiu_xing': self.JIU_XING_FULL[self.JIU_XING.index(jiu_xing.get(gong, '芮'))] if jiu_xing.get(gong) in self.JIU_XING else '天芮',
                'ba_shen': self.BA_SHEN_FULL[self.BA_SHEN.index(ba_shen.get(gong, '符'))] if ba_shen.get(gong) in self.BA_SHEN else '值符'
            }
            
            jiugong.append(gong_info)
        
        return jiugong
    
    def _calculate_ge_ju(self, jiugong: List[Dict], day_gan: str, hour_gan: str, 
                          is_yang: bool) -> List[Dict]:
        """计算格局（参考mingpan的GeJuCalculator）"""
        ge_ju_list = []
        
        san_qi = ['乙', '丙', '丁']
        ji_men = ['开门', '休门', '生门']
        xiong_men = ['死门', '惊门', '杜门']
        
        for gong in jiugong:
            tian_gan = gong['tian_pan_gan']
            di_gan = gong['di_pan_gan']
            men = gong['ba_men']
            xing = gong['jiu_xing']
            shen = gong['ba_shen']
            gong_name = gong['gong_name']
            
            # 三奇得使
            if tian_gan in san_qi and men in ji_men:
                ge_ju_list.append({
                    'name': '三奇得使',
                    'type': '吉格',
                    'description': f"{tian_gan}奇临{men}于{gong_name}",
                    'gong': gong_name
                })
            
            # 三奇得门（精确配对）
            qi_men_pair = {'乙': '开门', '丙': '生门', '丁': '休门'}
            if tian_gan in qi_men_pair and men == qi_men_pair[tian_gan]:
                ge_ju_list.append({
                    'name': '三奇得门',
                    'type': '吉格',
                    'description': f"{tian_gan}奇得{men}于{gong_name}",
                    'gong': gong_name
                })
            
            # 九遁格局
            # 天遁：丙+生门+天心
            if tian_gan == '丙' and men == '生门' and xing == '天心':
                ge_ju_list.append({
                    'name': '天遁',
                    'type': '吉格',
                    'description': f"丙奇临生门天心于{gong_name}",
                    'gong': gong_name
                })
            
            # 地遁：乙+开门+地盘己
            if tian_gan == '乙' and men == '开门' and di_gan == '己':
                ge_ju_list.append({
                    'name': '地遁',
                    'type': '吉格',
                    'description': f"乙奇临开门遇地盘己于{gong_name}",
                    'gong': gong_name
                })
            
            # 人遁：丁+休门+太阴
            if tian_gan == '丁' and men == '休门' and shen == '太阴':
                ge_ju_list.append({
                    'name': '人遁',
                    'type': '吉格',
                    'description': f"丁奇临休门遇太阴于{gong_name}",
                    'gong': gong_name
                })
            
            # 神遁：丙+生门+九天
            if tian_gan == '丙' and men == '生门' and shen == '九天':
                ge_ju_list.append({
                    'name': '神遁',
                    'type': '吉格',
                    'description': f"丙奇临生门遇九天于{gong_name}",
                    'gong': gong_name
                })
            
            # 鬼遁：乙+生门+九地
            if tian_gan == '乙' and men == '生门' and shen == '九地':
                ge_ju_list.append({
                    'name': '鬼遁',
                    'type': '吉格',
                    'description': f"乙奇临生门遇九地于{gong_name}",
                    'gong': gong_name
                })
            
            # 龙遁：乙+休门+六合
            if tian_gan == '乙' and men == '休门' and shen == '六合':
                ge_ju_list.append({
                    'name': '龙遁',
                    'type': '吉格',
                    'description': f"乙奇临休门遇六合于{gong_name}",
                    'gong': gong_name
                })
            
            # 虎遁：乙+开门+太阴
            if tian_gan == '乙' and men == '开门' and shen == '太阴':
                ge_ju_list.append({
                    'name': '虎遁',
                    'type': '吉格',
                    'description': f"乙奇临开门遇太阴于{gong_name}",
                    'gong': gong_name
                })
            
            # 凶格：白虎猖狂
            if tian_gan == '庚' and men == '开门' and shen == '白虎':
                ge_ju_list.append({
                    'name': '白虎猖狂',
                    'type': '凶格',
                    'description': f"庚临开门遇白虎于{gong_name}",
                    'gong': gong_name
                })
            
            # 天牢：庚+杜门
            if tian_gan == '庚' and men == '杜门':
                ge_ju_list.append({
                    'name': '天牢',
                    'type': '凶格',
                    'description': f"庚临杜门于{gong_name}，主阻滞闭塞",
                    'gong': gong_name
                })
            
            # 奇仪相合
            if tian_gan in self.GAN_HE_MAP and self.GAN_HE_MAP[tian_gan] == di_gan:
                ge_ju_list.append({
                    'name': f"{tian_gan}{di_gan}合",
                    'type': '吉格',
                    'description': f"{tian_gan}与{di_gan}相合于{gong_name}",
                    'gong': gong_name
                })
            
            # 伏吟：天地盘干相同
            if tian_gan == di_gan:
                ge_ju_list.append({
                    'name': '伏吟',
                    'type': '中性',
                    'description': f"天地盘{tian_gan}同位于{gong_name}",
                    'gong': gong_name
                })
        
        # 五不遇时：时干克日干
        wu_bu_yu_map = {'甲': '庚', '乙': '辛', '丙': '壬', '丁': '癸',
                        '戊': '甲', '己': '乙', '庚': '丙', '辛': '丁',
                        '壬': '戊', '癸': '己'}
        if wu_bu_yu_map.get(day_gan) == hour_gan:
            ge_ju_list.append({
                'name': '五不遇时',
                'type': '凶格',
                'description': f"时干{hour_gan}克日干{day_gan}",
                'gong': '全盘'
            })
        
        return ge_ju_list


# 便捷函数
def qimen_paipan(year: int, month: int, day: int, hour: int,
                 minute: int = 0, pan_type: str = '时盘',
                 pan_style: str = '转盘') -> Dict:
    """快速奇门遁甲排盘
    
    Args:
        year, month, day, hour, minute: 起盘时间
        pan_type: 盘类型（时盘/日盘）
        pan_style: 盘式（转盘/飞盘）
        
    Returns:
        排盘结果
    """
    paipan = QimenPaipan()
    return paipan.paipan(year, month, day, hour, minute, pan_type, pan_style)

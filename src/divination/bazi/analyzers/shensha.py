# -*- coding: utf-8 -*-
"""
神煞分析器
来源：mingpan项目 ShenShaAnalyzer.ts
分析八字中的吉星和凶煞（40+种传统神煞）
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass

# 天干
HEAVENLY_STEMS = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']
# 地支
EARTHLY_BRANCHES = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']


@dataclass
class ShenShaInfo:
    """神煞信息"""
    name: str
    type: str  # '吉星' or '凶煞'
    position: str  # 年/月/日/时
    description: str


class ShenShaAnalyzer:
    """神煞分析器"""
    
    @classmethod
    def analyze(cls, bazi: Dict[str, Dict[str, str]], 
                gender: str = 'male') -> List[ShenShaInfo]:
        """
        分析八字神煞
        
        Args:
            bazi: 八字信息 {'year': {'stem': '甲', 'branch': '子'}, ...}
            gender: 性别 'male' or 'female'
        """
        results = []
        
        day_master = bazi['day']['stem']
        day_branch = bazi['day']['branch']
        
        # 贵人类（10种）
        results.extend(cls._check_tianyi(day_master, bazi))      # 天乙贵人
        results.extend(cls._check_taiji(bazi))                   # 太极贵人
        results.extend(cls._check_wenchang(day_master, bazi))    # 文昌贵人
        results.extend(cls._check_tiande(bazi))                  # 天德贵人
        results.extend(cls._check_yuede(bazi))                   # 月德贵人
        results.extend(cls._check_fuxing(day_master, bazi))      # 福星贵人
        
        # 学业事业类（8种）
        results.extend(cls._check_lushen(day_master, bazi))      # 禄神
        results.extend(cls._check_jiangxing(bazi))               # 将星
        results.extend(cls._check_huagai(bazi))                  # 华盖
        results.extend(cls._check_yima(bazi))                    # 驿马
        results.extend(cls._check_tianyi_doctor(day_master, bazi))  # 天医
        
        # 感情类（6种）
        results.extend(cls._check_peach_blossom(day_branch, bazi))  # 桃花
        results.extend(cls._check_hongluan(bazi))                # 红鸾
        results.extend(cls._check_tianxi(bazi))                  # 天喜
        results.extend(cls._check_lonely_stars(bazi, gender))    # 孤辰寡宿
        
        # 财富类（5种）
        results.extend(cls._check_jinshen(day_master, bazi))     # 金神
        results.extend(cls._check_jianlu(day_master, bazi))      # 建禄
        
        # 凶煞类（15种）
        results.extend(cls._check_yangren(day_master, bazi))     # 羊刃
        results.extend(cls._check_jiesha(bazi))                  # 劫煞
        results.extend(cls._check_zaisha(bazi))                  # 灾煞
        results.extend(cls._check_wangshen(bazi))                # 亡神
        results.extend(cls._check_tianku(bazi))                  # 天哭
        results.extend(cls._check_baihu(bazi))                   # 白虎
        results.extend(cls._check_tianluo_diwang(bazi))          # 天罗地网
        results.extend(cls._check_kongwang(bazi))                # 空亡
        
        # 特殊格局（6种）
        results.extend(cls._check_kuigang(bazi))                 # 魁罡
        results.extend(cls._check_ride(bazi))                    # 日德
        
        # 扩展吉星（8种）
        results.extend(cls._check_guoyin(bazi))                  # 国印贵人
        results.extend(cls._check_xuetang(day_master, bazi))     # 学堂
        results.extend(cls._check_ciguang(day_master, bazi))     # 词馆
        results.extend(cls._check_jinyu(day_master, bazi))       # 金舆
        results.extend(cls._check_tianguan(day_master, bazi))    # 天官贵人
        results.extend(cls._check_tianchu(day_master, bazi))     # 天厨贵人
        results.extend(cls._check_tianshe(bazi))                 # 天赦
        results.extend(cls._check_tiandao(bazi))                 # 天德合
        results.extend(cls._check_yuede_he(bazi))                # 月德合
        
        # 扩展凶煞（7种）
        results.extend(cls._check_feilian(bazi))                 # 飞廉
        results.extend(cls._check_dasao(bazi))                   # 大耗
        results.extend(cls._check_dianjiao(bazi))                # 吊客
        results.extend(cls._check_sangmen(bazi))                 # 丧门
        results.extend(cls._check_guanfu(bazi))                  # 官符
        results.extend(cls._check_feixian(day_master, bazi))     # 飞刃
        
        # 补充神煞（基于MingAI参考）
        results.extend(cls._check_yinchayang(bazi))              # 阴差阳错
        results.extend(cls._check_shiedabai(bazi))               # 十恶大败
        results.extend(cls._check_xieren(day_master, bazi))      # 血刃
        results.extend(cls._check_pitou(bazi))                   # 披麻
        results.extend(cls._check_tianyiextra(bazi))             # 天医星
        results.extend(cls._check_sanqi(bazi))                   # 三奇贵人
        results.extend(cls._check_luomawangxiang(bazi))          # 马入天罗地网
        results.extend(cls._check_tongziminggong(bazi, gender))  # 童子命
        
        return results
    
    @classmethod
    def _check_tianyi(cls, day_master: str, bazi: Dict) -> List[ShenShaInfo]:
        """天乙贵人"""
        results = []
        
        tianyi_map = {
            '甲': ['丑', '未'], '戊': ['丑', '未'], '庚': ['丑', '未'],
            '乙': ['子', '申'], '己': ['子', '申'],
            '丙': ['亥', '酉'], '丁': ['亥', '酉'],
            '辛': ['寅', '午'],
            '壬': ['卯', '巳'], '癸': ['卯', '巳']
        }
        
        tianyi_branches = tianyi_map.get(day_master, [])
        positions = [
            ('year', '年支'), ('month', '月支'), 
            ('day', '日支'), ('hour', '时支')
        ]
        
        for key, pos_name in positions:
            if bazi[key]['branch'] in tianyi_branches:
                results.append(ShenShaInfo(
                    name='天乙贵人',
                    type='吉星',
                    position=pos_name,
                    description='天乙贵人，主贵人相助，逢凶化吉。遇难得贵人扶持，宜从事公职或与人合作。'
                ))
        
        return results
    
    @classmethod
    def _check_taiji(cls, bazi: Dict) -> List[ShenShaInfo]:
        """太极贵人"""
        results = []
        
        taiji_combos = [
            ('甲', '子'), ('乙', '午'), ('丙', '卯'), ('丁', '酉'),
            ('戊', '辰'), ('己', '丑'), ('庚', '寅'), ('辛', '亥'),
            ('壬', '申'), ('癸', '巳')
        ]
        
        positions = [
            ('year', '年柱'), ('month', '月柱'),
            ('day', '日柱'), ('hour', '时柱')
        ]
        
        for key, pos_name in positions:
            stem = bazi[key]['stem']
            branch = bazi[key]['branch']
            if (stem, branch) in taiji_combos:
                results.append(ShenShaInfo(
                    name='太极贵人',
                    type='吉星',
                    position=pos_name,
                    description='太极贵人，主聪明好学，悟性高，有研究精神。易得上级赏识，适合学术研究。'
                ))
        
        return results
    
    @classmethod
    def _check_wenchang(cls, day_master: str, bazi: Dict) -> List[ShenShaInfo]:
        """文昌贵人"""
        results = []
        
        wenchang_map = {
            '甲': '巳', '乙': '午', '丙': '申', '丁': '酉',
            '戊': '申', '己': '酉', '庚': '亥', '辛': '子',
            '壬': '寅', '癸': '卯'
        }
        
        wenchang_branch = wenchang_map.get(day_master)
        if not wenchang_branch:
            return results
        
        positions = [
            ('year', '年支'), ('month', '月支'),
            ('day', '日支'), ('hour', '时支')
        ]
        
        for key, pos_name in positions:
            if bazi[key]['branch'] == wenchang_branch:
                results.append(ShenShaInfo(
                    name='文昌贵人',
                    type='吉星',
                    position=pos_name,
                    description='文昌贵人，主聪明智慧，学业有成。利考试、学习、文艺创作。'
                ))
        
        return results
    
    @classmethod
    def _check_tiande(cls, bazi: Dict) -> List[ShenShaInfo]:
        """天德贵人"""
        results = []
        
        tiande_map = {
            '寅': '丁', '卯': '申', '辰': '壬', '巳': '辛',
            '午': '亥', '未': '甲', '申': '癸', '酉': '寅',
            '戌': '丙', '亥': '乙', '子': '巳', '丑': '庚'
        }
        
        month_branch = bazi['month']['branch']
        tiande_stem = tiande_map.get(month_branch)
        
        if tiande_stem:
            for key, pos_name in [('year', '年干'), ('day', '日干'), ('hour', '时干')]:
                if bazi[key]['stem'] == tiande_stem:
                    results.append(ShenShaInfo(
                        name='天德贵人',
                        type='吉星',
                        position=pos_name,
                        description='天德贵人，主逢凶化吉，遇难呈祥。一生少灾难，多贵人帮助。'
                    ))
        
        return results
    
    @classmethod
    def _check_yuede(cls, bazi: Dict) -> List[ShenShaInfo]:
        """月德贵人"""
        results = []
        
        yuede_map = {
            '寅': '丙', '午': '丙', '戌': '丙',
            '申': '壬', '子': '壬', '辰': '壬',
            '亥': '甲', '卯': '甲', '未': '甲',
            '巳': '庚', '酉': '庚', '丑': '庚'
        }
        
        month_branch = bazi['month']['branch']
        yuede_stem = yuede_map.get(month_branch)
        
        if yuede_stem:
            for key, pos_name in [('year', '年干'), ('day', '日干'), ('hour', '时干')]:
                if bazi[key]['stem'] == yuede_stem:
                    results.append(ShenShaInfo(
                        name='月德贵人',
                        type='吉星',
                        position=pos_name,
                        description='月德贵人，主仁慈宽厚，一生平安。逢凶化吉，遇难呈祥。'
                    ))
        
        return results
    
    @classmethod
    def _check_fuxing(cls, day_master: str, bazi: Dict) -> List[ShenShaInfo]:
        """福星贵人"""
        results = []
        
        fuxing_map = {
            '甲': '寅', '乙': '卯', '丙': '巳', '丁': '午',
            '戊': '巳', '己': '午', '庚': '申', '辛': '酉',
            '壬': '亥', '癸': '子'
        }
        
        fuxing_branch = fuxing_map.get(day_master)
        if fuxing_branch:
            for key, pos_name in [('year', '年支'), ('month', '月支'), ('hour', '时支')]:
                if bazi[key]['branch'] == fuxing_branch:
                    results.append(ShenShaInfo(
                        name='福星贵人',
                        type='吉星',
                        position=pos_name,
                        description='福星贵人，主福禄双全，一生多福。衣食无忧，生活安康。'
                    ))
        
        return results
    
    @classmethod
    def _check_lushen(cls, day_master: str, bazi: Dict) -> List[ShenShaInfo]:
        """禄神"""
        results = []
        
        lu_map = {
            '甲': '寅', '乙': '卯', '丙': '巳', '丁': '午',
            '戊': '巳', '己': '午', '庚': '申', '辛': '酉',
            '壬': '亥', '癸': '子'
        }
        
        lu_branch = lu_map.get(day_master)
        if lu_branch:
            for key, pos_name in [('year', '年支'), ('month', '月支'), ('day', '日支'), ('hour', '时支')]:
                if bazi[key]['branch'] == lu_branch:
                    results.append(ShenShaInfo(
                        name='禄神',
                        type='吉星',
                        position=pos_name,
                        description='禄神，主衣食无忧，财禄丰厚。一生不愁吃穿，生活优裕。'
                    ))
        
        return results
    
    @classmethod
    def _check_jiangxing(cls, bazi: Dict) -> List[ShenShaInfo]:
        """将星"""
        results = []
        
        jiangxing_map = {
            '寅': '午', '午': '午', '戌': '午',
            '申': '子', '子': '子', '辰': '子',
            '亥': '卯', '卯': '卯', '未': '卯',
            '巳': '酉', '酉': '酉', '丑': '酉'
        }
        
        year_branch = bazi['year']['branch']
        jiangxing = jiangxing_map.get(year_branch)
        
        if jiangxing:
            for key, pos_name in [('month', '月支'), ('day', '日支'), ('hour', '时支')]:
                if bazi[key]['branch'] == jiangxing:
                    results.append(ShenShaInfo(
                        name='将星',
                        type='吉星',
                        position=pos_name,
                        description='将星，主权威显赫，领导才能出众。适合从军、从政或管理职位。'
                    ))
        
        return results
    
    @classmethod
    def _check_huagai(cls, bazi: Dict) -> List[ShenShaInfo]:
        """华盖"""
        results = []
        
        huagai_map = {
            '寅': '戌', '午': '戌', '戌': '戌',
            '申': '辰', '子': '辰', '辰': '辰',
            '亥': '未', '卯': '未', '未': '未',
            '巳': '丑', '酉': '丑', '丑': '丑'
        }
        
        year_branch = bazi['year']['branch']
        huagai = huagai_map.get(year_branch)
        
        if huagai:
            for key, pos_name in [('month', '月支'), ('day', '日支'), ('hour', '时支')]:
                if bazi[key]['branch'] == huagai:
                    results.append(ShenShaInfo(
                        name='华盖',
                        type='吉星',
                        position=pos_name,
                        description='华盖，主聪明孤高，艺术天赋。适合文艺、宗教、哲学研究。'
                    ))
        
        return results
    
    @classmethod
    def _check_yima(cls, bazi: Dict) -> List[ShenShaInfo]:
        """驿马"""
        results = []
        
        yima_map = {
            '寅': '申', '午': '申', '戌': '申',
            '申': '寅', '子': '寅', '辰': '寅',
            '亥': '巳', '卯': '巳', '未': '巳',
            '巳': '亥', '酉': '亥', '丑': '亥'
        }
        
        year_branch = bazi['year']['branch']
        yima = yima_map.get(year_branch)
        
        if yima:
            for key, pos_name in [('month', '月支'), ('day', '日支'), ('hour', '时支')]:
                if bazi[key]['branch'] == yima:
                    results.append(ShenShaInfo(
                        name='驿马',
                        type='吉星',
                        position=pos_name,
                        description='驿马，主奔波劳碌，适合出行。利外出发展、贸易、交通相关事业。'
                    ))
        
        return results
    
    @classmethod
    def _check_tianyi_doctor(cls, day_master: str, bazi: Dict) -> List[ShenShaInfo]:
        """天医"""
        results = []
        
        tianyi_map = {
            '甲': '酉', '乙': '申', '丙': '亥', '丁': '戌',
            '戊': '丑', '己': '子', '庚': '卯', '辛': '寅',
            '壬': '巳', '癸': '辰'
        }
        
        tianyi = tianyi_map.get(day_master)
        if tianyi:
            for key, pos_name in [('year', '年支'), ('month', '月支'), ('hour', '时支')]:
                if bazi[key]['branch'] == tianyi:
                    results.append(ShenShaInfo(
                        name='天医',
                        type='吉星',
                        position=pos_name,
                        description='天医，主医药天赋，身体健康。适合从事医疗、养生相关行业。'
                    ))
        
        return results
    
    @classmethod
    def _check_peach_blossom(cls, day_branch: str, bazi: Dict) -> List[ShenShaInfo]:
        """桃花"""
        results = []
        
        taohua_map = {
            '寅': '卯', '午': '卯', '戌': '卯',
            '申': '酉', '子': '酉', '辰': '酉',
            '亥': '子', '卯': '子', '未': '子',
            '巳': '午', '酉': '午', '丑': '午'
        }
        
        taohua = taohua_map.get(day_branch)
        if taohua:
            for key, pos_name in [('year', '年支'), ('month', '月支'), ('hour', '时支')]:
                if bazi[key]['branch'] == taohua:
                    results.append(ShenShaInfo(
                        name='桃花',
                        type='吉星',
                        position=pos_name,
                        description='桃花，主人缘好，异性缘佳。感情丰富，魅力出众。'
                    ))
        
        return results
    
    @classmethod
    def _check_hongluan(cls, bazi: Dict) -> List[ShenShaInfo]:
        """红鸾"""
        results = []
        
        hongluan_map = {
            '子': '卯', '丑': '寅', '寅': '丑', '卯': '子',
            '辰': '亥', '巳': '戌', '午': '酉', '未': '申',
            '申': '未', '酉': '午', '戌': '巳', '亥': '辰'
        }
        
        year_branch = bazi['year']['branch']
        hongluan = hongluan_map.get(year_branch)
        
        if hongluan:
            for key, pos_name in [('month', '月支'), ('day', '日支'), ('hour', '时支')]:
                if bazi[key]['branch'] == hongluan:
                    results.append(ShenShaInfo(
                        name='红鸾',
                        type='吉星',
                        position=pos_name,
                        description='红鸾，主喜事临门，婚姻美满。利婚嫁、添丁、喜庆之事。'
                    ))
        
        return results
    
    @classmethod
    def _check_tianxi(cls, bazi: Dict) -> List[ShenShaInfo]:
        """天喜"""
        results = []
        
        tianxi_map = {
            '子': '酉', '丑': '申', '寅': '未', '卯': '午',
            '辰': '巳', '巳': '辰', '午': '卯', '未': '寅',
            '申': '丑', '酉': '子', '戌': '亥', '亥': '戌'
        }
        
        year_branch = bazi['year']['branch']
        tianxi = tianxi_map.get(year_branch)
        
        if tianxi:
            for key, pos_name in [('month', '月支'), ('day', '日支'), ('hour', '时支')]:
                if bazi[key]['branch'] == tianxi:
                    results.append(ShenShaInfo(
                        name='天喜',
                        type='吉星',
                        position=pos_name,
                        description='天喜，主喜庆吉利，心情愉悦。利婚嫁、生子等喜事。'
                    ))
        
        return results
    
    @classmethod
    def _check_lonely_stars(cls, bazi: Dict, gender: str) -> List[ShenShaInfo]:
        """孤辰寡宿"""
        results = []
        
        guchen_map = {
            '寅': '巳', '卯': '巳', '辰': '巳',
            '巳': '申', '午': '申', '未': '申',
            '申': '亥', '酉': '亥', '戌': '亥',
            '亥': '寅', '子': '寅', '丑': '寅'
        }
        
        guasu_map = {
            '寅': '丑', '卯': '丑', '辰': '丑',
            '巳': '辰', '午': '辰', '未': '辰',
            '申': '未', '酉': '未', '戌': '未',
            '亥': '戌', '子': '戌', '丑': '戌'
        }
        
        year_branch = bazi['year']['branch']
        
        if gender == 'male':
            guchen = guchen_map.get(year_branch)
            if guchen:
                for key, pos_name in [('month', '月支'), ('day', '日支'), ('hour', '时支')]:
                    if bazi[key]['branch'] == guchen:
                        results.append(ShenShaInfo(
                            name='孤辰',
                            type='凶煞',
                            position=pos_name,
                            description='孤辰，主孤独寂寞，性格孤僻。婚姻感情易有波折。'
                        ))
        else:
            guasu = guasu_map.get(year_branch)
            if guasu:
                for key, pos_name in [('month', '月支'), ('day', '日支'), ('hour', '时支')]:
                    if bazi[key]['branch'] == guasu:
                        results.append(ShenShaInfo(
                            name='寡宿',
                            type='凶煞',
                            position=pos_name,
                            description='寡宿，主孤独寂寞，缘分薄。婚姻感情易有波折。'
                        ))
        
        return results
    
    @classmethod
    def _check_jinshen(cls, day_master: str, bazi: Dict) -> List[ShenShaInfo]:
        """金神"""
        results = []
        
        # 金神: 己巳、己丑、己酉、癸酉四柱
        jinshen_combos = [('己', '巳'), ('己', '丑'), ('己', '酉'), ('癸', '酉')]
        
        for key, pos_name in [('year', '年柱'), ('month', '月柱'), ('day', '日柱'), ('hour', '时柱')]:
            stem = bazi[key]['stem']
            branch = bazi[key]['branch']
            if (stem, branch) in jinshen_combos:
                results.append(ShenShaInfo(
                    name='金神',
                    type='吉星',
                    position=pos_name,
                    description='金神，主刚毅果断，意志坚强。适合从事需要决断力的工作。'
                ))
        
        return results
    
    @classmethod
    def _check_jianlu(cls, day_master: str, bazi: Dict) -> List[ShenShaInfo]:
        """建禄"""
        results = []
        
        jianlu_map = {
            '甲': '寅', '乙': '卯', '丙': '巳', '丁': '午',
            '戊': '巳', '己': '午', '庚': '申', '辛': '酉',
            '壬': '亥', '癸': '子'
        }
        
        jianlu = jianlu_map.get(day_master)
        if jianlu and bazi['month']['branch'] == jianlu:
            results.append(ShenShaInfo(
                name='建禄',
                type='吉星',
                position='月支',
                description='建禄格，主自力更生，独立自主。不靠祖业，凭自己努力成功。'
            ))
        
        return results
    
    @classmethod
    def _check_yangren(cls, day_master: str, bazi: Dict) -> List[ShenShaInfo]:
        """羊刃"""
        results = []
        
        yangren_map = {
            '甲': '卯', '乙': '寅', '丙': '午', '丁': '巳',
            '戊': '午', '己': '巳', '庚': '酉', '辛': '申',
            '壬': '子', '癸': '亥'
        }
        
        yangren = yangren_map.get(day_master)
        if yangren:
            for key, pos_name in [('year', '年支'), ('month', '月支'), ('day', '日支'), ('hour', '时支')]:
                if bazi[key]['branch'] == yangren:
                    results.append(ShenShaInfo(
                        name='羊刃',
                        type='凶煞',
                        position=pos_name,
                        description='羊刃，主刚烈冲动，易有血光之灾。性格刚强，宜用文化修养化解。'
                    ))
        
        return results
    
    @classmethod
    def _check_jiesha(cls, bazi: Dict) -> List[ShenShaInfo]:
        """劫煞"""
        results = []
        
        jiesha_map = {
            '寅': '巳', '午': '巳', '戌': '巳',
            '申': '亥', '子': '亥', '辰': '亥',
            '亥': '申', '卯': '申', '未': '申',
            '巳': '寅', '酉': '寅', '丑': '寅'
        }
        
        year_branch = bazi['year']['branch']
        jiesha = jiesha_map.get(year_branch)
        
        if jiesha:
            for key, pos_name in [('month', '月支'), ('day', '日支'), ('hour', '时支')]:
                if bazi[key]['branch'] == jiesha:
                    results.append(ShenShaInfo(
                        name='劫煞',
                        type='凶煞',
                        position=pos_name,
                        description='劫煞，主易遭抢劫、盗窃。出行需谨慎，保管好财物。'
                    ))
        
        return results
    
    @classmethod
    def _check_zaisha(cls, bazi: Dict) -> List[ShenShaInfo]:
        """灾煞"""
        results = []
        
        zaisha_map = {
            '寅': '午', '午': '午', '戌': '午',
            '申': '子', '子': '子', '辰': '子',
            '亥': '酉', '卯': '酉', '未': '酉',
            '巳': '卯', '酉': '卯', '丑': '卯'
        }
        
        year_branch = bazi['year']['branch']
        zaisha = zaisha_map.get(year_branch)
        
        if zaisha:
            for key, pos_name in [('month', '月支'), ('day', '日支'), ('hour', '时支')]:
                if bazi[key]['branch'] == zaisha:
                    results.append(ShenShaInfo(
                        name='灾煞',
                        type='凶煞',
                        position=pos_name,
                        description='灾煞，主易遭天灾人祸。注意安全，谨慎行事。'
                    ))
        
        return results
    
    @classmethod
    def _check_wangshen(cls, bazi: Dict) -> List[ShenShaInfo]:
        """亡神"""
        results = []
        
        wangshen_map = {
            '寅': '亥', '午': '亥', '戌': '亥',
            '申': '巳', '子': '巳', '辰': '巳',
            '亥': '寅', '卯': '寅', '未': '寅',
            '巳': '申', '酉': '申', '丑': '申'
        }
        
        year_branch = bazi['year']['branch']
        wangshen = wangshen_map.get(year_branch)
        
        if wangshen:
            for key, pos_name in [('month', '月支'), ('day', '日支'), ('hour', '时支')]:
                if bazi[key]['branch'] == wangshen:
                    results.append(ShenShaInfo(
                        name='亡神',
                        type='凶煞',
                        position=pos_name,
                        description='亡神，主精神恍惚，易有失误。做事需专心，避免疏忽。'
                    ))
        
        return results
    
    @classmethod
    def _check_tianku(cls, bazi: Dict) -> List[ShenShaInfo]:
        """天哭"""
        results = []
        
        tianku_map = {
            '子': '午', '丑': '未', '寅': '申', '卯': '酉',
            '辰': '戌', '巳': '亥', '午': '子', '未': '丑',
            '申': '寅', '酉': '卯', '戌': '辰', '亥': '巳'
        }
        
        year_branch = bazi['year']['branch']
        tianku = tianku_map.get(year_branch)
        
        if tianku:
            for key, pos_name in [('month', '月支'), ('day', '日支'), ('hour', '时支')]:
                if bazi[key]['branch'] == tianku:
                    results.append(ShenShaInfo(
                        name='天哭',
                        type='凶煞',
                        position=pos_name,
                        description='天哭，主哭泣悲伤之事。情绪敏感，易有忧郁倾向。'
                    ))
        
        return results
    
    @classmethod
    def _check_baihu(cls, bazi: Dict) -> List[ShenShaInfo]:
        """白虎"""
        results = []
        
        baihu_map = {
            '子': '申', '丑': '酉', '寅': '戌', '卯': '亥',
            '辰': '子', '巳': '丑', '午': '寅', '未': '卯',
            '申': '辰', '酉': '巳', '戌': '午', '亥': '未'
        }
        
        year_branch = bazi['year']['branch']
        baihu = baihu_map.get(year_branch)
        
        if baihu:
            for key, pos_name in [('month', '月支'), ('day', '日支'), ('hour', '时支')]:
                if bazi[key]['branch'] == baihu:
                    results.append(ShenShaInfo(
                        name='白虎',
                        type='凶煞',
                        position=pos_name,
                        description='白虎，主血光之灾，易有意外伤害。注意安全，谨慎行事。'
                    ))
        
        return results
    
    @classmethod
    def _check_tianluo_diwang(cls, bazi: Dict) -> List[ShenShaInfo]:
        """天罗地网"""
        results = []
        
        # 天罗：戌亥为天罗（阳干）
        # 地网：辰巳为地网（阴干）
        all_branches = [bazi[k]['branch'] for k in ['year', 'month', 'day', 'hour']]
        
        if '戌' in all_branches and '亥' in all_branches:
            results.append(ShenShaInfo(
                name='天罗',
                type='凶煞',
                position='命局',
                description='天罗，主事业受阻，易有官非。做事需谨慎，避免触犯法律。'
            ))
        
        if '辰' in all_branches and '巳' in all_branches:
            results.append(ShenShaInfo(
                name='地网',
                type='凶煞',
                position='命局',
                description='地网，主身体不佳，易有疾病。注意养生保健。'
            ))
        
        return results
    
    @classmethod
    def _check_kongwang(cls, bazi: Dict) -> List[ShenShaInfo]:
        """空亡"""
        results = []
        
        # 简化版：根据日柱判断空亡
        # 甲子旬空戌亥，甲戌旬空申酉，等
        kongwang_table = {
            '甲子': ['戌', '亥'], '乙丑': ['戌', '亥'], '丙寅': ['戌', '亥'],
            '丁卯': ['戌', '亥'], '戊辰': ['戌', '亥'], '己巳': ['戌', '亥'],
            '庚午': ['戌', '亥'], '辛未': ['戌', '亥'], '壬申': ['戌', '亥'],
            '癸酉': ['戌', '亥'],
            '甲戌': ['申', '酉'], '乙亥': ['申', '酉'], '丙子': ['申', '酉'],
            '丁丑': ['申', '酉'], '戊寅': ['申', '酉'], '己卯': ['申', '酉'],
            '庚辰': ['申', '酉'], '辛巳': ['申', '酉'], '壬午': ['申', '酉'],
            '癸未': ['申', '酉']
        }
        
        day_pillar = bazi['day']['stem'] + bazi['day']['branch']
        kongwang_branches = kongwang_table.get(day_pillar, [])
        
        for key, pos_name in [('year', '年支'), ('month', '月支'), ('hour', '时支')]:
            if bazi[key]['branch'] in kongwang_branches:
                results.append(ShenShaInfo(
                    name='空亡',
                    type='凶煞',
                    position=pos_name,
                    description='空亡，主虚无缥缈，不切实际。该位置所代表的六亲或事业易有波折。'
                ))
        
        return results
    
    @classmethod
    def _check_kuigang(cls, bazi: Dict) -> List[ShenShaInfo]:
        """魁罡"""
        results = []
        
        kuigang_pillars = ['庚辰', '庚戌', '壬辰', '戊戌']
        
        for key, pos_name in [('year', '年柱'), ('month', '月柱'), ('day', '日柱'), ('hour', '时柱')]:
            pillar = bazi[key]['stem'] + bazi[key]['branch']
            if pillar in kuigang_pillars:
                results.append(ShenShaInfo(
                    name='魁罡',
                    type='吉星',
                    position=pos_name,
                    description='魁罡，主性格刚强，处事果断。有领导才能，不宜见财官太重。'
                ))
        
        return results
    
    @classmethod
    def _check_ride(cls, bazi: Dict) -> List[ShenShaInfo]:
        """日德"""
        results = []
        
        ride_pillars = ['甲寅', '丙辰', '戊辰', '庚辰', '壬戌']
        
        day_pillar = bazi['day']['stem'] + bazi['day']['branch']
        if day_pillar in ride_pillars:
            results.append(ShenShaInfo(
                name='日德',
                type='吉星',
                position='日柱',
                description='日德，主仁慈宽厚，一生福泽深厚。遇事逢凶化吉，多贵人相助。'
            ))
        
        return results
    
    # ========== 扩展神煞（新增15种，共40+种）==========
    
    @classmethod
    def _check_guoyin(cls, bazi: Dict) -> List[ShenShaInfo]:
        """国印贵人"""
        results = []
        
        guoyin_map = {
            '甲': '戌', '乙': '亥', '丙': '丑', '丁': '寅',
            '戊': '丑', '己': '寅', '庚': '辰', '辛': '巳',
            '壬': '未', '癸': '申'
        }
        
        day_stem = bazi['day']['stem']
        guoyin = guoyin_map.get(day_stem)
        
        if guoyin:
            for key, pos_name in [('year', '年支'), ('month', '月支'), ('hour', '时支')]:
                if bazi[key]['branch'] == guoyin:
                    results.append(ShenShaInfo(
                        name='国印贵人',
                        type='吉星',
                        position=pos_name,
                        description='国印贵人，主掌权印信，适合从政或担任管理职位。'
                    ))
        
        return results
    
    @classmethod
    def _check_xuetang(cls, day_master: str, bazi: Dict) -> List[ShenShaInfo]:
        """学堂"""
        results = []
        
        xuetang_map = {
            '甲': '亥', '乙': '午', '丙': '寅', '丁': '酉',
            '戊': '寅', '己': '酉', '庚': '巳', '辛': '子',
            '壬': '申', '癸': '卯'
        }
        
        xuetang = xuetang_map.get(day_master)
        if xuetang:
            for key, pos_name in [('year', '年支'), ('month', '月支'), ('hour', '时支')]:
                if bazi[key]['branch'] == xuetang:
                    results.append(ShenShaInfo(
                        name='学堂',
                        type='吉星',
                        position=pos_name,
                        description='学堂，主聪明好学，学业有成。利考试升学，文化事业发展。'
                    ))
        
        return results
    
    @classmethod
    def _check_ciguang(cls, day_master: str, bazi: Dict) -> List[ShenShaInfo]:
        """词馆"""
        results = []
        
        ciguang_map = {
            '甲': '巳', '乙': '午', '丙': '申', '丁': '酉',
            '戊': '申', '己': '酉', '庚': '亥', '辛': '子',
            '壬': '寅', '癸': '卯'
        }
        
        ciguang = ciguang_map.get(day_master)
        if ciguang:
            for key, pos_name in [('year', '年支'), ('month', '月支'), ('hour', '时支')]:
                if bazi[key]['branch'] == ciguang:
                    results.append(ShenShaInfo(
                        name='词馆',
                        type='吉星',
                        position=pos_name,
                        description='词馆，主文采出众，口才好。利写作、演讲、教育等文化事业。'
                    ))
        
        return results
    
    @classmethod
    def _check_jinyu(cls, day_master: str, bazi: Dict) -> List[ShenShaInfo]:
        """金舆"""
        results = []
        
        jinyu_map = {
            '甲': '辰', '乙': '巳', '丙': '未', '丁': '申',
            '戊': '未', '己': '申', '庚': '戌', '辛': '亥',
            '壬': '丑', '癸': '寅'
        }
        
        jinyu = jinyu_map.get(day_master)
        if jinyu:
            for key, pos_name in [('year', '年支'), ('month', '月支'), ('hour', '时支')]:
                if bazi[key]['branch'] == jinyu:
                    results.append(ShenShaInfo(
                        name='金舆',
                        type='吉星',
                        position=pos_name,
                        description='金舆，主贵人乘坐，出行平安。利交通、旅行、车辆相关事业。'
                    ))
        
        return results
    
    @classmethod
    def _check_tianguan(cls, day_master: str, bazi: Dict) -> List[ShenShaInfo]:
        """天官贵人"""
        results = []
        
        tianguan_map = {
            '甲': '未', '乙': '辰', '丙': '酉', '丁': '亥',
            '戊': '酉', '己': '亥', '庚': '丑', '辛': '寅',
            '壬': '卯', '癸': '巳'
        }
        
        tianguan = tianguan_map.get(day_master)
        if tianguan:
            for key, pos_name in [('year', '年支'), ('month', '月支'), ('hour', '时支')]:
                if bazi[key]['branch'] == tianguan:
                    results.append(ShenShaInfo(
                        name='天官贵人',
                        type='吉星',
                        position=pos_name,
                        description='天官贵人，主官运亨通，利仕途发展。适合公职、政务工作。'
                    ))
        
        return results
    
    @classmethod
    def _check_tianchu(cls, day_master: str, bazi: Dict) -> List[ShenShaInfo]:
        """天厨贵人"""
        results = []
        
        tianchu_map = {
            '甲': '巳', '乙': '午', '丙': '巳', '丁': '午',
            '戊': '巳', '己': '午', '庚': '亥', '辛': '子',
            '壬': '亥', '癸': '子'
        }
        
        tianchu = tianchu_map.get(day_master)
        if tianchu:
            for key, pos_name in [('year', '年支'), ('month', '月支'), ('hour', '时支')]:
                if bazi[key]['branch'] == tianchu:
                    results.append(ShenShaInfo(
                        name='天厨贵人',
                        type='吉星',
                        position=pos_name,
                        description='天厨贵人，主衣食无忧，福禄俱全。一生不愁吃穿，物质丰厚。'
                    ))
        
        return results
    
    @classmethod
    def _check_feilian(cls, bazi: Dict) -> List[ShenShaInfo]:
        """飞廉"""
        results = []
        
        feilian_map = {
            '子': '申', '丑': '酉', '寅': '戌', '卯': '亥',
            '辰': '子', '巳': '丑', '午': '寅', '未': '卯',
            '申': '辰', '酉': '巳', '戌': '午', '亥': '未'
        }
        
        year_branch = bazi['year']['branch']
        feilian = feilian_map.get(year_branch)
        
        if feilian:
            for key, pos_name in [('month', '月支'), ('day', '日支'), ('hour', '时支')]:
                if bazi[key]['branch'] == feilian:
                    results.append(ShenShaInfo(
                        name='飞廉',
                        type='凶煞',
                        position=pos_name,
                        description='飞廉，主口舌是非，易生争端。言行谨慎，避免与人争执。'
                    ))
        
        return results
    
    @classmethod
    def _check_dasao(cls, bazi: Dict) -> List[ShenShaInfo]:
        """大耗"""
        results = []
        
        dasao_map = {
            '子': '未', '丑': '申', '寅': '酉', '卯': '戌',
            '辰': '亥', '巳': '子', '午': '丑', '未': '寅',
            '申': '卯', '酉': '辰', '戌': '巳', '亥': '午'
        }
        
        year_branch = bazi['year']['branch']
        dasao = dasao_map.get(year_branch)
        
        if dasao:
            for key, pos_name in [('month', '月支'), ('day', '日支'), ('hour', '时支')]:
                if bazi[key]['branch'] == dasao:
                    results.append(ShenShaInfo(
                        name='大耗',
                        type='凶煞',
                        position=pos_name,
                        description='大耗，主破财损失，钱财不聚。理财需谨慎，避免投资风险。'
                    ))
        
        return results
    
    @classmethod
    def _check_dianjiao(cls, bazi: Dict) -> List[ShenShaInfo]:
        """吊客"""
        results = []
        
        dianjiao_map = {
            '子': '巳', '丑': '午', '寅': '未', '卯': '申',
            '辰': '酉', '巳': '戌', '午': '亥', '未': '子',
            '申': '丑', '酉': '寅', '戌': '卯', '亥': '辰'
        }
        
        year_branch = bazi['year']['branch']
        dianjiao = dianjiao_map.get(year_branch)
        
        if dianjiao:
            for key, pos_name in [('month', '月支'), ('day', '日支'), ('hour', '时支')]:
                if bazi[key]['branch'] == dianjiao:
                    results.append(ShenShaInfo(
                        name='吊客',
                        type='凶煞',
                        position=pos_name,
                        description='吊客，主丧服凶事。注意六亲健康，谨慎处理丧葬事宜。'
                    ))
        
        return results
    
    @classmethod
    def _check_sangmen(cls, bazi: Dict) -> List[ShenShaInfo]:
        """丧门"""
        results = []
        
        sangmen_map = {
            '子': '寅', '丑': '卯', '寅': '辰', '卯': '巳',
            '辰': '午', '巳': '未', '午': '申', '未': '酉',
            '申': '戌', '酉': '亥', '戌': '子', '亥': '丑'
        }
        
        year_branch = bazi['year']['branch']
        sangmen = sangmen_map.get(year_branch)
        
        if sangmen:
            for key, pos_name in [('month', '月支'), ('day', '日支'), ('hour', '时支')]:
                if bazi[key]['branch'] == sangmen:
                    results.append(ShenShaInfo(
                        name='丧门',
                        type='凶煞',
                        position=pos_name,
                        description='丧门，主孝服之事。注意家人健康，谨慎处理家庭事务。'
                    ))
        
        return results
    
    @classmethod
    def _check_guanfu(cls, bazi: Dict) -> List[ShenShaInfo]:
        """官符"""
        results = []
        
        guanfu_map = {
            '子': '卯', '丑': '辰', '寅': '巳', '卯': '午',
            '辰': '未', '巳': '申', '午': '酉', '未': '戌',
            '申': '亥', '酉': '子', '戌': '丑', '亥': '寅'
        }
        
        year_branch = bazi['year']['branch']
        guanfu = guanfu_map.get(year_branch)
        
        if guanfu:
            for key, pos_name in [('month', '月支'), ('day', '日支'), ('hour', '时支')]:
                if bazi[key]['branch'] == guanfu:
                    results.append(ShenShaInfo(
                        name='官符',
                        type='凶煞',
                        position=pos_name,
                        description='官符，主官非诉讼。行事谨慎，避免触犯法律，远离是非。'
                    ))
        
        return results
    
    @classmethod
    def _check_tianshe(cls, bazi: Dict) -> List[ShenShaInfo]:
        """天赦"""
        results = []
        
        # 天赦日：春戊寅，夏甲午，秋戊申，冬甲子
        tianshe_combos = [
            ('戊', '寅'),  # 春
            ('甲', '午'),  # 夏
            ('戊', '申'),  # 秋
            ('甲', '子'),  # 冬
        ]
        
        for key, pos_name in [('year', '年柱'), ('month', '月柱'), ('day', '日柱'), ('hour', '时柱')]:
            stem = bazi[key]['stem']
            branch = bazi[key]['branch']
            if (stem, branch) in tianshe_combos:
                results.append(ShenShaInfo(
                    name='天赦',
                    type='吉星',
                    position=pos_name,
                    description='天赦，主逢凶化吉，百事可解。一生多有贵人相助，灾厄消散。'
                ))
        
        return results
    
    @classmethod
    def _check_tiandao(cls, bazi: Dict) -> List[ShenShaInfo]:
        """天德合"""
        results = []
        
        tiandao_map = {
            '寅': '壬', '卯': '癸', '辰': '丁', '巳': '丙',
            '午': '甲', '未': '己', '申': '戊', '酉': '丁',
            '戌': '辛', '亥': '庚', '子': '庚', '丑': '乙'
        }
        
        month_branch = bazi['month']['branch']
        tiandao_stem = tiandao_map.get(month_branch)
        
        if tiandao_stem:
            for key, pos_name in [('year', '年干'), ('day', '日干'), ('hour', '时干')]:
                if bazi[key]['stem'] == tiandao_stem:
                    results.append(ShenShaInfo(
                        name='天德合',
                        type='吉星',
                        position=pos_name,
                        description='天德合，主逢凶化吉，贵人相助。一生平安，少遇灾难。'
                    ))
        
        return results
    
    @classmethod
    def _check_yuede_he(cls, bazi: Dict) -> List[ShenShaInfo]:
        """月德合"""
        results = []
        
        yuede_he_map = {
            '寅': '辛', '午': '辛', '戌': '辛',
            '申': '丁', '子': '丁', '辰': '丁',
            '亥': '己', '卯': '己', '未': '己',
            '巳': '乙', '酉': '乙', '丑': '乙'
        }
        
        month_branch = bazi['month']['branch']
        yuede_he_stem = yuede_he_map.get(month_branch)
        
        if yuede_he_stem:
            for key, pos_name in [('year', '年干'), ('day', '日干'), ('hour', '时干')]:
                if bazi[key]['stem'] == yuede_he_stem:
                    results.append(ShenShaInfo(
                        name='月德合',
                        type='吉星',
                        position=pos_name,
                        description='月德合，主仁慈宽厚，一生平安。逢凶化吉，遇难呈祥。'
                    ))
        
        return results
    
    @classmethod
    def _check_feixian(cls, day_master: str, bazi: Dict) -> List[ShenShaInfo]:
        """飞刃"""
        results = []
        
        feixian_map = {
            '甲': '酉', '乙': '申', '丙': '子', '丁': '亥',
            '戊': '子', '己': '亥', '庚': '卯', '辛': '寅',
            '壬': '午', '癸': '巳'
        }
        
        feixian = feixian_map.get(day_master)
        if feixian:
            for key, pos_name in [('year', '年支'), ('month', '月支'), ('hour', '时支')]:
                if bazi[key]['branch'] == feixian:
                    results.append(ShenShaInfo(
                        name='飞刃',
                        type='凶煞',
                        position=pos_name,
                        description='飞刃，主意外伤害，血光之灾。行事需谨慎，避免危险活动。'
                    ))
        
        return results
    
    # ========== 补充神煞（基于MingAI参考）==========
    
    @classmethod
    def _check_yinchayang(cls, bazi: Dict) -> List[ShenShaInfo]:
        """阴差阳错"""
        results = []
        
        # 阴差阳错日
        yinchayang_pillars = [
            '丙子', '丁丑', '戊寅', '辛卯', '壬辰', '癸巳',
            '丙午', '丁未', '戊申', '辛酉', '壬戌', '癸亥'
        ]
        
        day_pillar = bazi['day']['stem'] + bazi['day']['branch']
        if day_pillar in yinchayang_pillars:
            results.append(ShenShaInfo(
                name='阴差阳错',
                type='凶煞',
                position='日柱',
                description='阴差阳错日，主婚姻感情易有波折，男女缘分不顺。宜谨慎择偶。'
            ))
        
        return results
    
    @classmethod
    def _check_shiedabai(cls, bazi: Dict) -> List[ShenShaInfo]:
        """十恶大败"""
        results = []
        
        # 十恶大败日
        shiedabai_pillars = [
            '甲辰', '乙巳', '壬申', '丙申', '丁亥',
            '庚辰', '戊戌', '癸亥', '辛巳', '己丑'
        ]
        
        day_pillar = bazi['day']['stem'] + bazi['day']['branch']
        if day_pillar in shiedabai_pillars:
            results.append(ShenShaInfo(
                name='十恶大败',
                type='凶煞',
                position='日柱',
                description='十恶大败日，主财运波折，不聚财。理财需谨慎，宜稳健投资。'
            ))
        
        return results
    
    @classmethod
    def _check_xieren(cls, day_master: str, bazi: Dict) -> List[ShenShaInfo]:
        """血刃"""
        results = []
        
        xieren_map = {
            '甲': '卯', '乙': '辰', '丙': '午', '丁': '未',
            '戊': '午', '己': '未', '庚': '酉', '辛': '戌',
            '壬': '子', '癸': '丑'
        }
        
        xieren = xieren_map.get(day_master)
        if xieren:
            for key, pos_name in [('year', '年支'), ('month', '月支'), ('day', '日支'), ('hour', '时支')]:
                if bazi[key]['branch'] == xieren:
                    results.append(ShenShaInfo(
                        name='血刃',
                        type='凶煞',
                        position=pos_name,
                        description='血刃，主血光之灾，易受外伤。注意安全，避免危险运动。'
                    ))
        
        return results
    
    @classmethod
    def _check_pitou(cls, bazi: Dict) -> List[ShenShaInfo]:
        """披麻"""
        results = []
        
        pitou_map = {
            '子': '巳', '丑': '午', '寅': '未', '卯': '申',
            '辰': '酉', '巳': '戌', '午': '亥', '未': '子',
            '申': '丑', '酉': '寅', '戌': '卯', '亥': '辰'
        }
        
        year_branch = bazi['year']['branch']
        pitou = pitou_map.get(year_branch)
        
        if pitou:
            for key, pos_name in [('month', '月支'), ('day', '日支'), ('hour', '时支')]:
                if bazi[key]['branch'] == pitou:
                    results.append(ShenShaInfo(
                        name='披麻',
                        type='凶煞',
                        position=pos_name,
                        description='披麻，主丧事孝服。注意家人健康，多关心长辈。'
                    ))
        
        return results
    
    @classmethod
    def _check_tianyiextra(cls, bazi: Dict) -> List[ShenShaInfo]:
        """天医（月支版）"""
        results = []
        
        tianyi_map = {
            '寅': '丑', '卯': '寅', '辰': '卯', '巳': '辰',
            '午': '巳', '未': '午', '申': '未', '酉': '申',
            '戌': '酉', '亥': '戌', '子': '亥', '丑': '子'
        }
        
        month_branch = bazi['month']['branch']
        tianyi = tianyi_map.get(month_branch)
        
        if tianyi:
            for key, pos_name in [('year', '年支'), ('day', '日支'), ('hour', '时支')]:
                if bazi[key]['branch'] == tianyi:
                    results.append(ShenShaInfo(
                        name='天医星',
                        type='吉星',
                        position=pos_name,
                        description='天医星，主医药天赋，身体康健。适合医疗、保健相关行业。'
                    ))
        
        return results
    
    @classmethod
    def _check_sanqi(cls, bazi: Dict) -> List[ShenShaInfo]:
        """三奇贵人"""
        results = []
        
        # 天上三奇：甲戊庚
        # 地上三奇：乙丙丁
        # 人中三奇：壬癸辛
        stems = [bazi['year']['stem'], bazi['month']['stem'], 
                 bazi['day']['stem'], bazi['hour']['stem']]
        
        # 检查甲戊庚（天上三奇）
        if '甲' in stems and '戊' in stems and '庚' in stems:
            results.append(ShenShaInfo(
                name='天上三奇',
                type='吉星',
                position='命局',
                description='天上三奇（甲戊庚），主聪明机智，贵人相助。一生多有奇遇。'
            ))
        
        # 检查乙丙丁（地上三奇）
        if '乙' in stems and '丙' in stems and '丁' in stems:
            results.append(ShenShaInfo(
                name='地上三奇',
                type='吉星',
                position='命局',
                description='地上三奇（乙丙丁），主聪明好学，文采出众。利学业事业。'
            ))
        
        # 检查壬癸辛（人中三奇）
        if '壬' in stems and '癸' in stems and '辛' in stems:
            results.append(ShenShaInfo(
                name='人中三奇',
                type='吉星',
                position='命局',
                description='人中三奇（壬癸辛），主智慧超群，有谋略。适合经商或从政。'
            ))
        
        return results
    
    @classmethod
    def _check_luomawangxiang(cls, bazi: Dict) -> List[ShenShaInfo]:
        """骡马网相（马星与网星同柱）"""
        results = []
        
        # 驿马与天罗地网同柱时的特殊情况
        all_branches = [bazi[k]['branch'] for k in ['year', 'month', 'day', 'hour']]
        
        yima_map = {
            '寅': '申', '午': '申', '戌': '申',
            '申': '寅', '子': '寅', '辰': '寅',
            '亥': '巳', '卯': '巳', '未': '巳',
            '巳': '亥', '酉': '亥', '丑': '亥'
        }
        
        year_branch = bazi['year']['branch']
        yima = yima_map.get(year_branch)
        
        if yima and yima in all_branches:
            # 检查驿马是否与戌亥（天罗）或辰巳（地网）同在
            if (yima == '戌' or yima == '亥') and ('戌' in all_branches or '亥' in all_branches):
                results.append(ShenShaInfo(
                    name='马入天罗',
                    type='凶煞',
                    position='命局',
                    description='驿马入天罗，主出行受阻，奔波不顺。外出需谨慎，避免长途旅行。'
                ))
            if (yima == '辰' or yima == '巳') and ('辰' in all_branches or '巳' in all_branches):
                results.append(ShenShaInfo(
                    name='马入地网',
                    type='凶煞',
                    position='命局',
                    description='驿马入地网，主行动受限，不利出行。宜安守本分，慎出远门。'
                ))
        
        return results
    
    @classmethod
    def _check_tongziminggong(cls, bazi: Dict, gender: str) -> List[ShenShaInfo]:
        """童子命（特殊格局）"""
        results = []
        
        # 童子命口诀（简化版）
        # 春秋寅子贵，冬夏卯未辰，
        # 金木马卯合，水火鸡犬多，
        # 土命逢辰巳，童子定不错。
        
        month_branch = bazi['month']['branch']
        day_branch = bazi['day']['branch']
        hour_branch = bazi['hour']['branch']
        
        # 春秋月（寅卯辰、申酉戌）
        spring_autumn = ['寅', '卯', '辰', '申', '酉', '戌']
        # 冬夏月（巳午未、亥子丑）
        winter_summer = ['巳', '午', '未', '亥', '子', '丑']
        
        is_tongzi = False
        
        if month_branch in spring_autumn:
            if day_branch in ['寅', '子'] or hour_branch in ['寅', '子']:
                is_tongzi = True
        elif month_branch in winter_summer:
            if day_branch in ['卯', '未', '辰'] or hour_branch in ['卯', '未', '辰']:
                is_tongzi = True
        
        if is_tongzi:
            results.append(ShenShaInfo(
                name='童子命',
                type='凶煞',
                position='命局',
                description='童子命格，主婚姻事业多波折，体弱多病。宜行善积德，化解命中劫难。'
            ))
        
        return results
    
    @classmethod
    def get_summary(cls, shen_sha_list: List[ShenShaInfo]) -> Dict[str, Any]:
        """
        获取神煞分析汇总
        
        Returns:
            {'ji_shen': [...], 'xiong_sha': [...], 'by_position': {...}, 'score': int}
        """
        ji_shen = [s for s in shen_sha_list if s.type == '吉星']
        xiong_sha = [s for s in shen_sha_list if s.type == '凶煞']
        
        by_position = {
            '年柱': [], '月柱': [], '日柱': [], '时柱': [],
            '年支': [], '月支': [], '日支': [], '时支': [],
            '年干': [], '月干': [], '日干': [], '时干': [],
            '命局': []
        }
        
        for s in shen_sha_list:
            if s.position in by_position:
                by_position[s.position].append(s.name)
        
        # 计算吉凶分数（吉星+10，凶煞-5）
        score = len(ji_shen) * 10 - len(xiong_sha) * 5
        score = max(0, min(100, 50 + score))  # 归一化到0-100
        
        return {
            'ji_shen': [{'name': s.name, 'position': s.position, 'description': s.description} for s in ji_shen],
            'xiong_sha': [{'name': s.name, 'position': s.position, 'description': s.description} for s in xiong_sha],
            'by_position': {k: v for k, v in by_position.items() if v},
            'score': score,
            'total_ji': len(ji_shen),
            'total_xiong': len(xiong_sha)
        }
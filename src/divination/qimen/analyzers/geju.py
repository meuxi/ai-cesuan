"""
格局分析器
分析奇门遁甲的吉凶格局
参考 mingpan 的 GeJuCalculator.ts 实现
"""
from typing import Dict, List


class GeJuAnalyzer:
    """格局分析类"""
    
    # 吉格定义
    JI_GE = {
        '天遁': {'condition': '丙加戊', 'meaning': '贵人相助，诸事大吉'},
        '地遁': {'condition': '乙加己', 'meaning': '安居乐业，稳固发展'},
        '人遁': {'condition': '丁加癸', 'meaning': '贵人扶持，心想事成'},
        '神遁': {'condition': '丙加壬', 'meaning': '神助鬼使，逢凶化吉'},
        '鬼遁': {'condition': '丁加辛', 'meaning': '阴助暗扶，绝处逢生'},
        '龙遁': {'condition': '乙加癸', 'meaning': '青龙护佑，吉祥如意'},
        '虎遁': {'condition': '辛加丁', 'meaning': '白虎归顺，威武有力'},
        '风遁': {'condition': '乙加辛', 'meaning': '顺风顺水，如虎添翼'},
        '云遁': {'condition': '丙加己', 'meaning': '云开见日，转危为安'},
        '三奇得使': {'condition': '三奇临本宫', 'meaning': '三奇得位，吉上加吉'},
        '三奇得门': {'condition': '三奇临吉门', 'meaning': '奇门相合，诸事皆宜'},
        '奇仪相合': {'condition': '天地盘相合', 'meaning': '阴阳调和，万事亨通'}
    }
    
    # 凶格定义
    XIONG_GE = {
        '白虎猖狂': {'condition': '庚加庚', 'meaning': '凶险重重，诸事不利'},
        '天牢': {'condition': '庚加壬', 'meaning': '困顿受阻，难以脱身'},
        '五不遇时': {'condition': '时干克日干', 'meaning': '时运不济，诸事难成'},
        '入墓': {'condition': '奇仪入墓', 'meaning': '晦暗不明，进退两难'},
        '击刑': {'condition': '门星相刑', 'meaning': '冲突矛盾，损伤破败'},
        '门迫': {'condition': '门克宫', 'meaning': '受制受限，难以施展'},
        '悖格': {'condition': '戊加癸', 'meaning': '阴阳相悖，事与愿违'},
        '飞宫格': {'condition': '庚加丙', 'meaning': '飞来横祸，防不胜防'},
        '伏干格': {'condition': '庚加戊', 'meaning': '暗箭难防，小人作祟'}
    }
    
    # 中性格局
    ZHONG_GE = {
        '伏吟': {'condition': '天地盘相同', 'meaning': '守静待时，不宜妄动'},
        '反吟': {'condition': '天地盘相冲', 'meaning': '反复无常，变化多端'}
    }
    
    @classmethod
    def analyze(cls, tian_pan: Dict[int, str], di_pan: Dict[int, str],
                ba_men: Dict[int, str], jiu_xing: Dict[int, str]) -> Dict:
        """分析格局
        
        Args:
            tian_pan: 天盘布局 {宫位: 天干}
            di_pan: 地盘布局 {宫位: 天干}
            ba_men: 八门布局 {宫位: 门}
            jiu_xing: 九星布局 {宫位: 星}
            
        Returns:
            格局分析结果
        """
        ji_ge_list = []
        xiong_ge_list = []
        zhong_ge_list = []
        
        # 遍历每个宫位分析格局
        for gong in range(1, 10):
            if gong == 5:
                continue  # 中宫特殊处理
            
            tian_gan = tian_pan.get(gong, '')
            di_gan = di_pan.get(gong, '')
            men = ba_men.get(gong, '')
            xing = jiu_xing.get(gong, '')
            
            # 分析九遁格局
            ge_info = cls._check_jiu_dun(tian_gan, di_gan, gong)
            if ge_info:
                if ge_info['type'] == 'ji':
                    ji_ge_list.append(ge_info)
                elif ge_info['type'] == 'xiong':
                    xiong_ge_list.append(ge_info)
            
            # 分析伏吟反吟
            if tian_gan == di_gan:
                zhong_ge_list.append({
                    'name': '伏吟',
                    'gong': gong,
                    'meaning': cls.ZHONG_GE['伏吟']['meaning']
                })
        
        return {
            'ji_ge': ji_ge_list,
            'xiong_ge': xiong_ge_list,
            'zhong_ge': zhong_ge_list,
            'summary': cls._generate_summary(ji_ge_list, xiong_ge_list, zhong_ge_list)
        }
    
    @classmethod
    def _check_jiu_dun(cls, tian_gan: str, di_gan: str, gong: int) -> Dict:
        """检查九遁格局"""
        # 天遁：丙加戊
        if tian_gan == '丙' and di_gan == '戊':
            return {'name': '天遁', 'gong': gong, 'type': 'ji',
                    'meaning': cls.JI_GE['天遁']['meaning']}
        
        # 地遁：乙加己
        if tian_gan == '乙' and di_gan == '己':
            return {'name': '地遁', 'gong': gong, 'type': 'ji',
                    'meaning': cls.JI_GE['地遁']['meaning']}
        
        # 人遁：丁加癸
        if tian_gan == '丁' and di_gan == '癸':
            return {'name': '人遁', 'gong': gong, 'type': 'ji',
                    'meaning': cls.JI_GE['人遁']['meaning']}
        
        # 神遁：丙加壬
        if tian_gan == '丙' and di_gan == '壬':
            return {'name': '神遁', 'gong': gong, 'type': 'ji',
                    'meaning': cls.JI_GE['神遁']['meaning']}
        
        # 鬼遁：丁加辛
        if tian_gan == '丁' and di_gan == '辛':
            return {'name': '鬼遁', 'gong': gong, 'type': 'ji',
                    'meaning': cls.JI_GE['鬼遁']['meaning']}
        
        # 龙遁：乙加癸
        if tian_gan == '乙' and di_gan == '癸':
            return {'name': '龙遁', 'gong': gong, 'type': 'ji',
                    'meaning': cls.JI_GE['龙遁']['meaning']}
        
        # 虎遁：辛加丁
        if tian_gan == '辛' and di_gan == '丁':
            return {'name': '虎遁', 'gong': gong, 'type': 'ji',
                    'meaning': cls.JI_GE['虎遁']['meaning']}
        
        # 风遁：乙加辛
        if tian_gan == '乙' and di_gan == '辛':
            return {'name': '风遁', 'gong': gong, 'type': 'ji',
                    'meaning': cls.JI_GE['风遁']['meaning']}
        
        # 云遁：丙加己
        if tian_gan == '丙' and di_gan == '己':
            return {'name': '云遁', 'gong': gong, 'type': 'ji',
                    'meaning': cls.JI_GE['云遁']['meaning']}
        
        # 白虎猖狂：庚加庚
        if tian_gan == '庚' and di_gan == '庚':
            return {'name': '白虎猖狂', 'gong': gong, 'type': 'xiong',
                    'meaning': cls.XIONG_GE['白虎猖狂']['meaning']}
        
        # 天牢：庚加壬
        if tian_gan == '庚' and di_gan == '壬':
            return {'name': '天牢', 'gong': gong, 'type': 'xiong',
                    'meaning': cls.XIONG_GE['天牢']['meaning']}
        
        # 悖格：戊加癸
        if tian_gan == '戊' and di_gan == '癸':
            return {'name': '悖格', 'gong': gong, 'type': 'xiong',
                    'meaning': cls.XIONG_GE['悖格']['meaning']}
        
        # 飞宫格：庚加丙
        if tian_gan == '庚' and di_gan == '丙':
            return {'name': '飞宫格', 'gong': gong, 'type': 'xiong',
                    'meaning': cls.XIONG_GE['飞宫格']['meaning']}
        
        # 伏干格：庚加戊
        if tian_gan == '庚' and di_gan == '戊':
            return {'name': '伏干格', 'gong': gong, 'type': 'xiong',
                    'meaning': cls.XIONG_GE['伏干格']['meaning']}
        
        return None
    
    @classmethod
    def _generate_summary(cls, ji_ge: List, xiong_ge: List, zhong_ge: List) -> str:
        """生成格局总结"""
        parts = []
        
        if ji_ge:
            parts.append(f"吉格{len(ji_ge)}个：" + '、'.join([g['name'] for g in ji_ge]))
        
        if xiong_ge:
            parts.append(f"凶格{len(xiong_ge)}个：" + '、'.join([g['name'] for g in xiong_ge]))
        
        if zhong_ge:
            parts.append(f"中性格{len(zhong_ge)}个：" + '、'.join([g['name'] for g in zhong_ge]))
        
        if not parts:
            return '无明显格局'
        
        return '；'.join(parts)

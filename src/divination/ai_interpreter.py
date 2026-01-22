"""
AI解读服务增强模块
提供专业版+大白话版双模块命理解读

功能：
1. 专业版分析：引用理论依据，标注出处
2. 大白话版解读：通俗易懂，落地建议
3. 多术数通用：支持八字、紫微、六爻等
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from enum import Enum


class DivinationType(Enum):
    """占卜类型"""
    BAZI = "bazi"           # 八字
    ZIWEI = "ziwei"         # 紫微斗数
    LIUYAO = "liuyao"       # 六爻
    QIMEN = "qimen"         # 奇门遁甲
    DALIUREN = "daliuren"   # 大六壬
    MEIHUA = "meihua"       # 梅花易数
    TAROT = "tarot"         # 塔罗牌


@dataclass
class InterpretationResult:
    """解读结果"""
    professional: Dict[str, Any]    # 专业版分析
    vernacular: Dict[str, Any]      # 大白话版解读
    summary: str                    # 简短总结
    disclaimer: str                 # 免责声明


class AIInterpreter:
    """AI解读器基类"""
    
    DEFAULT_DISCLAIMER = "命理仅供参考，人生路径最终取决于个人选择与努力。"
    
    def __init__(self, divination_type: DivinationType):
        self.divination_type = divination_type
    
    def interpret(self, data: Dict[str, Any]) -> InterpretationResult:
        """生成解读结果"""
        professional = self._generate_professional(data)
        vernacular = self._generate_vernacular(data)
        summary = self._generate_summary(data)
        
        return InterpretationResult(
            professional=professional,
            vernacular=vernacular,
            summary=summary,
            disclaimer=self.DEFAULT_DISCLAIMER
        )
    
    def _generate_professional(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """生成专业版分析（子类重写）"""
        raise NotImplementedError
    
    def _generate_vernacular(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """生成大白话版解读（子类重写）"""
        raise NotImplementedError
    
    def _generate_summary(self, data: Dict[str, Any]) -> str:
        """生成简短总结（子类重写）"""
        raise NotImplementedError


class BaziInterpreter(AIInterpreter):
    """八字解读器"""
    
    # 日主强弱解读模板
    STRENGTH_TEMPLATES = {
        '身旺': {
            'professional': '日主得令得地，比劫印绶有力，身旺需泄秀',
            'vernacular': '你的命格属于能量充沛型，需要找到发挥的渠道'
        },
        '身弱': {
            'professional': '日主失令失地，财官食伤耗泄，身弱需生扶',
            'vernacular': '你的命格需要外部支持，适合借力发展'
        },
        '中和': {
            'professional': '日主不偏不倚，五行流通，命局中和',
            'vernacular': '你的命格比较平衡，适应能力强'
        }
    }
    
    # 十神性格解读
    TEN_GOD_PERSONALITY = {
        '正官': '正直守规矩，有责任感，适合管理岗位',
        '七杀': '有魄力敢拼搏，压力下能爆发，适合创业或武职',
        '正财': '务实稳健，擅长理财，收入稳定',
        '偏财': '人缘好运气好，适合做生意或投资',
        '正印': '聪明好学，有长辈缘，适合文教工作',
        '偏印': '思维独特，有艺术天赋，适合创意工作',
        '食神': '性格温和，口才好，适合服务或餐饮业',
        '伤官': '才华横溢，有创新精神，适合技术或艺术',
        '比肩': '独立自主，竞争意识强，适合自主创业',
        '劫财': '胆大心细，善于交际，但需防破财'
    }
    
    # 用神五行补运建议
    WUXING_ADVICE = {
        '木': {
            'color': '绿色',
            'direction': '东方',
            'number': '3、8',
            'career': '教育、文化、园林、家具',
            'advice': '多亲近自然，养绿植，穿绿色衣物'
        },
        '火': {
            'color': '红色',
            'direction': '南方',
            'number': '2、7',
            'career': '电子、能源、餐饮、娱乐',
            'advice': '多晒太阳，穿红色衣物，住阳光充足的房间'
        },
        '土': {
            'color': '黄色',
            'direction': '中央',
            'number': '5、10',
            'career': '房产、建筑、农业、矿业',
            'advice': '多接地气，穿黄色衣物，从事稳定工作'
        },
        '金': {
            'color': '白色',
            'direction': '西方',
            'number': '4、9',
            'career': '金融、法律、机械、IT',
            'advice': '佩戴金属饰品，穿白色衣物，住西边房间'
        },
        '水': {
            'color': '黑色',
            'direction': '北方',
            'number': '1、6',
            'career': '物流、航运、水产、旅游',
            'advice': '多喝水，亲近水源，穿黑蓝色衣物'
        }
    }
    
    def __init__(self):
        super().__init__(DivinationType.BAZI)
    
    def _generate_professional(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """生成专业版八字分析"""
        result = {
            'title': '八字命理专业分析',
            'sections': []
        }
        
        # 1. 四柱信息
        if 'sizhu' in data:
            sizhu = data['sizhu']
            result['sections'].append({
                'name': '四柱排盘',
                'content': f"年柱{sizhu.get('year', '')}  月柱{sizhu.get('month', '')}  日柱{sizhu.get('day', '')}  时柱{sizhu.get('hour', '')}",
                'theory': '四柱八字以年月日时四柱推算，年为根，月为苗，日为花，时为果'
            })
        
        # 2. 日主分析
        if 'day_master' in data:
            day_master = data['day_master']
            strength = data.get('strength', '中和')
            template = self.STRENGTH_TEMPLATES.get(strength, self.STRENGTH_TEMPLATES['中和'])
            result['sections'].append({
                'name': '日主分析',
                'content': f"日主{day_master}，{template['professional']}",
                'theory': '日主为命主本身，其强弱决定用神取法'
            })
        
        # 3. 十神分布
        if 'shishen' in data:
            shishen = data['shishen']
            distribution = shishen.get('distribution', {})
            result['sections'].append({
                'name': '十神分布',
                'content': self._format_shishen_distribution(distribution),
                'theory': '十神代表六亲关系和人生领域'
            })
        
        # 4. 用神分析
        if 'yongshen' in data:
            yongshen = data['yongshen']
            result['sections'].append({
                'name': '用神分析',
                'content': f"用神：{yongshen.get('yongshen', '未知')}，喜神：{yongshen.get('xishen', '未知')}，忌神：{yongshen.get('jishen', '未知')}",
                'theory': '用神为八字之药，调候平衡之关键'
            })
        
        # 5. 神煞信息
        if 'shensha' in data:
            shensha_list = data['shensha']
            if shensha_list:
                result['sections'].append({
                    'name': '神煞信息',
                    'content': self._format_shensha(shensha_list),
                    'theory': '神煞为八字之辅助判断，吉神增福，凶煞需防'
                })
        
        return result
    
    def _generate_vernacular(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """生成大白话版解读"""
        result = {
            'title': '通俗解读',
            'sections': []
        }
        
        # 1. 性格分析
        personality = self._analyze_personality(data)
        result['sections'].append({
            'name': '你的性格',
            'content': personality
        })
        
        # 2. 事业财运
        career = self._analyze_career(data)
        result['sections'].append({
            'name': '事业财运',
            'content': career
        })
        
        # 3. 感情婚姻
        relationship = self._analyze_relationship(data)
        result['sections'].append({
            'name': '感情婚姻',
            'content': relationship
        })
        
        # 4. 健康提醒
        health = self._analyze_health(data)
        result['sections'].append({
            'name': '健康提醒',
            'content': health
        })
        
        # 5. 开运建议
        advice = self._generate_advice(data)
        result['sections'].append({
            'name': '开运建议',
            'content': advice
        })
        
        return result
    
    def _generate_summary(self, data: Dict[str, Any]) -> str:
        """生成简短总结"""
        day_master = data.get('day_master', '')
        strength = data.get('strength', '中和')
        
        strength_desc = {
            '身旺': '能量充沛，适合主动出击',
            '身弱': '需要借力，适合稳扎稳打',
            '中和': '平衡稳定，顺势而为'
        }
        
        return f"日主{day_master}，{strength_desc.get(strength, '')}。把握机遇，顺势发展。"
    
    def _format_shishen_distribution(self, distribution: Dict[str, int]) -> str:
        """格式化十神分布"""
        if not distribution:
            return "十神分布未知"
        
        items = [f"{god}{count}个" for god, count in distribution.items() if count > 0]
        return "，".join(items) if items else "十神分布均衡"
    
    def _format_shensha(self, shensha_list: List) -> str:
        """格式化神煞信息"""
        if not shensha_list:
            return "无明显神煞"
        
        # 按吉凶分类
        ji_shen = []
        xiong_sha = []
        
        for ss in shensha_list:
            if hasattr(ss, 'type'):
                if ss.type == '吉星':
                    ji_shen.append(ss.name)
                else:
                    xiong_sha.append(ss.name)
            elif isinstance(ss, dict):
                if ss.get('type') == '吉星':
                    ji_shen.append(ss.get('name', ''))
                else:
                    xiong_sha.append(ss.get('name', ''))
        
        result = []
        if ji_shen:
            result.append(f"吉神：{', '.join(ji_shen[:5])}")
        if xiong_sha:
            result.append(f"凶煞：{', '.join(xiong_sha[:5])}")
        
        return "；".join(result) if result else "无明显神煞"
    
    def _analyze_personality(self, data: Dict[str, Any]) -> str:
        """分析性格"""
        strength = data.get('strength', '中和')
        shishen = data.get('shishen', {})
        distribution = shishen.get('distribution', {}) if isinstance(shishen, dict) else {}
        
        # 基础性格（根据强弱）
        base = {
            '身旺': '你是个有主见、有能力的人，做事果断，喜欢掌控局面',
            '身弱': '你是个善于借力、懂得合作的人，擅长与人沟通协调',
            '中和': '你是个性格平衡、适应力强的人，能屈能伸'
        }.get(strength, '你的性格比较平衡')
        
        # 补充性格（根据十神）
        if distribution:
            main_god = max(distribution.items(), key=lambda x: x[1])[0] if distribution else None
            if main_god and main_god in self.TEN_GOD_PERSONALITY:
                base += f"。{self.TEN_GOD_PERSONALITY[main_god]}"
        
        return base
    
    def _analyze_career(self, data: Dict[str, Any]) -> str:
        """分析事业财运"""
        yongshen = data.get('yongshen', {})
        yongshen_wuxing = yongshen.get('yongshen', '') if isinstance(yongshen, dict) else ''
        
        # 根据用神五行给出事业建议
        for wx, advice in self.WUXING_ADVICE.items():
            if wx in yongshen_wuxing:
                return f"适合从事{advice['career']}相关行业，{advice['direction']}方向发展更有利。"
        
        return "事业发展需把握时机，稳扎稳打，积累经验后再图大发展。"
    
    def _analyze_relationship(self, data: Dict[str, Any]) -> str:
        """分析感情婚姻"""
        shensha = data.get('shensha', [])
        
        has_taohua = False
        has_guchen = False
        
        for ss in shensha:
            name = ss.name if hasattr(ss, 'name') else ss.get('name', '')
            if '桃花' in name or '红鸾' in name or '天喜' in name:
                has_taohua = True
            if '孤辰' in name or '寡宿' in name:
                has_guchen = True
        
        if has_taohua:
            return "异性缘佳，感情机会多，但需注意选择，不要因冲动而错失良缘。"
        elif has_guchen:
            return "感情上可能会经历一些波折，但这也是成长的机会，晚婚反而更稳定。"
        else:
            return "感情运势平稳，顺其自然即可，遇到合适的人要主动把握。"
    
    def _analyze_health(self, data: Dict[str, Any]) -> str:
        """分析健康"""
        yongshen = data.get('yongshen', {})
        jishen = yongshen.get('jishen', '') if isinstance(yongshen, dict) else ''
        
        health_advice = {
            '木': '注意肝胆、眼睛健康，保持心情舒畅',
            '火': '注意心脏、血压健康，避免熬夜',
            '土': '注意脾胃、消化系统，饮食规律',
            '金': '注意呼吸系统、皮肤健康，多运动',
            '水': '注意肾脏、泌尿系统，多喝水'
        }
        
        for wx, advice in health_advice.items():
            if wx in jishen:
                return advice
        
        return "注意劳逸结合，保持规律作息，定期体检。"
    
    def _generate_advice(self, data: Dict[str, Any]) -> str:
        """生成开运建议"""
        yongshen = data.get('yongshen', {})
        yongshen_wuxing = yongshen.get('yongshen', '') if isinstance(yongshen, dict) else ''
        
        for wx, advice in self.WUXING_ADVICE.items():
            if wx in yongshen_wuxing:
                return f"幸运色：{advice['color']}；幸运方位：{advice['direction']}；幸运数字：{advice['number']}。{advice['advice']}"
        
        return "保持积极心态，多行善事，自然会有好运降临。"


class ZiweiInterpreter(AIInterpreter):
    """紫微斗数解读器"""
    
    def __init__(self):
        super().__init__(DivinationType.ZIWEI)
    
    def _generate_professional(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """生成专业版紫微分析"""
        result = {
            'title': '紫微斗数专业分析',
            'sections': []
        }
        
        # 命宫分析
        if 'ming_gong' in data:
            result['sections'].append({
                'name': '命宫分析',
                'content': f"命宫在{data['ming_gong']}",
                'theory': '命宫为紫微斗数之本，主一生格局'
            })
        
        # 五行局
        if 'wuxing_ju' in data:
            result['sections'].append({
                'name': '五行局',
                'content': f"定盘为{data['wuxing_ju']}",
                'theory': '五行局决定大限起运年龄'
            })
        
        return result
    
    def _generate_vernacular(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """生成大白话版解读"""
        return {
            'title': '通俗解读',
            'sections': [
                {'name': '整体运势', 'content': '紫微斗数显示您的命格稳定，把握机遇即可顺利发展。'}
            ]
        }
    
    def _generate_summary(self, data: Dict[str, Any]) -> str:
        return "命宫星曜配置良好，顺势而为即可。"


class LiuyaoInterpreter(AIInterpreter):
    """六爻解读器"""
    
    def __init__(self):
        super().__init__(DivinationType.LIUYAO)
    
    def _generate_professional(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """生成专业版六爻分析"""
        result = {
            'title': '六爻专业分析',
            'sections': []
        }
        
        if 'ben_gua' in data:
            result['sections'].append({
                'name': '本卦',
                'content': f"本卦：{data['ben_gua']}",
                'theory': '本卦代表事情的起因和现状'
            })
        
        if 'bian_gua' in data:
            result['sections'].append({
                'name': '变卦',
                'content': f"变卦：{data['bian_gua']}",
                'theory': '变卦代表事情的发展和结果'
            })
        
        return result
    
    def _generate_vernacular(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """生成大白话版解读"""
        return {
            'title': '通俗解读',
            'sections': [
                {'name': '卦象解读', 'content': '此卦显示事情发展向好，但需耐心等待时机。'}
            ]
        }
    
    def _generate_summary(self, data: Dict[str, Any]) -> str:
        return "卦象显示事情可成，但需把握时机。"


# 解读器工厂
class InterpreterFactory:
    """解读器工厂"""
    
    _interpreters = {
        DivinationType.BAZI: BaziInterpreter,
        DivinationType.ZIWEI: ZiweiInterpreter,
        DivinationType.LIUYAO: LiuyaoInterpreter,
    }
    
    @classmethod
    def get(cls, divination_type: DivinationType) -> AIInterpreter:
        """获取对应的解读器"""
        interpreter_class = cls._interpreters.get(divination_type)
        if interpreter_class:
            return interpreter_class()
        raise ValueError(f"不支持的占卜类型: {divination_type}")
    
    @classmethod
    def register(cls, divination_type: DivinationType, interpreter_class):
        """注册新的解读器"""
        cls._interpreters[divination_type] = interpreter_class


# 便捷函数
def interpret_bazi(data: Dict[str, Any]) -> InterpretationResult:
    """解读八字"""
    interpreter = BaziInterpreter()
    return interpreter.interpret(data)


def interpret_ziwei(data: Dict[str, Any]) -> InterpretationResult:
    """解读紫微"""
    interpreter = ZiweiInterpreter()
    return interpreter.interpret(data)


def interpret_liuyao(data: Dict[str, Any]) -> InterpretationResult:
    """解读六爻"""
    interpreter = LiuyaoInterpreter()
    return interpreter.interpret(data)


def get_interpreter(divination_type: str) -> AIInterpreter:
    """根据类型字符串获取解读器"""
    type_map = {
        'bazi': DivinationType.BAZI,
        'ziwei': DivinationType.ZIWEI,
        'liuyao': DivinationType.LIUYAO,
        'qimen': DivinationType.QIMEN,
        'daliuren': DivinationType.DALIUREN,
        'meihua': DivinationType.MEIHUA,
        'tarot': DivinationType.TAROT,
    }
    dtype = type_map.get(divination_type.lower())
    if dtype:
        return InterpreterFactory.get(dtype)
    raise ValueError(f"不支持的占卜类型: {divination_type}")

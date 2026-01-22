"""
伦理约束过滤器
实现年龄相关的内容过滤，保护未成年人

移植自 Y-AI-Fortune/ethics_filter.py
"""

from typing import Dict, Any, List
import logging

logger = logging.getLogger(__name__)


class EthicsFilter:
    """伦理约束过滤器"""
    
    def __init__(self):
        # 敏感词汇映射表（18岁以下禁用）
        self.sensitive_marriage_terms = [
            "配偶", "婚姻", "恋爱", "结婚", "老公", "老婆", "夫妻", "情感",
            "桃花", "正缘", "偏缘", "婚恋", "感情", "另一半", "伴侣"
        ]
        
        # 替换词汇表（未成年人适用）
        self.replacement_terms = {
            "配偶星": "人际关系星",
            "配偶宫": "人际宫位", 
            "婚姻": "人际交往",
            "恋爱": "友谊发展",
            "感情": "情感管理",
            "桃花": "人缘",
            "正缘": "重要朋友",
            "另一半": "好朋友"
        }
        
        # 年龄段适用的分析模板
        self.age_templates = {
            "minor": {
                "ten_gods_focus": {
                    "比肩": "兄弟姐妹关系、同伴友谊",
                    "劫财": "竞争意识、团队合作", 
                    "食神": "创造力、艺术天赋",
                    "伤官": "表达能力、创新思维",
                    "正财": "理财意识、勤俭节约",
                    "偏财": "机遇把握、灵活思维",
                    "正官": "纪律性、责任感",
                    "七杀": "挑战精神、领导潜质",
                    "正印": "学习能力、知识吸收",
                    "偏印": "独特思维、专业特长"
                },
                "excluded": ["配偶星相关分析", "婚恋时机", "桃花运势"]
            },
            "student": {
                "focus": ["学业深造", "专业选择", "能力培养"],
                "caution": ["婚姻时机", "生育计划"]
            },
            "adult": {
                "full_analysis": ["事业", "婚恋", "财运", "健康"],
                "focus": ["人生规划", "家庭建设"]
            },
            "mature": {
                "focus": ["健康养生", "家庭和谐", "财富传承"],
                "avoid": ["激进建议", "重大变动"]
            }
        }
    
    def get_life_stage(self, age: int) -> str:
        """根据年龄获取人生阶段"""
        if age < 18:
            return "minor"
        elif age < 25:
            return "student"
        elif age < 50:
            return "adult"
        else:
            return "mature"
    
    def filter_content(
        self, 
        content: Dict[str, Any], 
        age: int
    ) -> Dict[str, Any]:
        """
        根据年龄过滤分析内容
        
        Args:
            content: 原始分析内容
            age: 年龄
            
        Returns:
            过滤后的内容
        """
        try:
            life_stage = self.get_life_stage(age)
            
            if life_stage == "minor":
                return self._filter_minor_content(content, age)
            elif life_stage == "student":
                return self._filter_student_content(content, age)
            else:
                return self._add_disclaimers(content, age, life_stage)
                
        except Exception as e:
            logger.error(f"内容过滤失败: {str(e)}")
            return content
    
    def check_minor(self, age: int) -> Dict[str, Any]:
        """
        检查是否为未成年人
        
        Args:
            age: 年龄
            
        Returns:
            检查结果
        """
        if age < 18:
            return {
                "is_minor": True,
                "age": age,
                "message": "根据相关规定，未成年人命理咨询需要监护人陪同。我们为您提供积极正面的指导建议。",
                "guidance": "注重学习成长，培养良好品格，未来可期。"
            }
        else:
            return {
                "is_minor": False,
                "age": age,
                "can_proceed": True
            }
    
    def _filter_minor_content(self, content: Dict[str, Any], age: int) -> Dict[str, Any]:
        """过滤未成年人不适宜内容"""
        filtered = content.copy()
        
        # 移除婚恋相关分析
        keys_to_remove = ["婚恋分析", "配偶分析", "桃花运势", "marriage", "love_fortune"]
        for key in keys_to_remove:
            if key in filtered:
                del filtered[key]
        
        # 替换敏感词汇
        filtered = self._replace_sensitive_terms(filtered)
        
        # 添加未成年人专用分析
        filtered["minor_analysis"] = self._generate_minor_analysis(age)
        
        # 添加伦理声明
        filtered["ethics_notice"] = {
            "age_group": f"{age}岁（未成年人）",
            "focus_areas": ["学业发展", "健康成长", "兴趣培养"],
            "excluded_areas": ["婚恋", "配偶", "投资等成人话题"],
            "note": "命理服务生活，需契合人生阶段"
        }
        
        return filtered
    
    def _replace_sensitive_terms(self, content: Dict[str, Any]) -> Dict[str, Any]:
        """替换敏感词汇"""
        def replace_in_value(value):
            if isinstance(value, str):
                for sensitive, replacement in self.replacement_terms.items():
                    value = value.replace(sensitive, replacement)
                return value
            elif isinstance(value, dict):
                return {k: replace_in_value(v) for k, v in value.items()}
            elif isinstance(value, list):
                return [replace_in_value(item) for item in value]
            else:
                return value
        
        return replace_in_value(content)
    
    def _generate_minor_analysis(self, age: int) -> Dict[str, Any]:
        """生成未成年人专用分析内容"""
        return {
            "learning_ability": {
                "description": "学习吸收能力分析",
                "focus": ["知识理解深度", "创造表达能力", "艺术天赋发挥"],
                "suggestion": "根据五行特点选择适合的学科方向"
            },
            "character_development": {
                "description": "性格培养重点",
                "aspects": ["全面发展", "优势发挥", "弱点改善"],
                "suggestion": "培养良好品格，建立自信心"
            },
            "health_guidance": {
                "description": "健康成长指导",
                "aspects": ["体质特点", "饮食建议", "运动方向"],
                "suggestion": "养成良好的生活习惯"
            },
            "family_relations": {
                "description": "家庭关系分析",
                "aspects": ["父母关系", "同辈关系", "师长缘分"],
                "suggestion": "培养良好的沟通能力"
            },
            "future_potential": {
                "description": "未来发展潜质",
                "aspects": ["天赋方向", "兴趣培养", "成长建议"],
                "suggestion": "发掘潜能，全面发展"
            }
        }
    
    def _filter_student_content(self, content: Dict[str, Any], age: int) -> Dict[str, Any]:
        """过滤学业期的内容"""
        filtered = content.copy()
        
        # 添加学业期特别提醒
        filtered["student_notice"] = {
            "age": age,
            "stage": "学业期",
            "priority": "学业为重，感情分析仅供参考",
            "suggestions": [
                "优先完成学业目标",
                "理性对待感情问题",
                "注重个人能力提升",
                "为未来发展打好基础"
            ]
        }
        
        return filtered
    
    def _add_disclaimers(self, content: Dict[str, Any], age: int, stage: str) -> Dict[str, Any]:
        """为成年人分析添加声明"""
        content["disclaimer"] = {
            "age_group": f"{age}岁成年人",
            "stage": stage,
            "nature": "趋势参考，非绝对定论",
            "usage": "结合个人实际情况，理性参考",
            "note": "命运趋势可通过努力和选择改变"
        }
        
        return content
    
    def validate_content(self, text: str, age: int) -> Dict[str, Any]:
        """验证内容的年龄适宜性"""
        issues = []
        
        if age < 18:
            for term in self.sensitive_marriage_terms:
                if term in text:
                    issues.append(f"包含不适合未成年人的词汇：{term}")
        
        return {
            "is_appropriate": len(issues) == 0,
            "issues": issues,
            "age_requirement": "18岁以上" if issues else "全年龄适用"
        }
    
    def get_age_appropriate_advice(self, age: int, ten_god: str) -> str:
        """获取年龄适宜的十神建议"""
        if age < 18:
            return self.age_templates["minor"]["ten_gods_focus"].get(
                ten_god, "培养良好品格，全面发展"
            )
        else:
            return ""


# 全局实例
ethics_filter = EthicsFilter()


def filter_by_age(content: Dict[str, Any], age: int) -> Dict[str, Any]:
    """便捷函数：根据年龄过滤内容"""
    return ethics_filter.filter_content(content, age)


def check_minor(age: int) -> Dict[str, Any]:
    """便捷函数：检查是否为未成年人"""
    return ethics_filter.check_minor(age)


def validate_content(text: str, age: int) -> Dict[str, Any]:
    """便捷函数：验证内容适宜性"""
    return ethics_filter.validate_content(text, age)

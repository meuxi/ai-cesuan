"""
翻译服务
"""

from typing import Optional
from .glossary import get_translation, translate_text, build_glossary_text


class Translator:
    """翻译器"""
    
    SUPPORTED_LANGUAGES = ["en", "ja", "ko", "zh-TW"]
    
    LANGUAGE_NAMES = {
        "en": "英文",
        "ja": "日文",
        "ko": "韩文",
        "zh": "简体中文",
        "zh-TW": "繁體中文",
    }
    
    def __init__(self, default_lang: str = "zh"):
        self.default_lang = default_lang
    
    def translate_term(self, term: str, target_lang: str) -> str:
        """翻译单个术语"""
        if target_lang == "zh" or target_lang not in self.SUPPORTED_LANGUAGES:
            return term
        
        translation = get_translation(term, target_lang)
        return translation if translation else term
    
    def translate(self, text: str, target_lang: str) -> str:
        """翻译文本中的术语"""
        if target_lang == "zh" or target_lang not in self.SUPPORTED_LANGUAGES:
            return text
        
        return translate_text(text, target_lang)
    
    def get_glossary(self, target_lang: str) -> str:
        """获取术语表（用于AI提示词）"""
        if target_lang == "zh" or target_lang not in self.SUPPORTED_LANGUAGES:
            return ""
        
        return build_glossary_text(target_lang)
    
    def get_language_name(self, lang_code: str) -> str:
        """获取语言名称"""
        return self.LANGUAGE_NAMES.get(lang_code, lang_code)
    
    def build_translation_prompt(self, target_lang: str) -> str:
        """
        构建翻译提示词（用于指导AI输出特定语言）
        
        Args:
            target_lang: 目标语言代码
        
        Returns:
            提示词文本
        """
        if target_lang == "zh" or target_lang not in self.SUPPORTED_LANGUAGES:
            return ""
        
        lang_name = self.get_language_name(target_lang)
        glossary = self.get_glossary(target_lang)
        
        # 繁体中文特殊处理
        if target_lang == "zh-TW":
            prompt = f"""
輸出語言要求：請用{lang_name}撰寫最終回答。
分析與理解過程以中文進行，術語請按下表轉換為繁體字。

{glossary}
"""
        else:
            prompt = f"""
输出语言要求：请用{lang_name}撰写最终回答。
分析与理解过程以中文进行，术语翻译按下表执行，首次出现请保留中文括注。

{glossary}
"""
        return prompt.strip()

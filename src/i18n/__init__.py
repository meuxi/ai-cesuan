"""
多语言支持模块
参考 zhanwen 项目的 i18n 设计
"""

from .glossary import TERMINOLOGY_GLOSSARY, get_translation, translate_text
from .translator import Translator

__all__ = [
    "TERMINOLOGY_GLOSSARY",
    "get_translation",
    "translate_text",
    "Translator",
]

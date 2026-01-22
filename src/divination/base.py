"""
占卜基类模块 - 定义占卜类型的元类和工厂模式

所有占卜类型都需要继承DivinationFactory并设置divination_type属性，
系统会自动注册到占卜类型映射表中。
"""
from src.models import DivinationBody
from typing import Optional


class MetaDivination(type):
    """
    占卜元类 - 自动注册占卜类型
    
    当子类定义divination_type属性时，会自动将其注册到divination_map中。
    """
    divination_map = {}

    def __init__(cls, name, bases, attrs):
        super().__init__(name, bases, attrs)
        if hasattr(cls, 'divination_type'):
            MetaDivination.divination_map[cls.divination_type] = cls


class DivinationFactory(metaclass=MetaDivination):
    """
    占卜工厂基类 - 所有占卜类型的基类
    
    子类需要:
        1. 设置 divination_type 类属性（如 'xiaoliu', 'tarot' 等）
        2. 重写 build_prompt 方法返回用户prompt和系统prompt
    
    Example:
        class TarotDivination(DivinationFactory):
            divination_type = 'tarot'
            
            def build_prompt(self, body: DivinationBody) -> tuple[str, str]:
                return user_prompt, system_prompt
    """

    @staticmethod
    def get(divination_type: str) -> Optional["DivinationFactory"]:
        """
        获取指定类型的占卜实例
        
        Args:
            divination_type: 占卜类型标识符
        
        Returns:
            对应类型的占卜实例，未找到返回None
        """
        cls = MetaDivination.divination_map.get(divination_type)
        if cls is None:
            return
        return cls()

    def build_prompt(self, divination_body: DivinationBody) -> tuple[str, str]:
        """
        构建占卜prompt（需子类重写）
        
        Args:
            divination_body: 占卜请求体
        
        Returns:
            tuple[str, str]: (用户prompt, 系统prompt)
        """
        return '', ''

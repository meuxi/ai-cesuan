"""诸葛神算服务 - 从ASP源码完整移植

算法说明：
1. 用户输入三个汉字
2. 通过AI计算每个汉字的笔画数
3. 取每个笔画数的个位数（0改为1）
4. 三个个位数组成三位数
5. 如果>=384则减384，循环直到<384
6. 根据签号查询诸葛神数384爻，结合AI生成解签
"""

import json
from pathlib import Path
from typing import Optional, Tuple


class ZhugeService:
    """诸葛神算服务"""
    
    def __init__(self):
        self.data_dir = Path(__file__).parent / "data"
        self._zhuge_data = []  # 诸葛神数384爻
        self._load_data()
    
    def _load_data(self):
        """加载数据"""
        # 加载诸葛神数
        zhuge_file = self.data_dir / "zhuge_384.json"
        if zhuge_file.exists():
            with open(zhuge_file, 'r', encoding='utf-8-sig') as f:
                self._zhuge_data = json.load(f)
    
    async def get_bihua_from_ai(self, char: str) -> int:
        """通过AI获取单个汉字的笔画数
        
        Args:
            char: 单个汉字
            
        Returns:
            笔画数
        """
        # 此方法将由路由层调用AI服务来实现
        # 这里返回占位值，实际笔画由调用方通过AI获取
        return 0
    
    def calculate_qian_number(self, char1: str, char2: str, char3: str) -> int:
        """根据三个汉字计算签号
        
        算法：
        1. 取每个字笔画数的个位（0改为1）
        2. 组成三位数
        3. 若>=384则减384，循环直到<384
        4. 若结果为0则改为384
        
        Args:
            char1: 第一个汉字
            char2: 第二个汉字
            char3: 第三个汉字
            
        Returns:
            签号(1-384)
        """
        # 获取笔画并取个位
        b1 = self.get_bihua(char1) % 10
        b2 = self.get_bihua(char2) % 10
        b3 = self.get_bihua(char3) % 10
        
        # 0改为1
        if b1 == 0:
            b1 = 1
        if b2 == 0:
            b2 = 1
        if b3 == 0:
            b3 = 1
        
        # 组成三位数
        number = int(f"{b1}{b2}{b3}")
        
        # 若>=384则减384
        while number >= 384:
            number -= 384
        
        # 若结果为0则改为384
        if number == 0:
            number = 384
        
        return number
    
    def divine(self, text: str) -> dict:
        """诸葛神算占卜
        
        Args:
            text: 用户输入的三个汉字
            
        Returns:
            占卜结果
        """
        # 只取前三个字符
        chars = list(text.replace(" ", ""))[:3]
        
        if len(chars) < 3:
            return {
                "success": False,
                "error": "请输入三个汉字"
            }
        
        char1, char2, char3 = chars[0], chars[1], chars[2]
        
        # 获取笔画
        b1 = self.get_bihua(char1)
        b2 = self.get_bihua(char2)
        b3 = self.get_bihua(char3)
        
        # 计算签号
        qian_number = self.calculate_qian_number(char1, char2, char3)
        
        # 格式化签号为三位数
        qian_id = str(qian_number).zfill(3)
        
        # 查询签文
        result = self._get_zhuge_by_number(qian_number)
        
        return {
            "success": True,
            "input": {
                "char1": char1,
                "char2": char2,
                "char3": char3,
                "bihua1": b1,
                "bihua2": b2,
                "bihua3": b3
            },
            "qian_number": qian_number,
            "qian_id": qian_id,
            "title": result.get("title", f"第{qian_number}签"),
            "content": result.get("content", "签文数据待补充")
        }
    
    def _get_zhuge_by_number(self, number: int) -> dict:
        """根据签号获取签文"""
        for item in self._zhuge_data:
            if item.get("number") == number or item.get("id") == number:
                return item
        return {"title": f"第{number}签", "content": "签文数据待补充"}
    
    def get_all(self) -> list:
        """获取所有384爻"""
        return self._zhuge_data


# 单例
zhuge_service = ZhugeService()

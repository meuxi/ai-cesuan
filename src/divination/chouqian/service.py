"""抽签服务"""
import json
import random
from pathlib import Path
from typing import List, Dict
from .models import ChouqianResult


QIAN_TYPES = {
    "guanyin": {"name": "观音灵签", "count": 100, "has_image": True},
    "guandi": {"name": "关帝灵签", "count": 100, "has_image": True},
    "lvzu": {"name": "吕祖灵签", "count": 100, "has_image": True},
    "tianhou": {"name": "天后灵签", "count": 60, "has_image": True},
    "huangdaxian": {"name": "黄大仙灵签", "count": 100, "has_image": False},
    "zhuge": {"name": "诸葛神算", "count": 384, "has_image": False},
}


class ChouqianService:
    """抽签服务类"""
    
    def __init__(self):
        self.data_dir = Path(__file__).parent / "data"
        self._data: Dict[str, List[ChouqianResult]] = {}
        self._load_data()
    
    def _load_data(self):
        """加载所有签文数据"""
        for qian_type in QIAN_TYPES.keys():
            file_path = self.data_dir / f"{qian_type}.json"
            if file_path.exists():
                with open(file_path, 'r', encoding='utf-8-sig') as f:
                    data = json.load(f)
                    results = []
                    for item in data:
                        # 兼容处理：观音签使用jieqian字段作为content
                        if 'content' not in item and 'jieqian' in item:
                            item['content'] = item['jieqian']
                        # 确保content字段存在
                        if 'content' not in item:
                            item['content'] = item.get('shiyi', '') or item.get('title', '')
                        results.append(ChouqianResult(**item))
                    self._data[qian_type] = results
    
    def draw(self, qian_type: str) -> ChouqianResult:
        """抽签"""
        if qian_type not in self._data:
            raise ValueError(f"不支持的签类型: {qian_type}")
        
        data = self._data[qian_type]
        if not data:
            raise ValueError(f"{QIAN_TYPES[qian_type]['name']}数据未加载")
        
        return random.choice(data)
    
    def get_by_number(self, qian_type: str, number: int) -> ChouqianResult:
        """根据签号获取签文"""
        if qian_type not in self._data:
            raise ValueError(f"不支持的签类型: {qian_type}")
        
        for item in self._data[qian_type]:
            if item.number == number:
                return item
        
        raise ValueError(f"签号{number}不存在")
    
    def get_all(self, qian_type: str) -> List[ChouqianResult]:
        """获取所有签文"""
        if qian_type not in self._data:
            raise ValueError(f"不支持的签类型: {qian_type}")
        return self._data[qian_type]
    
    def get_types(self) -> Dict[str, dict]:
        """获取所有签类型"""
        return QIAN_TYPES


# 全局服务实例
chouqian_service = ChouqianService()

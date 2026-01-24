from typing import Optional


class MetaCacheClient(type):

    client_map = {}

    def __init__(cls, name, bases, attrs):
        super().__init__(name, bases, attrs)
        if hasattr(cls, '_type'):
            MetaCacheClient.client_map[cls._type] = cls


class CacheClientBase(metaclass=MetaCacheClient):

    @classmethod
    def store_token(cls, key: str, token: str, expire_seconds: int) -> None:
        return

    @classmethod
    def get_token(cls, key: str) -> Optional[str]:
        return None

    @classmethod
    def delete_token(cls, key: str) -> bool:
        """删除指定 key，返回是否删除成功"""
        return False

    @classmethod
    def check_rate_limit(cls, key: str, time_window_seconds: int, max_requests: int) -> None:
        return

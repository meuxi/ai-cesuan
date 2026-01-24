import logging
import ipaddress
import os
from typing import Optional

from fastapi import Request

from .cache import CacheClientFactory

_logger = logging.getLogger(__name__)

# 可信代理 IP 列表（生产环境应通过环境变量配置）
# 格式: 逗号分隔的 IP 或 CIDR，如 "10.0.0.0/8,172.16.0.0/12,192.168.0.0/16"
TRUSTED_PROXIES_ENV = os.getenv("TRUSTED_PROXIES", "")

# 默认信任的本地/私有网络（常见代理部署位置）
DEFAULT_TRUSTED_NETWORKS = [
    "127.0.0.0/8",      # localhost
    "10.0.0.0/8",       # 私有网络 A 类
    "172.16.0.0/12",    # 私有网络 B 类
    "192.168.0.0/16",   # 私有网络 C 类
    "::1/128",          # IPv6 localhost
    "fc00::/7",         # IPv6 私有地址
]


def _parse_trusted_proxies() -> list:
    """解析可信代理列表"""
    networks = []
    
    # 添加默认可信网络
    for cidr in DEFAULT_TRUSTED_NETWORKS:
        try:
            networks.append(ipaddress.ip_network(cidr, strict=False))
        except ValueError:
            pass
    
    # 添加环境变量配置的可信代理
    if TRUSTED_PROXIES_ENV:
        for proxy in TRUSTED_PROXIES_ENV.split(","):
            proxy = proxy.strip()
            if proxy:
                try:
                    networks.append(ipaddress.ip_network(proxy, strict=False))
                except ValueError:
                    _logger.warning(f"无效的可信代理配置: {proxy}")
    
    return networks


# 预解析可信代理列表
_trusted_networks = _parse_trusted_proxies()


def _is_trusted_proxy(ip: str) -> bool:
    """检查 IP 是否为可信代理"""
    try:
        addr = ipaddress.ip_address(ip)
        return any(addr in network for network in _trusted_networks)
    except ValueError:
        return False


def _validate_ip(ip: str) -> Optional[str]:
    """验证 IP 地址格式，返回规范化的 IP 或 None"""
    if not ip:
        return None
    
    # 去除空白和端口号
    ip = ip.strip().split(",")[0].strip()  # 取第一个 IP（X-Forwarded-For 可能有多个）
    
    # 去除可能的端口号（IPv4:port 或 [IPv6]:port）
    if ":" in ip and not ip.startswith("["):
        # 可能是 IPv4:port 格式
        parts = ip.rsplit(":", 1)
        if len(parts) == 2 and parts[1].isdigit():
            ip = parts[0]
    
    try:
        # 尝试解析为 IP 地址
        addr = ipaddress.ip_address(ip)
        return str(addr)
    except ValueError:
        return None


def get_real_ipaddr(request: Request) -> str:
    """
    获取真实客户端 IP 地址
    
    安全策略：
    1. 首先获取直连 IP（request.client.host）
    2. 只有当直连 IP 是可信代理时，才读取代理头
    3. 按优先级检查多个头：X-Real-IP > X-Forwarded-For > CF-Connecting-IP
    4. 验证 IP 格式，防止注入攻击
    
    Returns:
        验证后的客户端 IP 地址
    """
    # 获取直连 IP
    direct_ip = "127.0.0.1"
    if request.client and request.client.host:
        validated_direct = _validate_ip(request.client.host)
        if validated_direct:
            direct_ip = validated_direct
    
    # 如果直连 IP 不是可信代理，直接返回直连 IP（防止伪造）
    if not _is_trusted_proxy(direct_ip):
        return direct_ip
    
    # 按优先级检查代理头
    proxy_headers = [
        "x-real-ip",           # Nginx 设置的真实 IP
        "x-forwarded-for",     # 标准代理头（取第一个）
        "cf-connecting-ip",    # Cloudflare
        "true-client-ip",      # Akamai / Cloudflare Enterprise
    ]
    
    for header in proxy_headers:
        if header in request.headers:
            header_value = request.headers[header]
            
            # X-Forwarded-For 可能包含多个 IP，取第一个（最初客户端）
            if header == "x-forwarded-for":
                header_value = header_value.split(",")[0].strip()
            
            validated_ip = _validate_ip(header_value)
            if validated_ip:
                return validated_ip
    
    # 所有代理头都无效，返回直连 IP
    return direct_ip


def check_rate_limit(key: str, time_window_seconds: int, max_requests: int) -> None:
    cache_client = CacheClientFactory.get_client()
    cache_client.check_rate_limit(key, time_window_seconds, max_requests)

"""
Pytest 配置和通用 fixtures

使用方式：
    pytest tests/ -v
    pytest tests/test_validators.py -v
"""
import os
import sys
import pytest
from typing import Generator

# 确保项目根目录在 Python 路径中
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)


@pytest.fixture(scope="session")
def project_root() -> str:
    """返回项目根目录路径"""
    return PROJECT_ROOT


@pytest.fixture
def sample_birthday_data() -> dict:
    """示例生日数据"""
    return {
        "year": 2000,
        "month": 8,
        "day": 17,
        "hour": 14,
        "minute": 30,
        "gender": "男"
    }


@pytest.fixture
def sample_invalid_dates() -> list:
    """无效日期示例"""
    return [
        {"year": 1800, "month": 1, "day": 1},   # 年份过小
        {"year": 2200, "month": 1, "day": 1},   # 年份过大
        {"year": 2000, "month": 13, "day": 1},  # 月份无效
        {"year": 2000, "month": 2, "day": 30},  # 2月没有30号
        {"year": 2000, "month": 1, "day": -1},  # 日期为负
    ]


@pytest.fixture
def mock_env_vars(monkeypatch) -> Generator:
    """模拟环境变量"""
    test_vars = {
        "ENVIRONMENT": "test",
        "JWT_SECRET": "test_secret_key_for_testing_only_32chars",
    }
    for key, value in test_vars.items():
        monkeypatch.setenv(key, value)
    yield test_vars

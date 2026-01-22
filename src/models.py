from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class SettingsInfo(BaseModel):
    login_type: str
    user_name: str
    rate_limit: str
    user_rate_limit: str
    ad_client: str = ""
    ad_slot: str = ""
    enable_login: bool = False
    enable_rate_limit: bool = False
    default_api_base: str = ""
    default_model: str = ""
    purchase_url: str = ""


class OauthBody(BaseModel):
    login_type: str
    code: Optional[str]


class User(BaseModel):
    login_type: str
    user_name: str
    expire_at: float


class NewName(BaseModel):
    surname: str
    sex: str
    birthday: str
    new_name_prompt: str


class PlumFlower(BaseModel):
    num1: int
    num2: int


class Fate(BaseModel):
    name1: str
    name2: str


class DivinationBody(BaseModel):
    prompt: str
    prompt_type: str
    birthday: Optional[str] = None
    lunar_birthday: Optional[str] = None  # 农历生日字符串
    bazi_data: Optional[dict] = None  # 八字排盘数据（用于增强AI分析）
    new_name: Optional[NewName] = None
    plum_flower: Optional[PlumFlower] = None
    fate: Optional[Fate] = None
    # 塔罗牌占卜字段
    cards: Optional[List[Dict[str, Any]]] = None  # 抽取的牌 [{position, name, isReversed, meaning}, ...]
    spread: Optional[Dict[str, Any]] = None  # 牌阵信息 {code, name}
    master: Optional[Dict[str, Any]] = None  # 解读大师配置 {id, name, prompt, gamePrompt}
    # 多语言输出支持
    language: Optional[str] = None  # 目标语言: zh/zh-TW/en/ja/ko


class BirthdayBody(BaseModel):
    birthday: str = Field(example="2000-08-17 00:00:00")


class CommonResponse(BaseModel):
    content: str
    request_id: str

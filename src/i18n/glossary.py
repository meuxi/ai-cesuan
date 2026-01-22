"""
术语对照表
包含命理术语的多语言翻译
"""

from typing import Dict, Optional

# 术语对照表
TERMINOLOGY_GLOSSARY: Dict[str, Dict[str, str]] = {
    # 中英对照
    "zh-en": {
        # 小六壬六宫
        "大安": "Great Peace",
        "留连": "Lingering",
        "速喜": "Swift Joy",
        "赤口": "Red Mouth",
        "小吉": "Lesser Fortune",
        "空亡": "Void",
        
        # 五行
        "五行": "Five Elements",
        "木": "Wood",
        "火": "Fire",
        "土": "Earth",
        "金": "Metal",
        "水": "Water",
        "相生": "Generating",
        "相克": "Overcoming",
        
        # 六神
        "青龙": "Azure Dragon",
        "朱雀": "Vermilion Bird",
        "勾陈": "Gou Chen",
        "腾蛇": "Soaring Snake",
        "白虎": "White Tiger",
        "玄武": "Black Tortoise",
        "六合": "Six Harmony",
        
        # 八字
        "八字": "BaZi / Four Pillars",
        "四柱": "Four Pillars",
        "年柱": "Year Pillar",
        "月柱": "Month Pillar",
        "日柱": "Day Pillar",
        "时柱": "Hour Pillar",
        "天干": "Heavenly Stems",
        "地支": "Earthly Branches",
        "日主": "Day Master",
        "用神": "Useful God",
        "喜神": "Favorable God",
        "忌神": "Unfavorable God",
        "大运": "Major Luck Cycle",
        "流年": "Annual Luck",
        
        # 十神
        "正官": "Direct Officer",
        "七杀": "Seven Killings",
        "正财": "Direct Wealth",
        "偏财": "Indirect Wealth",
        "正印": "Direct Seal",
        "偏印": "Indirect Seal",
        "食神": "Eating God",
        "伤官": "Hurting Officer",
        "比肩": "Shoulder to Shoulder",
        "劫财": "Rob Wealth",
        
        # 吉凶
        "大吉": "Very Auspicious",
        "中吉": "Moderately Auspicious",
        "小吉": "Slightly Auspicious",
        "大凶": "Very Inauspicious",
        "中凶": "Moderately Inauspicious",
        "小凶": "Slightly Inauspicious",
        
        # 六爻
        "六爻": "Six Lines",
        "本卦": "Original Hexagram",
        "变卦": "Changed Hexagram",
        "世爻": "Self Line",
        "应爻": "Response Line",
        "用爻": "Active Line",
        
        # 塔罗
        "塔罗牌": "Tarot Cards",
        "大阿尔卡那": "Major Arcana",
        "小阿尔卡那": "Minor Arcana",
        "正位": "Upright",
        "逆位": "Reversed",
        "牌阵": "Spread",
    },
    
    # 中日对照
    "zh-ja": {
        "大安": "大安（たいあん）",
        "留连": "留連（りゅうれん）",
        "速喜": "速喜（そっき）",
        "赤口": "赤口（しゃっこう）",
        "小吉": "小吉（しょうきち）",
        "空亡": "空亡（くうぼう）",
        
        "五行": "五行（ごぎょう）",
        "木": "木（もく）",
        "火": "火（か）",
        "土": "土（ど）",
        "金": "金（きん）",
        "水": "水（すい）",
        
        "青龙": "青龍（せいりゅう）",
        "朱雀": "朱雀（すざく）",
        "勾陈": "勾陳（こうちん）",
        "腾蛇": "騰蛇（とうだ）",
        "白虎": "白虎（びゃっこ）",
        "玄武": "玄武（げんぶ）",
        
        "八字": "四柱推命（しちゅうすいめい）",
        "大运": "大運（だいうん）",
        "流年": "流年（りゅうねん）",
    },
    
    # 中韩对照
    "zh-ko": {
        "大安": "대안",
        "留连": "유련",
        "速喜": "속희",
        "赤口": "적구",
        "小吉": "소길",
        "空亡": "공망",
        
        "五行": "오행",
        "木": "목",
        "火": "화",
        "土": "토",
        "金": "금",
        "水": "수",
        
        "青龙": "청룡",
        "朱雀": "주작",
        "勾陈": "구진",
        "腾蛇": "등사",
        "白虎": "백호",
        "玄武": "현무",
        
        "八字": "사주",
        "大运": "대운",
        "流年": "유년",
    },
    
    # 简繁对照
    "zh-zh-TW": {
        # 小六壬六宫
        "大安": "大安",
        "留连": "留連",
        "速喜": "速喜",
        "赤口": "赤口",
        "小吉": "小吉",
        "空亡": "空亡",
        
        # 五行
        "五行": "五行",
        "木": "木",
        "火": "火",
        "土": "土",
        "金": "金",
        "水": "水",
        "相生": "相生",
        "相克": "相剋",
        
        # 六神
        "青龙": "青龍",
        "朱雀": "朱雀",
        "勾陈": "勾陳",
        "腾蛇": "騰蛇",
        "白虎": "白虎",
        "玄武": "玄武",
        "六合": "六合",
        
        # 八字
        "八字": "八字",
        "四柱": "四柱",
        "年柱": "年柱",
        "月柱": "月柱",
        "日柱": "日柱",
        "时柱": "時柱",
        "天干": "天干",
        "地支": "地支",
        "日主": "日主",
        "用神": "用神",
        "喜神": "喜神",
        "忌神": "忌神",
        "大运": "大運",
        "流年": "流年",
        
        # 十神
        "正官": "正官",
        "七杀": "七殺",
        "正财": "正財",
        "偏财": "偏財",
        "正印": "正印",
        "偏印": "偏印",
        "食神": "食神",
        "伤官": "傷官",
        "比肩": "比肩",
        "劫财": "劫財",
        
        # 吉凶
        "大吉": "大吉",
        "中吉": "中吉",
        "小吉": "小吉",
        "大凶": "大凶",
        "中凶": "中凶",
        "小凶": "小凶",
        
        # 六爻
        "六爻": "六爻",
        "本卦": "本卦",
        "变卦": "變卦",
        "世爻": "世爻",
        "应爻": "應爻",
        "用爻": "用爻",
        
        # 塔罗
        "塔罗牌": "塔羅牌",
        "大阿尔卡那": "大阿爾卡那",
        "小阿尔卡那": "小阿爾卡那",
        "正位": "正位",
        "逆位": "逆位",
        "牌阵": "牌陣",
        
        # 紫微斗数
        "紫微斗数": "紫微斗數",
        "命宫": "命宮",
        "财帛宫": "財帛宮",
        "官禄宫": "官祿宮",
        "迁移宫": "遷移宮",
        "疾厄宫": "疾厄宮",
        
        # 梅花易数
        "梅花易数": "梅花易數",
        "体卦": "體卦",
        "用卦": "用卦",
        
        # 奇门遁甲
        "奇门遁甲": "奇門遁甲",
        "天盘": "天盤",
        "地盘": "地盤",
        "人盘": "人盤",
        "神盘": "神盤",
    },
}


def get_translation(term: str, target_lang: str = "en") -> Optional[str]:
    """
    获取术语翻译
    
    Args:
        term: 中文术语
        target_lang: 目标语言 (en/ja/ko)
    
    Returns:
        翻译结果，未找到则返回 None
    """
    lang_key = f"zh-{target_lang}"
    glossary = TERMINOLOGY_GLOSSARY.get(lang_key, {})
    return glossary.get(term)


def translate_text(text: str, target_lang: str = "en") -> str:
    """
    翻译文本中的术语
    
    Args:
        text: 包含术语的文本
        target_lang: 目标语言
    
    Returns:
        替换术语后的文本
    """
    lang_key = f"zh-{target_lang}"
    glossary = TERMINOLOGY_GLOSSARY.get(lang_key, {})
    
    result = text
    for zh_term, translation in glossary.items():
        if zh_term in result:
            # 首次出现保留中文括注
            if result.count(zh_term) == 1:
                result = result.replace(zh_term, f"{translation}（{zh_term}）", 1)
            else:
                # 后续出现只用翻译
                first_occurrence = True
                new_result = ""
                remaining = result
                while zh_term in remaining:
                    idx = remaining.index(zh_term)
                    new_result += remaining[:idx]
                    if first_occurrence:
                        new_result += f"{translation}（{zh_term}）"
                        first_occurrence = False
                    else:
                        new_result += translation
                    remaining = remaining[idx + len(zh_term):]
                new_result += remaining
                result = new_result
    
    return result


def build_glossary_text(target_lang: str = "en") -> str:
    """
    构建术语对照表文本（用于AI提示词）
    
    Args:
        target_lang: 目标语言
    
    Returns:
        格式化的术语表文本
    """
    lang_key = f"zh-{target_lang}"
    glossary = TERMINOLOGY_GLOSSARY.get(lang_key, {})
    
    if not glossary:
        return ""
    
    # 繁体中文使用繁体标题
    if target_lang == "zh-TW":
        lines = ["術語對照表："]
    else:
        lines = ["术语对照表："]
    
    for zh, trans in glossary.items():
        lines.append(f"{zh}={trans}")
    
    return "\n".join(lines)

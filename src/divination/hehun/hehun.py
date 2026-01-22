"""合婚算法 - 从PHP移植"""

# 九宫名称
JIUGONG = {
    1: "坎宫", 2: "坤宫", 3: "震宫", 4: "巽宫",
    5: "中宫", 6: "乾宫", 7: "兑宫", 8: "艮宫", 9: "离宫"
}

# 九宫五行
JIUGONG_WUXING = {
    1: "水", 2: "土", 3: "木", 4: "木",
    6: "金", 7: "金", 8: "土", 9: "火"
}


def get_male_gong(year: int) -> int:
    """计算男命所属宫位
    算法: (100 - year后两位) % 9, 如果是5则改为2
    """
    x = year % 100
    r = 100 - x
    s = r % 9
    if s == 5:
        s = 2
    if s == 0:
        s = 9
    return s


def get_female_gong(year: int) -> int:
    """计算女命所属宫位
    算法: (year后两位 - 4) % 9, 如果是5则改为8
    """
    x = year % 100
    r = x - 4
    s = r % 9
    if s == 5:
        s = 8
    if s == 0:
        s = 9
    if s < 0:
        s += 9
    return s


def get_year_ganzhi(year: int) -> str:
    """获取年份干支"""
    tiangan = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
    dizhi = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
    
    gan_index = (year - 4) % 10
    zhi_index = (year - 4) % 12
    
    return tiangan[gan_index] + dizhi[zhi_index]


def analyze_hehun(male_year: int, female_year: int) -> dict:
    """分析合婚结果"""
    male_gong = get_male_gong(male_year)
    female_gong = get_female_gong(female_year)
    
    male_ganzhi = get_year_ganzhi(male_year)
    female_ganzhi = get_year_ganzhi(female_year)
    
    # 判断五行关系
    male_wuxing = JIUGONG_WUXING.get(male_gong, "土")
    female_wuxing = JIUGONG_WUXING.get(female_gong, "土")
    
    # 五行相生相克关系
    shengke = {
        ("木", "火"): "生", ("火", "土"): "生", ("土", "金"): "生",
        ("金", "水"): "生", ("水", "木"): "生",
        ("木", "土"): "克", ("土", "水"): "克", ("水", "火"): "克",
        ("火", "金"): "克", ("金", "木"): "克"
    }
    
    relation = shengke.get((male_wuxing, female_wuxing), "")
    if not relation:
        relation = shengke.get((female_wuxing, male_wuxing), "")
        if relation == "生":
            relation = "被生"
        elif relation == "克":
            relation = "被克"
    
    if male_wuxing == female_wuxing:
        relation = "比和"
    
    # 计算配对分数
    score = 60
    if relation == "生":
        score = 85
    elif relation == "被生":
        score = 80
    elif relation == "比和":
        score = 75
    elif relation == "克":
        score = 50
    elif relation == "被克":
        score = 55
    
    return {
        "male_year": male_year,
        "female_year": female_year,
        "male_ganzhi": male_ganzhi,
        "female_ganzhi": female_ganzhi,
        "male_gong": JIUGONG[male_gong],
        "female_gong": JIUGONG[female_gong],
        "male_wuxing": male_wuxing,
        "female_wuxing": female_wuxing,
        "relation": relation,
        "score": score
    }

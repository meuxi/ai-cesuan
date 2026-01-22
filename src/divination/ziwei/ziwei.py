"""紫微斗数算法 - 从PHP移植"""

# 地支对应
DIZHI = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
TIANGAN = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]


def liunum(gong: int, yaozhi: int) -> int:
    """计算六亲宫位号"""
    table = {
        1: {1: 2, 2: 4, 3: 5, 4: 1, 5: 3},
        2: {1: 3, 2: 2, 3: 1, 4: 4, 5: 5},
        3: {1: 1, 2: 5, 3: 2, 4: 3, 5: 4},
        4: {1: 5, 2: 3, 3: 4, 4: 2, 5: 1},
        5: {1: 4, 2: 1, 3: 3, 4: 5, 5: 2}
    }
    return table.get(gong, {}).get(yaozhi, 1)


def get_maxing(dizhi_index: int) -> tuple:
    """配驿马桃花
    返回: (驿马宫位, 桃花宫位)
    """
    if dizhi_index in [2, 6, 10]:  # 寅午戌
        return (7, 0)  # 申, 子
    elif dizhi_index in [0, 4, 8]:  # 子辰申
        return (6, 1)  # 巳, 丑
    elif dizhi_index in [3, 7, 11]:  # 卯未亥
        return (9, 4)  # 戌, 辰
    elif dizhi_index in [1, 5, 9]:  # 丑巳酉
        return (3, 10)  # 卯, 戌
    return (0, 0)


def get_lushen(tiangan_index: int) -> int:
    """配禄神
    返回禄神所在宫位(地支序号)
    """
    lu_table = {
        0: 1,   # 甲禄在寅
        1: 3,   # 乙禄在卯
        2: 4,   # 丙禄在巳
        3: 6,   # 丁禄在午
        4: 7,   # 戊禄在巳
        5: 6,   # 己禄在午
        6: 7,   # 庚禄在申
        7: 9,   # 辛禄在酉
        8: 10,  # 壬禄在亥
        9: 0    # 癸禄在子
    }
    return lu_table.get(tiangan_index, 0)


def get_guiren(tiangan_index: int) -> tuple:
    """配天乙贵人
    返回: (贵人1宫位, 贵人2宫位)
    """
    if tiangan_index in [3, 4]:  # 丁戊
        return (10, 0)  # 戌, 子
    elif tiangan_index in [1, 5, 7]:  # 乙己辛
        return (2, 8)  # 丑, 未
    elif tiangan_index in [2, 6]:  # 丙庚
        return (1, 9)  # 丑, 酉
    elif tiangan_index in [0, 9]:  # 甲癸
        return (6, 4)  # 未, 辰
    elif tiangan_index == 8:  # 壬
        return (3, 7)  # 卯, 未
    return (0, 0)


def get_tiangan_index(gan: str) -> int:
    """获取天干序号"""
    return TIANGAN.index(gan) if gan in TIANGAN else -1


def get_dizhi_index(zhi: str) -> int:
    """获取地支序号"""
    return DIZHI.index(zhi) if zhi in DIZHI else -1


def analyze_ziwei_stars(day_gan: str, day_zhi: str) -> dict:
    """分析紫微星曜
    根据日干支计算驿马、桃花、禄神、贵人等
    """
    gan_idx = get_tiangan_index(day_gan)
    zhi_idx = get_dizhi_index(day_zhi)
    
    maxing, taohua = get_maxing(zhi_idx)
    lushen = get_lushen(gan_idx)
    guiren1, guiren2 = get_guiren(gan_idx)
    
    return {
        "day_ganzhi": day_gan + day_zhi,
        "yima": DIZHI[maxing],
        "taohua": DIZHI[taohua],
        "lushen": DIZHI[lushen],
        "guiren": [DIZHI[guiren1], DIZHI[guiren2]]
    }

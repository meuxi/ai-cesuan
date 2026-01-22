"""
紫微斗数杂曜安置算法
补充iztro-py缺失的杂曜计算逻辑
"""

from typing import List, Dict, Any

# 地支列表
EARTHLY_BRANCHES = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']

# 天干列表
HEAVENLY_STEMS = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']

# 长生12神名称
CHANGSHENG_NAMES = ['长生', '沐浴', '冠带', '临官', '帝旺', '衰', '病', '死', '墓', '绝', '胎', '养']

# 博士12神名称
BOSHI_NAMES = ['博士', '力士', '青龙', '小耗', '将军', '奏书', '飞廉', '喜神', '病符', '大耗', '伏兵', '官府']

# 将前12神名称（流年神煞）
JIANGQIAN_NAMES = ['将星', '攀鞍', '岁驿', '息神', '华盖', '劫煞', '灾煞', '天煞', '指背', '咸池', '月煞', '亡神']

# 岁前12神名称（流年神煞）
SUIQIAN_NAMES = ['岁建', '晦气', '丧门', '贯索', '官符', '小耗', '大耗', '龙德', '白虎', '天德', '吊客', '病符']


def get_branch_index(branch: str) -> int:
    """获取地支索引"""
    try:
        return EARTHLY_BRANCHES.index(branch)
    except ValueError:
        return 0


def get_stem_index(stem: str) -> int:
    """获取天干索引"""
    try:
        return HEAVENLY_STEMS.index(stem)
    except ValueError:
        return 0


def calculate_changsheng12(five_element_class: str, palace_branches: List[str]) -> Dict[str, str]:
    """
    计算长生12神
    
    Args:
        five_element_class: 五行局（如"水二局"、"木三局"等）
        palace_branches: 各宫位的地支列表（按宫位顺序）
    
    Returns:
        {地支: 长生12神名称} 的映射
    """
    # 根据五行局确定长生起点
    # 水二局：长生在申
    # 木三局：长生在亥
    # 金四局：长生在巳
    # 土五局：长生在申
    # 火六局：长生在寅
    
    start_branches = {
        '水': '申', '木': '亥', '金': '巳', '土': '申', '火': '寅'
    }
    
    # 提取五行
    element = None
    for e in ['水', '木', '金', '土', '火']:
        if e in five_element_class:
            element = e
            break
    
    if not element:
        return {}
    
    start_branch = start_branches.get(element, '申')
    start_idx = get_branch_index(start_branch)
    
    result = {}
    for i, name in enumerate(CHANGSHENG_NAMES):
        branch_idx = (start_idx + i) % 12
        result[EARTHLY_BRANCHES[branch_idx]] = name
    
    return result


def calculate_boshi12(lucun_branch: str) -> Dict[str, str]:
    """
    计算博士12神
    从禄存所在宫位起博士，顺行
    
    Args:
        lucun_branch: 禄存所在地支
    
    Returns:
        {地支: 博士12神名称} 的映射
    """
    start_idx = get_branch_index(lucun_branch)
    
    result = {}
    for i, name in enumerate(BOSHI_NAMES):
        branch_idx = (start_idx + i) % 12
        result[EARTHLY_BRANCHES[branch_idx]] = name
    
    return result


def calculate_jiangqian12(year_branch: str) -> Dict[str, str]:
    """
    计算将前12神（流年神煞）
    将星起法：寅午戌年将星在午，申子辰年将星在子，巳酉丑年将星在酉，亥卯未年将星在卯
    
    Args:
        year_branch: 年支
    
    Returns:
        {地支: 将前12神名称} 的映射
    """
    # 将星起点
    jiangxing_map = {
        '寅': '午', '午': '午', '戌': '午',
        '申': '子', '子': '子', '辰': '子',
        '巳': '酉', '酉': '酉', '丑': '酉',
        '亥': '卯', '卯': '卯', '未': '卯'
    }
    
    start_branch = jiangxing_map.get(year_branch, '子')
    start_idx = get_branch_index(start_branch)
    
    result = {}
    for i, name in enumerate(JIANGQIAN_NAMES):
        branch_idx = (start_idx + i) % 12
        result[EARTHLY_BRANCHES[branch_idx]] = name
    
    return result


def calculate_suiqian12(year_branch: str) -> Dict[str, str]:
    """
    计算岁前12神（流年神煞）
    岁建起于年支所在宫位
    
    Args:
        year_branch: 年支
    
    Returns:
        {地支: 岁前12神名称} 的映射
    """
    start_idx = get_branch_index(year_branch)
    
    result = {}
    for i, name in enumerate(SUIQIAN_NAMES):
        branch_idx = (start_idx + i) % 12
        result[EARTHLY_BRANCHES[branch_idx]] = name
    
    return result


def calculate_adjective_stars(year_branch: str, lunar_month: int) -> Dict[str, List[str]]:
    """
    计算杂曜（按年支和月份安置）
    
    Args:
        year_branch: 年支
        lunar_month: 农历月份
    
    Returns:
        {地支: [杂曜名称列表]} 的映射
    """
    result = {branch: [] for branch in EARTHLY_BRANCHES}
    year_idx = get_branch_index(year_branch)
    
    # 红鸾（子年在卯，逆行）
    # 子年红鸾在卯，丑年在寅，寅年在丑...
    hongluan_idx = (3 - year_idx + 12) % 12
    result[EARTHLY_BRANCHES[hongluan_idx]].append('红鸾')
    
    # 天喜（红鸾对冲）
    tianxi_idx = (hongluan_idx + 6) % 12
    result[EARTHLY_BRANCHES[tianxi_idx]].append('天喜')
    
    # 天刑（按年支，子年在酉，顺行）
    tianxing_idx = (9 + year_idx) % 12  # 子年在酉
    result[EARTHLY_BRANCHES[tianxing_idx]].append('天刑')
    
    # 天姚（按年支，子年在丑，顺行）
    tianyao_idx = (1 + year_idx) % 12  # 子年在丑
    result[EARTHLY_BRANCHES[tianyao_idx]].append('天姚')
    
    # 解神（按年支，子年在申，顺行）
    jieshen_idx = (8 + year_idx) % 12  # 子年在申
    result[EARTHLY_BRANCHES[jieshen_idx]].append('解神')
    
    # 天巫（按年支，子年在巳，顺行）
    tianwu_idx = (5 + year_idx) % 12  # 子年在巳
    result[EARTHLY_BRANCHES[tianwu_idx]].append('天巫')
    
    # 天月（按年支安置）
    tianyue_positions = {
        '子': '戌', '丑': '巳', '寅': '辰', '卯': '寅',
        '辰': '未', '巳': '卯', '午': '亥', '未': '未',
        '申': '寅', '酉': '戌', '戌': '巳', '亥': '子'
    }
    tianyue_branch = tianyue_positions.get(year_branch, '子')
    result[tianyue_branch].append('天月')
    
    # 阴煞（按年支安置）
    yinsha_positions = {
        '寅': '子', '卯': '戌', '辰': '申', '巳': '午',
        '午': '辰', '未': '寅', '申': '子', '酉': '戌',
        '戌': '申', '亥': '午', '子': '辰', '丑': '寅'
    }
    yinsha_branch = yinsha_positions.get(year_branch, '子')
    result[yinsha_branch].append('阴煞')
    
    # 孤辰、寡宿（按年支三合局安置）
    guchen_gusu = {
        '寅': ('巳', '丑'), '卯': ('巳', '丑'), '辰': ('巳', '丑'),
        '巳': ('申', '辰'), '午': ('申', '辰'), '未': ('申', '辰'),
        '申': ('亥', '未'), '酉': ('亥', '未'), '戌': ('亥', '未'),
        '亥': ('寅', '戌'), '子': ('寅', '戌'), '丑': ('寅', '戌')
    }
    gc, gs = guchen_gusu.get(year_branch, ('寅', '戌'))
    result[gc].append('孤辰')
    result[gs].append('寡宿')
    
    # 截空（按年干安置，甲己年截空在申酉）
    # 这里简化处理，实际需要年干
    
    # 天空（按年支安置）
    tiankong_idx = (year_idx + 1) % 12
    result[EARTHLY_BRANCHES[tiankong_idx]].append('天空')
    
    # 旬空（需要年干支完整信息，这里简化）
    
    # 台辅、封诰（按年支安置）
    taifu_idx = (6 + year_idx) % 12  # 午位起
    result[EARTHLY_BRANCHES[taifu_idx]].append('台辅')
    
    fenggao_idx = (2 + year_idx) % 12  # 寅位起
    result[EARTHLY_BRANCHES[fenggao_idx]].append('封诰')
    
    # 天官、天福（按年干安置，需要年干，这里简化）
    
    # 三台、八座（按农历月安置）
    santai_idx = (lunar_month + 5) % 12  # 左辅起
    result[EARTHLY_BRANCHES[santai_idx]].append('三台')
    
    bazuo_idx = (10 - lunar_month) % 12  # 右弼起
    result[EARTHLY_BRANCHES[bazuo_idx]].append('八座')
    
    # 恩光、天贵（按日干安置，需要日干，这里省略）
    
    # 天才、天寿（按命宫和身宫安置，需要额外信息，这里省略）
    
    return result


def get_lucun_position(year_stem: str) -> str:
    """
    获取禄存所在地支
    
    Args:
        year_stem: 年干
    
    Returns:
        禄存所在地支
    """
    lucun_map = {
        '甲': '寅', '乙': '卯', '丙': '巳', '丁': '午',
        '戊': '巳', '己': '午', '庚': '申', '辛': '酉',
        '壬': '亥', '癸': '子'
    }
    return lucun_map.get(year_stem, '寅')


def apply_adjective_stars_to_palaces(
    palaces: List[Dict[str, Any]], 
    year_stem: str,
    year_branch: str, 
    lunar_month: int,
    five_element_class: str
) -> List[Dict[str, Any]]:
    """
    将杂曜应用到宫位
    
    Args:
        palaces: 宫位列表
        year_stem: 年干
        year_branch: 年支
        lunar_month: 农历月份
        five_element_class: 五行局
    
    Returns:
        更新后的宫位列表
    """
    # 计算各种杂曜
    adjective_stars = calculate_adjective_stars(year_branch, lunar_month)
    
    # 计算12神
    changsheng12 = calculate_changsheng12(five_element_class, [p.get('earthlyBranch', '') for p in palaces])
    lucun_branch = get_lucun_position(year_stem)
    boshi12 = calculate_boshi12(lucun_branch)
    jiangqian12 = calculate_jiangqian12(year_branch)
    suiqian12 = calculate_suiqian12(year_branch)
    
    # 应用到宫位
    for palace in palaces:
        branch = palace.get('earthlyBranch', '')
        
        # 添加杂曜到minorStars
        if branch in adjective_stars:
            for star_name in adjective_stars[branch]:
                palace['minorStars'].append({
                    "name": star_name,
                    "type": "auxiliary",
                    "brightness": "",
                    "mutagen": None
                })
        
        # 添加12神到extras
        if 'extras' not in palace:
            palace['extras'] = {}
        
        palace['extras']['changsheng12'] = changsheng12.get(branch, '')
        palace['extras']['boshi12'] = boshi12.get(branch, '')
        palace['extras']['jiangqian12'] = jiangqian12.get(branch, '')
        palace['extras']['suiqian12'] = suiqian12.get(branch, '')
    
    return palaces

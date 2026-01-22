"""
奇门遁甲用神系统
根据不同事类选取相应用神进行分析

基于 mingpan/docs/qimen-yongshen-guide.md 实现
"""

from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum


class ShiLei(Enum):
    """事类枚举"""
    QIUCAI = "求财"      # 财运、投资、经商
    HUNYIN = "婚姻"      # 恋爱、婚配、感情
    JIBING = "疾病"      # 健康、就医、康复
    CHUXING = "出行"     # 旅行、迁移、外出
    SUSONG = "诉讼"      # 官司、纠纷、争执
    KAOSHI = "考试"      # 考学、面试、竞争
    GONGZUO = "工作"     # 事业、职位、升迁
    SHIWU = "失物"       # 寻物、追回、遗失
    ZHIYE = "置业"       # 购房、投资、资产
    QIUGUAN = "求官"     # 仕途、权位、晋升
    YUNCHAN = "孕产"     # 怀孕、生育、母婴
    XUNREN = "寻人"      # 找人、联络、会面
    HEZUO = "合作"       # 合伙、谈判、签约
    QITA = "其他"        # 通用类型


@dataclass
class YongShenConfig:
    """用神配置"""
    zhu_yongshen: List[str]   # 主用神
    fu_yongshen: List[str]    # 辅用神
    description: str           # 说明


# 事类用神配置表
SHILEI_YONGSHEN_MAP: Dict[str, YongShenConfig] = {
    "求财": YongShenConfig(
        zhu_yongshen=["生门", "戊仪"],
        fu_yongshen=["开门", "日干"],
        description="财运、投资、经商"
    ),
    "婚姻": YongShenConfig(
        zhu_yongshen=["六合", "乙奇"],
        fu_yongshen=["开门", "太阴"],
        description="恋爱、婚配、感情"
    ),
    "疾病": YongShenConfig(
        zhu_yongshen=["天芮", "死门"],
        fu_yongshen=["日干", "时干"],
        description="健康、就医、康复"
    ),
    "出行": YongShenConfig(
        zhu_yongshen=["日干", "开门"],
        fu_yongshen=["马星", "太冲"],
        description="旅行、迁移、外出"
    ),
    "诉讼": YongShenConfig(
        zhu_yongshen=["开门", "庚仪"],
        fu_yongshen=["惊门", "日干"],
        description="官司、纠纷、争执"
    ),
    "考试": YongShenConfig(
        zhu_yongshen=["丁奇", "景门"],
        fu_yongshen=["天辅", "日干"],
        description="考学、面试、竞争"
    ),
    "工作": YongShenConfig(
        zhu_yongshen=["开门", "日干"],
        fu_yongshen=["生门", "值符"],
        description="事业、职位、升迁"
    ),
    "失物": YongShenConfig(
        zhu_yongshen=["玄武", "时干"],
        fu_yongshen=["六仪"],
        description="寻物、追回、遗失"
    ),
    "置业": YongShenConfig(
        zhu_yongshen=["生门", "戊仪"],
        fu_yongshen=["天盘戊", "日干"],
        description="购房、投资、资产"
    ),
    "求官": YongShenConfig(
        zhu_yongshen=["开门", "值符"],
        fu_yongshen=["日干", "景门"],
        description="仕途、权位、晋升"
    ),
    "孕产": YongShenConfig(
        zhu_yongshen=["天芮", "六合"],
        fu_yongshen=["日干", "太阴"],
        description="怀孕、生育、母婴"
    ),
    "寻人": YongShenConfig(
        zhu_yongshen=["时干", "日干"],
        fu_yongshen=["开门"],
        description="找人、联络、会面"
    ),
    "合作": YongShenConfig(
        zhu_yongshen=["日干", "时干"],
        fu_yongshen=["六合", "开门"],
        description="合伙、谈判、签约"
    ),
    "其他": YongShenConfig(
        zhu_yongshen=["日干", "时干"],
        fu_yongshen=["开门"],
        description="通用类型"
    ),
}

# 宫位五行
GONG_WUXING = {
    1: "水",  # 坎一宫
    2: "土",  # 坤二宫
    3: "木",  # 震三宫
    4: "木",  # 巽四宫
    5: "土",  # 中五宫
    6: "金",  # 乾六宫
    7: "金",  # 兑七宫
    8: "土",  # 艮八宫
    9: "火",  # 离九宫
}

# 宫位方位
GONG_FANGWEI = {
    1: "北",
    2: "西南",
    3: "东",
    4: "东南",
    5: "中",
    6: "西北",
    7: "西",
    8: "东北",
    9: "南",
}

# 月令五行旺相休囚死
YUELING_WANGXIANG = {
    "春": {"木": "旺", "火": "相", "土": "死", "金": "囚", "水": "休"},
    "夏": {"火": "旺", "土": "相", "金": "死", "水": "囚", "木": "休"},
    "秋": {"金": "旺", "水": "相", "木": "死", "火": "囚", "土": "休"},
    "冬": {"水": "旺", "木": "相", "火": "死", "土": "囚", "金": "休"},
    "四季": {"土": "旺", "金": "相", "水": "死", "木": "囚", "火": "休"},
}

# 旺相休囚死评分
WANGXIANG_SCORE = {
    "旺": 20,
    "相": 10,
    "休": 0,
    "囚": -10,
    "死": -15,
}

# 五行生克关系评分
WUXING_RELATION_SCORE = {
    "生": 5,    # 用神生日干
    "比": 0,    # 同五行相助
    "克": -5,   # 用神克日干
    "泄": -3,   # 日干生用神
    "耗": -5,   # 日干克用神
}


def get_season(month: int) -> str:
    """根据月份获取季节"""
    if month in [1, 2, 3]:
        return "春"
    elif month in [4, 5, 6]:
        return "夏"
    elif month in [7, 8, 9]:
        return "秋"
    else:
        return "冬"


def get_wangxiang(gong: int, month: int) -> Tuple[str, int]:
    """
    获取宫位的旺相休囚死状态
    
    Args:
        gong: 宫位 (1-9)
        month: 月份 (1-12)
    
    Returns:
        (状态, 评分)
    """
    season = get_season(month)
    gong_wuxing = GONG_WUXING.get(gong, "土")
    
    # 四季月特殊处理（3、6、9、12月末各18天为土旺）
    if month in [3, 6, 9, 12]:
        season = "四季"
    
    status = YUELING_WANGXIANG.get(season, {}).get(gong_wuxing, "休")
    score = WANGXIANG_SCORE.get(status, 0)
    
    return status, score


def get_wuxing_relation(yongshen_wuxing: str, rigan_wuxing: str) -> Tuple[str, int]:
    """
    获取用神与日干的五行关系
    
    Args:
        yongshen_wuxing: 用神所在宫位五行
        rigan_wuxing: 日干五行
    
    Returns:
        (关系, 评分)
    """
    # 五行生克关系
    sheng_map = {"木": "火", "火": "土", "土": "金", "金": "水", "水": "木"}
    ke_map = {"木": "土", "火": "金", "土": "水", "金": "木", "水": "火"}
    
    if yongshen_wuxing == rigan_wuxing:
        return "比", WUXING_RELATION_SCORE["比"]
    elif sheng_map.get(yongshen_wuxing) == rigan_wuxing:
        return "生", WUXING_RELATION_SCORE["生"]
    elif ke_map.get(yongshen_wuxing) == rigan_wuxing:
        return "克", WUXING_RELATION_SCORE["克"]
    elif sheng_map.get(rigan_wuxing) == yongshen_wuxing:
        return "泄", WUXING_RELATION_SCORE["泄"]
    elif ke_map.get(rigan_wuxing) == yongshen_wuxing:
        return "耗", WUXING_RELATION_SCORE["耗"]
    else:
        return "无", 0


class QimenYongShen:
    """奇门用神分析器"""
    
    def __init__(self):
        pass
    
    def get_yongshen_config(self, shi_lei: str) -> YongShenConfig:
        """获取事类对应的用神配置"""
        return SHILEI_YONGSHEN_MAP.get(shi_lei, SHILEI_YONGSHEN_MAP["其他"])
    
    def analyze_yongshen(
        self,
        shi_lei: str,
        yongshen_gong: int,
        rigan_gong: int,
        shigan_gong: int,
        month: int,
        rigan_wuxing: str,
        kongwang: List[int] = None,
    ) -> Dict[str, Any]:
        """
        分析用神状态
        
        Args:
            shi_lei: 事类
            yongshen_gong: 用神落宫
            rigan_gong: 日干落宫
            shigan_gong: 时干落宫
            month: 月份
            rigan_wuxing: 日干五行
            kongwang: 空亡宫位列表
        
        Returns:
            用神分析结果
        """
        config = self.get_yongshen_config(shi_lei)
        
        # 用神落宫旺相休囚死
        wangxiang_status, wangxiang_score = get_wangxiang(yongshen_gong, month)
        
        # 用神与日干的五行关系
        yongshen_wuxing = GONG_WUXING.get(yongshen_gong, "土")
        relation, relation_score = get_wuxing_relation(yongshen_wuxing, rigan_wuxing)
        
        # 空亡检测
        is_kongwang = kongwang and yongshen_gong in kongwang
        kongwang_score = -15 if is_kongwang else 0
        
        # 计算总分
        total_score = wangxiang_score + relation_score + kongwang_score
        
        # 生成分析结论
        analysis = self._generate_analysis(
            shi_lei, config, yongshen_gong, wangxiang_status, 
            relation, is_kongwang, total_score
        )
        
        return {
            "shi_lei": shi_lei,
            "description": config.description,
            "zhu_yongshen": config.zhu_yongshen,
            "fu_yongshen": config.fu_yongshen,
            "yongshen_gong": yongshen_gong,
            "yongshen_fangwei": GONG_FANGWEI.get(yongshen_gong, ""),
            "wangxiang": {
                "status": wangxiang_status,
                "score": wangxiang_score
            },
            "rigan_relation": {
                "relation": relation,
                "score": relation_score
            },
            "kongwang": {
                "is_kongwang": is_kongwang,
                "score": kongwang_score
            },
            "total_score": total_score,
            "rating": self._get_rating(total_score),
            "analysis": analysis
        }
    
    def analyze_zhuke(
        self,
        rigan_gong: int,
        shigan_gong: int,
        month: int,
        rigan_wuxing: str,
        shigan_wuxing: str,
    ) -> Dict[str, Any]:
        """
        主客分析（用于合作、诉讼等双方事类）
        
        Args:
            rigan_gong: 日干落宫（我方）
            shigan_gong: 时干落宫（对方）
            month: 月份
            rigan_wuxing: 日干五行
            shigan_wuxing: 时干五行
        
        Returns:
            主客分析结果
        """
        # 日干（我方）状态
        wo_wangxiang, wo_score = get_wangxiang(rigan_gong, month)
        
        # 时干（对方）状态
        bi_wangxiang, bi_score = get_wangxiang(shigan_gong, month)
        
        # 双方生克关系
        relation, _ = get_wuxing_relation(rigan_wuxing, shigan_wuxing)
        
        # 判断胜负
        if wo_score > bi_score + 5:
            conclusion = "我方占优，利于主动出击"
        elif bi_score > wo_score + 5:
            conclusion = "对方占优，宜守不宜攻"
        else:
            conclusion = "双方势均力敌，需看格局配合"
        
        return {
            "wo_fang": {
                "gong": rigan_gong,
                "fangwei": GONG_FANGWEI.get(rigan_gong, ""),
                "wangxiang": wo_wangxiang,
                "score": wo_score
            },
            "bi_fang": {
                "gong": shigan_gong,
                "fangwei": GONG_FANGWEI.get(shigan_gong, ""),
                "wangxiang": bi_wangxiang,
                "score": bi_score
            },
            "relation": relation,
            "conclusion": conclusion
        }
    
    def _generate_analysis(
        self,
        shi_lei: str,
        config: YongShenConfig,
        gong: int,
        wangxiang: str,
        relation: str,
        is_kongwang: bool,
        score: int
    ) -> str:
        """生成分析结论"""
        fangwei = GONG_FANGWEI.get(gong, "")
        
        parts = []
        parts.append(f"【{shi_lei}】用神落{fangwei}方{gong}宫")
        
        # 旺相状态
        if wangxiang in ["旺", "相"]:
            parts.append(f"得{wangxiang}气，力量充足")
        elif wangxiang in ["囚", "死"]:
            parts.append(f"处{wangxiang}地，力量不足")
        else:
            parts.append(f"处{wangxiang}地，力量中平")
        
        # 空亡
        if is_kongwang:
            parts.append("用神落空，事难成就，需待填实")
        
        # 与日干关系
        if relation == "生":
            parts.append("用神生日干，利于事成")
        elif relation == "克":
            parts.append("用神克日干，需防阻碍")
        
        # 总体建议
        if score >= 15:
            parts.append("综合评估：大吉，可积极进行")
        elif score >= 5:
            parts.append("综合评估：较吉，可以进行")
        elif score >= -5:
            parts.append("综合评估：中平，谨慎进行")
        else:
            parts.append("综合评估：不利，建议另择时机")
        
        return "；".join(parts)
    
    def _get_rating(self, score: int) -> str:
        """根据分数获取评级"""
        if score >= 15:
            return "优"
        elif score >= 5:
            return "良"
        elif score >= -5:
            return "中"
        else:
            return "差"


# 全局实例
qimen_yongshen = QimenYongShen()


def get_shilei_list() -> List[Dict[str, str]]:
    """获取所有事类列表"""
    return [
        {"value": k, "label": k, "description": v.description}
        for k, v in SHILEI_YONGSHEN_MAP.items()
    ]


def analyze_yongshen(
    shi_lei: str,
    yongshen_gong: int,
    rigan_gong: int,
    shigan_gong: int,
    month: int,
    rigan_wuxing: str,
    kongwang: List[int] = None,
) -> Dict[str, Any]:
    """便捷函数：分析用神"""
    return qimen_yongshen.analyze_yongshen(
        shi_lei, yongshen_gong, rigan_gong, shigan_gong, 
        month, rigan_wuxing, kongwang
    )

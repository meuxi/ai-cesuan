"""
紫微斗数计算服务 - 通过Node.js桥接调用原版iztro
解决iztro-py算法不准确的问题
"""

import subprocess
import json
import logging
import os
from typing import Dict, Any, Optional
from pathlib import Path

logger = logging.getLogger(__name__)

# Node.js脚本路径
BRIDGE_SCRIPT_PATH = Path(__file__).parent.parent.parent.parent / "scripts" / "iztro_bridge.js"


class IztroBridgeService:
    """
    通过Node.js调用原版iztro库的桥接服务
    提供比iztro-py更准确的紫微斗数计算
    """
    
    def __init__(self, node_path: str = "node"):
        """
        初始化桥接服务
        
        Args:
            node_path: Node.js可执行文件路径，默认使用系统PATH中的node
        """
        self.node_path = node_path
        self.script_path = str(BRIDGE_SCRIPT_PATH)
        self._check_prerequisites()
    
    def _check_prerequisites(self) -> bool:
        """检查Node.js和iztro是否可用"""
        try:
            # 检查Node.js
            result = subprocess.run(
                [self.node_path, "--version"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode != 0:
                logger.warning("Node.js不可用，将回退到iztro-py")
                return False
            
            logger.info(f"Node.js版本: {result.stdout.strip()}")
            
            # 检查脚本文件
            if not os.path.exists(self.script_path):
                logger.warning(f"桥接脚本不存在: {self.script_path}")
                return False
            
            return True
            
        except Exception as e:
            logger.warning(f"检查Node.js环境失败: {e}")
            return False
    
    def calculate(
        self,
        year: int,
        month: int,
        day: int,
        hour: int,
        minute: int = 0,
        gender: str = "male",
        language: str = "zh-CN"
    ) -> Dict[str, Any]:
        """
        计算紫微斗数命盘
        
        Args:
            year: 出生年份
            month: 出生月份
            day: 出生日
            hour: 出生时
            minute: 出生分（暂不使用）
            gender: 性别 ('male'/'female')
            language: 语言 ('zh-CN'/'zh-TW')
        
        Returns:
            完整的紫微斗数命盘数据
        """
        try:
            # 构建输入参数
            input_data = {
                "year": year,
                "month": month,
                "day": day,
                "hour": hour,
                "gender": gender,
                "language": language
            }
            
            # 调用Node.js脚本
            result = subprocess.run(
                [self.node_path, self.script_path, json.dumps(input_data)],
                capture_output=True,
                text=True,
                timeout=30,
                cwd=str(BRIDGE_SCRIPT_PATH.parent),
                encoding='utf-8',
                errors='replace'
            )
            
            if result.returncode != 0:
                error_msg = result.stderr or "Node.js脚本执行失败"
                logger.error(f"iztro桥接调用失败: {error_msg}")
                raise RuntimeError(f"iztro桥接调用失败: {error_msg}")
            
            # 解析返回结果
            response = json.loads(result.stdout)
            
            if not response.get("success"):
                error = response.get("error", "未知错误")
                raise RuntimeError(f"紫微斗数计算失败: {error}")
            
            # 补充大限信息
            response = self._add_decade_info(response, year, gender)
            
            return response
            
        except subprocess.TimeoutExpired:
            logger.error("iztro桥接调用超时")
            raise RuntimeError("紫微斗数计算超时")
        except json.JSONDecodeError as e:
            logger.error(f"解析iztro返回数据失败: {e}")
            raise RuntimeError(f"解析命盘数据失败: {e}")
        except Exception as e:
            logger.error(f"紫微斗数计算失败: {e}")
            raise
    
    def _add_decade_info(self, response: Dict[str, Any], birth_year: int, gender: str) -> Dict[str, Any]:
        """添加大限信息（含童限计算）
        
        童限规则（参考iztro）：
        一命二财三疾厄，四岁夫妻五福德，六岁事业为童限
        1岁看命宫，2岁看财帛宫，3岁看疾厄宫，
        4岁看夫妻宫，5岁看福德宫，6岁看官禄宫
        """
        from datetime import datetime
        
        palace_names = ['命宫', '兄弟宫', '夫妻宫', '子女宫', '财帛宫', '疾厄宫',
                       '迁移宫', '仆役宫', '官禄宫', '田宅宫', '福德宫', '父母宫']
        
        # 童限对应的宫位（1-6岁）
        # 一命二财三疾厄，四岁夫妻五福德，六岁事业
        CHILDHOOD_PALACE_NAMES = ['命宫', '财帛宫', '疾厄宫', '夫妻宫', '福德宫', '官禄宫']
        
        # 地支对应关系（宫位索引到地支）
        dizhi_for_palace = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']
        
        # 获取五行局以确定起运年龄
        five_element = response.get("basicInfo", {}).get("fiveElement", "")
        start_age = self._get_start_age(five_element)
        
        # 获取年干判断顺逆
        year_stem = response.get("basicInfo", {}).get("fourPillars", {}).get("year", {}).get("stem", "")
        is_clockwise = self._is_clockwise(year_stem, gender)
        
        # 获取宫位信息
        palaces = response.get("palaces", [])
        
        # 建立宫位名称到索引的映射
        palace_name_to_idx = {}
        for idx, palace in enumerate(palaces):
            palace_name_to_idx[palace.get("name", "")] = idx
        
        # 当前虚岁
        current_age = datetime.now().year - birth_year + 1
        
        # ========== 童限计算 ==========
        childhood_limits = []
        current_childhood = None
        
        for age in range(1, 7):
            childhood_palace_name = CHILDHOOD_PALACE_NAMES[age - 1]
            palace_idx = palace_name_to_idx.get(childhood_palace_name, age - 1)
            
            # 获取对应宫位的天干地支
            heavenly_stem = ""
            earthly_branch = ""
            if 0 <= palace_idx < len(palaces):
                heavenly_stem = palaces[palace_idx].get("heavenlyStem", "")
                earthly_branch = palaces[palace_idx].get("earthlyBranch", "")
            
            childhood = {
                "age": age,
                "palaceIndex": palace_idx,
                "palaceName": childhood_palace_name,
                "heavenlyStem": heavenly_stem,
                "earthlyBranch": earthly_branch,
                "label": f"{age}岁",
                "isCurrent": current_age == age,
                "ganzhi": f"{heavenly_stem}{earthly_branch}" if heavenly_stem else ""
            }
            childhood_limits.append(childhood)
            
            if current_age == age:
                current_childhood = childhood
        
        response["childhoodLimits"] = childhood_limits
        response["currentChildhood"] = current_childhood
        response["isInChildhood"] = 1 <= current_age <= 6
        
        # ========== 大限计算 ==========
        decades = []
        current_decade = None
        
        for i in range(12):
            decade_start = start_age + i * 10
            decade_end = decade_start + 9
            
            # 根据顺逆确定宫位索引
            if is_clockwise:
                palace_idx = i % 12
            else:
                palace_idx = (12 - i) % 12
            
            # 获取大限天干地支
            heavenly_stem, earthly_branch = self._get_decade_ganzhi(
                palaces, palace_idx, dizhi_for_palace
            )
            
            decade = {
                "index": i,
                "palaceIndex": palace_idx,
                "startAge": decade_start,
                "endAge": decade_end,
                "heavenlyStem": heavenly_stem,
                "earthlyBranch": earthly_branch,
                "palaceName": palace_names[palace_idx],
                "label": f"{decade_start}-{decade_end}岁",
                "isCurrent": decade_start <= current_age <= decade_end and current_age > 6,
                "ganzhi": f"{heavenly_stem}{earthly_branch}" if heavenly_stem else ""
            }
            
            decades.append(decade)
            
            if decade["isCurrent"]:
                current_decade = decade
        
        response["decades"] = decades
        response["currentDecade"] = current_decade
        
        # 如果在童限期间，大限信息使用童限对应的宫位
        if response["isInChildhood"] and current_childhood:
            response["currentDecade"] = {
                "index": -1,
                "palaceIndex": current_childhood["palaceIndex"],
                "startAge": current_childhood["age"],
                "endAge": current_childhood["age"],
                "heavenlyStem": current_childhood["heavenlyStem"],
                "earthlyBranch": current_childhood["earthlyBranch"],
                "palaceName": current_childhood["palaceName"],
                "label": f"童限{current_childhood['age']}岁",
                "isCurrent": True,
                "ganzhi": current_childhood["ganzhi"],
                "isChildhood": True
            }
        
        return response
    
    def _get_decade_ganzhi(self, palaces: list, palace_idx: int, dizhi_for_palace: list) -> tuple:
        """获取大限的天干地支
        
        大限天干取自对应宫位的天干，地支取自对应宫位的地支
        """
        heavenly_stem = ""
        earthly_branch = ""
        
        if palaces and 0 <= palace_idx < len(palaces):
            palace = palaces[palace_idx]
            heavenly_stem = palace.get("heavenlyStem", "")
            earthly_branch = palace.get("earthlyBranch", "")
        
        # 如果从宫位获取失败，使用默认地支
        if not earthly_branch and 0 <= palace_idx < len(dizhi_for_palace):
            earthly_branch = dizhi_for_palace[palace_idx]
        
        return heavenly_stem, earthly_branch
    
    def _get_start_age(self, five_element: str) -> int:
        """根据五行局获取起运年龄
        
        五行局决定大限起始年龄：
        - 水二局: 2岁起运
        - 木三局: 3岁起运
        - 金四局: 4岁起运
        - 土五局: 5岁起运
        - 火六局: 6岁起运
        """
        mapping = {
            "水二局": 2,
            "木三局": 3,
            "金四局": 4,
            "土五局": 5,
            "火六局": 6
        }
        return mapping.get(five_element, 2)
    
    def _is_clockwise(self, year_stem: str, gender: str) -> bool:
        """判断大限顺逆（阳男阴女顺行，阴男阳女逆行）
        
        紫微斗数大限行运规则：
        - 阳年出生的男性：顺行（从命宫开始顺时针）
        - 阴年出生的女性：顺行
        - 阴年出生的男性：逆行（从命宫开始逆时针）
        - 阳年出生的女性：逆行
        """
        yang_stems = ['甲', '丙', '戊', '庚', '壬']
        is_yang_stem = year_stem in yang_stems
        is_male = gender == "male"
        
        # 阳男阴女顺行
        return (is_yang_stem and is_male) or (not is_yang_stem and not is_male)


class HybridIztroService:
    """
    混合紫微斗数服务
    优先使用Node.js桥接（更准确），失败时回退到iztro-py
    """
    
    def __init__(self):
        self._bridge_service: Optional[IztroBridgeService] = None
        self._fallback_service = None
        self._use_bridge = True
        
        # 尝试初始化桥接服务
        try:
            self._bridge_service = IztroBridgeService()
            logger.info("iztro桥接服务初始化成功")
        except Exception as e:
            logger.warning(f"iztro桥接服务初始化失败，将使用iztro-py: {e}")
            self._use_bridge = False
    
    def calculate(
        self,
        year: int,
        month: int,
        day: int,
        hour: int,
        minute: int = 0,
        gender: str = "male",
        language: str = "zh-CN"
    ) -> Dict[str, Any]:
        """
        计算紫微斗数命盘
        优先使用Node.js桥接，失败时回退到iztro-py
        """
        # 尝试使用桥接服务
        if self._use_bridge and self._bridge_service:
            try:
                result = self._bridge_service.calculate(
                    year, month, day, hour, minute, gender, language
                )
                result["_source"] = "iztro-node"
                return result
            except Exception as e:
                logger.warning(f"桥接服务调用失败，回退到iztro-py: {e}")
        
        # 回退到iztro-py
        from .iztro_service import iztro_service
        result = iztro_service.calculate(year, month, day, hour, minute, gender, language)
        result["_source"] = "iztro-py"
        return result


# 全局单例
hybrid_iztro_service = HybridIztroService()

"""
塔罗牌占卜类 - 支持通用占卜接口
"""
from src.divination.base import DivinationFactory
from src.models import DivinationBody


class TarotDivination(DivinationFactory):
    """
    塔罗牌占卜 - 三牌阵解读
    """
    divination_type = 'tarot'
    
    def build_prompt(self, divination_body: DivinationBody) -> tuple[str, str]:
        """
        构建塔罗牌解读prompt
        
        Args:
            divination_body: 占卜请求体，包含:
                - prompt: 用户问题
                - cards: 抽取的牌列表 [{position, name}, ...]
                - master: 解读大师配置 {id, name, prompt, gamePrompt}
        
        Returns:
            tuple[str, str]: (用户prompt, 系统prompt)
        """
        question = divination_body.prompt or "请为我解读"
        cards = divination_body.cards or []
        master = divination_body.master or {}
        
        # 构建牌面信息
        spread = divination_body.spread or {}
        spread_name = spread.get('name', '塔罗牌阵') if isinstance(spread, dict) else '塔罗牌阵'
        
        cards_text = ""
        if cards:
            for card in cards:
                position = card.get('position', '未知位置')
                name = card.get('name', '未知牌')
                is_reversed = card.get('isReversed', False)
                meaning = card.get('meaning', '')
                
                # 显示正逆位状态
                status = "（逆位）" if is_reversed else "（正位）"
                cards_text += f"- **{position}**：{name} {status}\n"
                if meaning:
                    cards_text += f"  牌义：{meaning}\n"
        else:
            cards_text = "（未提供牌面信息）"
        
        # 用户prompt
        user_prompt = f"""我想请你为我解读塔罗牌。

我的问题是：{question}

使用的牌阵：{spread_name}

我抽到的牌是：
{cards_text}

请根据牌面（注意正逆位）和我的问题，给出详细的解读和建议。"""

        # 系统prompt - 使用大师配置或默认
        master_prompt = master.get('prompt', '')
        game_prompt = master.get('gamePrompt')
        master_name = master.get('name', '塔罗师')
        
        # 处理 gamePrompt - 可能是字符串或对象
        system_prompt = ''
        if game_prompt:
            if isinstance(game_prompt, dict):
                base_role = game_prompt.get('baseRole', '')
                analysis_style = game_prompt.get('analysisStyle', '')
                system_prompt = f"{base_role}\n\n{analysis_style}".strip()
            elif isinstance(game_prompt, str):
                system_prompt = game_prompt
        
        # 如果 gamePrompt 没有产生有效内容，使用 master_prompt
        if not system_prompt and master_prompt:
            system_prompt = f"""{master_prompt}

你现在要为用户进行塔罗牌解读。请结合牌面含义和用户的问题，给出深入、有洞察力的解读。

解读格式：
1. 简要说明每张牌在其位置的含义
2. 分析三张牌之间的联系
3. 结合用户问题给出整体解读
4. 提供具体可行的建议"""
        
        # 如果仍然没有有效的system_prompt，使用默认
        if not system_prompt:
            system_prompt = f"""你是一位资深的塔罗牌解读师"{master_name}"，拥有深厚的塔罗牌知识和直觉洞察力。

你的解读风格：
- 温和而富有智慧
- 善于发现牌面之间的联系
- 注重实际可行的建议
- 尊重求问者的选择权

解读原则：
1. 塔罗牌是一面镜子，反映的是当前的能量和趋势
2. 未来不是固定的，牌面显示的是如果继续当前路径的可能性
3. 每张牌都有正反两面的含义，要根据问题和位置综合解读
4. 给出的建议应该是具体、可执行的

请根据用户抽到的牌和问题，按以下格式进行解读：

## 🎴 牌面解读
（逐张解释每张牌在其位置的含义）

## 🔮 整体分析
（分析牌面之间的关联，给出对问题的整体解答）

## 💡 建议与指引
（给出具体可行的建议）

## ✨ 开运提示
（提供一些积极的能量和祝福）"""

        return user_prompt, system_prompt

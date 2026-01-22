"""
RAG 生成器

结合检索结果生成增强回答，支持：
- 上下文增强生成
- 多种回答风格
- 来源引用
"""

import logging
from typing import List, Dict, Any, Optional
from dataclasses import dataclass

from .models import RetrievalResult, RAGQuery, RAGResponse, ConversationSession, MessageRole

logger = logging.getLogger(__name__)


@dataclass
class GeneratorConfig:
    """生成器配置"""
    max_context_length: int = 4000      # 最大上下文长度
    include_sources: bool = True        # 是否包含来源
    style: str = "professional"         # 回答风格: professional/casual/master
    temperature: float = 0.7
    max_tokens: int = 2000


class PromptBuilder:
    """提示词构建器"""
    
    # 系统提示词模板
    SYSTEM_PROMPTS = {
        "professional": """你是一位专业的玄学顾问，精通八字、紫微斗数、六爻、塔罗、奇门遁甲等各类术数。
请根据提供的知识库内容，为用户提供专业、准确的解答。

回答要求：
1. 基于知识库内容进行回答，确保准确性
2. 使用专业术语，但要解释清楚
3. 结构清晰，条理分明
4. 如果知识库中没有相关内容，诚实告知并给出一般性建议""",

        "casual": """你是一位亲切的玄学顾问，擅长用通俗易懂的方式解释复杂的命理知识。
请根据提供的知识库内容，用平易近人的语言为用户解答。

回答要求：
1. 语言亲切自然，避免过于晦涩的术语
2. 必要时用比喻或举例帮助理解
3. 关注用户的实际困惑，给出实用建议
4. 如果不确定，坦诚相告""",

        "master": """你是玄机子大师，终南山紫霄观修行五十载的玄学高人。
精通八字、紫微斗数、梅花易数、六爻、奇门遁甲、风水、塔罗等各门术数。

回答风格：
1. 【】标注标题，「」高亮重点
2. 引用古籍典故，增添神秘感
3. 言辞稳重有力，透露高深莫测
4. 结尾附上命运箴言

请根据知识库内容，以大师的口吻为求测者解惑。""",
    }
    
    # 上下文模板
    CONTEXT_TEMPLATE = """
## 相关知识

{context}

---

"""
    
    # 对话历史模板
    HISTORY_TEMPLATE = """
## 对话历史

{history}

---

"""
    
    # 占卜上下文模板
    DIVINATION_CONTEXT_TEMPLATE = """
## 占卜信息

占卜类型：{divination_type}
{context_details}

---

"""
    
    def build_system_prompt(self, style: str = "professional") -> str:
        """构建系统提示词"""
        return self.SYSTEM_PROMPTS.get(style, self.SYSTEM_PROMPTS["professional"])
    
    def build_context(
        self,
        retrieval_results: List[RetrievalResult],
        max_length: int = 4000,
    ) -> str:
        """构建知识上下文"""
        if not retrieval_results:
            return ""
        
        context_parts = []
        current_length = 0
        
        for i, result in enumerate(retrieval_results, 1):
            content = result.chunk.content.strip()
            entry = f"[知识{i}] {content}\n"
            
            if current_length + len(entry) > max_length:
                break
            
            context_parts.append(entry)
            current_length += len(entry)
        
        if not context_parts:
            return ""
        
        return self.CONTEXT_TEMPLATE.format(context="\n".join(context_parts))
    
    def build_history(
        self,
        session: ConversationSession,
        max_turns: int = 5,
    ) -> str:
        """构建对话历史"""
        if not session or not session.messages:
            return ""
        
        # 获取最近的对话
        recent_messages = session.messages[-max_turns * 2:]
        
        history_parts = []
        for msg in recent_messages:
            role = "用户" if msg.role == MessageRole.USER else "助手"
            history_parts.append(f"{role}：{msg.content}")
        
        if not history_parts:
            return ""
        
        return self.HISTORY_TEMPLATE.format(history="\n".join(history_parts))
    
    def build_divination_context(
        self,
        divination_type: str,
        context: Dict[str, Any],
    ) -> str:
        """构建占卜上下文"""
        if not divination_type and not context:
            return ""
        
        details = []
        
        # 根据占卜类型构建详情
        if divination_type == "bazi" and context:
            if "四柱" in context:
                details.append(f"四柱：{context['四柱']}")
            if "日主" in context:
                details.append(f"日主：{context['日主']}")
            if "格局" in context:
                details.append(f"格局：{context['格局']}")
        
        elif divination_type == "liuyao" and context:
            if "卦名" in context:
                details.append(f"卦名：{context['卦名']}")
            if "用神" in context:
                details.append(f"用神：{context['用神']}")
        
        elif divination_type == "tarot" and context:
            if "牌阵" in context:
                details.append(f"牌阵：{context['牌阵']}")
            if "抽取的牌" in context:
                details.append(f"牌面：{context['抽取的牌']}")
        
        # 通用字段
        for key, value in context.items():
            if key not in ["四柱", "日主", "格局", "卦名", "用神", "牌阵", "抽取的牌"]:
                if isinstance(value, (str, int, float)):
                    details.append(f"{key}：{value}")
        
        if not details:
            return ""
        
        return self.DIVINATION_CONTEXT_TEMPLATE.format(
            divination_type=divination_type or "通用",
            context_details="\n".join(details),
        )
    
    def build_full_prompt(
        self,
        query: str,
        retrieval_results: List[RetrievalResult] = None,
        session: ConversationSession = None,
        divination_type: str = None,
        divination_context: Dict[str, Any] = None,
        style: str = "professional",
        max_context_length: int = 4000,
    ) -> List[Dict[str, str]]:
        """构建完整的消息列表"""
        messages = []
        
        # 系统提示词
        system_prompt = self.build_system_prompt(style)
        messages.append({"role": "system", "content": system_prompt})
        
        # 构建用户消息
        user_content_parts = []
        
        # 知识上下文
        if retrieval_results:
            context = self.build_context(retrieval_results, max_context_length)
            if context:
                user_content_parts.append(context)
        
        # 占卜上下文
        if divination_type or divination_context:
            div_context = self.build_divination_context(
                divination_type, divination_context or {}
            )
            if div_context:
                user_content_parts.append(div_context)
        
        # 对话历史
        if session and session.messages:
            history = self.build_history(session)
            if history:
                user_content_parts.append(history)
        
        # 用户问题
        user_content_parts.append(f"## 用户问题\n\n{query}")
        
        messages.append({"role": "user", "content": "\n".join(user_content_parts)})
        
        return messages


class RAGGenerator:
    """RAG 生成器"""
    
    def __init__(self, ai_client=None):
        """
        初始化生成器
        
        Args:
            ai_client: AI 客户端，需要实现 chat 方法
                       如果不提供，将使用 src.ai 模块
        """
        self.ai_client = ai_client
        self.prompt_builder = PromptBuilder()
    
    async def generate(
        self,
        query: RAGQuery,
        retrieval_results: List[RetrievalResult],
        session: ConversationSession = None,
        config: GeneratorConfig = None,
    ) -> RAGResponse:
        """生成回答"""
        config = config or GeneratorConfig()
        
        # 构建提示词
        messages = self.prompt_builder.build_full_prompt(
            query=query.query,
            retrieval_results=retrieval_results if query.include_sources else [],
            session=session,
            divination_type=query.divination_type,
            divination_context=query.divination_context,
            style=config.style,
            max_context_length=config.max_context_length,
        )
        
        # 调用 AI 生成回答
        try:
            answer = await self._call_ai(messages, config)
        except Exception as e:
            logger.error(f"AI 生成失败: {e}")
            answer = self._fallback_answer(query, retrieval_results)
        
        # 构建响应
        response = RAGResponse(
            answer=answer,
            session_id=session.id if session else "",
            sources=retrieval_results if config.include_sources else [],
            metadata={
                "style": config.style,
                "context_count": len(retrieval_results),
            },
        )
        
        return response
    
    async def _call_ai(
        self,
        messages: List[Dict[str, str]],
        config: GeneratorConfig,
    ) -> str:
        """调用 AI 模型"""
        if self.ai_client:
            # 使用提供的 AI 客户端
            return await self.ai_client.chat(
                messages=messages,
                temperature=config.temperature,
                max_tokens=config.max_tokens,
            )
        
        # 尝试使用 src.ai 模块
        try:
            from ..ai.provider import AIProviderManager
            from ..config import settings
            
            manager = AIProviderManager()
            response = await manager.chat_with_failover(
                messages=messages,
                temperature=config.temperature,
                max_tokens=config.max_tokens,
            )
            return response.content
        except ImportError:
            logger.warning("AI 模块不可用，使用后备回答")
            return ""
        except Exception as e:
            logger.error(f"AI 调用失败: {e}")
            raise
    
    def _fallback_answer(
        self,
        query: RAGQuery,
        retrieval_results: List[RetrievalResult],
    ) -> str:
        """后备回答（当 AI 不可用时）"""
        if not retrieval_results:
            return "抱歉，暂时无法找到相关信息。请稍后再试或换一种方式提问。"
        
        # 基于检索结果生成简单回答
        answer_parts = ["根据知识库，以下是相关信息：\n"]
        
        for i, result in enumerate(retrieval_results[:3], 1):
            content = result.chunk.content[:200]
            if len(result.chunk.content) > 200:
                content += "..."
            answer_parts.append(f"{i}. {content}\n")
        
        answer_parts.append("\n如需更详细的解读，请稍后再试。")
        
        return "\n".join(answer_parts)

"""
对话管理

支持追问对话和会话管理，包括：
- 会话创建与管理
- 对话历史存储
- 上下文传递
"""

import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import threading

from .models import ConversationSession, ConversationMessage, MessageRole

logger = logging.getLogger(__name__)


class ConversationStore:
    """会话存储"""
    
    def __init__(self, store_path: str = None):
        self.store_path = Path(store_path) if store_path else Path("data/conversations")
        self.store_path.mkdir(parents=True, exist_ok=True)
        self._sessions: Dict[str, ConversationSession] = {}
        self._lock = threading.Lock()
        
        # 加载已有会话
        self._load_active_sessions()
    
    def create_session(
        self,
        divination_type: str = "",
        divination_id: str = None,
        context: Dict[str, Any] = None,
        max_history: int = 20,
    ) -> ConversationSession:
        """创建新会话"""
        session = ConversationSession(
            divination_type=divination_type,
            divination_id=divination_id,
            context=context or {},
            max_history=max_history,
        )
        
        with self._lock:
            self._sessions[session.id] = session
            self._save_session(session)
        
        logger.info(f"创建会话: {session.id}, 类型: {divination_type}")
        return session
    
    def get_session(self, session_id: str) -> Optional[ConversationSession]:
        """获取会话"""
        with self._lock:
            if session_id in self._sessions:
                return self._sessions[session_id]
            
            # 尝试从文件加载
            session = self._load_session(session_id)
            if session:
                self._sessions[session_id] = session
            return session
    
    def update_session(self, session: ConversationSession):
        """更新会话"""
        session.updated_at = datetime.now()
        with self._lock:
            self._sessions[session.id] = session
            self._save_session(session)
    
    def add_message(
        self,
        session_id: str,
        role: MessageRole,
        content: str,
        metadata: Dict[str, Any] = None,
    ) -> Optional[ConversationMessage]:
        """添加消息到会话"""
        session = self.get_session(session_id)
        if not session:
            logger.warning(f"会话不存在: {session_id}")
            return None
        
        message = session.add_message(role, content, metadata)
        self.update_session(session)
        
        return message
    
    def end_session(self, session_id: str) -> bool:
        """结束会话"""
        session = self.get_session(session_id)
        if not session:
            return False
        
        session.ended_at = datetime.now()
        self.update_session(session)
        
        logger.info(f"结束会话: {session_id}")
        return True
    
    def delete_session(self, session_id: str) -> bool:
        """删除会话"""
        with self._lock:
            if session_id in self._sessions:
                del self._sessions[session_id]
            
            session_file = self.store_path / f"{session_id}.json"
            if session_file.exists():
                session_file.unlink()
                return True
        return False
    
    def list_sessions(
        self,
        divination_type: str = None,
        include_ended: bool = False,
        limit: int = 50,
    ) -> List[ConversationSession]:
        """列出会话"""
        sessions = []
        
        # 扫描文件
        for session_file in self.store_path.glob("*.json"):
            session = self._load_session(session_file.stem)
            if session:
                # 过滤条件
                if divination_type and session.divination_type != divination_type:
                    continue
                if not include_ended and session.ended_at:
                    continue
                sessions.append(session)
        
        # 按更新时间排序
        sessions.sort(key=lambda s: s.updated_at, reverse=True)
        return sessions[:limit]
    
    def cleanup_old_sessions(self, days: int = 7) -> int:
        """清理旧会话"""
        cutoff = datetime.now() - timedelta(days=days)
        count = 0
        
        for session_file in self.store_path.glob("*.json"):
            try:
                session = self._load_session(session_file.stem)
                if session and session.updated_at < cutoff:
                    self.delete_session(session.id)
                    count += 1
            except Exception as e:
                logger.warning(f"清理会话失败 {session_file}: {e}")
        
        logger.info(f"清理了 {count} 个旧会话")
        return count
    
    def _save_session(self, session: ConversationSession):
        """保存会话到文件"""
        try:
            session_file = self.store_path / f"{session.id}.json"
            with open(session_file, 'w', encoding='utf-8') as f:
                json.dump(session.to_dict(), f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"保存会话失败: {e}")
    
    def _load_session(self, session_id: str) -> Optional[ConversationSession]:
        """从文件加载会话"""
        session_file = self.store_path / f"{session_id}.json"
        if not session_file.exists():
            return None
        
        try:
            with open(session_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return ConversationSession.from_dict(data)
        except Exception as e:
            logger.warning(f"加载会话失败 {session_id}: {e}")
            return None
    
    def _load_active_sessions(self):
        """加载活跃会话到内存"""
        cutoff = datetime.now() - timedelta(hours=24)
        
        for session_file in self.store_path.glob("*.json"):
            try:
                # 检查文件修改时间
                if datetime.fromtimestamp(session_file.stat().st_mtime) > cutoff:
                    session = self._load_session(session_file.stem)
                    if session and not session.ended_at:
                        self._sessions[session.id] = session
            except Exception:
                pass
        
        logger.info(f"加载了 {len(self._sessions)} 个活跃会话")


class ConversationManager:
    """对话管理器"""
    
    def __init__(self, store_path: str = None):
        self.store = ConversationStore(store_path)
    
    def start_conversation(
        self,
        divination_type: str = "",
        divination_id: str = None,
        context: Dict[str, Any] = None,
    ) -> ConversationSession:
        """开始新对话"""
        return self.store.create_session(
            divination_type=divination_type,
            divination_id=divination_id,
            context=context,
        )
    
    def continue_conversation(
        self,
        session_id: str,
        user_message: str,
    ) -> Optional[ConversationSession]:
        """继续对话（添加用户消息）"""
        session = self.store.get_session(session_id)
        if not session:
            return None
        
        if session.ended_at:
            logger.warning(f"会话已结束: {session_id}")
            return None
        
        self.store.add_message(session_id, MessageRole.USER, user_message)
        return self.store.get_session(session_id)
    
    def add_assistant_response(
        self,
        session_id: str,
        response: str,
        metadata: Dict[str, Any] = None,
    ) -> Optional[ConversationMessage]:
        """添加助手回复"""
        return self.store.add_message(
            session_id, MessageRole.ASSISTANT, response, metadata
        )
    
    def get_conversation_context(
        self,
        session_id: str,
    ) -> Dict[str, Any]:
        """获取对话上下文"""
        session = self.store.get_session(session_id)
        if not session:
            return {}
        
        return {
            "session_id": session.id,
            "divination_type": session.divination_type,
            "divination_id": session.divination_id,
            "context": session.context,
            "history": session.get_history_for_prompt(),
            "message_count": len(session.messages),
        }
    
    def end_conversation(self, session_id: str) -> bool:
        """结束对话"""
        return self.store.end_session(session_id)
    
    def get_session(self, session_id: str) -> Optional[ConversationSession]:
        """获取会话"""
        return self.store.get_session(session_id)
    
    def list_conversations(
        self,
        divination_type: str = None,
        include_ended: bool = False,
    ) -> List[Dict[str, Any]]:
        """列出对话"""
        sessions = self.store.list_sessions(
            divination_type=divination_type,
            include_ended=include_ended,
        )
        
        return [
            {
                "id": s.id,
                "divination_type": s.divination_type,
                "divination_id": s.divination_id,
                "message_count": len(s.messages),
                "created_at": s.created_at.isoformat(),
                "updated_at": s.updated_at.isoformat(),
                "ended_at": s.ended_at.isoformat() if s.ended_at else None,
            }
            for s in sessions
        ]

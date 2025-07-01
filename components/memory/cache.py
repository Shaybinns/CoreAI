from typing import Dict, Any, List, Optional
import asyncio
from collections import deque
import time

class MemoryManager:
    """Manages short-term cache and long-term retrieval"""
    
    def __init__(self, config):
        self.config = config
        self.short_term_cache = {}  # In-memory cache
        self.conversation_buffer = {}  # Recent conversations
        self.vector_store = None  # For RAG
        
    async def initialize(self):
        """Initialize memory systems"""
        # Initialize vector store if configured
        if self.config.vector_db_url:
            # Initialize Pinecone/Weaviate/etc
            pass
    
    async def add_message(self, session_id: str, role: str, content: str):
        """Add message to memory"""
        if session_id not in self.conversation_buffer:
            self.conversation_buffer[session_id] = deque(
                maxlen=self.config.max_memory_items
            )
        
        self.conversation_buffer[session_id].append({
            "role": role,
            "content": content,
            "timestamp": time.time()
        })
    
    async def retrieve_context(self, session_id: str, query: str) -> Dict[str, Any]:
        """Retrieve relevant context using RAG"""
        context = {
            "recent_messages": list(self.conversation_buffer.get(session_id, [])),
            "cached_data": self.short_term_cache.get(session_id, {}),
            "relevant_memories": []
        }
        
        # RAG retrieval if available
        if self.vector_store:
            context["relevant_memories"] = await self._vector_search(query)
        
        return context

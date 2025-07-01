from typing import Dict, Any, Optional, AsyncGenerator
import asyncio
from dataclasses import dataclass
from datetime import datetime

@dataclass
class BrainConfig:
    """Configuration for the AI Brain"""
    app_name: str
    version: str = "1.0.0"
    
    # Database
    db_url: str = "postgresql://localhost/aicore"
    db_pool_size: int = 10
    
    # Memory
    cache_ttl: int = 3600
    vector_db_url: Optional[str] = None
    max_memory_items: int = 1000
    
    # AI Model
    model_provider: str = "openai"  # openai, anthropic, local
    model_name: str = "gpt-4"
    temperature: float = 0.7
    
    # Response
    stream_enabled: bool = True
    max_conversation_length: int = 100
    response_timeout: int = 30
    
    # Tools
    max_concurrent_tools: int = 5
    tool_timeout: int = 10

class AIBrain:
    """
    Universal AI Brain - Central controller for all AI operations
    This is the main class you'll instantiate for any AI application
    """
    
    def __init__(self, config: BrainConfig):
        self.config = config
        self.components = {}
        self._initialized = False
        
    async def initialize(self):
        """Initialize all brain components"""
        if self._initialized:
            return
            
        # Initialize components
        from ..components.database import DatabaseManager
        from ..components.memory import MemoryManager
        from ..components.characteristics import CharacteristicsManager
        from ..components.response import ResponseManager
        from ..components.tools import ToolManager
        
        self.components['database'] = DatabaseManager(self.config)
        self.components['memory'] = MemoryManager(self.config)
        self.components['characteristics'] = CharacteristicsManager(self.config)
        self.components['response'] = ResponseManager(self.config)
        self.components['tools'] = ToolManager(self.config)
        
        # Initialize all components
        for component in self.components.values():
            await component.initialize()
        
        self._initialized = True
        
    async def process(self, 
                     user_id: str, 
                     message: str,
                     context: Optional[Dict[str, Any]] = None) -> AsyncGenerator[str, None]:
        """
        Main processing method - handles infinite conversation flow
        
        Args:
            user_id: Unique user identifier
            message: User's message
            context: Optional context
            
        Yields:
            Response chunks for streaming
        """
        if not self._initialized:
            await self.initialize()
        
        # Create or retrieve session
        session = await self.components['database'].get_or_create_session(user_id)
        
        # Add to conversation history
        await self.components['memory'].add_message(session.id, "user", message)
        
        # Retrieve relevant context from memory
        memory_context = await self.components['memory'].retrieve_context(
            session.id, message
        )
        
        # Get characteristics for this interaction
        characteristics = await self.components['characteristics'].get_profile(
            session.id, memory_context
        )
        
        # Determine required tools
        required_tools = await self.components['tools'].analyze_requirements(
            message, memory_context, characteristics
        )
        
        # Execute tools if needed
        tool_results = {}
        if required_tools:
            tool_results = await self.components['tools'].execute_batch(
                required_tools, context
            )
        
        # Generate response
        async for chunk in self.components['response'].generate(
            message=message,
            session=session,
            memory_context=memory_context,
            characteristics=characteristics,
            tool_results=tool_results
        ):
            yield chunk
        
        # Update long-term memory
        await self.components['memory'].update_long_term(
            session.id, message, tool_results
        )
    
    async def shutdown(self):
        """Gracefully shutdown all components"""
        for component in self.components.values():
            if hasattr(component, 'shutdown'):
                await component.shutdown()

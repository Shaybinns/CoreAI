from typing import Dict, Any, List, AsyncGenerator
import asyncio
import json

class ResponseManager:
    """Manages response generation and streaming"""
    
    def __init__(self, config):
        self.config = config
        self.llm_client = None
        
    async def initialize(self):
        """Initialize LLM client"""
        # For now, we'll use mock responses
        # Later you can add OpenAI/Anthropic here
        pass
    
    async def generate(self, **kwargs) -> AsyncGenerator[str, None]:
        """Generate streaming response"""
        # Mock response for testing
        messages = self._build_messages(kwargs)
        
        # Create a mock response based on the input
        user_message = kwargs.get('message', '')
        tool_results = kwargs.get('tool_results', {})
        
        # Build response
        response = f"I received your message: '{user_message}'. "
        
        if tool_results:
            response += f"I used these tools: {', '.join(tool_results.keys())}. "
            for tool, result in tool_results.items():
                response += f"The {tool} returned: {result}. "
        
        response += "How else can I help you?"
        
        # Stream the response character by character
        for char in response:
            yield char
            await asyncio.sleep(0.01)  # Simulate streaming delay
    
    def _build_messages(self, kwargs) -> List[Dict[str, str]]:
        """Build messages for LLM"""
        messages = []
        
        # Add system prompt
        if 'characteristics' in kwargs:
            messages.append({
                "role": "system", 
                "content": kwargs['characteristics'].get('system_prompt', '')
            })
        
        # Add conversation history
        if 'memory_context' in kwargs:
            for msg in kwargs['memory_context'].get('recent_messages', []):
                messages.append({
                    "role": msg.get('role', 'user'),
                    "content": msg.get('content', '')
                })
        
        # Add current message
        messages.append({
            "role": "user",
            "content": kwargs.get('message', '')
        })
        
        # Add tool results if any
        if kwargs.get('tool_results'):
            tool_msg = "Tool results:\n"
            for tool, result in kwargs['tool_results'].items():
                tool_msg += f"{tool}: {json.dumps(result)}\n"
            messages.append({
                "role": "system",
                "content": tool_msg
            })
        
        return messages

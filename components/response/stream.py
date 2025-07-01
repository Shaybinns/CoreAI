class ResponseManager:
    """Manages response generation and streaming"""
    
    def __init__(self, config):
        self.config = config
        self.llm_client = None
        
    async def initialize(self):
        """Initialize LLM client"""
        if self.config.model_provider == "openai":
            import openai
            self.llm_client = openai.AsyncOpenAI()
        elif self.config.model_provider == "anthropic":
            import anthropic
            self.llm_client = anthropic.AsyncAnthropic()
    
    async def generate(self, **kwargs) -> AsyncGenerator[str, None]:
        """Generate streaming response"""
        # Build messages
        messages = self._build_messages(kwargs)
        
        # Stream from LLM
        async for chunk in self._stream_llm(messages):
            yield chunk
    
    async def _stream_llm(self, messages: List[Dict[str, str]]) -> AsyncGenerator[str, None]:
        """Stream response from LLM"""
        if self.config.model_provider == "openai":
            stream = await self.llm_client.chat.completions.create(
                model=self.config.model_name,
                messages=messages,
                temperature=self.config.temperature,
                stream=True
            )
            
            async for chunk in stream:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content

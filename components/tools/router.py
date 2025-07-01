from abc import ABC, abstractmethod

class BaseTool(ABC):
    """Base interface for all tools"""
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Tool name"""
        pass
    
    @property
    @abstractmethod
    def description(self) -> str:
        """Tool description"""
        pass
    
    @abstractmethod
    async def execute(self, params: Dict[str, Any]) -> Any:
        """Execute tool with parameters"""
        pass

class ToolManager:
    """Manages tool registration and execution"""
    
    def __init__(self, config):
        self.config = config
        self.tools = {}
        self.command_stack = []
        
    async def initialize(self):
        """Initialize tool system"""
        # Auto-discover and register tools
        self._discover_tools()
    
    def register_tool(self, tool: BaseTool):
        """Register a new tool"""
        self.tools[tool.name] = tool
    
    async def analyze_requirements(self, message: str, context: Dict[str, Any], 
                                  characteristics: Dict[str, Any]) -> List[str]:
        """Analyze what tools are needed"""
        # Use LLM or rules to determine required tools
        required = []
        
        # Simple example
        if "calculate" in message.lower():
            required.append("calculator")
        if "search" in message.lower():
            required.append("web_search")
        
        return required
    
    async def execute_batch(self, tool_names: List[str], context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute multiple tools"""
        results = {}
        
        # Execute tools concurrently
        tasks = []
        for tool_name in tool_names:
            if tool_name in self.tools:
                task = self.tools[tool_name].execute(context)
                tasks.append((tool_name, task))
        
        # Gather results
        for tool_name, task in tasks:
            try:
                results[tool_name] = await asyncio.wait_for(
                    task, timeout=self.config.tool_timeout
                )
            except asyncio.TimeoutError:
                results[tool_name] = {"error": "Tool execution timed out"}
        
        return results

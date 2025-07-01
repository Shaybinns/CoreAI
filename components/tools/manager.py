from typing import Dict, Any, List
import asyncio
from .base import BaseTool

class ToolManager:
    """Manages tool registration and execution"""
    
    def __init__(self, config):
        self.config = config
        self.tools = {}
        
    async def initialize(self):
        """Initialize tool system"""
        # Tools will be registered from outside
        pass
    
    def register_tool(self, tool: BaseTool):
        """Register a new tool"""
        self.tools[tool.name] = tool
        print(f"Registered tool: {tool.name}")
    
    async def analyze_requirements(self, message: str, context: Dict[str, Any], 
                                  characteristics: Dict[str, Any]) -> List[str]:
        """Analyze what tools are needed"""
        # Simple keyword matching for now
        required = []
        
        lower_msg = message.lower()
        
        # Check for calculator needs
        if any(word in lower_msg for word in ["calculate", "compute", "math", "add", "subtract", "multiply", "divide"]):
            if "calculator" in self.tools:
                required.append("calculator")
        
        # Check for search needs
        if any(word in lower_msg for word in ["search", "find", "look up", "what is", "who is"]):
            if "search" in self.tools:
                required.append("search")
        
        # Check for weather needs
        if any(word in lower_msg for word in ["weather", "temperature", "forecast", "rain"]):
            if "weather" in self.tools:
                required.append("weather")
                
        return required
    
    async def execute_batch(self, tool_names: List[str], context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute multiple tools"""
        results = {}
        
        for tool_name in tool_names:
            if tool_name in self.tools:
                try:
                    # Execute tool with timeout
                    result = await asyncio.wait_for(
                        self.tools[tool_name].execute(context),
                        timeout=self.config.tool_timeout
                    )
                    results[tool_name] = result
                except asyncio.TimeoutError:
                    results[tool_name] = {"error": "Tool execution timed out"}
                except Exception as e:
                    results[tool_name] = {"error": str(e)}
            else:
                results[tool_name] = {"error": f"Tool '{tool_name}' not found"}
        
        return results
    
    def list_tools(self) -> List[Dict[str, str]]:
        """List all available tools"""
        return [
            {"name": tool.name, "description": tool.description}
            for tool in self.tools.values()
        ]

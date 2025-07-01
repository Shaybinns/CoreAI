from abc import ABC, abstractmethod
from typing import Dict, Any

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

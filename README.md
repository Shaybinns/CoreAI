# CoreAI

A modular, reusable AI assistant framework that can be adapted for any domain.

## Features
- 🧠 Modular brain architecture
- 💾 Database integration for sessions
- 🔄 Infinite conversation support
- 🛠️ Pluggable tool system
- 📝 Customizable characteristics
- 🚀 Async/streaming responses

## Structure
- `core/` - Main brain and configuration
- `components/` - Core components (database, memory, tools, etc.)
- `domain/` - Domain-specific implementations
- `utils/` - Utility functions


## Creating Custom Tools

See `example_tool.py` for the pattern to create your own tools.

```python
from components.tools.base import BaseTool

class YourTool(BaseTool):
    @property
    def name(self):
        return "your_tool_name"
    
    @property
    def description(self):
        return "What your tool does"
    
    async def execute(self, params):
        # Your logic here
        return {"result": "your_result"}

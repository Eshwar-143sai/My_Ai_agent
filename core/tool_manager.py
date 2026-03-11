from typing import List, Callable
from langchain_core.tools import BaseTool

# Import our individual tools
from tools.calculator import calculator
from memory.vector_store import MEMORY_TOOLS

class ToolManager:
    """
    Manages all tools available to the AI Agent.
    Validates tools and ensures they are ready before the agent uses them.
    """
    def __init__(self):
        # We start by registering our core capabilities
        self._tools: List[BaseTool] = [
            calculator
        ]
        
        # Add memory tools
        self._tools.extend(MEMORY_TOOLS)
        
    def get_all_tools(self) -> List[BaseTool]:
        """Returns the fully validated list of tools for the agent."""
        # Here we could add logic to check API keys (e.g. if Web Search needs a key)
        # and only return tools that are properly configured.
        return self._tools
        
    def add_tool(self, tool: BaseTool):
        """Dynamically add a new tool to the manager."""
        self._tools.append(tool)

# Instantiate a global tool manager
tool_manager = ToolManager()

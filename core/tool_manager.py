import importlib
import pkgutil
from typing import List, Dict
from langchain_core.tools import BaseTool

from memory.vector_store import MEMORY_TOOLS

class ToolManager:
    """
    Dynamic Tool Registry (Enterprise Point 2).
    Scans the 'tools' directory for any LangChain @tool decorators and loads them automatically.
    This eliminates hardcoded lists and allows drop-in tool capabilities.
    """
    def __init__(self):
        self._tools: Dict[str, BaseTool] = {}
        self._load_dynamic_tools()
        
        # Add core memory tools manually (we could also move these to the tools/ directory)
        for t in MEMORY_TOOLS:
            self.add_tool(t)

    def _load_dynamic_tools(self):
        """Discovers and imports tools automatically from the tools/ package."""
        import tools
        for _, module_name, _ in pkgutil.iter_modules(tools.__path__):
            module = importlib.import_module(f"tools.{module_name}")
            # Find all BaseTool instances inside the imported module
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                # Ensure we only pick up actual tools, and not BaseTool itself
                if isinstance(attr, BaseTool) and type(attr) is not type(BaseTool):
                    self.add_tool(attr)

    def get_all_tools(self) -> List[BaseTool]:
        """Returns the fully validated list of tools for the agent."""
        return list(self._tools.values())
        
    def add_tool(self, tool: BaseTool):
        """Dynamically add a new tool to the manager."""
        self._tools[tool.name] = tool

tool_manager = ToolManager()

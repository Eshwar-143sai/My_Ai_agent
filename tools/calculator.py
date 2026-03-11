from langchain_core.tools import tool

@tool
def calculator(expression: str) -> str:
    """
    Evaluates a mathematical expression safely and returns the result.
    Use this tool whenever the user asks a math question or needs a calculation.
    Example: calculator("25 * 4 + 10")
    """
    try:
        # We use a restricted evaluation environment for safety
        allowed_names = {"__builtins__": None}
        result = eval(expression, allowed_names, {})
        return str(result)
    except Exception as e:
        return f"Error evaluating expression: {e}"

# This list defines all the tools the agent currently has access to.
# We will add more tools (like web search or file reading) here later.
AVAILABLE_TOOLS = [calculator]

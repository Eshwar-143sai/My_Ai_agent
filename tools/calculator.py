from langchain_core.tools import tool
from pydantic import BaseModel, Field

class CalculatorInput(BaseModel):
    expression: str = Field(description="The mathematical expression to evaluate (e.g. '25 * 4 + 10'). Do not use text.")

@tool("calculator", args_schema=CalculatorInput)
def calculator(expression: str) -> str:
    """
    Evaluates a mathematical expression safely and returns the result.
    Use this tool whenever the user asks a math question or needs a calculation.
    """
    try:
        allowed_names = {"__builtins__": None}
        result = eval(expression, allowed_names, {})
        return str(result)
    except Exception as e:
        return f"Error evaluating expression: {e}"

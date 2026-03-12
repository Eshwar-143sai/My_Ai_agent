from langchain_core.tools import tool
from pydantic import BaseModel, Field

class PlanInput(BaseModel):
    plan: str = Field(description="The step-by-step breakdown of how to solve the user's request. Must be detailed.")

@tool("planning_tool", args_schema=PlanInput)
def planning_tool(plan: str) -> str:
    """Use this tool at the beginning of a complex request to outline your execution strategy."""
    return f"Plan registered successfully:\n{plan}\n\nPlease proceed with executing Step 1."

from typing import Annotated, Sequence, TypedDict, List
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages


class AgentState(TypedDict):
    """
    The state schema for the LangGraph Agent.
    This defines the memory structure passed between nodes.
    
    Attributes:
        messages: A list of messages (Human, AI, System, Tool).
                  The `add_messages` reducer ensures new messages are appended
                  rather than replacing the entire list.
    """
    messages: Annotated[Sequence[BaseMessage], add_messages]

from typing import Annotated, Sequence, TypedDict
from langchain_core.messages import BaseMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode, tools_condition
from tools.calculator import AVAILABLE_TOOLS
from langgraph.graph.message import add_messages
import os

# 1. Define the State
# This is the memory of the agent. The `add_messages` tells the graph 
# to append new messages to the list, rather than overwrite it.
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]

def build_graph():
    # 2. Define the LLM Model
    # Here, we initialize OpenAI. You need an OPENAI_API_KEY in your .env
    model = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    
    # 3. Bind tools to the model
    # We tell the model what tools it has available
    model_with_tools = model.bind_tools(AVAILABLE_TOOLS)

    # 4. Define the Nodes (The actual work the agent does)
    
    # Node A: The Brain (LLM)
    def call_model(state: AgentState):
        messages = state['messages']
        
        # We can add a system message to give the agent a personality/instructions if it's the first message
        if not any(isinstance(m, SystemMessage) for m in messages):
            system_msg = SystemMessage(content="You are a helpful, all-purpose AI assistant. Use the tools provided to you to answer the user's questions.")
            messages = [system_msg] + messages
            
        response = model_with_tools.invoke(messages)
        return {"messages": [response]}

    # Node B: The Hands (Tools execution)
    tool_node = ToolNode(AVAILABLE_TOOLS)

    # 5. Build the Graph structure
    workflow = StateGraph(AgentState)
    
    # Add the nodes into the graph
    workflow.add_node("agent", call_model)
    workflow.add_node("tools", tool_node)
    
    # 6. Define the Edges (How to move between nodes)
    
    # Set the starting point
    workflow.set_entry_point("agent")
    
    # If the LLM router wants to use a tool, go to "tools".
    # If it is done and has a final answer, go to END.
    workflow.add_conditional_edges("agent", tools_condition)
    
    # Once the tools are done executing, ALWAYS go back to the agent to interpret the result
    workflow.add_edge("tools", "agent")
    
    # 7. Compile the graph
    app = workflow.compile()
    
    return app

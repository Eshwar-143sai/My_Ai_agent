from typing import Annotated, Sequence, TypedDict
from langchain_core.messages import BaseMessage, SystemMessage, AIMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode, tools_condition
from core.tool_manager import tool_manager
from langgraph.graph.message import add_messages
import os
import logging

# Configure basic logging for the Safety System
logging.basicConfig(level=logging.INFO, format="%(asctime)s - SAFETY_SYSTEM - %(message)s")

# 1. Fetch available tools dynamically from the new Tool Manager
AVAILABLE_TOOLS = tool_manager.get_all_tools()

# 2. Define the State
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]

def build_graph():
    # 3. Define the LLM Model
    model = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    
    # 4. Bind tools to the model
    model_with_tools = model.bind_tools(AVAILABLE_TOOLS)

    # 5. Define the Nodes
    
    # Node A: The Core Reasoning Agent
    def call_model(state: AgentState):
        messages = state['messages']
        
        if not any(isinstance(m, SystemMessage) for m in messages):
            system_msg = SystemMessage(content="You are a helpful enterprise-grade AI assistant. Use your tools to remember facts, recall information, or perform calculations. Always be polite.")
            messages = [system_msg] + messages
            
        response = model_with_tools.invoke(messages)
        return {"messages": [response]}

    # Node B: The Tool Executor
    tool_node = ToolNode(AVAILABLE_TOOLS)
    
    # Node C: The Safety System & Logger
    # This node intercepts the final LLM response before it reaches the end.
    def safety_check(state: AgentState):
        """
        Interrogates the last message to ensure it is safe to return to the user.
        In an enterprise setting, this could call a moderation API or a secondary SLM.
        """
        last_message = state['messages'][-1]
        
        # Only check if it's an AI message and actually contains text (not just a tool call)
        if isinstance(last_message, AIMessage) and last_message.content:
            log_msg = f"Output Length: {len(last_message.content)} chars, Contains Tools: {bool(last_message.tool_calls)}"
            logging.info(f"Verified Safe Response: {log_msg}")
            
            # Simple content check (example: blocking certain words)
            forbidden_words = ["hack", "exploit", "password_leak"]
            for word in forbidden_words:
                if word in last_message.content.lower():
                    logging.warning(f"Blocked harmful output containing '{word}'")
                    # Overwrite the message with a safe response
                    new_message = AIMessage(content="I'm sorry, I cannot fulfill that request due to safety policies.")
                    # We append the safe message
                    return {"messages": [new_message]}
                    
        return {"messages": []} # No change needed


    # 6. Build the Graph structure
    workflow = StateGraph(AgentState)
    
    # Add all nodes
    workflow.add_node("agent", call_model)
    workflow.add_node("tools", tool_node)
    workflow.add_node("safety", safety_check)
    
    # 7. Define the Edges
    workflow.set_entry_point("agent")
    
    # If the LLM wants tools, go to tools. Otherwise, go to our new Safety Check.
    workflow.add_conditional_edges(
        "agent", 
        tools_condition,
        {"tools": "tools", "__end__": "safety"}
    )
    
    # After tools run, go back to the agent to reason about the result
    workflow.add_edge("tools", "agent")
    
    # After the safety check clears, we are done
    workflow.add_edge("safety", END)
    
    # 8. Compile the graph
    app = workflow.compile()
    return app

import logging
from langchain_core.messages import SystemMessage, AIMessage
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode, tools_condition

# Import configurations, states, and tools
from core.config import settings
from core.state import AgentState
from core.tool_manager import tool_manager
from core.prompts import agent_prompt

# Phase 7: Enable InMemory Caching for the LLM globally
from langchain_core.globals import set_llm_cache
from langchain_core.caches import InMemoryCache
set_llm_cache(InMemoryCache())

# Configure basic logging for the Safety System
logging.basicConfig(level=logging.INFO, format="%(asctime)s - SAFETY_SYSTEM - %(message)s")

from core.llm_manager import get_llm_with_fallbacks

# Fetch available tools dynamically from the Tool Manager
AVAILABLE_TOOLS = tool_manager.get_all_tools()

# Bind the dynamic tools to our (potentially fallback-wrapped) LLM
model = get_llm_with_fallbacks()
model_with_tools = model.bind_tools(AVAILABLE_TOOLS)

def build_graph():
    # Load LLM dynamically based on user config
    model = get_llm()
    
    # Bind tools to the model
    model_with_tools = model.bind_tools(AVAILABLE_TOOLS)

    def call_model(state: AgentState):
        """Invoke the LLM using the centralized Agent Persona Prompt (Phase 7)."""
        prompt_value = agent_prompt.invoke({"messages": state['messages']})
        response = model_with_tools.invoke(prompt_value)
        return {"messages": [response]}

    # tool execution node
    tool_node = ToolNode(AVAILABLE_TOOLS)
    
    # Safety System & Logger
    def safety_check(state: AgentState):
        last_message = state['messages'][-1]
        
        if isinstance(last_message, AIMessage) and last_message.content:
            log_msg = f"Output Length: {len(last_message.content)} chars, Contains Tools: {bool(last_message.tool_calls)}"
            logging.info(f"Verified Safe Response: {log_msg}")
            
            # Simple word block list
            forbidden_words = ["hack", "exploit", "password_leak"]
            for word in forbidden_words:
                if word in last_message.content.lower():
                    logging.warning(f"Blocked harmful output containing '{word}'")
                    new_message = AIMessage(content="I'm sorry, I cannot fulfill that request due to safety policies.")
                    return {"messages": [new_message]}
                    
        return {"messages": []}

    # Build the Graph structure using explicitly typed AgentState
    workflow = StateGraph(AgentState)
    
    workflow.add_node("agent", call_model)
    workflow.add_node("tools", tool_node)
    workflow.add_node("safety", safety_check)
    
    workflow.set_entry_point("agent")
    
    workflow.add_conditional_edges(
        "agent", 
        tools_condition,
        {"tools": "tools", "__end__": "safety"}
    )
    
    workflow.add_edge("tools", "agent")
    workflow.add_edge("safety", END)
    # 8. Compile the graph with checkpointer (Enterprise Point 9)
    from langgraph.checkpoint.memory import MemorySaver
    checkpointer = MemorySaver()
    app = workflow.compile(checkpointer=checkpointer)
    return app

import os
from dotenv import load_dotenv
from typing import Annotated, Sequence, TypedDict
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langgraph.graph.message import add_messages

# --- 1. Load Environment Variables ---
# This looks for a .env file and loads the OPENAI_API_KEY
load_dotenv()

# --- 2. Define the Tools ---
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

AVAILABLE_TOOLS = [calculator]

# --- 3. Define the Graph State ---
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]

# --- 4. Build the Graph ---
def build_graph():
    # Initialize the LLM
    model = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    
    # Bind the tools to the LLM so it knows they exist
    model_with_tools = model.bind_tools(AVAILABLE_TOOLS)

    # Node A: The Agent reasoning node
    def call_model(state: AgentState):
        messages = state['messages']
        
        # Add system prompt if it's the very first message in the state
        if not any(isinstance(m, SystemMessage) for m in messages):
            sys_msg = SystemMessage(content="You are a helpful, logical AI assistant. Use the tools provided to answer questions precisely.")
            messages = [sys_msg] + messages
            
        response = model_with_tools.invoke(messages)
        return {"messages": [response]}

    # Node B: The Tool execution node
    tool_node = ToolNode(AVAILABLE_TOOLS)

    # Initialize the graph
    workflow = StateGraph(AgentState)
    
    # Add nodes
    workflow.add_node("agent", call_model)
    workflow.add_node("tools", tool_node)
    
    # Add edges
    workflow.set_entry_point("agent")
    workflow.add_conditional_edges("agent", tools_condition)
    workflow.add_edge("tools", "agent")
    
    # Compile
    return workflow.compile()

# --- 5. Main Execution Loop ---
def main():
    if not os.environ.get("OPENAI_API_KEY"):
        print("Error: OPENAI_API_KEY not found in environment variables.")
        print("Please check your .env file.")
        return

    print("==================================================")
    print("🤖 Welcome to Your AI Agent (Powered by LangGraph)")
    print("==================================================")
    print("Type 'quit' or 'exit' to end the conversation.\n")
    
    # Compile the graph
    app = build_graph()
    
    # Create the state dictionary to hold our conversation
    state = {"messages": []}

    while True:
        try:
            user_input = input("You: ")
            if user_input.lower() in ['quit', 'exit']:
                print("Goodbye! 👋")
                break
            
            # Add user input to state
            state["messages"].append(HumanMessage(content=user_input))
            
            # Stream the response from the graph
            print("\nAgent is thinking...")
            
            # We invoke the graph with the current state
            final_state = app.invoke(state)
            
            # The final response is the last message added to the state
            final_message = final_state["messages"][-1]
            print(f"\n🤖 Agent: {final_message.content}\n")
            
            # Update our local state to match the graph's memory for the next loop
            state = final_state
                
        except KeyboardInterrupt:
            print("\nGoodbye! 👋")
            break
        except Exception as e:
            print(f"\nAn error occurred: {e}")

if __name__ == "__main__":
    main()

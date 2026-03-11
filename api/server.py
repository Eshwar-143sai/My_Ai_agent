from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from core.graph import build_graph
from langchain_core.messages import HumanMessage

# Initialize the API Application
app = FastAPI(
    title="AI Agent API",
    description="Backend API for the Master AI Agent",
    version="1.0.0"
)

# Compile the agent graph once when the server starts
agent_graph = build_graph()

# Define the structure of the incoming request
class ChatRequest(BaseModel):
    user_id: str = "default_user"
    message: str

# Define the structure of the outgoing response
class ChatResponse(BaseModel):
    response: str
    status: str

@app.get("/")
def read_root():
    return {"status": "AI Agent API is running!"}

@app.post("/chat", response_model=ChatResponse)
def execute_chat(request: ChatRequest):
    """
    Main endpoint to interact with the AI Agent.
    Takes a message from the user, passes it through the LangGraph,
    and returns the final agent response.
    """
    try:
        # In a real production app, we would load the 'state' from a database 
        # using the 'user_id' to maintain conversation history across API calls.
        # For now, we will create a fresh state for each request to keep it simple.
        state = {"messages": [HumanMessage(content=request.message)]}
        
        # Invoke the graph
        final_state = agent_graph.invoke(state)
        
        # The final message in the state is the agent's response
        final_message = final_state["messages"][-1].content
        
        return ChatResponse(response=final_message, status="success")
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Note: To run this server, use the command:
# uvicorn api.server:app --reload

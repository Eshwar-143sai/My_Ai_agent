from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from core.graph import build_graph
from langchain_core.messages import HumanMessage
import json
import asyncio
import logging
from prometheus_fastapi_instrumentator import Instrumentator

# Configure Logging
logger = logging.getLogger("uvicorn.error")

# Initialize the API Application
app = FastAPI(
    title="Enterprise AI Agent API",
    description="A robust backend API for communicating with the LangGraph state machine.",
    version="2.0.0"
)

# Enterprise Phase 8: Point 8 - Monitoring Dashboard Metrics
# This auto-generates a /metrics endpoint that Prometheus can scrape!
Instrumentator().instrument(app).expose(app)

# Compile the agent graph once
agent_graph = build_graph()

# Input Schema for the standard chat
class ChatInput(BaseModel):
    user_id: str
    message: str

# Application State for the Graph (This schema is not directly used as an endpoint input/output, but for internal representation if needed)
class RequestState(BaseModel):
    messages: list

# Feedback Input Schema (Phase 8, Point 3)
class FeedbackInput(BaseModel):
    user_id: str
    message_id: str  # In the future, every generation gets a unique ID
    rating: int      # e.g., 1 (poor) to 5 (excellent)
    comment: str = None

class ChatResponse(BaseModel):
    response: str
    status: str

@app.get("/")
def read_root():
    return {"status": "AI Agent Enterprise API is running!"}

@app.post("/feedback")
async def submit_feedback(feedback: FeedbackInput):
    """
    RLHF / User Feedback Loop.
    For now, we log this asynchronously. Later, this feeds into PostgreSQL or LangSmith datasets.
    """
    logger.info(f"FEEDBACK RECIEVED: User {feedback.user_id} rated msg '{feedback.message_id}' a {feedback.rating}/5. Comment: {feedback.comment}")
    return {"status": "success", "message": "Feedback securely recorded for evaluation."}

@app.post("/chat", response_model=ChatResponse)
def execute_chat(request: ChatInput): # Changed ChatRequest to ChatInput
    """
    Standard endpoint (Enterprise Point 9: Session Management).
    Uses the user_id as a thread_id to persist memory across calls in the Graph checkpointer.
    """
    try:
        # Config allows the MemorySaver to store state per thread_id
        config = {"configurable": {"thread_id": request.user_id}}
        state = {"messages": [HumanMessage(content=request.message)]}
        
        final_state = agent_graph.invoke(state, config=config)
        final_message = final_state["messages"][-1].content
        
        return ChatResponse(response=final_message, status="success")
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat/stream")
async def execute_chat_stream(request: ChatRequest):
    """
    Streaming endpoint using Server-Sent Events (SSE) (Enterprise Point 4).
    Streams tokens back to the client in real-time.
    """
    config = {"configurable": {"thread_id": request.user_id}}
    state = {"messages": [HumanMessage(content=request.message)]}
    
    async def event_generator():
        try:
            # stream_mode="messages" yields tuples of (MessageChunk, Metadata)
            async for msg, metadata in agent_graph.astream(state, config=config, stream_mode="messages"):
                # Only stream content back from the AI
                if msg.content and metadata.get("langgraph_node") == "agent":
                    yield f"data: {json.dumps({'content': msg.content})}\n\n"
            yield "data: [DONE]\n\n"
        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")

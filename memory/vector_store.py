import os
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_core.tools import tool
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pydantic import BaseModel, Field
from core.config import settings

# 1. Initialize DB & Embeddings
embeddings = OpenAIEmbeddings(model="text-embedding-3-small", api_key=settings.openai_api_key)

# Initialize Chunking Strategy (Enterprise Point 3)
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

DB_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "chroma_data")
vector_store = Chroma(
    collection_name="agent_memory",
    embedding_function=embeddings,
    persist_directory=DB_DIR
)

# 2. Pydantic Schemas for Tools (Enterprise Point 2)
class MemorizeInput(BaseModel):
    text: str = Field(description="The actual information or document text to remember.")
    source: str = Field(description="Where this info came from (e.g., 'user', 'filename.pdf').", default="user_conversation")
    user_id: str = Field(description="The unique ID of the user this memory belongs to.", default="default_user")

class RecallInput(BaseModel):
    query: str = Field(description="What you are trying to remember or search for.")
    user_id: str = Field(description="The unique ID of the user whose memory you are searching.", default="default_user")

@tool("memorize_information", args_schema=MemorizeInput)
def memorize_information(text: str, source: str = "user_conversation", user_id: str = "default_user") -> str:
    """Saves important information, facts, or documents into long-term memory."""
    try:
        # Point 3: Document Chunking
        chunks = text_splitter.split_text(text)
        
        # Point 3: Metadata Storage
        docs = [Document(page_content=chunk, metadata={"source": source, "user_id": user_id}) for chunk in chunks]
        
        vector_store.add_documents(docs)
        return f"Successfully chunked and saved {len(docs)} segments to memory for user {user_id}."
    except Exception as e:
        return f"Failed to save to memory: {e}"

@tool("recall_information", args_schema=RecallInput)
def recall_information(query: str, user_id: str = "default_user") -> str:
    """Searches long-term memory for information relating to the query."""
    try:
        # Point 3: Metadata filtering (ensures agent only recalls memories for the matching user_id)
        filter_dict = {"user_id": user_id}
        results = vector_store.similarity_search(query, k=3, filter=filter_dict)
        
        if not results:
            return f"No relevant information found in memory for user {user_id}."
            
        formatted_results = []
        for i, res in enumerate(results):
            src = res.metadata.get('source', 'unknown')
            formatted_results.append(f"Match {i+1} (Source: {src}): {res.page_content}")
            
        return "\n\n".join(formatted_results)
    except Exception as e:
        return f"Failed to recall information: {e}"

# Export the tools
MEMORY_TOOLS = [memorize_information, recall_information]

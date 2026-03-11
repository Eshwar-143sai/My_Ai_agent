import os
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_core.tools import tool
from langchain_core.documents import Document

# 1. Initialize the Database and Embeddings
# We use OpenAI's embedding model to turn text into vectors
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

# Create a local ChromaDB instance that persists to a folder named 'chroma_data'
DB_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "chroma_data")
vector_store = Chroma(
    collection_name="agent_memory",
    embedding_function=embeddings,
    persist_directory=DB_DIR
)

# 2. Define the Tools for the Agent

@tool
def memorize_information(text: str, source: str = "user_conversation") -> str:
    """
    Saves important information, facts, or documents into long-term memory.
    Use this tool when the user tells you to remember something, or when you read
    a document that might be useful later.
    Args:
        text: The actual information to remember.
        source: Where this info came from (e.g., 'user', 'filename.pdf').
    """
    try:
        doc = Document(page_content=text, metadata={"source": source})
        vector_store.add_documents([doc])
        return f"Successfully saved to long-term memory: '{text[:50]}...'"
    except Exception as e:
        return f"Failed to save to memory: {e}"


@tool
def recall_information(query: str) -> str:
    """
    Searches your long-term memory for information relating to the query.
    Use this tool when you need to remember past facts, read past documents, 
    or answer questions about things the user told you before.
    Args:
        query: What you are trying to remember (be descriptive).
    """
    try:
        # Perform a vector similarity search, fetching the top 3 closest matches
        results = vector_store.similarity_search(query, k=3)
        
        if not results:
            return "No relevant information found in memory."
            
        formatted_results = []
        for i, res in enumerate(results):
            source = res.metadata.get('source', 'unknown')
            formatted_results.append(f"Match {i+1} (Source: {source}): {res.page_content}")
            
        return "\n\n".join(formatted_results)
    except Exception as e:
        return f"Failed to recall information: {e}"

# Export the tools
MEMORY_TOOLS = [memorize_information, recall_information]

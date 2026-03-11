import os
import uvicorn
from dotenv import load_dotenv

# Load Environment Variables from .env file
load_dotenv()

def main():
    if not os.environ.get("OPENAI_API_KEY"):
        print("Error: OPENAI_API_KEY not found in environment variables.")
        print("Please configure your .env file before starting the server.")
        return

    print("==================================================")
    print("🚀 Starting AI Agent API Server...")
    print("==================================================")
    print("To chat with the agent, send a POST request to:")
    print("http://127.0.0.1:8000/chat")
    print("\nOr open the interactive docs at: http://127.0.0.1:8000/docs\n")
    
    # Run the FastAPI server via Uvicorn
    # Make sure to run this file so uvicorn starts the server
    uvicorn.run("api.server:app", host="127.0.0.1", port=8000, reload=True)

if __name__ == "__main__":
    main()

# Enterprise AI Agent Architecture

This document describes the flow of our LangGraph state machine.

```mermaid
graph TD
    %% Define styles
    classDef llm fill:#f9f,stroke:#333,stroke-width:2px;
    classDef tool fill:#bbf,stroke:#333,stroke-width:2px;
    classDef safety fill:#ff9,stroke:#333,stroke-width:2px;
    classDef endpoint fill:#bfb,stroke:#333,stroke-width:2px;

    %% Client / API Layer
    Client([Client / API User]) --> FastAPI[FastAPI Backend]:::endpoint
    FastAPI --> DB[(SQLite Feedback DB)]
    FastAPI --> Checkpointer[(SQLite Memory Saver)]

    %% LangGraph Core
    FastAPI -- State Context --> AgentNode{LLM Router Node}:::llm
    
    %% Routing Logic
    AgentNode -- Tool Call --> ToolNode[Tool Execution Node]:::tool
    ToolNode -- Result --> AgentNode
    
    %% Tools Available
    subgraph "Dynamic Tools Library"
        ToolNode -.-> VectorStore[(Chroma Vector DB)]
        ToolNode -.-> WebSearch[Tavily Search API]
        ToolNode -.-> CodeExec[Sandboxed Python Exec]
        ToolNode -.-> Planner[Task Planner]
    end

    %% Safety & Egress
    AgentNode -- Final Answer --> SafetyNode{Safety Output Filter}:::safety
    SafetyNode -- OK --> Return[Stream / Return Response]
    SafetyNode -- Blocked --> BlockError[Return Block Message]
    
    Return --> Client
    BlockError --> Client
```

## Key Components

1.  **FastAPI Endpoint:** Receives the `/chat` or `/feedback` requests and initializes connection to the LangGraph graph using `thread_id` session memory.
2.  **LLM Router Node (`core/graph.py`):** The primary brain. Prompts the OpenAI model and determines if internal tool execution is necessary.
3.  **Tool Execution Node:** Dynamically loads available python tools from the `tools/` folder. Contains tools for vector storage retrieval, web searching, planning, and executing code snippets.
4.  **Safety System:** Intercepts the final message before it returns to the user to ensure it does not contain restricted content or fail business rules.
5.  **Telemetry & Feedback:** Exposes `/metrics` for Prometheus and stores 5-star conversation RLHF flags in `feedback.db`.

# My AI Agent 🤖 Enterprise Edition

![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.103.2-009688.svg)
![LangGraph](https://img.shields.io/badge/LangGraph-State_Machine-orange.svg)
![Docker](https://img.shields.io/badge/Docker-Supported-2496ED.svg)

A modular, multi-capable, and production-ready AI assistant built with **LangGraph** and **Python FastApi**. 

![Demo GIF](https://via.placeholder.com/800x400?text=Agent+Demonstration+GIF+Placeholder)

## 🚀 Features

*   **Production API:** Robust FastAPI backend with standard `/chat`, streaming `/chat/stream`, and `/feedback` endpoints.
*   **Stateful Memory:** Persists conversation threads using LangGraph's Checkpointer and saves contextual facts to ChromaDB.
*   **Dynamic Tools:** Includes Web Search, Python Sandbox, Calculator, and advanced Planner routing.
*   **Telemetry:** Built-in Prometheus `/metrics` endpoint with ready-to-deploy Grafana dashboards.
*   **Safety Layer:** Custom graph node intercepts and validates LLM generation before responding.

## 🛠️ Architecture

See our full [Architecture Flowchart](ARCHITECTURE.md) for a detailed look at how the LangGraph nodes communicate.

## 📦 Project Structure

```text
My_Ai_agent/
├── api/              # FastAPI server and HTTP endpoints
├── core/             # LangGraph state machine, config, tools manager
├── memory/           # ChromaDB Semantic chunking and vector retrieval
├── tools/            # Python functionality (Calculator, Code Exec, Web, Planner)
├── tests/            # Pytest test suites
├── grafana/          # Telemetry dashboard definitions
└── main.py           # CLI Loop
```

## 🚀 Getting Started

Ensure you have Python 3.10+ and optionally Docker installed.

### 1. Setup

Clone and install dependencies via pip:
```bash
git clone https://github.com/Eshwar-143sai/My_Ai_agent.git
cd My_Ai_agent
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configuration
Create a `.env` file in the root directory:
```env
OPENAI_API_KEY=your_api_key_here
TAVILY_API_KEY=your_tavily_key
```

### 3. Run the Agent Server!
```bash
uvicorn api.server:app --reload
```
You can now access the Swagger Documentation at `http://localhost:8000/docs`.

### cURL Examples

**Standard Chat:**
```bash
curl -X POST "http://localhost:8000/chat" \
     -H "Content-Type: application/json" \
     -d '{"user_id": "user123", "message": "What is the capital of France?"}'
```

**Add Feedback:**
```bash
curl -X POST "http://localhost:8000/feedback" \
     -H "Content-Type: application/json" \
     -d '{"conversation_id": "conv-1", "rating": 5, "comment": "Perfect answer."}'
```

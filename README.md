# My AI Agent 🤖

A modular, multi-capable AI assistant built with **LangGraph** and **Python**.
This agent uses a state-graph architecture (Reason & Act) to orchestrate LLM intelligence with real-world tool execution.

## 🚀 Features

*   **Stateful Memory:** Remembers conversation history throughout the session using LangGraph's `AgentState`.
*   **Tool Calling:** Automatically routes to specialized tools when required (e.g., performing complex math calculations).
*   **Dynamic Routing:** The LLM acts as the central router, deciding whether to answer directly or execute code based on the user's prompt.
*   **Command Line Interface:** A clean built-in terminal loop for easy communication.

## 🛠️ Architecture

*   **[LangGraph](https://langchain-ai.github.io/langgraph/):** Orchestrates the node-based workflow (`call_model` node and `tools` node).
*   **[LangChain](https://python.langchain.com/):** Provides the underlying abstractions for LLMs and Tools.
*   **LLM Provider:** Powered by OpenAI (`gpt-4o-mini`).

## 📦 Project Structure

```text
ai_agent/
│
├── core/
│   └── graph.py          # The core LangGraph state machine logic
├── tools/
│   └── calculator.py     # Custom tool definitions
├── main.py               # The CLI execution loop
├── architecture_plan.md  # Detailed explanation of how the graph works
└── .env                  # (Hidden) API Key configuration
```

## 🚀 Getting Started

### 1. Requirements
Ensure you have Python 3.10+ installed.

### 2. Setup

Clone the repository and create a virtual environment:
```bash
git clone https://github.com/Eshwar-143sai/My_Ai_agent.git
cd My_Ai_agent
python -m venv venv
```

Activate the virtual environment:
*   **Windows:** `.\venv\Scripts\activate`
*   **Mac/Linux:** `source venv/bin/activate`

Install dependencies:
```bash
pip install langgraph langchain langchain-openai python-dotenv
```

### 3. Configuration
Create a `.env` file in the root directory and add your OpenAI API key:
```env
OPENAI_API_KEY=your_api_key_here
```

### 4. Run the Agent
```bash
python main.py
```

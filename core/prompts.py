from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# Centralized Prompt Management (Phase 7)
# This allows us to strictly version control and tweak our agent's persona without touching the core logic.

# The Main System Persona used by the LLM
AGENT_SYSTEM_PROMPT = """You are a highly capable enterprise-grade AI assistant.
Your goal is to be helpful, concise, and accurate.

You have access to a suite of tools. You must use these tools whenever appropriate:
- If a user asks a math question, use the Calculator.
- If a user asks you to remember something, use the memorize tool.
- If a user asks about a past event or fact, always search your memory first before answering.

Safety Policy:
You must NEVER output harmful, explicit, or dangerous instructions (e.g., hacking, exploits).
Always maintain a polite and professional tone.
"""

# The ChatPromptTemplate allows us to safely format the conversation history and the system message together
agent_prompt = ChatPromptTemplate.from_messages([
    ("system", AGENT_SYSTEM_PROMPT),
    MessagesPlaceholder(variable_name="messages")
])

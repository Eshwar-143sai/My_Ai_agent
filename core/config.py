from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Literal

class Settings(BaseSettings):
    """
    Project Configuration using pydantic-settings.
    Automatically loads variables from the .env file and validates them.
    """
    # LLM Settings
    llm_provider: Literal["openai", "anthropic", "ollama"] = "openai"
    llm_model_name: str = "gpt-4o-mini"
    llm_temperature: float = 0.0
    
    
    # API Keys
    openai_api_key: str = ""
    anthropic_api_key: str = ""
    tavily_api_key: str = ""
    
    # LangSmith / Logging Management (Phase 7 Monitoring)
    langchain_tracing_v2: bool = False
    langchain_api_key: str = ""
    langchain_project: str = "My_AI_Agent"
    
    # Check that it loads `.env`
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

# Instantiate a global settings object
settings = Settings()

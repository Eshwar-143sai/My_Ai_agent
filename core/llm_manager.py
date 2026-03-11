from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_core.language_models.chat_models import BaseChatModel
from core.config import settings

def get_llm_with_fallbacks() -> BaseChatModel:
    """
    Creates an abstraction layer for the LLM client supporting multiple providers (OpenAI, Anthropic).
    Includes automated fallback routing: if the primary provider hits rate limits or fails, 
    it tries the secondary models automatically.
    """
    primary_model_name = settings.llm_model_name
    primary_model = ChatOpenAI(model=primary_model_name, temperature=settings.llm_temperature)

    fallbacks = []
    
    # Priority Fallback: Anthropic Claude 3
    if settings.anthropic_api_key:
        fallbacks.append(ChatAnthropic(model="claude-3-haiku-20240307", temperature=settings.llm_temperature))

    # Secondary Fallback: Cheaper OpenAI model
    if primary_model_name != "gpt-4o-mini" and settings.openai_api_key:
        fallbacks.append(ChatOpenAI(model="gpt-4o-mini", temperature=settings.llm_temperature))

    # Return abstracted agent brain
    if fallbacks:
        return primary_model.with_fallbacks(fallbacks)
    return primary_model

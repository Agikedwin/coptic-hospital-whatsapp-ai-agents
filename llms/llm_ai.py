import os

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_ollama import ChatOllama


# Load variables from .env
load_dotenv()


def get_llm(provider: str, model: str):
    provider = provider.lower().strip()
    # =========================================================
    # OPENAI
    # =========================================================
    if provider == "openai":
        return init_chat_model(
            f"openai:{model}",
            api_key=os.getenv("OPENAI_API_KEY"),
            temperature=0
        )

    # =========================================================
    # ANTHROPIC
    # =========================================================
    elif provider == "anthropic":
        return init_chat_model(
            f"anthropic:{model}",
            api_key=os.getenv("ANTHROPIC_API_KEY"),
            temperature=0
        )

    # =========================================================
    # GOOGLE / GEMINI
    # =========================================================
    elif provider in ["google", "gemini"]:
        return init_chat_model(
            f"google_genai:{model}",
            api_key=os.getenv("GEMINI_API_KEY"),
            temperature=0
        )

    # =========================================================
    # GROQ
    # =========================================================
    elif provider == "groq":

        groq_api_key = os.getenv("GROQ_API_KEY")

        if not groq_api_key:
            raise ValueError(
                "GROQ_API_KEY is not set in the environment."
            )

        return init_chat_model(
            f"groq:{model}",
            api_key=groq_api_key,
            temperature=0
        )

    # =========================================================
    # DEEPSEEK
    # =========================================================
    elif provider in ["deepseek", "seepseek"]:

        api_key = os.getenv("DEEPSEEK_API_KEY")

        if not api_key:
            raise ValueError(
                "DEEPSEEK_API_KEY is not set in the environment."
            )

        return init_chat_model(
            model=model,
            api_key=api_key,
            temperature=0
        )

    # =========================================================
    # OLLAMA / LOCAL LLM
    # =========================================================
    elif provider in ["ollama", "local"]:

        ollama_base_url = os.getenv(
            "OLLAMA_BASE_URL",
            "http://10.1.1.33:11434"
        )

        return ChatOllama(
            model=model,
            base_url=ollama_base_url,
            temperature=0
        )

    # =========================================================
    # UNSUPPORTED PROVIDER
    # =========================================================
    else:
        raise ValueError(
            f"Unsupported provider: {provider}"
        )
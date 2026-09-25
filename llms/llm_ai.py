import os

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model


# Load variables from .env
load_dotenv()


def get_llm(provider: str, model: str):
    provider = provider.lower().strip()

    if provider == "openai":
        return init_chat_model(
            f"openai:{model}",
            api_key=os.getenv("OPENAI_API_KEY"),
            temperature=0
        )

    elif provider == "anthropic":
        return init_chat_model(
            f"anthropic:{model}",
            api_key=os.getenv("ANTHROPIC_API_KEY"),
            temperature=0
        )

    elif provider in ["google", "gemini"]:
        return init_chat_model(
            f"google_genai:{model}",
            api_key=os.getenv("GEMINI_API_KEY"),
            temperature=0
        )

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

    else:
        raise ValueError(
            f"Unsupported provider: {provider}"
        )
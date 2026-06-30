from src.config import LLM_PROVIDER, OLLAMA_BASE_URL

# Local LLM provided by Ollama
if LLM_PROVIDER == "ollama":
    from langchain_ollama import ChatOllama

    llm = ChatOllama(
        model="qwen2.5:3b",
        temperature=0.0,
        base_url=OLLAMA_BASE_URL,
        )

# Cloud LLM provided by the Google Gemini API
elif LLM_PROVIDER == "google":
    from langchain_google_genai import ChatGoogleGenerativeAI

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.0,
        )
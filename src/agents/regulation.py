from pathlib import Path
from src.schemas import MarketState
from src.tools.web_search import search_web
from src.tools.rag import retrieve_internal_context
from src.llm import llm


# Regulation Agent focusing on the legal and political aspects


def load_prompt() -> str:
    path = Path("src/prompts/regulation.txt")
    return path.read_text(encoding="utf-8")


def regulation_node(state: MarketState):
    template = load_prompt()

    # Web search & RAG
    search_results = search_web(f"{state['topic']} regulation and sustainability risks {state['industry']} {state['region']} {state['horizon']}")
    internal_context = retrieve_internal_context(f"{state['topic']} supply chain {state['industry']} {state['region']}")

    prompt = template.format(
        topic=state["topic"],
        industry=state["industry"],
        region=state["region"],
        horizon=state["horizon"],
        search_results=search_results["text"],
        internal_context=internal_context,
    )

    # Prompting LLM
    result = llm.invoke(prompt)

    return {
        "regulation_result": result.content,
        "regulation_sources": search_results["sources"],
        }
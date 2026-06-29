from pathlib import Path
from schemas import MarketState
from tools.web_search import search_web
from tools.rag import retrieve_internal_context
from llm import llm


# Market Trends Agent focusing on market dynamics and future outlook


def load_prompt() -> str:
    path = Path("prompts/market_trends.txt")
    return path.read_text(encoding="utf-8")


def market_trends_node(state: MarketState):
    template = load_prompt()

    # Web search & RAG
    search_results = search_web(f"{state['topic']} market trends {state['industry']} {state['region']} {state['horizon']}")
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
        "market_trends_result": result.content,
        "market_trends_sources": search_results["sources"],
        }
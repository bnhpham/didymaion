from pathlib import Path
from schemas import MarketState, QueryUnderstandingOutput
from llm import llm


# Query Understanding Agent processing natural language business questions


def load_prompt() -> str:
    return Path("prompts/query_understanding.txt").read_text(encoding="utf-8")


def query_understanding_node(state: MarketState):
    prompt = load_prompt().format(
        query=state["query"]
    )

    structured_llm = llm.with_structured_output(QueryUnderstandingOutput)
    result = structured_llm.invoke(prompt)

    return {
        "topic": result.topic,
        "industry": result.industry,
        "region": result.region,
        "horizon": result.horizon,
        "query_understanding": result,
    }
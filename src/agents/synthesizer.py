from pathlib import Path
from src.schemas import MarketState
from src.llm import llm


# Synthesis Agent that combines all specialist analyses into one business report


def load_prompt() -> str:
    path = Path("src/prompts/synthesis.txt")
    return path.read_text(encoding="utf-8")


def synthesis_node(state: MarketState):
    template = load_prompt()

    prompt = template.format(
        supply_chain_result=state["supply_chain_result"],
        regulation_result=state["regulation_result"],
        market_trends_result=state["market_trends_result"],
        supply_chain_sources=state["supply_chain_sources"],
        regulation_sources=state["regulation_sources"],
        market_trends_sources=state["market_trends_sources"],
    )

    result = llm.invoke(prompt)

    return {"final_report": result.content}
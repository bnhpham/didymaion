from pathlib import Path
from src.schemas import MarketState, PlannerOutput
from src.llm import llm


# Planning Agent dynamically selecting specialist agents


def load_prompt() -> str:
    return Path("src/prompts/planner.txt").read_text(encoding="utf-8")


def planner_node(state: MarketState):
    prompt = load_prompt().format(
        topic=state["topic"],
        industry=state["industry"],
        region=state["region"],
        horizon=state["horizon"],
    )
    
    structured_llm = llm.with_structured_output(PlannerOutput)
    planner_output = structured_llm.invoke(prompt)

    return {"planner": planner_output}
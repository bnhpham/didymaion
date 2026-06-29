from fastapi import FastAPI

from schemas import AnalysisResponse, NaturalLanguageRequest
from orchestrator import run_market_analysis_from_query


app = FastAPI(title="Didymaion")


@app.get("/")
def root():
    return {"message": "Multi-Agent System \"Didymaion\" is running."}


# Forwards the user's business question to the multi-agent system and returns the final report
@app.post("/analyze-query", response_model=AnalysisResponse)
def analyze_query(request: NaturalLanguageRequest):
    report = run_market_analysis_from_query(request.query)

    return {
        "topic": report["topic"],
        "industry": report["industry"],
        "region": report["region"],
        "horizon": report["horizon"],
        "selected_agents": report["planner"].selected_agents,
        "reasoning": report["planner"].reasoning,
        "report": report["final_report"],
        "sources": {
            "supply_chain": report["supply_chain_sources"],
            "regulation": report["regulation_sources"],
            "market_trends": report["market_trends_sources"],
        },
    }
       
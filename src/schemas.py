from typing import TypedDict
from pydantic import BaseModel


# This file defines the structure of API requests, API responses and LLM outputs


# User's natural language input sent to the API
class NaturalLanguageRequest(BaseModel):
    query: str


# Output produced by the Query Understanding Agent
class QueryUnderstandingOutput(BaseModel):
    topic: str
    industry: str
    region: str
    horizon: str


# Stores the URLs returned by each specialist agent
class SourceGroups(BaseModel):
    supply_chain: list[str]
    regulation: list[str]
    market_trends: list[str]


# Planning Agent's decision
class PlannerOutput(BaseModel):
    selected_agents: list[str]
    reasoning: str


# Complete JSON response returned by your FastAPI endpoint
class AnalysisResponse(BaseModel):
    topic: str
    industry: str
    region: str
    horizon: str

    selected_agents: list[str]
    reasoning: str
    
    report: str

    sources: SourceGroups


# Shared memory (state) of the LangGraph workflow
# Passed from one node to the next: Query Understanding -> Planning -> Supply Chain -> Regulation -> Market Trends -> Synthesis
# Each node reads values from the state and writes new values back into it
class MarketState(TypedDict):
    query: str

    topic: str
    industry: str
    region: str
    horizon: str

    query_understanding: QueryUnderstandingOutput
    planner: PlannerOutput

    supply_chain_result: str
    regulation_result: str
    market_trends_result: str

    # Web sources
    supply_chain_sources: list[str]
    regulation_sources: list[str]
    market_trends_sources: list[str]

    final_report: str
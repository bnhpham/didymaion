from langgraph.graph import StateGraph, END

from schemas import MarketState, PlannerOutput, QueryUnderstandingOutput
from agents.query_understanding import query_understanding_node
from agents.planner import planner_node
from agents.supply_chain import supply_chain_node
from agents.regulation import regulation_node
from agents.market_trends import market_trends_node
from agents.synthesizer import synthesis_node


# This file defines the workflow of the multi-agent system
# it decides which agent runs next, builds the LangGraph, and coordinates the execution


# Reads the Planning Agent's output and decides which specialist agent should execute first based on the selected agents
def route_after_planner(state: MarketState):
    selected = state["planner"].selected_agents

    if "supply_chain" in selected:
        return "supply_chain"
    if "regulation" in selected:
        return "regulation"
    if "market_trends" in selected:
        return "market_trends"

    return "synthesis"


# After the Supply Chain Agent finishes, it checks whether the Regulation and/or Market Trends agents still need to run 
# If not, it proceeds directly to the Synthesis Agent
def route_after_supply_chain(state: MarketState):
    selected = state["planner"].selected_agents

    if "regulation" in selected:
        return "regulation"
    if "market_trends" in selected:
        return "market_trends"

    return "synthesis"


# After the Regulation Agent finishes, it checks whether the Market Trends Agent still needs to run
# If not, it proceeds to the Synthesis Agent
def route_after_regulation(state: MarketState):
    selected = state["planner"].selected_agents

    if "market_trends" in selected:
        return "market_trends"

    return "synthesis"


# Construct the complete LangGraph workflow
def build_graph():

    graph = StateGraph(MarketState)

    graph.add_node("query_understanding", query_understanding_node)
    graph.add_node("planner", planner_node)
    graph.add_node("supply_chain", supply_chain_node)
    graph.add_node("regulation", regulation_node)
    graph.add_node("market_trends", market_trends_node)
    graph.add_node("synthesis", synthesis_node)

    graph.set_entry_point("query_understanding")
    graph.add_edge("query_understanding", "planner")

    graph.add_conditional_edges("planner", route_after_planner)
    graph.add_conditional_edges("supply_chain", route_after_supply_chain)
    graph.add_conditional_edges("regulation", route_after_regulation)

    graph.add_edge("market_trends", "synthesis")
    graph.add_edge("synthesis", END)

    return graph.compile()


# Build the lang graph once when the application starts
market_graph = build_graph()


# Initialize the shared MarketState with the user's query and empty placeholders
# Execute the LangGraph workflow and return the final state containing all intermediate and final results
def run_market_analysis_from_query(query: str) -> dict:
    
    result = market_graph.invoke({
        "query": query,

        "topic": "",
        "industry": "",
        "region": "",
        "horizon": "",

        "query_understanding": QueryUnderstandingOutput(
            topic="",
            industry="",
            region="",
            horizon="",
        ),

        "planner": PlannerOutput(
            selected_agents=[],
            reasoning="",
        ),

        "supply_chain_result": "",
        "regulation_result": "",
        "market_trends_result": "",

        "supply_chain_sources": [],
        "regulation_sources": [],
        "market_trends_sources": [],

        "final_report": "",
    })

    print("RESULT: ")
    print(result)

    return result
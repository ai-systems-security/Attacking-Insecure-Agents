# multi_agent_runner.py
import sys
from typing import TypedDict, List
from langgraph.graph import StateGraph, END

from recruiter_core import (
    ingest_resumes,
    collection,
    SemanticSearchAgent,
    EvaluationAgent,
    DecisionAgent,
)

# -------------------------
# Define the LangGraph State schema
# -------------------------
class RecruiterState(TypedDict):
    job_desc: str
    candidates: List[dict]
    evals: List[dict]
    memory: List[dict]
    decision: str

# -------------------------
# Node functions
# -------------------------
def semantic_search_node(state: RecruiterState):
    search_agent = SemanticSearchAgent(collection)
    candidates = search_agent.search_candidates(state["job_desc"], k=3)
    return {"candidates": candidates}

def evaluation_node(state: RecruiterState):
    eval_agent = EvaluationAgent()
    evals, memory = eval_agent.evaluate_candidates(state["job_desc"], state["candidates"])
    return {"evals": evals, "memory": memory}

def decision_node(state: RecruiterState):
    dec_agent = DecisionAgent()
    decision = dec_agent.select_best_candidate(state["memory"])
    return {"decision": decision}

# -------------------------
# Build LangGraph pipeline
# -------------------------
def build_graph():
    graph = StateGraph(RecruiterState)

    graph.add_node("semantic_search", semantic_search_node)
    graph.add_node("evaluation", evaluation_node)
    graph.add_node("decision", decision_node)

    graph.set_entry_point("semantic_search")
    graph.add_edge("semantic_search", "evaluation")
    graph.add_edge("evaluation", "decision")
    graph.add_edge("decision", END)

    return graph.compile()

# -------------------------
# Main Runner
# -------------------------
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("❌ Usage: python multi_agent_runner.py '<job description>'")
        sys.exit(1)

    job_desc = sys.argv[1]

    print("📥 Ingesting resumes...")
    ingest_resumes("data/resumes")

    print("🚀 Running Multi-Agent Recruiter Pipeline...")
    graph = build_graph()

    initial_state: RecruiterState = {
        "job_desc": job_desc,
        "candidates": [],
        "evals": [],
        "memory": [],
        "decision": "",
    }

    final_state = graph.invoke(initial_state)

    print("\n📊 Candidate Evaluations:")
    for e in final_state["evals"]:
        print(f"\n--- {e['name']} ---\n{e['evaluation']}")

    print("\n✅ Final Decision:")
    print(final_state["decision"])
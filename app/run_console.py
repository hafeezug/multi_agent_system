import os
import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"  # Fix OpenMP DLL error on Windows

from app.memory.kb_loader import load_sample_kb
from app.agents.memory_agent import MemoryAgent
from app.agents.research_agent import ResearchAgent
from app.agents.analysis_agent import AnalysisAgent
from app.coordinator import Coordinator

def build_system():
    # Initializing memory
    mem = MemoryAgent()
    # Loading mock KB
    kb = load_sample_kb()
    for rec in kb:
        mem.add_knowledge(rec["id"], rec["text"], rec["meta"])
    # Initializing agents
    research = ResearchAgent(mem, kb=kb)
    analysis = AnalysisAgent(mem)
    # Return Coordinator + memory
    return Coordinator(research, analysis, mem), mem

def run_scenarios():
    manager, mem = build_system()
    # Predefined test scenarios
    scenarios = {
        "simple_query": "What are the main types of neural networks?",
        "complex_query": "Research transformer architectures, analyze their computational efficiency, and summarize key trade-offs.",
        "memory_test": "What did we discuss about neural networks earlier?",
        "multi_step": "Find recent papers on reinforcement learning, analyze their methodologies, and identify common challenges.",
        "collaborative": "Compare Adam and gradient descent and recommend which is better."
    }
    os.makedirs("outputs", exist_ok=True)
    for name, query in scenarios.items():
        # Handles each query via Coordinator
        result = manager.handle(query)
        # Saves result to file
        with open(f"outputs/{name}.txt", "w", encoding="utf-8") as f:
            f.write(result["answer"])
        print(f"\n{name.upper()}:\n{result['answer']}")
    # Saves trace of all interactions
    mem.dump_trace("outputs/memory_trace.json")

if __name__ == "__main__":
    run_scenarios()
    print("\nDone.")
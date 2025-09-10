import uuid

class ResearchAgent:
    def __init__(self, memory_agent, kb=None):
        self.memory = memory_agent
        self.kb = kb or []

    def find(self, query, top_k=5):
        # First it tries semantic search in memory
        results = self.memory.semantic_search(query, top_k=top_k)
        # If nothing found, it fallbacks to KB (mock search)
        if not results:
            results = [{"id": r["id"], "text": r["text"], "meta": r["meta"], "score": 0.1} for r in self.kb[:top_k]]
        # Then Adds results into memory
        for r in results:
            self.memory.add_knowledge(r["id"], r["text"], r["meta"])
        # Records agent’s action in memory
        self.memory.update_agent_state("research", str(uuid.uuid4()), {"query": query, "count": len(results)})
        return results

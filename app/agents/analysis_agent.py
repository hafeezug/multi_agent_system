import uuid

class AnalysisAgent:
    def __init__(self, memory_agent):
        self.memory = memory_agent

    def compare(self, items):
        ranked = []
        # Assignning simple heuristic scores for ranking items
        for it in items:
            score = 0.5
            if "adam" in it["text"].lower():
                score = 0.9
            elif "gradient descent" in it["text"].lower():
                score = 0.7
            ranked.append({"id": it["id"], "summary": it["text"], "score": score})
        # Sorts results by score
        ranked.sort(key=lambda x: x["score"], reverse=True)
        # Then Updates memory state
        self.memory.update_agent_state("analysis", str(uuid.uuid4()), {"ranking": [r["id"] for r in ranked]})
        # Returns ranking + confidence score
        return {"ranking": ranked, "confidence": sum(r["score"] for r in ranked)/len(ranked)}

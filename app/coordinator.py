import uuid
from app.utils import trace_msg
from app.llm_client import LLMClient

class Coordinator:
    def __init__(self, research_agent, analysis_agent, memory_agent):
        self.research = research_agent
        self.analysis = analysis_agent
        self.memory = memory_agent
        self.trace = []
        self.llm = LLMClient()

    def complexity_analysis(self, query):
        # Uses LLM to classify query complexity
        label, conf = self.llm.classify_complexity(query)
        # Record classification step
        self.trace.append(trace_msg("classification", {"query": query, "label": label, "confidence": conf}))
        return label

    def plan(self, query):
        # Decides the workflow based on complexity
        level = self.complexity_analysis(query)
        if level == "simple":
            return ["research"]
        return ["research", "analysis"]

    def handle(self, user_query):
        # Creates unique task ID
        task_id = str(uuid.uuid4())
        #  Workflow planning
        plan = self.plan(user_query)
        research_out, analysis_out = None, None
        #  Research step execution
        if "research" in plan:
            research_out = self.research.find(user_query)
        # Analysis step execution
        if "analysis" in plan and research_out:
            analysis_out = self.analysis.compare(research_out)
        #  Final answer generation
        answer = self.synthesize(user_query, research_out, analysis_out)
        # Saving conversation in memory
        self.memory.add_conversation(user_query, answer)
        return {"answer": answer, "plan": plan}

    def synthesize(self, query, research_out, analysis_out):
        # Merging outputs into human-readable response
        lines = [f"Q: {query}"]
        if research_out:
            lines.append("Research:")
            for r in research_out:
                lines.append(f"- {r['text']} (score={r['score']:.2f})")
        if analysis_out:
            lines.append("Analysis:")
            for r in analysis_out["ranking"]:
                lines.append(f"- {r['summary']} (score={r['score']})")
        return "\n".join(lines)

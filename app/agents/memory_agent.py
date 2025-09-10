import json
from app.memory.vector_store import VectorStore
from app.utils import now_ts, trace_msg

class MemoryAgent:
    def __init__(self):
        self.vector_store = VectorStore()   # semantic memory
        self.kv = {}                        # knowledge base (id → text/meta)
        self.conversation = []              # chat history
        self.agent_state = {}               # record what each agent did
        self.trace = []                     # timeline of actions

    def add_conversation(self, user_input, coordinator_response):
        # Saves user query + manager response in history
        rec = {"timestamp": now_ts(), "user": user_input, "manager": coordinator_response}
        self.conversation.append(rec)
        self.trace.append(trace_msg("conversation_add", rec))

    def add_knowledge(self, doc_id, text, meta):
        # Adding knowledge to vector store + kv store
        self.vector_store.add(doc_id, text, meta)
        self.kv[doc_id] = {"text": text, "meta": meta, "timestamp": now_ts()}
        self.trace.append(trace_msg("kb_add", {"id": doc_id, "meta": meta}))

    def update_agent_state(self, agent_name, task_id, info):
        # Keeps track of what each agent did
        if agent_name not in self.agent_state:
            self.agent_state[agent_name] = {}
        self.agent_state[agent_name][task_id] = {"info": info, "timestamp": now_ts()}
        self.trace.append(trace_msg("agent_state_update", {"agent": agent_name, "task_id": task_id}))

    def search_by_keyword(self, keyword, top_k=5):
        # Simple keyword search
        return [v for k, v in self.kv.items() if keyword.lower() in v["text"].lower()][:top_k]

    def semantic_search(self, query, top_k=5):
        # Semantic vector search
        return self.vector_store.search(query, top_k)

    def dump_trace(self, path):
        # Saves full trace + conversation history to JSON
        with open(path, "w", encoding="utf-8") as f:
            json.dump({"trace": self.trace, "conversation": self.conversation}, f, indent=2)

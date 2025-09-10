import json
from datetime import datetime

# Getting the current timestamp in ISO format (UTC)
def now_ts():
    return datetime.utcnow().isoformat() + "Z"

# Creating a structured trace message (for debugging/logging system events)
def trace_msg(action, payload):
    return {
        "timestamp": now_ts(),
        "action": action,   # what happened (e.g. "classification", "kb_add")
        "payload": payload  # details of the action
    }

# Saving a list of records (dictionaries) to a JSONL file (one JSON object per line)
def save_jsonl(path, records):
    with open(path, "w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

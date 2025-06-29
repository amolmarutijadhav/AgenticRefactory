import json

def load_config(path="config.json"):
    with open(path) as f:
        return json.load(f)

# Example config.json:
# {
#   "steps": ["detection", "refactor", "validation", "report"],
#   "verbosity": "debug",
#   "llm_provider": "openai"
# }


import json
from pathlib import Path

def load_actors():
    data_path = Path(__file__).resolve().parent.parent / "data" / "actors.json"
    with open(data_path, "r") as f:
        data = json.load(f)
    return data.get("top_priorizados", []) + data.get("pipeline_adicional", [])

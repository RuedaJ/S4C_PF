import json, sys
from pathlib import Path
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "actors.json"
SCHEMA = ROOT / "schemas" / "actor.schema.json"

def validate_actor_list(objs, schema):
    validator = Draft202012Validator(schema)
    errs = []
    for i, obj in enumerate(objs):
        for e in validator.iter_errors(obj):
            errs.append((i, e.message, list(e.path)))
    return errs

def main():
    with open(DATA, "r", encoding="utf-8") as f:
        payload = json.load(f)
    actors = (payload.get("top_priorizados", []) 
              + payload.get("pipeline_adicional", []))
    with open(SCHEMA, "r", encoding="utf-8") as f:
        schema = json.load(f)

    errors = validate_actor_list(actors, schema)

    # additional integrity checks
    extra = []
    for i, a in enumerate(actors):
        mn, mx = a.get("ticket_min_eur", 0), a.get("ticket_max_eur", 0)
        try:
            mxv = float(mx)
        except Exception:
            mxv = 0
        if isinstance(mn, (int, float)) and isinstance(mxv, (int, float)) and mn > mxv:
            extra.append((i, f"ticket_min_eur ({mn}) > ticket_max_eur ({mx})", ["ticket_min_eur","ticket_max_eur"]))

        # evidence date presence already validated via schema; could add recency warnings here if needed

    if errors or extra:
        print("❌ Validation failed.\n")
        if errors:
            print("Schema errors:")
            for idx, msg, path in errors:
                print(f" - [#{idx}] {msg} at {'.'.join(map(str,path))}")
        if extra:
            print("\nIntegrity errors:")
            for idx, msg, path in extra:
                print(f" - [#{idx}] {msg} at {'.'.join(map(str,path))}")
        sys.exit(1)
    else:
        total = len(actors)
        print(f"✅ actors.json is valid. Entries: {total}")
        sys.exit(0)

if __name__ == '__main__':
    main()
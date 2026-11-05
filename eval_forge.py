import argparse
import json
from pathlib import Path
import re

def evaluate(case):
    output = case["output"]
    if not isinstance(output, str):
        raise ValueError("output must be a string")
    checks = {}
    if "expected" in case:
        checks["exact"] = output.strip() == str(case["expected"]).strip()
    for term in case.get("contains", []):
        checks["contains:" + term] = term.casefold() in output.casefold()
    for term in case.get("forbidden", []):
        checks["forbidden:" + term] = term.casefold() not in output.casefold()
    if "pattern" in case:
        checks["pattern"] = re.fullmatch(case["pattern"], output) is not None
    if "json_types" in case:
        try:
            parsed = json.loads(output)
            types = {"string": str, "number": (int, float), "boolean": bool, "array": list, "object": dict, "null": type(None)}
            for key, kind in case["json_types"].items():
                if kind not in types:
                    raise ValueError("Unknown JSON type: " + kind)
                value = parsed.get(key) if isinstance(parsed, dict) else None
                checks["json:" + key] = isinstance(parsed, dict) and key in parsed and isinstance(value, types[kind]) and not (kind == "number" and isinstance(value, bool))
        except json.JSONDecodeError:
            checks["valid_json"] = False
    if not checks:
        raise ValueError("Every case needs at least one check")
    return {"id": case["id"], "passed": all(checks.values()), "checks": checks}

def run(cases):
    ids = [case["id"] for case in cases]
    if len(ids) != len(set(ids)):
        raise ValueError("Duplicate case IDs")
    if not cases:
        raise ValueError("Evaluation dataset is empty")
    results = [evaluate(case) for case in cases]
    passed = sum(result["passed"] for result in results)
    return {"total": len(results), "passed": passed, "pass_rate": passed / len(results), "results": results}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("dataset", type=Path)
    parser.add_argument("--minimum", type=float, default=1.0)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    if not 0 <= args.minimum <= 1:
        parser.error("minimum must be between zero and one")
    cases = [json.loads(line) for line in args.dataset.read_text(encoding="utf-8").splitlines() if line.strip()]
    report = run(cases)
    body = json.dumps(report, indent=2)
    if args.report:
        args.report.write_text(body + "\n", encoding="utf-8")
    print(body)
    raise SystemExit(0 if report["pass_rate"] >= args.minimum else 1)

if __name__ == "__main__":
    main()

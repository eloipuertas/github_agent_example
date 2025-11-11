from __future__ import annotations
import argparse, json
from dotenv import load_dotenv
from .agent import run_once

def parse_args():
    ap = argparse.ArgumentParser(description="Agent LangChain + OpenAI Functions (sense memòria, amb guardrails)")
    ap.add_argument("--objective", required=True, help="Objectiu de l'agent")
    ap.add_argument("--repo", required=True, help="Repositori target (owner/repo)")
    ap.add_argument("--confirm-pr", action="store_true", help="Permetre acció sensible: create_pull_request")
    return ap.parse_args()

def main():
    load_dotenv()
    args = parse_args()
    out = run_once(objective=args.objective, repo=args.repo, confirm_pr=args.confirm_pr)
    print(json.dumps(out, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()

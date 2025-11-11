from __future__ import annotations
from typing import Any
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.tools import tool
from .config import settings
from .guardrails import check_tool_allowed
from . import tools as t

class SearchIssuesArgs(t.SearchIssuesArgs): pass
class GetFileArgs(t.GetFileArgs): pass
class CreatePRArgs(t.CreatePRArgs): pass

@tool("search_issues", args_schema=SearchIssuesArgs)
def search_issues_tool(repo: str, query: str) -> Any:
    "Search issues in a GitHub repository"
    return t.search_issues(repo=repo, query=query)

@tool("get_file", args_schema=GetFileArgs)
def get_file_tool(repo: str, path: str) -> Any:
    "Get a file from a GitHub repository"
    return t.get_file(repo=repo, path=path)

@tool("create_pull_request", args_schema=CreatePRArgs)
def create_pull_request_tool(repo: str, branch: str, title: str, body: str) -> Any:
    "Create a pull request in a GitHub repository"
    return t.create_pull_request(repo=repo, branch=branch, title=title, body=body)

TOOLS = [search_issues_tool, get_file_tool, create_pull_request_tool]

SYSTEM_PROMPT = (
    "Ets un agent d'enginyeria de software. "
    "Objectiu: triatge d'issues i PRs petits i segurs. "
    "Polítiques: "
    "- Usa només funcions permeses. "
    "- No creïs PRs sense confirmació explícita. "
    "- Explica breument el teu pla abans d'actuar."
)

def build_model():
    llm = ChatOpenAI(model=settings.openai_model, temperature=0)
    return llm.bind_tools(TOOLS)

def run_once(objective: str, repo: str, confirm_pr: bool = False):
    llm = build_model()
    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=f"OBJECTIU: {objective}\nREPO: {repo}")
    ]
    result = llm.invoke(messages)

    if not hasattr(result, "tool_calls") or not result.tool_calls:
        return {"type": "text", "output": result.content}

    tc = result.tool_calls[0]
    tool_name = tc["name"]
    args = tc["args"] or {}

    decision = check_tool_allowed(tool_name, settings.allowed_tools)
    if not decision.allowed:
        return {"type": "error", "reason": decision.reason}
    if decision.require_confirmation and not confirm_pr:
        return {"type": "blocked", "reason": "Acció sensible bloquejada: falta confirmació (--confirm-pr)"}

    tool_map = {t.name: t for t in TOOLS}
    tool_fn = tool_map[tool_name]
    data = tool_fn.invoke(args)

    return {
        "type": "tool_result",
        "tool": tool_name,
        "args": args,
        "result": data,
        "note": "Executat amb guardrails (no memòria)"
    }

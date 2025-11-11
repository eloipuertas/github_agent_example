from __future__ import annotations
import subprocess, json, base64
from typing import List, Dict
from pydantic import BaseModel, Field

class SearchIssuesArgs(BaseModel):
    repo: str = Field(..., description="owner/repo")
    query: str = Field(..., description="issue query")

class GetFileArgs(BaseModel):
    repo: str
    path: str

class CreatePRArgs(BaseModel):
    repo: str
    branch: str
    title: str
    body: str

def run_gh_command(cmd: list[str]) -> str:
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return f"Error: {e.stderr.strip()}"

def search_issues(repo: str, query: str) -> List[Dict]:
    cmd = ["gh", "issue", "list", "--repo", repo, "--search", query, "--json", "number,title,url"]
    out = run_gh_command(cmd)
    try:
        return json.loads(out)
    except json.JSONDecodeError:
        return [{"error": out}]

def get_file(repo: str, path: str) -> Dict:
    cmd = ["gh", "api", f"repos/{repo}/contents/{path}"]
    out = run_gh_command(cmd)
    try:
        data = json.loads(out)
        if "content" in data:
            try:
                data["decoded"] = base64.b64decode(data["content"]).decode("utf-8", errors="ignore")
            except Exception:
                data["decoded"] = None
        return data
    except json.JSONDecodeError:
        return {"error": out}

def create_pull_request(repo: str, branch: str, title: str, body: str) -> Dict:
    cmd = ["gh", "pr", "create", "--repo", repo, "--title", title, "--body", body, "--head", branch, "--base", "main"]
    out = run_gh_command(cmd)
    return {"pr_url": out or "No PR created"}

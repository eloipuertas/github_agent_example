from __future__ import annotations
from dataclasses import dataclass
from typing import Iterable

SENSITIVE_ACTIONS = {"create_pull_request"}

@dataclass
class GuardDecision:
    allowed: bool
    reason: str = ""
    require_confirmation: bool = False

def check_tool_allowed(tool_name: str, allowed_tools: Iterable[str]) -> GuardDecision:
    if tool_name not in set(allowed_tools):
        return GuardDecision(False, reason=f"Eina no permesa: {tool_name}")
    if tool_name in SENSITIVE_ACTIONS:
        return GuardDecision(True, require_confirmation=True, reason="Acció sensible: requereix confirmació explícita")
    return GuardDecision(True)

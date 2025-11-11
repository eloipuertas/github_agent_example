from __future__ import annotations
import os
from dataclasses import dataclass

@dataclass
class Settings:
    openai_api_key: str = os.environ.get("OPENAI_API_KEY", "")
    openai_model: str = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")
    allowed_tools: list[str] = tuple(t.strip() for t in os.environ.get("ALLOWED_TOOLS","search_issues,get_file,create_pull_request").split(","))

settings = Settings()
if not settings.openai_api_key:
    raise RuntimeError("Falta OPENAI_API_KEY. Defineix-la a l'entorn o .env")

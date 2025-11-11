# Agents (LangChain + OpenAI Functions) — GuardRails + GitHub CLI

Agent d'enginyeria de software amb **LangChain** i **OpenAI Function Calling**, sense memòria, amb **GuardRails**
i eines reals via **GitHub CLI (`gh`)**.

**Codi generat amb IA**, només per a finalitats educatives i de demostració. No s'ha de utilitzar en producció sense una revisió exhaustiva.

# 🤖 Arquitectura de l’Agent LangChain + OpenAI Functions

**Objectiu:** agent que analitza issues, obté fitxers i crea PRs segures (amb confirmació).

```
Usuari / CLI  →  LangChain Agent
                     │
                     ▼
              OpenAI Function Calling
                     │
       ┌─────────────┴───────────────┐
       │ search_issues(repo, query)  │
       │ get_file(repo, path)        │
       │ create_pull_request(...)    │
       └─────────────┬───────────────┘
                     │
               GuardRails Layer
       (whitelist + confirmació prèvia)
```



---

# ⚙️ Solució i Implementació

**Stack:** LangChain · OpenAI Functions · Pydantic · GitHub CLI (`gh`) · GuardRails

**Flux:**
1) Usuari defineix objectiu i repo  
2) Agent decideix tool → *function calling*  
3) GuardRails valida (whitelist/confirmació)  
4) Execució real amb `gh` (subprocess)  
5) Retorn JSON amb resultat i traçabilitat

**Execució:**
```bash
python -m src.run   --objective "Trobar issues 'refactor' i fer PR"   --repo "org/project" --confirm-pr
```

---

# 🧠 Automatització amb GitHub Actions

**Action:** `.github/workflows/agent-from-commit.yml`  
Executa l’agent automàticament a cada *push* o via `workflow_dispatch`.

**Característiques principals:**
- 💬 Usa el **missatge del commit com a prompt**
- 🔒 Si conté `#confirm-pr` o `CONFIRM_PR` → permet crear PR
- 🤖 Executa l’agent amb els permisos necessaris (`contents: write`, `pull-requests: write`)
- 💾 Desa el resultat en un artifact JSON

**Flux:**  
```
commit → trigger action → llegeix missatge → executa agent
       → valida guardrails → retorna resultat
```



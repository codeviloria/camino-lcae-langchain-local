# Curso 02 · Deep Agents en local (camino LCAE)

> **EN:** Fork of LangChain Academy's *Deep Agents* course, adapted to run **locally on CPU with Ollama** (no paid LLM APIs). Python is the main track. Selected labs are also run in **TypeScript** to compare both SDKs. Every lesson is documented: what broke, why, and how it was fixed.

Fork del curso oficial [Deep Agents](https://academy.langchain.com/courses/foundation-introduction-to-deepagents) de LangChain Academy, adaptado para correr con **modelos locales en Ollama, sin GPU y sin APIs de pago**.

- **Repo principal del camino LCAE:** [README](../README.md) (curso 01 completo + progreso general).
- **Qué hay en esta carpeta:** solo los archivos que adapté (`python/`, `typescript/`) y las notas (`docs/`). El curso completo es de LangChain: [langchain-ai/lca-deepagents](https://github.com/langchain-ai/lca-deepagents).
- **Autor:** Gino. Ingeniero de telecomunicaciones (RAN/RF) en transición a ingeniería de IA y agentes.

---

## 🎯 Objetivo
- Dominar **Deep Agents**: planificación, filesystem, sandboxes, skills, memoria y subagentes, para el examen **LCAE**.
- Usar **Python** como camino principal y **TypeScript** como contraste en los labs clave ⭐.
- Documentar cada problema con el formato *problema → causa → solución → regla*.

## 📈 Progreso: 2/25 lecciones

Leyenda: 🐍 Python · 🟦 TypeScript (solo en los labs ⭐) · ✅ hecho · ⬜ pendiente

**Módulo 0 · Setup**

- [x] **M0.1** Setup (Ollama local) — 🐍 ✅ · [nota](docs/M0.1-setup-local.md)

**Módulo 1 · Fundamentos del deep agent**

- [ ] **M1.1** Overview — 🐍 ⬜
- [x] **M1.2** ⭐ Running a deep agent — 🐍 ✅ · 🟦 TS ✅ · [nota](docs/M1.2-running-a-deep-agent.md)
- [ ] **M1.3** Models — 🐍 ⬜
- [ ] **M1.4** System prompt — 🐍 ⬜
- [ ] **M1.5** ⭐ Tools — 🐍 ⬜ · 🟦 TS ⬜
- [ ] **M1.6** MCP — 🐍 ⬜
- [ ] **M1.7** ⭐ Messages, threads y checkpointers — 🐍 ⬜ · 🟦 TS ⬜
- [ ] **M1.8** ⭐ Human-in-the-loop — 🐍 ⬜ · 🟦 TS ⬜
- [ ] **M1.9** Práctica — 🐍 ⬜

**Módulo 2 · Entorno: filesystem, sandboxes, interpreter**

- [ ] **M2.1** El entorno del deep agent — 🐍 ⬜
- [ ] **M2.2** Filesystem backends — 🐍 ⬜
- [ ] **M2.3** Sandboxes y LocalShell — 🐍 ⬜
- [ ] **M2.4** Interpreter — 🐍 ⬜

**Módulo 3 · Contexto: summarization, skills, memoria**

- [ ] **M3.1** Summarization y context offloading — 🐍 ⬜
- [ ] **M3.2** Skills — 🐍 ⬜
- [ ] **M3.3** Memory — 🐍 ⬜

**Módulo 4 · Subagentes**

- [ ] **M4.1** ⭐ Delegation — 🐍 ⬜ · 🟦 TS ⬜
- [ ] **M4.2** Equipo de subagentes — 🐍 ⬜
- [ ] **M4.3** Subagentes dinámicos — 🐍 ⬜

**Módulo 5 · Proyecto y despliegue**

- [ ] **M5.1** Putting it all together — 🐍 ⬜
- [ ] **M5.2** Despliegue local — 🐍 ⬜
- [ ] **M5.3** ⭐ Sales assistant (capstone) — 🐍 ⬜ · 🟦 TS ⬜
- [ ] **M5.4** Subagentes asíncronos — 🐍 ⬜
- [ ] **M5.5** Agente asíncrono con sandbox — 🐍 ⬜

## 🔧 Qué cambia respecto al curso original
| Original | En este fork |
|---|---|
| `init_chat_model("anthropic:claude-haiku-4-5")` | `get_model("gemma4:latest")` vía [`python/local_model.py`](python/local_model.py) |
| `init_chat_model("anthropic:claude-sonnet-4-6")` | `get_model("qwen3:8b", num_ctx=32768)` |
| `ANTHROPIC_API_KEY` | No se necesita |

Las líneas originales quedan comentadas: **🔸 ORIGINAL DEL CURSO** (con el motivo) → **🟢 ADAPTADO LOCAL** (lo que corre).

## 📚 Documentación
- `docs/M*.md`: una nota por lección, con resultado, problemas, 🎯 notas de examen y 🧠 mnemotecnias.
- [`docs/python-vs-typescript.md`](docs/python-vs-typescript.md): cómo se escribe lo mismo en los dos SDKs.
- [`docs/banco-preguntas-examen.md`](docs/banco-preguntas-examen.md): preguntas tipo examen acumuladas.
- [`docs/plantilla-leccion.md`](docs/plantilla-leccion.md): formato de cada nota.

## 💼 Logros (se actualiza al cerrar cada módulo)
- Adaptación del curso a Ollama local en CPU con un solo punto de cambio, en Python (`models.py` → `local_model.py`) y TypeScript (`models.ts` → `local_model.ts`).
- Primer deep agent en ambos SDKs con medición de latencia en CPU: ~100 s con el modelo cargado; el arranque en frío suma ~35 s.

## 🚀 Cómo correrlo (Python)
Clona el curso oficial y copia encima los archivos de esta carpeta (`python/` y `typescript/`):
```bash
git clone https://github.com/langchain-ai/lca-deepagents.git
cp -r curso-02-deep-agents/python curso-02-deep-agents/typescript lca-deepagents/
cd lca-deepagents/python
cp .env.example .env
uv sync
uv run python -c "from models import model; print(model.invoke('hola').content)"
```

En el `.env`, `OLLAMA_BASE_URL=http://<ip-del-servidor>:11434`.

## 🔒 Privacidad
El `.env`, `_privado/` y las skills de terceros (`.agents/`, `.claude/`) no se versionan.

## 📜 Créditos
Material original © LangChain, Inc. ([langchain-ai/lca-deepagents](https://github.com/langchain-ai/lca-deepagents)). Las adaptaciones y notas son mías.

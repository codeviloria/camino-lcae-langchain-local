# Deep Agents en local: curso 02 del camino a la certificación LCAE

> **EN:** Fork of LangChain Academy's *Deep Agents* course, adapted to run **locally on CPU with Ollama** (no paid LLM APIs). Python is the main track. Selected labs are also run in **TypeScript** to compare both SDKs. Every lesson is documented: what broke, why, and how it was fixed.

Fork del curso oficial [Deep Agents](https://academy.langchain.com/courses/foundation-introduction-to-deepagents) de LangChain Academy, adaptado para correr con **modelos locales en Ollama, sin GPU y sin APIs de pago**.

- **Curso anterior:** [camino-lcae-langchain-local](https://github.com/codeviloria/camino-lcae-langchain-local), *Introduction to LangChain* completo.
- **Autor:** Gino. Ingeniero de telecomunicaciones (RAN/RF) en transición a ingeniería de IA y agentes.

---

## 🎯 Objetivo
- Dominar **Deep Agents**: planificación, filesystem, sandboxes, skills, memoria y subagentes, para el examen **LCAE**.
- Usar **Python** como camino principal y **TypeScript** como contraste en los labs clave ⭐.
- Documentar cada problema con el formato *problema → causa → solución → regla*.

## 📈 Progreso: 10/25 lecciones

Leyenda: 🐍 Python · 🟦 TypeScript (solo en los labs ⭐) · ✅ hecho · ⬜ pendiente

**Módulo 0 · Setup**

- [x] **M0.1** Setup (Ollama local) — 🐍 ✅ · [nota](docs/M0.1-setup-local.md)

**Módulo 1 · Fundamentos del deep agent**

- [x] **M1.1** Overview — 🐍 ✅ · [nota](docs/M1.1-overview.md)
- [x] **M1.2** ⭐ Running a deep agent — 🐍 ✅ · 🟦 TS ✅ · [nota](docs/M1.2-running-a-deep-agent.md)
- [x] **M1.3** Models — 🐍 ✅ · [nota](docs/M1.3-models.md)
- [x] **M1.4** System prompt — 🐍 ✅ · [nota](docs/M1.4-system-prompt.md)
- [x] **M1.5** ⭐ Tools — 🐍 ✅ · 🟦 TS ⬜ · [nota](docs/M1.5-tools.md)
- [x] **M1.6** MCP — 🐍 ✅ · [nota](docs/M1.6-mcp.md)
- [x] **M1.7** ⭐ Messages, threads y checkpointers — 🐍 ✅ · 🟦 TS ⬜ · [nota](docs/M1.7-messages-threads-checkpointers.md)
- [x] **M1.8** ⭐ Human-in-the-loop — 🐍 ✅ · 🟦 TS ⬜ · [nota](docs/M1.8-hitl.md)
- [x] **M1.9** Práctica — 🐍 ✅ · [nota](docs/M1.9-practica.md)
- 📝 **Resumen M1** para el examen: [docs/M1-resumen.md](docs/M1-resumen.md) · 📓 [notebook de práctica](python/notebooks/m1-practica.ipynb)

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
| `init_chat_model("anthropic:claude-haiku-4-5")` | `init_chat_model("ollama:gemma4:latest", base_url=…, num_ctx=16384, reasoning=False)` |
| `init_chat_model("anthropic:claude-sonnet-4-6")` | `init_chat_model("ollama:qwen3:8b", base_url=…, num_ctx=32768, reasoning=False)` |
| Cambiar de proveedor = editar `models.py` | Interruptor `MODEL_PROVIDER=ollama\|openrouter` en el `.env` (Python y TS) |
| `ANTHROPIC_API_KEY` | No se necesita (Ollama local u OpenRouter `:free`) |

Por qué esos parámetros: ver [M1.2 → "Por qué los parámetros de Ollama"](docs/M1.2-running-a-deep-agent.md).

Las líneas originales quedan comentadas: **🔸 ORIGINAL DEL CURSO** (con el motivo) → **🟢 ADAPTADO LOCAL** (lo que corre).

## 📚 Documentación
- `docs/M*.md`: una nota por lección, con resultado, problemas, 🎯 notas de examen y 🧠 mnemotecnias.
- [`docs/python-vs-typescript.md`](docs/python-vs-typescript.md): cómo se escribe lo mismo en los dos SDKs.
- [`docs/banco-preguntas-examen.md`](docs/banco-preguntas-examen.md): preguntas tipo examen acumuladas.
- [`docs/plantilla-leccion.md`](docs/plantilla-leccion.md): formato de cada nota.

## 💼 Logros (se actualiza al cerrar cada módulo)
- Adaptación del curso a modelos sin costo con un solo punto de cambio (`models.py` / `models.ts`) y un interruptor de proveedor en el `.env`: Ollama local (CPU) ↔ OpenRouter (nube).
- Primer deep agent en ambos SDKs con latencias medidas: ~100 s en CPU local (el arranque en frío suma ~35 s) vs 14–23 s en la nube.

## 🚀 Cómo correrlo (Python)
```bash
cd python
cp .env.example .env
uv sync
uv run python -c "from models import model; print(model.invoke('hola').content)"
```

En el `.env`: `OLLAMA_BASE_URL=http://<ip-del-servidor>:11434` y, para usar la nube, `MODEL_PROVIDER=openrouter` + `OPENROUTER_API_KEY`.

## 🔒 Privacidad
El `.env`, `_privado/` y las skills de terceros (`.agents/`, `.claude/`) no se versionan.

## 📜 Créditos
Material original © LangChain, Inc. ([langchain-ai/lca-deepagents](https://github.com/langchain-ai/lca-deepagents)). Las adaptaciones y notas son mías.

# Bitácora del proceso

Registro cronológico. Una entrada por sesión de estudio.

## Formato de entrada
```
### AAAA-MM-DD — Curso / lección
- Tiempo:
- Qué vi:
- Qué entendí (en mis palabras):
- Dudas abiertas:
- Próximo paso:
```

---

### 2026-10-03 — Setup
- Creada la estructura del vault: una carpeta por curso + guía del examen + glosario.
- Objetivo: certificación LCAE (40 preguntas, 28 para aprobar, 4 dominios: Build/Test/Deploy/Monitor).
- Próximo paso: iniciar **01 Introduction to LangChain (Python)**.

### 2026-10-03 — 01 Intro LangChain / M1.1 Foundational Models
- Qué vi: `init_chat_model`, `create_agent`, mensajes, streaming.
- Decisión: correr el curso con **Ollama local** en vez de OpenAI/Anthropic/Gemini.
- `.env`: keys de proveedores no necesarias; **LangSmith API key sí** (tracing/evals, base de Test/Deploy/Monitor).
- Próximo paso: adaptar notebook 1.1 a Ollama y verificar traces en LangSmith.

### 2026-10-03 — Setup entorno (Ollama remoto + LangSmith)
- Modelo: `local_model.py` → `ChatOllama` en `<ollama-host>:11434`, default `qwen3:30b-a3b`, `reasoning=False`, `num_ctx=8192`.
- Notebook 1.1 corre OK con Ollama.
- LangSmith: creada PAT "certification" (1 año, Workspace 1).
- Problema: 403 Forbidden en `/runs/multipart` y `/sessions`.
  - Causa: la key en `.env` tenía `API ` pegado al inicio (len 55 vs 51).
  - Fix: `LANGSMITH_API_KEY=lsv2_pt_...` limpio + reiniciar kernel (`load_dotenv` no sobrescribe sin `override=True`).
- Lección: PAT (usuario) vs Service Key (CI) y `X-Tenant-ID` → tema de auth (dominio Deploy).

### 2026-10-03 — M1.1 completado ✅
- Notebook 1.1 corrido completo con Ollama (`qwen3:8b`, `qwen3:4b`, `gemma3:4b`) y traces en LangSmith (`lca-lc-foundations`).
- Duda resuelta: las 3 formas de `create_agent` son alternativas, basta una; la última ejecutada es la activa.
- Hallazgo: forma string sin `reasoning=False` → tokens de razonamiento ocultos (448 vs ~110 visibles), ~5.7 tok/s.
- Próximo paso: M1.2.

### 2026-10-03 — M1.2 Prompting completado ✅
- Vi: system prompt, few-shot, structured prompts, structured output con Pydantic.
- Few-shot: con modelos locales hay que dar el formato explícito o los ejemplos como mensajes.
- `response_format` con gemma3 falla (no soporta tools) → usar qwen3 o `with_structured_output(method="json_schema")`.
- Próximo paso: M1.3.

### 2026-10-03 — M1.3 Tools completado ✅
- Vi: `@tool`, probar la tool sola (`√467 = 21.61`), agregarla con `create_agent(tools=[tool1])`.
- Problema: el agente nunca terminaba. Ollama no recibía peticiones → kernel bloqueado por un `invoke` colgado anterior.
- Fix: reiniciar kernel y correr todo; diagnóstico por capas (red → Ollama → tools → agente).
- Verificado: `qwen3:8b` y `gemma4` soportan tools; un solo server Ollama.
- Resultado: ciclo model → tool → model en ~25 s con `qwen3:8b` en CPU (~5,7 tok/s).
- Hallazgo: el modelo inventó el cuadrado de 467 (217,489 ≠ 218,089) porque el prompt lo pedía y no había tool.
- Próximo paso: siguiente notebook del módulo.

### 2026-10-03 — M1.4 Web Search completado ✅
- Vi: tool de búsqueda con Tavily (`TavilyClient().search`) dentro de `create_agent`.
- Sin tool, qwen3:8b afirmó que el presidente de Colombia es Uribe (falso). Con Tavily respondió bien, con fuentes.
- Hallazgo: la segunda llamada tardó 79 s porque leyó 1.978 tokens de resultados → recortar la salida de la tool.
- Decisión: hacer también la **Tavily Web Search API Certification** como parte del camino (_Curso).
- Próximo paso: siguiente notebook del módulo.

### 2026-10-03 — Apagón y setup documentado
- Se fue la luz: volver a levantar con `uv run jupyter lab` en la raíz del repo.
- `ModuleNotFoundError: local_model` en el notebook de tools → el script está en la raíz y el notebook en una subcarpeta. Fix: celda con `sys.path.insert`.
- Documentado `local_model.py` (la pieza que permite correr el curso con modelos locales) en [00 Setup lab local](setup-lab-local.md).

### 2026-10-03 — M1.5 Memory completado ✅
- Vi: agente sin memoria vs con `InMemorySaver` + `thread_id`.
- Sin memoria: "What's my favourite colour?" → no sabía. Con memoria: "green", y recordó el nombre (Seán).
- Hallazgo: con memoria el turno 2 leyó 91 tokens vs 22 → el historial se reenvía completo cada vez.
- Próximo paso: siguiente notebook del módulo.

### 2026-10-03 — M1.6 Multimodal completado ✅
- Cambio de modelo: `gemma4:latest` (vision + audio); qwen3 es solo texto.
- Audio: PortAudio faltante → `apt install`; `langchain-ollama` no soporta bloques `audio`.
- Trampa: el micrófono grababa silencio (device `default`) y el modelo alucinó transcripciones. Fix: Jabra `device=5`.
- Funcionó: audio 16 kHz mono + bloque `image` (workaround) + prompt en español → transcripción exacta.
- Imagen: funcionó con el bloque `image` estándar (Neo-Veridia, Aethelgard). El system prompt manda aunque la imagen no sea una ciudad.
- Aprendido: `mime_type` lo ignora Ollama, pero OpenAI/Anthropic/Gemini lo usan y validan.
- Próximo paso: siguiente notebook del módulo.

### 2026-10-04 — M1.7 Personal Chef completado ✅ — Módulo 1 terminado
- Proyecto: system prompt (en español) + `web_search` (Tavily) + `InMemorySaver`, con `gemma4:latest`.
- Funcionó: buscó solo, en español, y propuso "pollo al horno con uvas".
- Hallazgo: dijo "basándome en lo que encontré" pero la receta no estaba en los resultados → exigir fuentes en el prompt.
- Medición: gemma4 ~10,8 tok/s generando vs ~5,7 de qwen3 → más rápido para agentes en este lab. La receta tardó 108 s por su largo (863 tokens).
- Próximo paso: **Módulo 2** (MCP, context y state, multi-agente, Wedding Planner, bonus RAG y SQL). Modelo por defecto para tools: `gemma4:latest`.

### 2026-10-04 — M1.7 en LangGraph Studio
- `uv langgraph dev` → error; correcto: `uv run langgraph dev`.
- Studio "Connection failed": el servidor se caía por `GraphLoadError` (checkpointer `InMemorySaver` en el grafo).
- Limpieza del `.py`: quitar prints/`list_projects`, checkpointer e invokes; `sys.path` con `__file__`. Versión limpia en [M1.7 Personal Chef](module-1/M1.7-personal-chef.md).

### 2026-10-04 — Módulo 2 (MCP, context, state, multi-agente, Wedding Planner)
- M2.1 MCP: servidor propio por `stdio` y servidor de terceros; MCP es async → `await`/`ainvoke`.
- M2.1b Travel Agent (Kiwi): contexto desbordado con 8K; con `num_ctx` 32768 y solo `search-flight` respondió bien.
- M2.2a/b: runtime context y state con `Command(update=...)`; gemma4 a veces deja vacío el último mensaje.
- M2.3: subagents as tools con aislamiento de contexto (√456 ≈ 21,354).
- M2.4 Wedding Planner, 3 corridas. Fecha en el state → vuelos reales desde Bogotá (desde 2.032 EUR) y costo de la playlist $14,85 ✓; duración 0 min ✗ (regresión).
- Próximo paso: bonus RAG y SQL.

### 2026-10-04 — M2.B Bonus RAG ✅
- PDF de 1.943 caracteres → **3 chunks** (1000/200) → embeddings `nomic-embed-text` (768 dim) → `InMemoryVectorStore`.
- El agente reescribió la búsqueda (`'vacation days first year'`) y respondió **10 días** de PTO el primer año ✅. ~10,5 s en CPU.
- El vector store vive en la RAM del kernel: no hay BD vectorial persistente. Para producción: FAISS/Chroma (local) o pgvector/Qdrant.
- Próximo paso: **bonus SQL**.

### 2026-10-04 — M2.B Bonus SQL — Módulo 2 cerrado ✅
- 1er intento: gemma4 inventó `artists.popularity` y preguntó el esquema al usuario. La tool sola sí funciona (`SELECT * FROM Artist`).
- Referencia: Smashing Pumpkins (24 canciones vendidas). 2º intento: exploró el esquema pero respondió **System Of A Down** (incorrecto): usó `Track.ArtistId`, que no existe, y SQLite no dio error → todos empatan en 2240. Sin error ≠ correcto.
- 3er intento: esquema real (`db.get_table_info`) + camino de JOIN en el prompt → **Smashing Pumpkins ✅**. Celda evaluadora contra la referencia: v2 ❌, v3 ✅.
- **Módulo 2 terminado.** Próximo paso: **Módulo 3 (Production-Ready Agent)**.

### 2026-10-05 — Módulo 3 adaptado a local ✅
- 6 notebooks + `3.5_email_agent.py` con la convención 🔸/🟢. Cambios: `gpt-5-nano`/`gpt-4o-mini`/Claude → gemma4 y qwen3:8b (32K) en *dynamic models*; Tavily `max_results=3`; celda EXTRA con rol `internal`.
- Los 7 agentes compilan sin llamar al modelo (validación previa). Falta correrlos.
- Próximo paso: correr 3.2 → 3.5 y el proyecto en Agent Chat UI.

### 2026-10-05 — M3.2 Managing Messages ✅
- Summarization: 9 mensajes → 3 (resumen como `HumanMessage` + última pregunta + respuesta), sin perder hechos. Respuesta larga: 782 tokens en 76 s.
- Trim con `@before_agent`: borró los 2 `ToolMessage`; el agente no supo la temperatura (estaba en uno de ellos) → esperado.
- Agregué al notebook explicaciones antes de cada celda, una sección de índices/slicing de `response["messages"]` y demos del checkpointer (`get_state`, thread nuevo vs. mismo thread).

### 2026-10-05 — M3.3 Human-in-the-Loop ✅
- 1er intento: gemma4 pidió la dirección de correo en vez de llamar `read_email` (docstring engañosa) → sin pausa. Con system prompt explícito: pausa ✅.
- Approve ✅ (Email sent) · Reject ✅ (ToolMessage `status=error`; el modelo no reintentó) · Edit ✅ (se envió mi texto). Las 4 decisiones permitidas incluyen `respond`.
- Agregué al notebook: helper `nueva_pausa(thread_id)` (una pausa por decisión) y `ver(response)` para leer la salida sin `pprint`.

### 2026-10-05 — M3.3 corrida 3 + dataset HITL ✅
- Con la línea 3 del prompt, gemma4 **reintentó** tras el Reject (nueva pausa) pero repitió el mismo borrador → pedir reintento ≠ aplicar la crítica.
- Flujo completo en un thread: reject → reintento → edit → enviado. `decidir()` generó 3 ejemplos JSONL (approve/edit/reject).
- Idea propia documentada: decisiones HITL como datos para SFT/DPO/evaluación.
- Creada la **hoja de repaso del stack y el flow** (módulos 1–3) para repasar antes del examen.

### 2026-10-05 — M3.4 Dynamic models ✅
- `wrap_model_call` + `request.override(model=...)`: 1 mensaje → gemma4; 11 mensajes → qwen3:8b (32K). Confirmado con `response_metadata["model_name"]`.
- En LangSmith la elección no aparece como tool: está en el metadata del run del modelo (`ls_model_name`). Agregué una celda EXTRA con log del motivo y `tags`.

### 2026-10-05 — M3.4 Dynamic prompts ✅
- `@dynamic_prompt` + `runtime.context.user_language`: misma pregunta → irlandés, español y francés correctos (sin tools, 1 llamada).
- Hallazgo: el system prompt dinámico **no se guarda** en `messages`; agregué un middleware "espía" para verlo.
- Agregué mnemotecnias (teatro: actor/guion/utilería, L-O-H, Carnet vs Se mueve, A-E-R-R) a M3.4 y a la hoja de repaso.

### 2026-10-05 — M3.4 Dynamic tools ✅ + 🚨 hallazgo de seguridad
- `internal` vio `sql_query`; 1er intento falló por `artists` (es `Artist`). Con las tablas en el prompt → 275 ✅.
- 🚨 `external` **también ejecutó** `sql_query`: `override(tools=...)` solo oculta; la tool sigue registrada y se ejecuta si el modelo la nombra (el nombre salió de mi prompt). Reproducido con modelo simulado.
- Corrección: guardia `@wrap_tool_call` que valida permisos por rol antes de ejecutar ("Acceso denegado"). Módulo 3.4 completo.
- Corrida final 3.4 tools: guardia `@wrap_tool_call` verificado con gemma4. `external` → *Acceso denegado* (incluso cuando gemma4 inventó `database_query` y cuando el usuario pidió `sql_query` por nombre); `internal` → 275 ✅.

### 2026-10-05 — M3.5 Email Agent (notebook) ✅
- Al primer intento: authenticate → (cambian tools y prompt) → check_inbox → resumen → send_email → ⏸️ HITL → approve → enviado. `authenticated: True` en el state.
- Pendiente: servirlo con `uv run langgraph dev` y probar en Studio / Agent Chat UI.

### 2026-10-05 — M3.5 en LangGraph Studio ✅ — 🏁 Curso 01 completado
- `uv run langgraph dev` → Studio conectado; grafo `model ↔ HumanInTheLoopMiddleware.after_model → tools/__end__`. Los `wrap_model_call` (dynamic tools/prompt) corren dentro de `model`.
- **Curso 01 Introduction to LangChain terminado**: módulos 1–3 + bonus, todo con Ollama en CPU, documentado con 🔸/🟢.
- Próximo: repasar con la hoja de repaso; luego curso 02 (Deep Agents).

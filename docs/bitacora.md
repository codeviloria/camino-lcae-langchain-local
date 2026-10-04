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

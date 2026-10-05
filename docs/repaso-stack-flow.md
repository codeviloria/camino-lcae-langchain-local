# 🔁 Repaso: stack y flow de agentes con LangChain (módulos 1–3)

Hoja para repasar varias veces. Primero lee el **mapa** y el **flow**; después pruébate con las preguntas del final sin mirar las respuestas.

## 1. El stack en capas (de abajo hacia arriba)
| Capa | Qué es | En mi lab |
|---|---|---|
| **Modelo** | El LLM que piensa y decide qué tool pedir | Ollama: `gemma4` (tools), `qwen3:8b`; embeddings `nomic-embed-text` |
| **LangChain** | `create_agent`, `@tool`, mensajes, integraciones (`langchain-ollama`, `langchain-tavily`) | `local_model.py` → `get_model()` |
| **LangGraph** (debajo de `create_agent`) | El **grafo** que ejecuta el bucle: state, checkpointer, `interrupt()`, `Command` | `InMemorySaver`, `thread_id` |
| **Tools** | Lo que el agente puede **hacer**: Python, APIs web, SQL, RAG, MCP, subagentes | Tavily, Chinook, handbook PDF, Kiwi MCP |
| **Middleware** | Reglas alrededor del bucle: historial, HITL, modelo/prompt/tools dinámicos | Módulo 3 |
| **Observabilidad** | Ver qué pasó en cada paso | LangSmith (tags, trajectory, tokens, SQL del modelo) |
| **Servir / UI** | Exponer el agente | `langgraph dev` + `langgraph.json`, Studio, Agent Chat UI |

## 2. El flow de un `invoke`
```
agent.invoke({"messages": [...], <campos extra del state>}, config={"configurable": {"thread_id": "1"}}, context=...)
   │
   ├─ [before_agent] (1 vez)
   ▼
 ┌─► [before_model] ─► wrap_model_call( MODELO ) ─► [after_model] ──┐
 │                                                                  │
 │      ¿el AIMessage trae tool_calls? ── no ─► respuesta final ─► [after_agent] ─► return state
 │                │ sí
 │      (HITL aquí: after_model → interrupt() → return con __interrupt__ → Command(resume=...))
 │                ▼
 └──── wrap_tool_call( TOOL ) → ToolMessage (o Command(update=...) que cambia el state)
```
- Cada vuelta = **1 llamada al modelo**. 1 tool = 2 llamadas mínimo (pedirla + responder).
- El **checkpointer** guarda una foto del state después de cada paso, por `thread_id`.

## 3. Dónde vive cada dato (la confusión más común)
| | Messages | State (campos extra) | Runtime context | Checkpointer |
|---|---|---|---|---|
| Qué es | La conversación | Datos que **cambian** (`authenticated`, `email`, `destination`) | Datos **fijos** del invoke (rol, idioma, credenciales) | La libreta que guarda el state por `thread_id` |
| Se define con | — | `state_schema=MiState(AgentState)` | `context_schema=MiContexto` (dataclass) | `checkpointer=InMemorySaver()` |
| Se pasa en | `{"messages": [...]}` | `{"messages": [...], "email": "..."}` | `invoke(..., context=...)` | `config={"configurable": {"thread_id": ...}}` |
| La tool lo lee con | — | `runtime.state["campo"]` | `runtime.context.campo` | — |
| La tool lo escribe con | `ToolMessage` | `Command(update={...})` | ❌ no se escribe | automático |
| El middleware lo lee con | `request.messages` | `request.state` | `request.runtime.context` | — |
| Lección | M1.5 | M2.2b | M2.2a | M1.5, M3.2 |

## 4. Tools: cómo entra y sale la información
- **Lo que ve el modelo:** nombre + **docstring** + argumentos. Si la docstring menciona un dato que la tool no recibe, el modelo lo pide (M3.3).
- **Argumentos** = los decide el modelo. **`runtime`** (`ToolRuntime`) = lo pone el sistema: state, context, `tool_call_id`.
- **Salida:** un `str` → `ToolMessage`. O un `Command(update={...})` que cambia el state (y debe incluir el `ToolMessage` con el mismo `tool_call_id`).
- **Errores como texto** (`try/except` que devuelve `"Error: ..."`): el modelo puede corregirse (bonus SQL).
- Tipos que usé: Python, API web (Tavily), MCP local `stdio` y remoto `streamable_http` (async → `ainvoke`), SQL, RAG, **subagentes como tools**.

## 5. Middleware (módulo 3)
| Hook | Corre | Uso |
|---|---|---|
| `before_agent` | 1 vez por invoke | Limpiar el state (`RemoveMessage`) |
| `before_model` | Antes de cada llamada al modelo | `SummarizationMiddleware` (resumen como `HumanMessage`) |
| `wrap_model_call` | Envuelve cada llamada | `request.override(model=…/tools=…)`; `@dynamic_prompt` está construido sobre esto |
| `after_model` | Después de cada respuesta | `HumanInTheLoopMiddleware` → `interrupt()` |
| `wrap_tool_call` | Envuelve cada tool | Reintentos, errores (como el interceptor MCP) |

HITL: decisiones `approve`, `edit`, `reject`, `respond`; **requiere checkpointer**; se reanuda con `Command(resume={"decisions": [...]})` en el **mismo `thread_id`**; cada decisión **consume** la pausa.

## 6. Multi-agente y RAG en una línea
- **Subagents as tools:** el coordinador solo ve la docstring y el `return` del subagente (aislamiento de contexto). Los datos obligatorios deben llegar por el **state** (Wedding Planner).
- **RAG:** loader → splitter (caracteres) → embeddings → vector store (`InMemory` = RAM) → tool de búsqueda.

## 7. Leer la salida sin perderse
- `response` es un dict: `messages`, campos del state y `__interrupt__` (solo si hay pausa).
- `response["messages"][-1]` = último mensaje (la respuesta). `[0]` = primero. `[1:]`, `[-3:]` = pedazos.
- `AIMessage(content='', tool_calls=[...])` = el modelo **pidió una tool**, no habló.
- Mirar solo `content` y `tool_calls`; el resto es metadata. Herramientas: `m.pretty_print()` o `ver(response)`.

## 8. Checklist de depuración (lo que me pasó de verdad)
1. ¿El modelo **pidió** la tool? Si no: docstring, system prompt explícito (M3.3).
2. ¿Llegaron los datos obligatorios? (fecha en el Wedding Planner → state).
3. ¿Se desbordó el contexto? Subir `num_ctx`, filtrar tools, recortar salidas (M2.1b).
4. ¿La respuesta final está vacía? gemma4 a veces cierra con `content=''` (M2.2b, M3.3).
5. ¿El dato es correcto? **Comparar contra una referencia** (SQL: success ≠ correcto; M2.4, M2.B).
6. Revisar el **trace** en LangSmith: el input real de cada tool (el SQL que escribió el modelo).
7. En Jupyter: ¿corrí la celda correcta? El número `[n]` es el orden de ejecución.

## 9. Trampas probables del examen
- `chunk_size` en caracteres; `InMemoryVectorStore` no persiste; `similarity_search` devuelve `Document`s.
- Sin checkpointer no hay memoria ni HITL; el `thread_id` separa conversaciones.
- En `langgraph dev` **no** se pone checkpointer (lo maneja el servidor).
- Tools MCP son async → `ainvoke`/`await`.
- `request.override(...)` devuelve un request **nuevo**.
- 🚨 **Ocultar una tool no es bloquearla:** `override(tools=...)` solo cambia lo que ve el modelo; si la nombra, se ejecuta. Control de acceso real con `@wrap_tool_call`.
- `langchain-community` es legado; integraciones en `langchain-<proveedor>`.
- Status *success* no significa resultado correcto.
- El modelo que eligió un middleware de ruteo no aparece como tool: se ve en `response_metadata["model_name"]` o en el metadata del trace (`ls_model_name`).

## 🧠 Mnemotecnias (módulos 1–3)
| Concepto | Mnemotecnia |
|---|---|
| Checkpointer / `thread_id` | **Libreta y página**: la libreta guarda la conversación; cada `thread_id` es una página |
| Context vs State | **C**ontext = **C**arnet (no cambia). **S**tate = **S**e mueve |
| `wrap_model_call` | **Teatro:** cambia **actor** (modelo), **guion** (prompt) o **utilería** (tools) antes de cada escena |
| Patrón del middleware | **L-O-H:** Leer → Override → Handler |
| Orden de hooks | **"Entra, piensa, revisa, sale":** `before_agent` (entra) → `before_model`/`wrap_model_call` (piensa) → `after_model` (revisa: aquí pausa HITL) → `after_agent` (sale) |
| Decisiones HITL | **"A-E-R-R":** **A**pprove, **E**dit, **R**eject, **R**espond |
| HITL necesita | **"Libreta + misma página":** checkpointer + mismo `thread_id` |
| Leer mensajes | **Fila de niños:** `[0]` el primero, `[-1]` el último (la respuesta) |
| Mensajes que importan | Solo **`content`** y **`tool_calls`**; lo demás es metadata |
| Seguridad de tools | **"Esconder la llave no es cerrar la puerta":** ocultar (`wrap_model_call`) ≠ bloquear (`wrap_tool_call`) |
| Text-to-SQL / RAG | **"Sin error ≠ correcto":** comparar contra una referencia |

## ✍️ Autoevaluación (responde antes de abrir)
<details><summary>¿Qué diferencia hay entre state y runtime context?</summary>

El state cambia durante el invoke (las tools lo escriben con `Command(update=...)`); el context es fijo, lo pone quien llama y el modelo no lo cambia.
</details>

<details><summary>¿Para qué sirve el `thread_id`?</summary>

Identifica una conversación dentro del checkpointer: mismo id = continúa; otro = empieza de cero. HITL reanuda con el mismo id.
</details>

<details><summary>¿En qué hook vive `SummarizationMiddleware` y qué inserta?</summary>

`before_model`; borra el historial y pone un `HumanMessage` con el resumen + los `keep` mensajes recientes.
</details>

<details><summary>¿Por qué HITL necesita checkpointer?</summary>

Para congelar el grafo en la pausa y reanudarlo después con `Command(resume=...)`.
</details>

<details><summary>Nombra las 4 decisiones de HITL.</summary>

`approve`, `edit`, `reject`, `respond`.
</details>

<details><summary>¿Qué devuelve `invoke` cuando hay una pausa?</summary>

El state con la llave `__interrupt__` (lista de `Interrupt` con `action_requests` y `review_configs`).
</details>

<details><summary>¿Cómo cambias el modelo o las tools en cada llamada?</summary>

Con `@wrap_model_call` y `request.override(model=...)` o `request.override(tools=[...])`.
</details>

<details><summary>¿Qué ve el coordinador de un subagente-tool?</summary>

Solo la docstring (para decidir) y el `return` (como `ToolMessage`).
</details>

<details><summary>¿Por qué el agente SQL respondió *System Of A Down* sin error?</summary>

Su JOIN usó una columna inexistente que SQLite resolvió en silencio (todos empataron). Solución: esquema en el prompt + evaluación contra referencia.
</details>

<details><summary>¿Qué pasa si una tool que escribe el state no devuelve `ToolMessage`?</summary>

El modelo queda sin el resultado de su `tool_call`; hay que incluir el `ToolMessage` con el mismo `tool_call_id` en el `Command(update=...)`.
</details>

<details><summary>¿Cómo llamas tools MCP?</summary>

Son async: `await agent.ainvoke(...)`; `MultiServerMCPClient` con transporte `stdio` (local) o `streamable_http` (remoto).
</details>

<details><summary>¿Qué datos deja cada decisión HITL para entrenar?</summary>

approve = ejemplo bueno (SFT); edit = corrección; reject + motivo = preferencia (DPO) y caso de evaluación.
</details>

## 10. Plan de repaso (espaciado)
| Cuándo | Qué hacer |
|---|---|
| Hoy | Leer secciones 1–3 y responder las preguntas |
| +3 días | Rehacer de memoria el diagrama del flow (sección 2) y la tabla de la sección 3 |
| +7 días | Correr de nuevo `3.5_email_agent` explicando cada celda en voz alta |
| Antes del examen | Sección 9 + preguntas, y revisar las notas 🎯 de cada lección |

## Enlaces
- [Guía del examen](examen-lcae.md) · [Lecciones aprendidas](lecciones-aprendidas.md) · [M3.3 HITL](module-3/M3.3-hitl.md) · [M2.4 Wedding Planner](module-2/M2.4-wedding-planner.md)

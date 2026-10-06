# Banco de preguntas tipo examen: Deep Agents

Se agregan al cerrar cada lección: las del quiz del tutor que fallé, más las que salgan de los problemas del lab. Formato: pregunta → opciones → respuesta → por qué.

## M0 · Setup
**1.** En el curso, ¿qué hay que cambiar para que todos los labs usen otro proveedor de modelo?
- a) Cada lab
- b) Solo `models.py`
- c) El `langgraph.json`
- d) El `.env` únicamente

<details><summary>Respuesta</summary>

**b.** Los labs importan `model` desde `models.py`. Puede hacer falta agregar al `.env` la key del nuevo proveedor, pero el código se cambia en un solo lugar.
</details>

## M1.2 · Running a deep agent
**2.** ¿Cuál de estas herramientas **no** viene incluida por defecto en `create_deep_agent`?
- a) `write_todos`
- b) `read_file`
- c) `task`
- d) `web_search`

<details><summary>Respuesta</summary>

**d.** El kit trae filesystem (`ls`, `read_file`, `write_file`, `edit_file`, `delete`, `glob`, `grep`, `execute`) y subagentes (`task`). La búsqueda web hay que pasarla como tool propia. Ojo: desde deepagents 0.7, `write_todos` tampoco viene por defecto (es opt-in).
</details>

**3.** Un deep agent responde "What is an LLM?" sin llamar ninguna tool. ¿Qué significa?
- a) El kit no se cargó
- b) El modelo no soporta tool calling
- c) Es normal: el modelo decide que no necesita tools para una pregunta simple
- d) Falta el checkpointer

<details><summary>Respuesta</summary>

**c.** Tener herramientas no obliga a usarlas. Si el modelo no soportara tool calling, normalmente fallaría al enlazar las tools.
</details>

**4.** Por defecto, ¿dónde guarda los archivos el filesystem de un deep agent?
- a) En el disco local
- b) En el state del agente (virtual)
- c) En LangSmith
- d) En un sandbox remoto

<details><summary>Respuesta</summary>

**b.** Es un filesystem virtual dentro del state. Los backends de disco y sandbox se configuran aparte (M2.2–M2.3).
</details>

**5.** Para usar un modelo de NVIDIA alojado en OpenRouter, el curso usa `ChatOpenAI`. ¿Por qué?
- a) Porque NVIDIA es parte de OpenAI
- b) Porque la API de OpenRouter es compatible con OpenAI: basta cambiar `base_url`
- c) Porque `init_chat_model` no soporta NVIDIA
- d) Es un error del curso

<details><summary>Respuesta</summary>

**b.** Muchos proveedores (OpenRouter, Kimi, servidores locales) exponen una API compatible con OpenAI; se reutiliza `ChatOpenAI` apuntando a otro `base_url`.
</details>

**6.** Con Ollama, un deep agent ignora sus tools y responde raro, sin dar ningún error. ¿Qué revisas primero?
- a) La API key
- b) `num_ctx`: si el contexto es chico, Ollama recorta en silencio el system prompt largo del deep agent
- c) El checkpointer
- d) La versión de Python

<details><summary>Respuesta</summary>

**b.** Ollama trunca sin avisar cuando el prompt excede el contexto. Los deep agents tienen un system prompt de varios miles de tokens.
</details>

## M1.1 · Overview
**7.** En deepagents 0.7, ¿cómo se obtiene la tool `write_todos`?
- a) Viene siempre por defecto
- b) Pasándola en `tools=[write_todos]`
- c) Agregando `TodoListMiddleware` en `middleware`
- d) Ya no existe

<details><summary>Respuesta</summary>

**c.** Desde 0.7 la planificación es opt-in: se activa con `TodoListMiddleware`. Antes venía incluida.
</details>

## M1.3 · Models
**8.** Quieres pasar de Claude Haiku a GPT-4.1 en todos los labs. ¿Qué cambias?
- a) Cada `create_deep_agent(...)` de cada lab
- b) La línea de `models.py` a `init_chat_model("openai:gpt-4.1")`
- c) El system prompt, porque cada proveedor necesita uno distinto
- d) Las tools, porque OpenAI usa otro formato

<details><summary>Respuesta</summary>

**b.** El string `"proveedor:modelo"` elige el modelo; el resto del agente (prompt, tools) queda idéntico. LangChain traduce el formato de tools por ti.
</details>

**9.** Un modelo `:free` de OpenRouter responde `429 rate-limited upstream`. ¿Qué es lo más probable?
- a) Tu código tiene un bug en las tools
- b) Se acabó el cupo compartido del modelo gratis; reintenta más tarde o usa otro modelo
- c) Falta `num_ctx`
- d) El checkpointer está lleno

<details><summary>Respuesta</summary>

**b.** Los modelos gratis comparten cupo entre todos los usuarios. Es un límite del proveedor, no de tu agente.
</details>

## M1.4 · System prompt
**10.** Defines `SYSTEM_PROMPT = "Eres un pirata..."` pero llamas `create_deep_agent(model=model)`. ¿Qué pasa?
- a) El agente habla como pirata igual
- b) El agente no recibe tu persona: hay que pasar `system_prompt=SYSTEM_PROMPT`
- c) Error de Python
- d) Usa un prompt base largo del harness que lo reemplaza

<details><summary>Respuesta</summary>

**b.** Definir la variable no basta. Y en 0.7 tampoco hay un prompt base largo de respaldo (la **d** es la trampa).
</details>

**11.** En deepagents 0.7, ¿dónde queda tu `system_prompt` dentro del mensaje de sistema?
- a) Al final, después del prompt base
- b) Primero; para algunos modelos el harness agrega después una sección corta específica del modelo
- c) Como un mensaje de usuario
- d) Solo en el primer turno

<details><summary>Respuesta</summary>

**b.** Tu texto va primero. Para modelos como `claude-haiku-4-5` se añaden luego unas pautas cortas de uso de tools.
</details>

## M1.5 · Tools
**12.** ¿Qué pasa con las tools por defecto si llamas `create_deep_agent(tools=[read_sql])`?
- a) Se reemplazan: el agente solo tiene `read_sql`
- b) Se suman: `read_sql` + filesystem + `task`
- c) Se desactiva `task`
- d) Error: hay que heredar de `BaseTool`

<details><summary>Respuesta</summary>

**b.** `tools=` es aditivo. Nada se reemplaza.
</details>

**13.** ¿Quién ejecuta realmente la función de una tool?
- a) El LLM, dentro del proveedor
- b) El runner de Tools del agente, al leer los `tool_calls` del `AIMessage`
- c) LangSmith
- d) El checkpointer

<details><summary>Respuesta</summary>

**b.** El LLM solo emite un `AIMessage` con `tool_calls`; el nodo Tools corre la función y devuelve un `ToolMessage`.
</details>

## M1.6 · MCP
**14.** ¿Qué transport usarías para un servidor MCP remoto **nuevo**?
- a) `sse`
- b) `stdio`
- c) `http` (streamable HTTP)
- d) `websocket`

<details><summary>Respuesta</summary>

**c.** `sse` está deprecado desde la spec 2025-03-26. `stdio` es para subprocesos locales (`command` + `args`).
</details>

**15.** Tras filtrar las tools MCP con `ALLOWED = {"ask_question"}`, el agente dice "no tengo esa tool" y no hay error. ¿Causa más probable?
- a) El servidor está caído
- b) El nombre no coincide (el servidor renombró la tool) y el filtro quedó vacío
- c) Falta `await`
- d) El modelo no soporta MCP

<details><summary>Respuesta</summary>

**b.** Si el servidor estuviera caído, `get_tools()` fallaría. Un filtro vacío falla en silencio: imprime los nombres antes de filtrar.
</details>

## M1.7 · Messages, threads y checkpointers
**16.** Creas un agente nuevo con un `MemorySaver()` nuevo y usas el mismo `thread_id` de ayer. ¿Recuerda la conversación?
- a) Sí, el `thread_id` es la memoria
- b) No: el historial vive en la instancia del checkpointer, y esta es nueva
- c) Sí, si el modelo es el mismo
- d) Solo los mensajes de sistema

<details><summary>Respuesta</summary>

**b.** El `thread_id` es solo la etiqueta; el checkpointer es el archivador. `MemorySaver` además vive en RAM.
</details>

**17.** ¿Qué permite `get_state_history(config)`?
- a) Borrar checkpoints viejos
- b) Listar los checkpoints de un thread y reanudar desde uno anterior ("time travel")
- c) Ver las trazas de LangSmith
- d) Exportar el thread a Postgres

<details><summary>Respuesta</summary>

**b.** Invocar con el `config` (con `checkpoint_id`) de un snapshot viejo sigue desde ahí; los checkpoints nuevos no se borran.
</details>

## M1.8 · Human-in-the-loop
**18.** Quieres que el humano pueda **bloquear** un `send_email`. ¿Qué decisión permites?
- a) `respond`
- b) `reject`
- c) `approve`
- d) `edit` con el body vacío

<details><summary>Respuesta</summary>

**b.** Con `respond` el modelo lee tu texto como resultado exitoso y puede creer que el email salió. `respond` es para tools tipo `ask_user`.
</details>

**19.** ¿Cuál de estas piezas **no** es necesaria para pausar y reanudar con HITL?
- a) `interrupt_on`
- b) checkpointer
- c) mismo `thread_id` al reanudar
- d) `TodoListMiddleware`

<details><summary>Respuesta</summary>

**d.** Las 4 piezas son `interrupt_on`, checkpointer, `thread_id` y `Command(resume=...)`.
</details>

## M1.9 · Práctica
**20.** En la Judge Card, ¿por qué el producto lo elige la tool `score_and_match` y no el LLM?
- a) Porque el LLM no sabe de productos
- b) Para que la elección sea determinista; el LLM (y el MCP) solo redactan y describen
- c) Porque MCP no puede devolver texto
- d) Por el rate limit

<details><summary>Respuesta</summary>

**b.** Patrón útil: la lógica que debe ser exacta va en código (tool); el modelo pone la voz.
</details>

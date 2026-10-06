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

**d.** El kit trae planning (`write_todos`), filesystem (`ls`, `read_file`, `write_file`, `edit_file`, `glob`, `grep`) y subagentes (`task`). La búsqueda web hay que pasarla como tool propia.
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

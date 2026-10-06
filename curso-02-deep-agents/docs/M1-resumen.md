# M1 · Resumen: fundamentos del deep agent

> **Estado:** ✅ · **Fecha:** 2026-10-06 · Lecciones M1.1–M1.9 · Modelo: Nemotron 3 Ultra (OpenRouter `:free`) · Versión: **deepagents 0.7**

## 🧸 El módulo en una frase
Un deep agent es `create_agent` + un harness (filesystem, subagentes, summarization, planning opcional). Tú controlas **6 perillas**, y la práctica Judge Card las usa todas.

## 🎛️ Las 6 perillas de `create_deep_agent`
```python
agent = create_deep_agent(
    model=model,                      # M1.3 · "proveedor:modelo" vía init_chat_model
    system_prompt=SYSTEM_PROMPT,      # M1.4 · va PRIMERO en el mensaje de sistema
    tools=[mi_tool, *mcp_tools],      # M1.5/M1.6 · ADITIVO a los built-ins
    interrupt_on={"send_email": True},# M1.8 · pausa antes de ejecutar
    checkpointer=MemorySaver(),       # M1.7 · guarda threads (y las pausas HITL)
)
agent.invoke({"messages": [...]}, config={"configurable": {"thread_id": "t1"}}, version="v2")
```

## 📌 Lo esencial por lección
| Lección | Si solo recuerdas una cosa |
|---|---|
| M1.1 Overview | Lo "deep" está en el harness. **0.7:** `write_todos` es opt-in y no hay prompt base largo |
| M1.2 Running | Built-ins: `ls, read_file, write_file, edit_file, delete, glob, grep, execute, task`. Filesystem = **state** (virtual) |
| M1.3 Models | Cambiar de modelo = 1 línea en `models.py`. Prefijo = proveedor, sufijo = modelo |
| M1.4 System prompt | Escribirlo no basta: `system_prompt=`. Persona (voz) ≠ scope (dominio + negativa) |
| M1.5 Tools | `@tool` + docstring. El LLM **pide** (`tool_calls`), el nodo Tools **ejecuta** |
| M1.6 MCP | `MultiServerMCPClient` → `get_tools()` → `BaseTool`. `http` para remoto, `stdio` local, `sse` deprecado |
| M1.7 Threads | Checkpointer = archivador, thread = carpeta, `thread_id` = etiqueta. Misma etiqueta + **otro** archivador = vacío |
| M1.8 HITL | `approve` / `edit` / `reject` / `respond`. **Nunca `respond` para bloquear** acciones |
| M1.9 Práctica | Lógica exacta en la tool, voz en el LLM |

## ⚠️ Trampas típicas del examen
1. "`tools=` reemplaza las tools por defecto" → **falso**, se suman.
2. "`write_todos` viene por defecto" → **falso desde 0.7** (`TodoListMiddleware`).
3. "Sin `system_prompt` el agente usa un prompt base largo" → **falso desde 0.7**.
4. "El LLM ejecuta la tool" → **falso**, emite `tool_calls`.
5. "Mismo `thread_id` = misma memoria" → solo con la **misma instancia** de checkpointer.
6. "`respond` sirve para rechazar un email" → **peligroso**: el modelo cree que se envió. Usa `reject`.
7. "Para MCP remoto uso `sse`" → deprecado; usa `http`.
8. HITL sin checkpointer → no hay dónde guardar la pausa.

## 🛠️ Lecciones operativas (de mis corridas)
- **Filtros silenciosos:** DeepWiki renombró `ask_question` → `ask_wiki_question` y el agente siguió sin error, solo sin la tool. Imprime lo que expone el servidor antes de filtrar.
- **Modelos `:free`:** `429` (cupo compartido) y `503` (saturado). El `503` llega en el cuerpo de la respuesta y `max_retries` no lo reintenta. No lances muchos labs en paralelo. Y hay un tope de **50 requests/día** sin créditos (el módulo 1 completo lo agotó).
- **Tamaño ≠ éxito en tareas simples:** LFM 2.6B (1.7 s) resolvió la pregunta y el SQL igual que Nemotron 550B (27 s). La diferencia aparece en tareas largas y de varios pasos.

## 🧠 Mnemotecnia del módulo
**"Mo-Si-To-In-Che"**: **Mo**del, **Si**stem prompt, **To**ols, **In**terrupt_on, **Che**ckpointer. (El thread va en el `config` del invoke.)

## 📓 Para practicar
`python/notebooks/m1-practica.ipynb`: una sección por lección, con el núcleo de cada lab y una prueba rápida.

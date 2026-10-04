# Introduction to LangChain (Python)

Fundamentos de LangChain v1: modelos, tools, `create_agent`, middleware, memoria y salida estructurada.

**Dominio del examen:** Build — ver [00 Examen LCAE - Guía](../examen-lcae.md)

## Temas del examen que cubre
- [ ] Diferencias entre `create_agent` y `deepagents`
- [ ] Middleware
- [ ] Context engineering

## Lecciones
> Una nota por lección, escrita mientras corría cada notebook en el lab local.
- [x] [M1.1 Foundational Models](M1.1-foundational-models.md)
- [x] [M1.2 Prompting](M1.2-prompting.md)
- [x] [M1.3 Tools](M1.3-tools.md)
- [x] [M1.4 Web Search](M1.4-web-search.md)
- [x] [M1.5 Memory](M1.5-memory.md)
- [x] [M1.6 Multimodal](M1.6-multimodal.md)
- [x] [M1.7 Personal Chef](M1.7-personal-chef.md) (proyecto del módulo 1) ✅ **Módulo 1 completo**

### Módulo 2 — notebooks
- [ ] M2.1 MCP — `2.1_mcp.ipynb`, `2.1_travel_agent.ipynb`
- [ ] M2.2 Context and State — `2.2_runtime_context.ipynb`, `2.2_state.ipynb`
- [ ] M2.3 Multi-Agent Systems — `2.3_multi_agent.ipynb`
- [ ] M2.4 Wedding Planner (proyecto) — `2.4_wedding_planners.ipynb`
- [ ] Bonus: RAG — `bonus_rag.ipynb`
- [ ] Bonus: SQL Query — `bonus_sql.ipynb`

> Repo: https://github.com/langchain-ai/lca-lc-foundations

### Módulo 3 — Production-Ready Agent
- [ ] (10 lecciones; listar al empezar)

## Ideas clave del curso (resumen final)
### ⭐ Lo que más me gustó (para reutilizar en mis proyectos)
1. **Controlar lo que entra al modelo para bajar la latencia.** Tavily devuelve `raw_content: None` por defecto: solo trae un resumen (`content`) y no la página completa. Recortar todavía más (`max_results`, solo `title/url/content`) baja el tiempo en CPU. Regla: en local, cada token que entra al modelo cuesta tiempo. → [M1.4 Web Search](M1.4-web-search.md)
2. **Streaming para la experiencia de respuesta.** Con `stream` el texto aparece mientras se genera y la espera se siente mucho menor, aunque el tiempo total sea el mismo. `stream_mode="updates"` muestra además cada paso del agente (model → tools → model). → [M1.1 Foundational Models](M1.1-foundational-models.md) · [M1.3 Tools](M1.3-tools.md)
3. **Pydantic para salida estructurada.** `response_format=MiModelo` devuelve un objeto tipado en `response["structured_response"]`, listo para guardar en una base de datos o pasar a otro sistema. Con Ollama necesita un modelo con tools (qwen3) o `with_structured_output(method="json_schema")`. → [M1.2 Prompting](M1.2-prompting.md)
4. **Prompts para modelos pequeños.** Los modelos de 4B–8B no deducen el formato: hay que decirlo explícito ("Respond ONLY with…") y dar los ejemplos few-shot como `HumanMessage`/`AIMessage`. Y si el prompt promete algo sin tool que lo haga, el modelo lo inventa. → [M1.2 Prompting](M1.2-prompting.md) · [M1.3 Tools](M1.3-tools.md)
5. **Memoria = reenviar el historial.** Checkpointer + `thread_id`; cada turno cuesta más tokens. → [M1.5 Memory](M1.5-memory.md)
7. **Exigir fuentes a un agente con búsqueda.** Sin pedirlo, mezcla resultados con su propio conocimiento y dice "según lo que encontré". → [M1.7 Personal Chef](M1.7-personal-chef.md)
6. **Multimodal: probar las 3 capas.** El modelo puede soportar audio y la integración no; aislar con la API directa y verificar la entrada antes de culpar al modelo. → [M1.6 Multimodal](M1.6-multimodal.md)

### Aplicación al proyecto RF Optimization Copilot
- Tools que devuelvan KPIs **resumidos**, no tablas completas (punto 1).
- Diagnóstico de celda como modelo Pydantic: `causa`, `evidencia`, `acción`, `confianza` (punto 3).
- System prompts con formato explícito para modelos locales (punto 4).
- Un `thread_id` por celda o por caso investigado, con `PostgresSaver` (punto 5).

## Rutas de docs útiles (para el examen)
-

## Preguntas de repaso
1.

## Notebooks / repo
-

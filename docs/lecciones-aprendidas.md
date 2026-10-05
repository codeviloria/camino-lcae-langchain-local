# 🧠 Lecciones aprendidas — consolidado

Reglas generales que salen de las lecciones. El detalle de cada caso está en su nota.

## Entorno y setup
- **Editar el `.env` → reiniciar el kernel.** LangSmith guarda la key en caché; `load_dotenv()` no sobrescribe sin `override=True`. ([M1.1 Foundational Models](module-1/M1.1-foundational-models.md))
- **Validar la API key por formato y largo:** una PAT de LangSmith empieza con `lsv2_pt_` y mide 51 caracteres. ([M1.1 Foundational Models](module-1/M1.1-foundational-models.md))
- **Secretos:** nunca en capturas ni en git. Si se filtra uno, revocarlo y crear otro. ([M1.1 Foundational Models](module-1/M1.1-foundational-models.md))
- **Sin APIs de pago:** `local_model.py` → `get_model()` conecta todos los notebooks a Ollama en `<ollama-host>` ([00 Setup lab local](setup-lab-local.md)). Las celdas originales quedan comentadas al lado de las adaptadas. ([M1.1 Foundational Models](module-1/M1.1-foundational-models.md))

- **`ModuleNotFoundError: local_model`:** el kernel busca los imports en la carpeta del notebook, no en la raíz del repo. `local_model.py` vive en la raíz, así que en cada notebook va primero la línea que agrega esa carpeta a `sys.path`. ([M1.3 Tools](module-1/M1.3-tools.md) · [00 Setup lab local](setup-lab-local.md))
- **Después de un apagón:** montar el disco, correr `uv run jupyter lab` en la raíz del repo, revisar que Ollama responda (`curl …:11434/api/tags`) y correr las celdas desde arriba. ([00 Setup lab local](setup-lab-local.md))

## Modelos locales
- **`qwen3` + `reasoning=False`** (vía `get_model()`); si no, gasta tokens razonando en silencio. ([M1.1 Foundational Models](module-1/M1.1-foundational-models.md))
- **Agentes con tools → `qwen3`**, no `gemma3`. ([M1.1 Foundational Models](module-1/M1.1-foundational-models.md))
- **Medir rendimiento** con `eval_count / eval_duration` y `ollama ps`. ([M1.1 Foundational Models](module-1/M1.1-foundational-models.md))

- **Elegir el modelo según la lección:** `gemma3:4b` para prompts y texto (rápido); `qwen3` para tools, agentes y `response_format`. ([M1.2 Prompting](module-1/M1.2-prompting.md))
- **Para confirmar qué modelo se usó:** `model.model` o el trace; `inspect.signature` muestra solo el default. ([M1.2 Prompting](module-1/M1.2-prompting.md))

- **Ver tools en un modelo:** `ollama show <modelo>` → Capabilities. `qwen3:8b` y `gemma4` tienen `tools` (y thinking activo por defecto). ([M1.3 Tools](module-1/M1.3-tools.md))
- **Primera llamada lenta (~20 s) = carga del modelo**; cambiar `num_ctx` obliga a recargar. ([M1.3 Tools](module-1/M1.3-tools.md))
- **En CPU se generan ~5,7 tokens/s**: `reasoning=False` es obligatorio. ([M1.3 Tools](module-1/M1.3-tools.md))

## Jupyter y diagnóstico
- **Celda en `[*]` y el server sin peticiones → kernel bloqueado.** Las celdas nuevas quedan en cola; reiniciar el kernel. ([M1.3 Tools](module-1/M1.3-tools.md))
- **Después de reiniciar, correr todo desde arriba** (las variables se borran). ([M1.3 Tools](module-1/M1.3-tools.md))
- **Diagnosticar por capas:** red (`GET /`) → Ollama (`/api/chat`) → tool calling → agente. ([M1.3 Tools](module-1/M1.3-tools.md))
- **Ver el agente con `stream_mode="updates"`**, no con un `invoke` mudo; y poner timeout. ([M1.3 Tools](module-1/M1.3-tools.md))

## Tools
- **Si el system prompt promete algo que ninguna tool hace, el modelo lo inventa** (dio 467² = 217,489; es 218,089). ([M1.3 Tools](module-1/M1.3-tools.md))
- **El nombre que ve el modelo lo define `@tool("nombre")`**, no la variable de Python. ([M1.3 Tools](module-1/M1.3-tools.md))

## Web search
- **Sin tool de búsqueda, el modelo inventa datos actuales con seguridad** (dijo que Uribe es presidente, "reelegido en 2022"). ([M1.4 Web Search](module-1/M1.4-web-search.md))
- **En local, la salida de la tool es latencia:** 5 resultados de Tavily ≈ 2.000 tokens ≈ 1 min en CPU. Usar `max_results=3` y recortar `content`. ([M1.4 Web Search](module-1/M1.4-web-search.md))
- **La docstring debe decir cuándo usar la tool**, no solo qué hace. ([M1.4 Web Search](module-1/M1.4-web-search.md))

## Memoria
- **Memoria = checkpointer + `thread_id`.** Sin los dos, cada `invoke` empieza de cero. ([M1.5 Memory](module-1/M1.5-memory.md))
- **La memoria reenvía el historial:** los tokens de entrada crecen cada turno (22 → 91). En CPU eso es latencia y el contexto tiene techo (`num_ctx=8192`). ([M1.5 Memory](module-1/M1.5-memory.md))
- **`InMemorySaver` solo para pruebas;** en producción `PostgresSaver` o `SqliteSaver`. ([M1.5 Memory](module-1/M1.5-memory.md))

## Multimodal
- **Capacidad del modelo ≠ soporte de la integración.** gemma4 oye audio, pero `langchain-ollama` rechaza `{"type": "audio"}`. Revisar las 3 capas: modelo → runtime → integración. ([M1.6 Multimodal](module-1/M1.6-multimodal.md))
- **Aislar con la API directa** (`/api/chat`) para saber si falla LangChain u Ollama. ([M1.6 Multimodal](module-1/M1.6-multimodal.md))
- **Verificar la entrada antes de culpar al modelo:** nivel del audio y reproducirlo. Con audio mudo, el modelo inventó una transcripción. ([M1.6 Multimodal](module-1/M1.6-multimodal.md))
- **Audio para Gemma: 16 kHz, mono, WAV**, y el prompt en el mismo idioma del audio. ([M1.6 Multimodal](module-1/M1.6-multimodal.md))
- **Poner siempre el `mime_type` correcto:** Ollama lo ignora, pero OpenAI/Anthropic/Gemini lo validan. El truco audio-como-imagen solo sirve con Ollama. ([M1.6 Multimodal](module-1/M1.6-multimodal.md))
- **Elegir el modelo por modalidad:** `ollama show` → Capabilities (`vision`, `audio`). qwen3 es solo texto. ([M1.6 Multimodal](module-1/M1.6-multimodal.md))

## LangSmith
- **Todo cae en un proyecto** porque el `.env` fija `LANGSMITH_PROJECT`. Separar con un proyecto por notebook, `tracing_context`, o mejor **tags + metadata** en el `config`. ([00 LangSmith - Tracing y Monitor](langsmith-tracing-monitor.md))
- **Los traces guardan errores, latencia y tokens:** la imagen en CPU tardó 2 min; los errores de audio quedaron con su entrada exacta. ([00 LangSmith - Tracing y Monitor](langsmith-tracing-monitor.md))
- **Retención de 14 días** en el plan gratis: anotar lo importante en el vault. ([00 LangSmith - Tracing y Monitor](langsmith-tracing-monitor.md))

## Agentes completos
- **Una tool de búsqueda no garantiza respuestas fundamentadas:** el agente dijo "según lo que encontré" y la receta no estaba en los resultados. Pedir la URL fuente en el system prompt. ([M1.7 Personal Chef](module-1/M1.7-personal-chef.md))
- **La longitud de la respuesta es latencia:** 863 tokens = 80 s en CPU. Limitar desde el prompt ("máximo 3", "instrucciones solo si las pide"). ([M1.7 Personal Chef](module-1/M1.7-personal-chef.md))
- **gemma4 es el modelo más rápido del lab para agentes con tools** (~10,8 tok/s vs ~5,7 de qwen3:8b). ([M1.7 Personal Chef](module-1/M1.7-personal-chef.md))

## LangGraph dev / Studio
- **`uv run langgraph dev`**, no `uv langgraph dev`. Si falta: `uv add --dev "langgraph-cli[inmem]"`. ([M1.7 Personal Chef](module-1/M1.7-personal-chef.md))
- **Sin checkpointer en el grafo servido:** `langgraph dev` y Deployment manejan la persistencia; un `InMemorySaver` hace fallar la carga (`GraphLoadError`). ([M1.7 Personal Chef](module-1/M1.7-personal-chef.md))
- **El `.py` del grafo solo define, no ejecuta:** nada de `print`, `invoke` ni `list_projects` a nivel de módulo; se ejecutan en cada arranque. ([M1.7 Personal Chef](module-1/M1.7-personal-chef.md))
- **`__file__` en vez de `cwd()`** para encontrar `local_model.py` desde un `.py`. ([M1.7 Personal Chef](module-1/M1.7-personal-chef.md))
- **Studio "Connection failed" → revisar el log del servidor primero.** Casi siempre es que el grafo no cargó. ([M1.7 Personal Chef](module-1/M1.7-personal-chef.md))
- **Actualizar paquetes con uv:** `uv lock --upgrade-package <pkg>` + `uv sync`. Actualiza solo ese paquete y sus dependencias. `langgraph-api` 0.11.2 (EoL) → 0.15.1. ([M1.7 Personal Chef](module-1/M1.7-personal-chef.md))
- **No pegar comandos con comentarios `#` en zsh:** se toman como argumentos (`cp: target 'rompe'`, `grep: debe: No existe`). El respaldo de `uv.lock` **no se hizo**. Para volver atrás: `git checkout uv.lock && uv sync`.
- **Aviso `Failed to hardlink files`:** el caché de uv (home) y el proyecto (`/ruta/al/disco`) están en discos distintos. Silenciar con `export UV_LINK_MODE=copy` en `~/.zshrc`.

## Multi-agente
- **Los datos obligatorios de una tool deben llegar al subagente:** Kiwi exige fecha; sin ella el subagente la pidió. Solución: la fecha en el state y la tool la lee de `runtime.state`. ([M2.4 Wedding Planner](module-2/M2.4-wedding-planner.md))
- **Status `success` ≠ resultado correcto:** hacen falta evaluadores (dominio Test). ([M2.4 Wedding Planner](module-2/M2.4-wedding-planner.md))
- **Separar "el agente falló" de "el dato no existe":** Valledupar no tuvo vuelos (aeropuerto regional) y Bogotá sí. ([M2.4 Wedding Planner](module-2/M2.4-wedding-planner.md))
- **Un arreglo de prompt puede romper otra salida (regresión):** el costo quedó bien, la duración salió en 0 min. ([M2.4 Wedding Planner](module-2/M2.4-wedding-planner.md))
- **Validar el SQL que sugiere el LLM:** en el Wedding Planner corría sin error pero daba `00:00` (`STRFTIME` sin `'unixepoch'`), usaba una columna inexistente (`T.Title`) y `ORDER BY RANDOM()`. Si el SQL no es confiable, pasarlo en el prompt (few-shot) o fijarlo en el agente (tool con SQL parametrizado). Los totales, en código. ([M2.4 Wedding Planner](module-2/M2.4-wedding-planner.md))

## RAG
- **`InMemoryVectorStore` no es una base de datos:** los vectores viven en la RAM del kernel y se pierden al reiniciarlo. Para persistir: FAISS o Chroma (local), pgvector o Qdrant (servidor). ([M2.B Bonus RAG y SQL](module-2/M2.B-bonus-rag-sql.md))
- **`chunk_size` se mide en caracteres:** un PDF de 1.943 caracteres con 1000/200 da 3 chunks. ([M2.B Bonus RAG y SQL](module-2/M2.B-bonus-rag-sql.md))
- **Mismo modelo de embeddings para indexar y consultar** (`nomic-embed-text`, 768 dim); si se cambia, hay que reindexar. ([M2.B Bonus RAG y SQL](module-2/M2.B-bonus-rag-sql.md))
- **Text-to-SQL sin esquema = el modelo inventa tablas:** gemma4 consultó `artists`/`popularity` (no existen) y, ante el error, preguntó al usuario. Solución: system prompt que obligue a explorar el esquema y defina las métricas ambiguas. ([M2.B Bonus RAG y SQL](module-2/M2.B-bonus-rag-sql.md))
- **SQL que corre sin error puede dar una respuesta falsa:** con el esquema, gemma4 unió por `Track.ArtistId` (no existe); SQLite lo resolvió contra la tabla externa y todos los artistas empataron. Respondió con seguridad *System Of A Down*; la referencia es Smashing Pumpkins. Siempre comparar contra un valor conocido. ([M2.B Bonus RAG y SQL](module-2/M2.B-bonus-rag-sql.md))
- **Lo que funcionó en text-to-SQL:** el esquema real en el prompt (`db.get_table_info([...])`) y el camino de JOIN explícito → respuesta correcta en una sola query, confirmada por un evaluador contra la referencia (v2 ❌, v3 ✅). ([M2.B Bonus RAG y SQL](module-2/M2.B-bonus-rag-sql.md))
- **Integraciones en paquetes por proveedor** (`langchain-ollama`, `langchain-tavily`, `langchain-chroma`): cambia el `import`, no el código, porque todas cumplen las interfaces de `langchain-core`. `langchain-community` es legado. ([M2.B Bonus RAG y SQL](module-2/M2.B-bonus-rag-sql.md))

## Middleware y HITL
- **HITL solo protege lo que el modelo pide:** si el modelo no genera el `tool_call`, el semáforo nunca se activa. Verificar `"__interrupt__" in response`. ([M3.3 HITL](module-3/M3.3-hitl.md))
- **La docstring es la interfaz de la tool:** `read_email` decía "from the given address" sin tener argumentos y el modelo pidió la dirección en vez de actuar. ([M3.3 HITL](module-3/M3.3-hitl.md))
- **Cada decisión consume la pausa:** para probar otra decisión hace falta un `invoke` (o thread) nuevo. ([M3.3 HITL](module-3/M3.3-hitl.md))
- **Pedir reintento no garantiza que use la crítica:** tras el Reject, gemma4 volvió a pedir `send_email` con el mismo texto. Para cambios concretos, `edit` es más fiable. ([M3.3 HITL](module-3/M3.3-hitl.md))
- **Las decisiones HITL son datos de entrenamiento:** approve = ejemplo bueno (SFT), edit = corrección, reject + motivo = preferencia (DPO) y caso de evaluación. Registrarlas **antes** de reanudar. ([M3.3 HITL](module-3/M3.3-hitl.md))

## Prompting
- **Con modelos pequeños:** formato explícito ("Respond ONLY…") y few-shot como `HumanMessage`/`AIMessage`. ([M1.2 Prompting](module-1/M1.2-prompting.md))
- **Leer la respuesta con `messages[-1]`**, no con un índice fijo. ([M1.2 Prompting](module-1/M1.2-prompting.md))

## LangChain
- **`response_format` en Ollama = ToolStrategy** → requiere tool calling. Sin tools: `with_structured_output(..., method="json_schema")`. ([M1.2 Prompting](module-1/M1.2-prompting.md))
- **`create_agent`:** una sola forma basta; la última ejecutada sobrescribe `agent`. ([M1.1 Foundational Models](module-1/M1.1-foundational-models.md))
- **La forma string `"proveedor:modelo"`** configura el modelo por variables de entorno (`OLLAMA_HOST`). ([M1.1 Foundational Models](module-1/M1.1-foundational-models.md))

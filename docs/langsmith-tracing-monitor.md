# LangSmith — Tracing y Monitor

Nota transversal: lo que voy aprendiendo de LangSmith mientras hago los cursos. Base del dominio **Monitor** (y parte de **Test** y **Deploy**).

## Cómo se activa el tracing
Variables en `.env` (cargadas con `load_dotenv`):
```
LANGSMITH_TRACING=true
LANGSMITH_API_KEY=lsv2_pt_...      # 51 caracteres, sin prefijos
LANGSMITH_PROJECT=lca-lc-foundations
```
Con eso, **cada `invoke`/`stream` de un agente se registra solo** como un trace. No hay que tocar el código.

## Por qué todo cae en una sola página
Todos los notebooks cargan el mismo `.env` → mismo `LANGSMITH_PROJECT` → todos los traces en `lca-lc-foundations`, sin importar de qué notebook vienen.

## Cómo organizar los traces
| Opción | Código | Cuándo |
|---|---|---|
| **Proyecto por notebook** | `os.environ["LANGSMITH_PROJECT"] = "lca-m1.6-multimodal"` en la primera celda (antes de crear el agente) | Separación total por lección |
| **Proyecto por bloque** | `with tracing_context(project_name="..."): agent.invoke(...)` (`from langsmith import tracing_context`) | Solo una parte del código |
| **Tags + metadata** ⭐ | `agent.invoke(inp, config={"tags": ["M1.6", "audio"], "metadata": {"modelo": "gemma4", "lab": "cpu"}})` | Un solo proyecto, filtrable. **Mi opción para estudiar**: permite comparar todo |

Filtrar en la UI: panel izquierdo → *Tags* / *Metadata* / *Run Name* / *Status*.

## Conceptos de la UI
| Concepto | Qué es |
|---|---|
| **Project** | Contenedor de traces (aquí: `lca-lc-foundations`) |
| **Trace** | Una ejecución completa de punta a punta (un `invoke` del agente) |
| **Run** | Cada paso dentro del trace: `LangGraph` (raíz), `ChatOllama` (llm), `square_root` / `web_search` (tool) |
| **Thread** | Traces agrupados por `thread_id` → conversaciones con memoria ([M1.5 Memory](module-1/M1.5-memory.md)) |
| **Run Type** | `chain`, `llm`, `tool` |
| **Status** | `success`, `error`, `interrupted`, `pending` |
| **Retention** | Plan gratis: **14 días** → exportar o anotar lo importante |

## Lo que muestra mi proyecto (2026-10-03)
| Observación | Ejemplo en mis traces | Lección |
|---|---|---|
| **Errores con la entrada exacta** | `ValueError('Blocks of type audio not supported')`, status error, 0,02 s | LangSmith guarda el input que falló → reproducible ([M1.6 Multimodal](module-1/M1.6-multimodal.md)) |
| **Latencia de visión en CPU** | Imagen: **2,01 min** y **113 s**, ~1.400–1.500 tokens | La imagen domina el tiempo; achicarla |
| **Latencia de audio** | Transcripciones: 1,7 – 12,6 s, ~200–290 tokens | Audio corto es barato |
| **Tokens por run** | Texto simple: 76–151; ciudad lunar: 1.050 | Columna *Tokens* para ver costo |
| **Threads** | "Hello my name is Seán" → "What's my favourite colour" | Memoria visible como conversación |
| **Alucinación visible** | "The audio contains a sound of a dog barking" (audio mudo) | El trace guarda la evidencia para revisar después |

## Para el examen (dominio Monitor)
- Diferencia **trace / run / thread**.
- Cómo se activa el tracing (variables de entorno) y cómo cambiar de proyecto.
- **Tags y metadata** para filtrar y segmentar (por modelo, versión, usuario).
- Leer latencia, tokens, errores y costo por run.
- Traces públicos: botón *Share* → URL pública (ej. el de [M1.4 Web Search](module-1/M1.4-web-search.md)).

## Dónde está en la doc
- Observability: https://docs.langchain.com/langsmith/observability
- Tracing con LangChain: https://docs.langchain.com/langsmith/trace-with-langchain
- Proyectos y tags/metadata: https://docs.langchain.com/langsmith/add-metadata-tags

## Preguntas de repaso
1. ¿Por qué todos mis notebooks aparecen en el mismo proyecto?
2. ¿Qué tres formas hay de separar traces por lección?
3. ¿Qué diferencia hay entre un trace, un run y un thread?
4. ¿Cómo encontrarías en LangSmith todos los runs fallidos de gemma4?

## Enlaces
- 00 LCAE - Índice · [00 Lecciones aprendidas](lecciones-aprendidas.md) · [00 Examen LCAE - Guía](examen-lcae.md)

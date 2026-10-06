# Python vs TypeScript en Deep Agents

Hoja de contraste que se llena lab por lab (los ⭐ del README). Sirve para leer TypeScript con soltura y para explicar en una entrevista las diferencias entre los dos SDKs.

## Requisitos del lado TypeScript (`typescript/package.json`)
| Qué | Versión pedida | Nota del lab |
|---|---|---|
| Node.js | `>=24.15 <25` | El lab tiene Node 22: hay que subir a Node 24 antes del primer lab TS |
| pnpm | 11.x (`packageManager`) | El lab tiene pnpm 10 |
| Ejecutar scripts | `tsx` | `pnpm tsx m1/m1.2_scratch_agent.ts` |
| Modelo local | `@langchain/ollama` (ya es dependencia) | Adaptar `typescript/models.ts`, igual que `python/models.py` |

## Equivalencias base
| Concepto | Python | TypeScript |
|---|---|---|
| Cargar `.env` | `load_dotenv(path, override=True)` | `config({ path, override: true })` (dotenv) |
| Modelo genérico | `init_chat_model("anthropic:claude-haiku-4-5")` | `await initChatModel("anthropic:claude-haiku-4-5")` |
| Modelo Ollama | `init_chat_model("ollama:gemma4:latest", base_url=..., num_ctx=..., reasoning=False)` | `await initChatModel("ollama:gemma4:latest", { baseUrl, numCtx, think: false })` |
| Modelo OpenRouter | `ChatOpenAI(model=..., base_url="https://openrouter.ai/api/v1", api_key=...)` | `new ChatOpenAI({ model, apiKey, configuration: { baseURL } })` |
| Elegir proveedor | `if PROVIDER == "openrouter": ... else: ...` | Ternario: `PROVIDER === "openrouter" ? a : b` (no se puede declarar `export const` dos veces) |
| Nombres | `snake_case` | `camelCase` (`strong_model` → `strongModel`) |
| Asincronía | Opcional (`invoke` / `ainvoke`) | Siempre `await` |
| Esquema de una tool | Type hints + docstring | `zod` (`z.object({...})`) + `description` |
| Ejecutar un lab | `uv run python m1/archivo.py` | `pnpm tsx m1/archivo.ts` |

## ⚠️ Trampa: orden de los imports (ESM), aprendida con el helper `local_model.ts` (ya retirado)
En Python, `models.py` hace `load_dotenv()` y **después** importa `local_model`, y funciona porque Python ejecuta línea por línea. En TypeScript (ESM) **todos los `import` se ejecutan antes** que el cuerpo del archivo. Si `local_model.ts` leyera `process.env` al cargarse, todavía no habría `.env` y usaría `localhost`. Solución: leer la URL **dentro** de `getModel()`, en vez de en una constante a nivel de módulo.

## Tipos: el "type guard"
`AIMessage.isInstance(m)` le dice a TypeScript que dentro del `if`, `m` es un `AIMessage` y por lo tanto tiene `tool_calls`. En Python no hace falta: se usa `getattr(m, "tool_calls", None)`.

## Por lab (se completa al hacerlos)
| Lab | Diferencia que me llamó la atención |
|---|---|
| M1.2 | **O-A-J**: opciones en un Objeto (`createDeepAgent({ model })`), siempre `await`, y los imports locales llevan `.js` aunque el archivo sea `.ts`. Tiempos Ollama: TS 135.8 s (frío) vs Python 98.5 s; OpenRouter: TS 13.9 s vs Python 23.2 s (Python generó una respuesta más larga). La diferencia la ponen el arranque en frío y los tokens generados, no el lenguaje |
| M1.5 | |
| M1.7 | |
| M1.8 | |
| M4.1 | |
| M5.3 | |

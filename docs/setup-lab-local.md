# 🖥️ Setup del lab local — `local_model.py`

> **Este script es lo que permite correr el curso sin APIs de pago.** Todos los notebooks llaman a `get_model()` en vez de `init_chat_model("gpt-5-nano")`, y el modelo corre en Ollama en el server del lab.

## Dónde está
`<repo>/local_model.py` (raíz del repo del curso)

## El script
```python
import os
from langchain_ollama import ChatOllama

OLLAMA_URL = os.getenv("OLLAMA_BASE_URL", "http://<ollama-host>:11434")

def get_model(name: str = "qwen3:8b", temperature: float = 0, **kw):
    """Modelo local en el servidor Ollama. Alternativas: gemma4:e2b, qwen3:4b, gemma3:4b (sin tools)."""
    kw.setdefault("num_ctx", 8192)
    return ChatOllama(model=name, base_url=OLLAMA_URL, temperature=temperature,
                      reasoning=False, **kw)
```

Qué resuelve cada línea:
- **`base_url=OLLAMA_URL`**: apunta al server del lab (`<ollama-host>:11434`), no a localhost.
- **`reasoning=False`**: apaga el "thinking" de qwen3. Sin esto, gasta cientos de tokens razonando en silencio (79 s vs ~15 s en CPU). Ver [M1.1 Foundational Models](module-1/M1.1-foundational-models.md).
- **`num_ctx=8192`**: contexto suficiente para tools y resultados de búsqueda. Cambiarlo obliga a Ollama a recargar el modelo.
- **`temperature=0`**: respuestas reproducibles; cada celda puede cambiarla (`get_model(temperature=1.0)`).
- **`**kw`**: pasa cualquier otro parámetro de `ChatOllama` (`num_predict=10`, `client_kwargs={"timeout": 120}`).

## Primera celda de cada notebook
El kernel busca los imports en la **carpeta del notebook**, no en la raíz del repo. Esta línea sube por las carpetas hasta encontrar el script:
```python
import sys, pathlib
sys.path.insert(0, str(next(p for p in [pathlib.Path.cwd(), *pathlib.Path.cwd().parents] if (p / "local_model.py").exists())))

from dotenv import load_dotenv
load_dotenv()
from local_model import get_model, OLLAMA_URL
model = get_model()
```

## Cómo reemplazar las celdas del curso
| Celda original | Versión lab |
|---|---|
| `init_chat_model("gpt-5-nano")` | `get_model()` o `init_chat_model("ollama:qwen3:8b", base_url=OLLAMA_URL)` |
| `init_chat_model("claude-sonnet-4-6")` | `get_model("qwen3:4b")` |
| `ChatGoogleGenerativeAI(...)` | `ChatOllama(model="gemma3:4b", base_url=OLLAMA_URL)` |
| `create_agent("gpt-5-nano")` | `create_agent(model=get_model())` |

Regla: dejar la celda original comentada (`## Esto no lo corrí, lo adapté a Ollama local`) al lado de la adaptada.

## Qué modelo usar
| Modelo | Tools / `response_format` | Uso |
|---|---|---|
| `qwen3:8b` (default) | ✅ | Agentes, tools, salida estructurada |
| `gemma4:e2b` | ✅ (revisar con `ollama show`) | Tools; modelo del artículo y de la hackathon |
| `qwen3:4b` | ✅ | Más rápido, menos preciso |
| `gemma3:4b` | ❌ `does not support tools (400)` | Solo prompts y texto |

Para ver qué modelo se usó: `model.model` o `response.response_metadata["model_name"]`. `inspect.signature(get_model)` muestra solo el default.

## `.env` del curso
```env
LANGSMITH_API_KEY=lsv2_pt_...        # nunca en notas ni capturas
LANGSMITH_TRACING=true
LANGSMITH_PROJECT=lca-lc-foundations
OLLAMA_HOST=http://<ollama-host>:11434  # necesario para la forma string create_agent("ollama:qwen3:8b")
TAVILY_API_KEY=tvly-...               # web search (M1.4)
```
Después de editar el `.env`: **reiniciar el kernel**.

## Levantar todo (por ejemplo después de un apagón)
```bash
ls /ruta/al/disco                                   # el disco debe estar montado
cd <repo>
uv run jupyter lab                                # uv sync si faltan paquetes
curl http://<ollama-host>:11434/api/tags            # Ollama responde
```
En el server: `ollama ps` (modelo cargado, GPU o CPU) y el log de Ollama.

## Relacionado
- [00 Lecciones aprendidas](lecciones-aprendidas.md) · [M1.1 Foundational Models](module-1/M1.1-foundational-models.md) · [M1.2 Prompting](module-1/M1.2-prompting.md) · [M1.3 Tools](module-1/M1.3-tools.md)

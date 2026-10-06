"""🟢 ADAPTADO LOCAL — helper para usar Ollama en lugar de Anthropic/OpenAI.

Motivo: el lab corre en CPU con modelos locales (sin API keys de pago).
La URL del servidor sale del .env (OLLAMA_BASE_URL u OLLAMA_HOST); nunca se escribe aquí.

Uso:
    from local_model import get_model
    model = get_model("gemma4:latest")
    strong_model = get_model("qwen3:8b", num_ctx=32768)
"""

import os

from langchain_ollama import ChatOllama

OLLAMA_URL = os.getenv("OLLAMA_BASE_URL") or os.getenv("OLLAMA_HOST") or "http://localhost:11434"


def get_model(name: str = "qwen3:8b", temperature: float = 0, **kw):
    """Devuelve un ChatOllama listo para create_agent / create_deep_agent.

    - reasoning=False: evita que qwen3 gaste tokens "pensando" en CPU.
    - num_ctx: ventana de contexto. Deep Agents trae un system prompt largo
      (planning + filesystem + subagents), por eso aquí el default es 16k.
    """
    kw.setdefault("num_ctx", 16384)
    return ChatOllama(
        model=name,
        base_url=OLLAMA_URL,
        temperature=temperature,
        reasoning=False,
        **kw,
    )

"""Modelo local vía Ollama para correr el curso sin APIs de pago.

Configura el servidor en .env:
    OLLAMA_BASE_URL=http://<ip-del-servidor>:11434

Modelos probados (CPU, sin GPU):
    gemma4:latest  -> texto, tools, visión y audio (recomendado; el más rápido en el lab)
    qwen3:8b       -> texto y tools
    qwen3:4b       -> texto y tools (más liviano)
    gemma3:4b      -> texto y visión (sin tools)
"""
import os
from langchain_ollama import ChatOllama

OLLAMA_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")


def get_model(name: str = "qwen3:8b", temperature: float = 0, **kw):
    """Devuelve un ChatOllama con thinking apagado (reasoning=False) y contexto de 8K."""
    kw.setdefault("num_ctx", 8192)
    return ChatOllama(model=name, base_url=OLLAMA_URL,
                      temperature=temperature, reasoning=False, **kw)

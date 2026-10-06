"""Ayudas para los notebooks guiados del módulo 1.

- preparar(): busca la raíz del repo, carga el .env y revisa el servidor Ollama.
- semaforo(): dice si el servidor Ollama está libre u ocupado (es compartido).
- ver(respuesta): imprime la conversación de un agente con colores y emojis,
  más fácil de leer que pprint.
"""

import os
import pathlib
import sys

# Colores ANSI (Jupyter los muestra)
_AZUL, _VERDE, _AMARILLO, _GRIS, _FIN = "\033[94m", "\033[92m", "\033[93m", "\033[90m", "\033[0m"


def preparar():
    """Deja todo listo: raíz del repo en sys.path, .env cargado y semáforo."""
    aqui = pathlib.Path.cwd()
    raiz = next(p for p in [aqui, *aqui.parents] if (p / "local_model.py").exists())
    if str(raiz) not in sys.path:
        sys.path.insert(0, str(raiz))

    from dotenv import load_dotenv

    load_dotenv(raiz / ".env", override=True)

    # Revisamos que las llaves existan SIN imprimirlas (nunca muestres una API key)
    print("📁 Raíz del repo encontrada")
    print("🔑 LangSmith key presente:", bool(os.getenv("LANGSMITH_API_KEY")))
    print("🔑 Tavily key presente:   ", bool(os.getenv("TAVILY_API_KEY")))
    print("🖥️  Servidor Ollama configurado:", bool(os.getenv("OLLAMA_BASE_URL")))
    semaforo()


def semaforo():
    """🟢 libre · 🟡 hay un modelo cargado · 🔴 no hay conexión."""
    import requests

    url = os.getenv("OLLAMA_BASE_URL") or "http://localhost:11434"
    try:
        cargados = requests.get(f"{url}/api/ps", timeout=5).json().get("models", [])
    except Exception as e:  # noqa: BLE001
        print(f"🔴 No llego al servidor Ollama ({type(e).__name__}). Revisa OLLAMA_BASE_URL en tu .env y que el servidor esté encendido.")
        return
    if cargados:
        nombres = [m.get("name") for m in cargados]
        print(f"🟡 Hay un modelo cargado: {nombres}.")
        print("   Si fuiste tú hace menos de 5 minutos, sigue tranquila. Si no, alguien más lo está usando: espera un rato.")
    else:
        print("🟢 Servidor libre. ¡Adelante!")


def ver(respuesta):
    """Muestra cada mensaje de la conversación de forma legible."""
    mensajes = respuesta["messages"] if isinstance(respuesta, dict) else respuesta
    for i, m in enumerate(mensajes):
        tipo = type(m).__name__
        if tipo == "HumanMessage":
            print(f"{_AZUL}[{i}] 🧑 Humano:{_FIN} {m.content}")
        elif tipo == "AIMessage":
            if getattr(m, "tool_calls", None):
                for tc in m.tool_calls:
                    print(f"{_AMARILLO}[{i}] 🤖 Modelo pide usar la tool → {tc['name']}({tc['args']}){_FIN}")
            if m.content:
                print(f"{_VERDE}[{i}] 🤖 Modelo:{_FIN} {m.content}")
        elif tipo == "ToolMessage":
            texto = str(m.content)
            corto = texto[:300] + (" …" if len(texto) > 300 else "")
            print(f"{_GRIS}[{i}] 🔧 Resultado de la tool '{m.name}': {corto}{_FIN}")
        else:
            print(f"[{i}] {tipo}: {m.content}")
    print()

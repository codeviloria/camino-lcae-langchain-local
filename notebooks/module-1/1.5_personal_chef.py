"""Personal Chef (Módulo 1, proyecto) servido con `langgraph dev`.

Uso (desde esta carpeta):
    uv run langgraph dev
El grafo se define en langgraph.json como "agent".
Nota: sin checkpointer; LangGraph Server maneja la persistencia.
"""
import sys
import pathlib
from typing import Any, Dict

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.tools import tool
from tavily import TavilyClient

load_dotenv()

# local_model.py vive en la raíz del repo
_here = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(next(p for p in [_here, *_here.parents] if (p / "local_model.py").exists())))
from local_model import get_model  # noqa: E402

tavily_client = TavilyClient()


@tool
def web_search(query: str) -> Dict[str, Any]:
    """Search the web for recipes and current information."""
    return tavily_client.search(query, max_results=3)


system_prompt = """
Eres un chef personal. El usuario te dará los ingredientes que tiene en casa.
1. Usa web_search para buscar recetas con esos ingredientes.
2. Propón máximo 3 recetas: nombre, una línea de descripción y la URL de la fuente.
3. Si adaptas una receta o agregas ingredientes que el usuario no tiene, dilo.
4. Da las instrucciones completas solo si el usuario las pide.
Responde en español y de forma breve.
"""

agent = create_agent(
    model=get_model("gemma4:latest"),
    tools=[web_search],
    system_prompt=system_prompt,
)

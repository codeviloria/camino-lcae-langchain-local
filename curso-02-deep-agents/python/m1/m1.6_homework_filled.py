# python/m1/m1.6_homework_filled.py
"""Reference copy of m1.6_homework.py with TODOs 1 and 2 filled in so you
can run it end to end and see what "done" looks like. This is just one
possible answer, so yours might be different. Explore!

📚 Un servidor MCP anuncia sus tools; MultiServerMCPClient.get_tools() las convierte en
   tools de LangChain. Filtrar con ALLOWED = mínimo privilegio. Si el servidor renombra
   una tool, el filtro queda vacío y el agente sigue SIN error (solo con sus built-ins).
🧠 "MCP = enchufe universal; ALLOWED = el protector de enchufes."
▶️ cd python && uv run python m1/m1.6_homework_filled.py
"""

import asyncio
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)

from deepagents import create_deep_agent
from langchain_mcp_adapters.client import MultiServerMCPClient

from models import model


# TODO 1 filled in: a different public MCP server than the lab's,
# DeepWiki, which answers questions about any public GitHub repo.
async def build_tools():
    client = MultiServerMCPClient({
        "deepwiki": {
            "transport": "http",
            "url": "https://mcp.deepwiki.com/mcp",
        }
    })
    tools = await client.get_tools()

    # 🔸 ORIGINAL DEL CURSO — DeepWiki renombró la tool: el filtro quedaba vacío y el agente
    # respondía "no tengo esa tool" (sin error). Hoy expone ask_wiki_question, read_wiki_*.
    # ALLOWED = {"ask_question"}
    # 🟢 ADAPTADO LOCAL — nombre actual de la tool en el servidor MCP
    ALLOWED = {"ask_wiki_question"}
    # 🟢 EXTRA LOCAL: un filtro vacío falla en silencio → avisar fuerte
    if not any(t.name in ALLOWED for t in tools):
        print(f"⚠️  Ninguna tool coincide con {ALLOWED}. El servidor expone: {[t.name for t in tools]}")
    return [t for t in tools if t.name in ALLOWED]


# TODO 2 filled in
QUESTION = (
    "Use the DeepWiki tool to ask the langchain-ai/deepagents GitHub repo: "
    "what filesystem backends does deepagents support?"
)


async def main():
    tools = await build_tools()
    agent = create_deep_agent(model=model, tools=tools)
    result = await agent.ainvoke({"messages": [{"role": "user", "content": QUESTION}]})
    print(result["messages"][-1].text)


asyncio.run(main())

"""M1.2 · Running a deep agent: el primer deep agent.

📚 TEORÍA
  create_agent (curso 01)     = modelo + tools + bucle. Tú le das TODO.
  create_deep_agent (curso 02) = create_agent + un "kit de supervivencia" incluido:
      - write_todos     → planificar: lista de tareas que el agente va tachando
      - ls, read_file, write_file, edit_file, glob, grep → un filesystem virtual
        (vive en el state, no en tu disco) para guardar notas y resultados largos
      - task            → delegar en subagentes (módulo 4)
      - un system prompt largo que le explica cómo usar todo eso
      - middleware de resumen para conversaciones largas (módulo 3)

🧸 Analogía: create_agent es un chef con un cuchillo. create_deep_agent es el
   mismo chef con una cocina completa: libreta de tareas, despensa (archivos) y
   ayudantes (subagentes). Para una pregunta simple casi no usa la cocina, pero
   ya la tiene.

🧠 Mnemotecnia P-A-D: Planear (todos) · Archivar (filesystem) · Delegar (task).

▶️ Correr (desde python/):  uv run python m1/m1.2_scratch_agent.py
⏳ En CPU: 1–3 min. El system prompt del deep agent es largo y el modelo lo lee entero.
"""

import time  # 🟢 EXTRA LOCAL: medir cuánto tarda en CPU

from deepagents import create_deep_agent

from models import model  # 🟢 ya apunta a Ollama u OpenRouter (ver models.py)

# Sin cambios: el lab original funciona tal cual con el modelo local
agent = create_deep_agent(model=model)

t0 = time.perf_counter()
result = agent.invoke({"messages": [{"role": "user", "content": "What is an LLM?"}]})

print(result["messages"][-1].text)

# 🟢 EXTRA LOCAL: mirar por dentro qué pasó (¿usó alguna herramienta del kit?)
# Para una pregunta simple lo normal es que NO use tools: Human → AI.
print(f"\n⏱️  {time.perf_counter() - t0:.1f} s")
print("🔍 Mensajes:")
for m in result["messages"]:
    calls = [tc["name"] for tc in (getattr(m, "tool_calls", None) or [])]
    print(f"   {type(m).__name__:<12} {'→ tools: ' + ', '.join(calls) if calls else ''}")

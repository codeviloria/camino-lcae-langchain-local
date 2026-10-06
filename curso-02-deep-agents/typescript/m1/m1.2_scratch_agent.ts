/**
 * M1.2 · Running a deep agent (TypeScript): el mismo lab que python/m1/m1.2_scratch_agent.py
 *
 * 📚 TEORÍA: ver el lab de Python. Aquí nos fijamos en las DIFERENCIAS del SDK:
 *
 *   Python                                  TypeScript
 *   ──────────────────────────────────────  ─────────────────────────────────────
 *   from deepagents import create_deep_agent import { createDeepAgent } from "deepagents"
 *   create_deep_agent(model=model)           createDeepAgent({ model })  ← un objeto de opciones
 *   agent.invoke({...})                      await agent.invoke({...})   ← siempre async
 *   result["messages"][-1].text              result.messages.at(-1)?.text
 *   from models import model                 import { model } from "../models.js"  ← ".js" aunque el archivo sea .ts
 *
 * 🧠 Mnemotecnia O-A-J: en TS todo va en un Objeto, todo se Await-ea y los imports llevan .Js
 *
 * ▶️ Correr (desde typescript/):  pnpm tsx m1/m1.2_scratch_agent.ts
 * ⚠️ Requiere Node 24.15+ (ver package.json → engines) y un typescript/.env con OLLAMA_BASE_URL.
 */

import { createDeepAgent } from "deepagents";
import { AIMessage } from "langchain"; // 🟢 EXTRA LOCAL: para reconocer los mensajes de la IA

import { model } from "../models.js"; // 🟢 ya apunta a Ollama (ver models.ts → local_model.ts)

// Sin cambios: el lab original funciona tal cual con el modelo local
const agent = createDeepAgent({ model });

const t0 = performance.now(); // 🟢 EXTRA LOCAL: medir cuánto tarda en CPU
const result = await agent.invoke({
    messages: [{ role: "user", content: "What is an LLM?" }]
});

console.log(result.messages.at(-1)?.text);

// 🟢 EXTRA LOCAL: mirar por dentro qué pasó (¿usó alguna herramienta del kit?)
console.log(`\n⏱️  ${((performance.now() - t0) / 1000).toFixed(1)} s`);
console.log("🔍 Mensajes:");
for (const m of result.messages) {
    // `tool_calls` solo existe en los mensajes de la IA. AIMessage.isInstance() es un
    // "type guard": le dice a TypeScript "dentro de este if, m es un AIMessage".
    // El `as { name: string }[]` le aclara el tipo: el SDK lo infiere de las tools y aquí no las declaramos.
    const toolCalls = AIMessage.isInstance(m) ? ((m.tool_calls ?? []) as { name: string }[]) : [];
    const calls = toolCalls.map((tc) => tc.name);
    console.log(`   ${m.getType().padEnd(8)} ${calls.length ? "→ tools: " + calls.join(", ") : ""}`);
}

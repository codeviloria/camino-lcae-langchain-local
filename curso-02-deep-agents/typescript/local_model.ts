/**
 * 🟢 ADAPTADO LOCAL: helper para usar Ollama en lugar de Anthropic/OpenAI.
 *
 * Motivo: el lab corre en CPU con modelos locales (sin API keys de pago).
 * Es el equivalente TypeScript de `python/local_model.py`.
 *
 * Uso:
 *   import { getModel } from "./local_model.js";
 *   export const model = getModel("gemma4:latest");
 *
 * 📚 Diferencia importante con Python:
 *   En ESM (TypeScript con "module": "NodeNext") todos los `import` se
 *   ejecutan ANTES que el resto del archivo que importa. Por eso NO leemos
 *   process.env al cargar este módulo: `models.ts` todavía no ha cargado el
 *   `.env`. La URL se lee dentro de getModel(), cuando ya está cargado.
 *   En Python el orden es línea por línea, así que allá basta con importar
 *   después de load_dotenv().
 */

import { ChatOllama } from "@langchain/ollama";

export interface LocalModelOptions {
  temperature?: number;
  /** Ventana de contexto. Deep Agents trae un system prompt largo, así que el default es 16k. */
  numCtx?: number;
}

export function ollamaUrl(): string {
  return process.env.OLLAMA_BASE_URL ?? process.env.OLLAMA_HOST ?? "http://localhost:11434";
}

export function getModel(name = "qwen3:8b", opts: LocalModelOptions = {}): ChatOllama {
  return new ChatOllama({
    model: name,
    baseUrl: ollamaUrl(),
    temperature: opts.temperature ?? 0,
    numCtx: opts.numCtx ?? 16384,
    think: false, // = reasoning=False en Python: no gastar tokens "pensando" en CPU
  });
}

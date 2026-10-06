/**
 * Model Initialization File
 *
 * Configures the LLM model used throughout the course.
 *
 * Default: Anthropic claude-haiku-4-5 (fast, cheap, great for learning).
 *
 * ═══════════════════════════════════════════════════════════════════════════
 *   ⚠  IMPORTANT: install the matching package BEFORE swapping providers
 * ═══════════════════════════════════════════════════════════════════════════
 *
 *   Provider              Package                      Installed?
 *   --------------------  ---------------------------  ---------------------
 *   Anthropic (default)   @langchain/anthropic          yes (default dep)
 *   OpenAI                @langchain/openai             yes (default dep)
 *   Ollama                @langchain/ollama             yes (default dep)
 *   AWS Bedrock           @langchain/aws               install separately
 *   Google Gemini         @langchain/google-genai       install separately
 *
 * ═══════════════════════════════════════════════════════════════════════════
 *
 * To swap providers:
 *   1. Comment out the active model line(s) below.
 *   2. Uncomment the section for your desired provider.
 *   3. Set the provider's env vars in `.env` (see notes inline).
 */

import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

import { config } from "dotenv";
import { Agent, setGlobalDispatcher } from "undici";
import { initChatModel } from "langchain";

// 🟢 ADAPTADO LOCAL: para la opción OpenRouter (API compatible con OpenAI)
import { ChatOpenAI } from "@langchain/openai";

// Force `.env` to win over any same-named variable already exported by the
// shell (default dotenv behavior leaves pre-existing shell vars in place,
// which silently ignores this file's values).
config({ path: join(dirname(fileURLToPath(import.meta.url)), ".env"), override: true });

// Node's default global fetch (undici) connection pool serializes concurrent
// requests once it fills, causing multi-minute client-side queueing when
// several subagents call the same LLM endpoint concurrently (see
// STALL_FIX_REPORT.md). Widen it once here, before any model is constructed,
// so every lesson that imports this file is covered.
setGlobalDispatcher(new Agent({ connections: 64 }));

// ═══ Default Models ══════════════════════════════════════════════════════════
// 🔸 ORIGINAL DEL CURSO: no se corre en este lab.
// Motivo: requiere ANTHROPIC_API_KEY (de pago); aquí usamos Ollama local u OpenRouter gratis.
// Ver el bloque siguiente (🟢 ADAPTADO LOCAL).
//
// Workshop default: Anthropic claude-haiku-4-5, fast and cost-effective.
// Requires ANTHROPIC_API_KEY in .env
// export const model = await initChatModel("anthropic:claude-haiku-4-5", { timeout: 60_000, maxRetries: 2 });
//
// // A more capable model for steps that need stronger reasoning
// export const strongModel = await initChatModel("anthropic:claude-sonnet-4-6", { timeout: 120_000, maxRetries: 2 });

// 🟢 ADAPTADO LOCAL — mismo estilo del curso: initChatModel("proveedor:modelo", { parámetros })
// Motivo: mismo contrato (exporta `model` y `strongModel`), sin API de pago.
// Los labs hacen `import { model } from "../models.js"`: no hay que tocarlos.
//
// 🔀 INTERRUPTOR DE PROVEEDOR (M1.3 Models): se elige en el .env, sin tocar código
//   MODEL_PROVIDER=ollama       → local, gratis, lento en CPU (por defecto)
//   MODEL_PROVIDER=openrouter   → nube, modelos ":free", rápido, necesita OPENROUTER_API_KEY
//   OPENROUTER_MODEL=...        → opcional, otro modelo de OpenRouter
//
// 📚 Por qué los parámetros de Ollama (sin ellos falla en silencio):
//   baseUrl      → Ollama está en otro servidor de la red, no en localhost
//   numCtx       → el system prompt del deep agent ocupa varios miles de tokens; con el contexto
//                  por defecto Ollama lo RECORTA sin avisar y el agente "olvida" sus tools
//   think: false → qwen3/gemma4 "piensan" por defecto: en CPU son minutos extra
// 📚 En TS no se puede declarar `export const model` dos veces (en Python la última línea "gana"):
//    por eso se decide con un ternario  →  condición ? siEsVerdad : siEsFalso
const PROVIDER = (process.env.MODEL_PROVIDER ?? "ollama").toLowerCase();
const OLLAMA = { baseUrl: process.env.OLLAMA_BASE_URL ?? "http://localhost:11434", think: false };
const OPENROUTER_MODEL = process.env.OPENROUTER_MODEL ?? "nvidia/nemotron-3-ultra-550b-a55b:free";

const openRouter = () =>
  new ChatOpenAI({
    model: OPENROUTER_MODEL,
    apiKey: process.env.OPENROUTER_API_KEY,
    timeout: 120_000,
    maxRetries: 2,
    configuration: { baseURL: "https://openrouter.ai/api/v1" },
  });

export const model =
  PROVIDER === "openrouter"
    ? openRouter()
    : await initChatModel("ollama:gemma4:latest", { ...OLLAMA, numCtx: 16384 });   // rápido: hace de haiku

export const strongModel =
  PROVIDER === "openrouter"
    ? model
    : await initChatModel("ollama:qwen3:8b", { ...OLLAMA, numCtx: 32768 });        // "pensador": hace de sonnet

console.log(`[models] proveedor=${PROVIDER} · model=${PROVIDER === "openrouter" ? OPENROUTER_MODEL : "gemma4:latest"}`);

// ═══ Alternative Models (comment out default above, uncomment one below) ═════
// export const model = await initChatModel("anthropic:claude-sonnet-4-6");
// export const model = await initChatModel("openai:gpt-4.1-mini");
// export const model = await initChatModel("openai:gpt-4.1");
// export const strongModel = await initChatModel("openai:gpt-4.1");

// ═══ Open-Source / Alternative Hosted Models ══════════════════════════════════

// Ollama: run models locally (no API key required)
// Install the Ollama app first: https://ollama.com
// Pull a model first, e.g.:  ollama pull qwen2.5:7b
//
// export const model = await initChatModel("ollama:qwen2.5:7b");

// OpenRouter: hosted open-source models via OpenAI-compatible API
// Free models available; sign up at openrouter.ai and get an API key
// Requires OPENROUTER_API_KEY in .env
//
// 🔸 ORIGINAL DEL CURSO (comentado): ahora se activa con MODEL_PROVIDER=openrouter en el .env
// (ver el bloque 🟢 de arriba)
// import { ChatOpenAI } from "@langchain/openai";
// export const model = new ChatOpenAI({
//   model: "nvidia/nemotron-3-ultra-550b-a55b:free",
//   apiKey: process.env.OPENROUTER_API_KEY,
//   configuration: { baseURL: "https://openrouter.ai/api/v1" },
// });

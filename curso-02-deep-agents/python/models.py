"""Model Initialization File

Configures the LLM model used throughout the course.

Default: Anthropic claude-haiku-4-5 (fast, cheap, great for learning).

═══════════════════════════════════════════════════════════════════════════
  ⚠  IMPORTANT: install the matching extra BEFORE swapping providers
═══════════════════════════════════════════════════════════════════════════

  Provider              Install command              Already installed?
  --------------------  ---------------------------  ---------------------
  Anthropic (default)   -                            yes (default dep)
  OpenAI                -                            yes (default dep)
  Azure OpenAI          uv sync --extra azure        no - install first
  AWS Bedrock           uv sync --extra bedrock      no - install first
  Google Vertex/Gemini  uv sync --extra google       no - install first

═══════════════════════════════════════════════════════════════════════════

To swap providers:
  1. Run the install command above (if needed).
  2. Comment out the active model line(s) below.
  3. Uncomment the section for your desired provider.
  4. Set the provider's env vars in `.env` (see notes inline).
"""

import os  # 🟢 se usa en el interruptor de proveedor (MODEL_PROVIDER)
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(dotenv_path=Path(__file__).resolve().parent / ".env", override=True)

from langchain.chat_models import init_chat_model

# ═══ Default Models ══════════════════════════════════════════════════════════
# 🔸 ORIGINAL DEL CURSO — no se corre en este lab.
# Motivo: requiere ANTHROPIC_API_KEY (de pago); aquí usamos Ollama local u OpenRouter gratis.
# Ver el bloque siguiente (🟢 ADAPTADO LOCAL).
#
# Workshop default: Anthropic claude-haiku-4-5, fast and cost-effective.
# Requires ANTHROPIC_API_KEY in .env
# model = init_chat_model("anthropic:claude-haiku-4-5", timeout=60, max_retries=2)
#
# #A more capable model for steps that need stronger reasoning
# strong_model = init_chat_model("anthropic:claude-sonnet-4-6", timeout=120, max_retries=2)

# 🟢 ADAPTADO LOCAL — mismo estilo del curso: init_chat_model("proveedor:modelo", **parámetros)
# Motivo: mismo contrato (exporta `model` y `strong_model`), sin API de pago.
# Los labs hacen `from models import model`: no hay que tocarlos.
#
# 🔀 INTERRUPTOR DE PROVEEDOR (M1.3 Models): se elige en el .env, sin tocar código
#   MODEL_PROVIDER=ollama       → local, gratis, lento en CPU (por defecto)
#   MODEL_PROVIDER=openrouter   → nube, modelos ":free", rápido, necesita OPENROUTER_API_KEY
#   OPENROUTER_MODEL=...        → opcional, otro modelo de OpenRouter
#
# 📚 Por qué los parámetros de Ollama (sin ellos falla en silencio):
#   base_url        → Ollama está en otro servidor de la red, no en localhost
#   num_ctx         → el system prompt del deep agent ocupa varios miles de tokens; con el contexto
#                     por defecto Ollama lo RECORTA sin avisar y el agente "olvida" sus tools
#   reasoning=False → qwen3/gemma4 "piensan" por defecto: en CPU son minutos extra
PROVIDER = os.getenv("MODEL_PROVIDER", "ollama").lower()


def build(provider: str = PROVIDER):
    """Devuelve (model, strong_model) para un proveedor: "ollama" u "openrouter".

    🟢 EXTRA LOCAL: permite que un notebook use otro proveedor que el .env,
    p. ej. `model, strong_model = build("ollama")` para explorar sin gastar el límite de OpenRouter.
    """
    if provider == "openrouter":
        # Igual que la opción OpenRouter del curso: API compatible con OpenAI → ChatOpenAI + base_url
        from langchain_openai import ChatOpenAI

        m = ChatOpenAI(
            model=os.getenv("OPENROUTER_MODEL", "nvidia/nemotron-3-ultra-550b-a55b:free"),
            base_url="https://openrouter.ai/api/v1",
            api_key=os.environ["OPENROUTER_API_KEY"],
            timeout=120,
            max_retries=2,
        )
        return m, m                           # el mismo modelo hace de los dos
    ollama = dict(base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"), reasoning=False)
    return (
        init_chat_model("ollama:gemma4:latest", num_ctx=16384, **ollama),   # rápido: hace de haiku
        init_chat_model("ollama:qwen3:8b", num_ctx=32768, **ollama),        # "pensador": hace de sonnet
    )


model, strong_model = build(PROVIDER)

print(f"[models] proveedor={PROVIDER} · model={getattr(model, 'model', None) or getattr(model, 'model_name', None)}")

# ═══ Alternative Models (comment out default above, uncomment one below) ═════
# model = init_chat_model("anthropic:claude-sonnet-4-6")
# model = init_chat_model("openai:gpt-4.1-mini")
# model = init_chat_model("openai:gpt-4.1")
# strong_model = init_chat_model("openai:gpt-4.1")

# ═══ Open-Source / Alternative Hosted Models ══════════════════════════════════

# Groq: fast hosted inference for Llama, Mixtral, and others (free tier available)
# Install first:  uv add langchain-groq
# Requires GROQ_API_KEY in .env  (get one at console.groq.com)
#
# model = init_chat_model("groq:llama-3.3-70b-versatile")

# Ollama: run models locally (no API key required)
# langchain-ollama is already installed (default dep)
# Install the Ollama app first: https://ollama.com
# Pull a model first, e.g.:  ollama pull qwen2.5:7b
#
# model = init_chat_model("ollama:qwen2.5:7b")

# Kimi (Moonshot AI): OpenAI-compatible hosted API
# No extra install needed (langchain-openai is already a default dep)
# Requires KIMI_API_KEY in .env  (get one at platform.moonshot.cn)
#
# from langchain_openai import ChatOpenAI
# model = ChatOpenAI(model="moonshot-v1-8k", base_url="https://api.moonshot.cn/v1", api_key=os.environ["KIMI_API_KEY"])

# OpenRouter: hosted open-source models via OpenAI-compatible API
# No extra install needed (langchain-openai is already a default dep)
# Free models available; sign up at openrouter.ai and get an API key
# Requires OPENROUTER_API_KEY in .env
#
# 🔸 ORIGINAL DEL CURSO (comentado): ahora se activa con MODEL_PROVIDER=openrouter en el .env
# (ver el bloque 🟢 de arriba)
# from langchain_openai import ChatOpenAI
# model = ChatOpenAI(model="nvidia/nemotron-3-ultra-550b-a55b:free", base_url="https://openrouter.ai/api/v1", api_key=os.environ["OPENROUTER_API_KEY"])


# ═══ Cloud Provider Models (extra install required, see table above) ═════════
# ─── Azure OpenAI ─────────────────────────────────────────────────────────────
# Install first:  uv sync --extra azure
# Requires AZURE_OPENAI_API_KEY, AZURE_OPENAI_ENDPOINT, OPENAI_API_VERSION in .env
# Set your deployment name directly below (it isn't read from .env)
#
# from langchain_openai import AzureChatOpenAI
# model = AzureChatOpenAI(azure_deployment="gpt-4.1", api_version="2024-12-01-preview")


# ─── AWS Bedrock ──────────────────────────────────────────────────────────────
# Install first:  uv sync --extra bedrock
# Requires AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY in .env
# Set your region directly below (it isn't read from .env)
#
# from langchain_aws import ChatBedrockConverse
# model = ChatBedrockConverse(model_id="anthropic.claude-sonnet-4-6", region_name="us-east-1")


# ─── Google Gemini ────────────────────────────────────────────────────────────
# Install first:  uv sync --extra google
# Requires GOOGLE_API_KEY in .env
#
# model = init_chat_model("google_genai:gemini-2.5-flash")

"""Email Agent (Módulo 3, proyecto) servido con `langgraph dev`.

🟢 ADAPTADO LOCAL — cambios respecto al curso (ver comentarios 🔸/🟢 abajo):
  - "gpt-5-nano" (API de pago) → get_model("gemma4:latest") desde local_model.py (raíz del repo).
  - Sin checkpointer: LangGraph Server maneja la persistencia (igual que en el curso).

Uso (desde esta carpeta):
    uv run langgraph dev
Luego: Studio (https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:2024)
o Agent Chat UI (agent-chat-ui/, http://localhost:3000, assistant "agent").
"""
import sys
import pathlib
from dotenv import load_dotenv
from dataclasses import dataclass
from langchain.agents import AgentState, create_agent
from langchain.tools import tool, ToolRuntime
from langgraph.types import Command
from langchain.messages import ToolMessage
from langchain.agents.middleware import wrap_model_call, dynamic_prompt, HumanInTheLoopMiddleware
from langchain.agents.middleware import ModelRequest, ModelResponse
from typing import Callable

load_dotenv()

# 🟢 ADAPTADO LOCAL: local_model.py vive en la raíz del repo
_here = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(next(p for p in [_here, *_here.parents] if (p / "local_model.py").exists())))
from local_model import get_model  # noqa: E402


@dataclass
class EmailContext:
    email_address: str = "julie@example.com"
    password: str = "password123"


class AuthenticatedState(AgentState):
    authenticated: bool


@tool
def check_inbox() -> str:
    """Check the inbox for recent emails"""
    return """
    Hi Julie, 
    I'm going to be in town next week and was wondering if we could grab a coffee?
    - best, Jane (jane@example.com)
    """


@tool
def send_email(to: str, subject: str, body: str) -> str:
    """Send an response email"""
    return f"Email sent to {to} with subject {subject} and body {body}"


@tool
def authenticate(email: str, password: str, runtime: ToolRuntime) -> Command:
    """Authenticate the user with the given email and password"""
    if email == runtime.context.email_address and password == runtime.context.password:
        return Command(
            update={
                "authenticated": True,
                "messages": [
                    ToolMessage("Successfully authenticated", tool_call_id=runtime.tool_call_id)
                ],
            }
        )
    else:
        return Command(
            update={
                "authenticated": False,
                "messages": [
                    ToolMessage("Authentication failed", tool_call_id=runtime.tool_call_id)
                ],
            }
        )


@wrap_model_call
async def dynamic_tool_call(
    request: ModelRequest, handler: Callable[[ModelRequest], ModelResponse]
) -> ModelResponse:
    """Allow read inbox and send email tools only if user provides correct email and password"""

    authenticated = request.state.get("authenticated")

    if authenticated:
        tools = [check_inbox, send_email]
    else:
        tools = [authenticate]

    request = request.override(tools=tools)
    return await handler(request)


authenticated_prompt = "You are a helpful assistant that can check the inbox and send emails."
unauthenticated_prompt = "You are a helpful assistant that can authenticate users."


@dynamic_prompt
def dynamic_prompt_func(request: ModelRequest) -> str:
    """Generate system prompt based on authentication status"""
    authenticated = request.state.get("authenticated")

    if authenticated:
        return authenticated_prompt
    else:
        return unauthenticated_prompt


# 🔸 ORIGINAL DEL CURSO: agent = create_agent("gpt-5-nano", ...)  → API de pago
# 🟢 ADAPTADO LOCAL: gemma4 en Ollama
agent = create_agent(
        get_model("gemma4:latest"),
        tools=[authenticate, check_inbox, send_email],
        state_schema=AuthenticatedState,
        context_schema=EmailContext,
        middleware=[
            dynamic_tool_call,
            dynamic_prompt_func,
            HumanInTheLoopMiddleware(
                interrupt_on={
                    "authenticate": False,
                    "check_inbox": False,
                    "send_email": True,
                }
            ),
        ],
    )

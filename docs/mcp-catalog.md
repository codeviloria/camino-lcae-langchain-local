# Catálogo de servidores MCP

Ficha de cada servidor MCP que uso en el curso y en mis proyectos: qué hace, cómo se conecta y **qué tools, resources y prompts expone**.

> **Cómo listar lo que expone cualquier servidor** (así se llenan estas fichas):
> ```python
> tools = await client.get_tools()
> for t in tools:
>     print(f"- {t.name}: {(t.description or '').splitlines()[0][:120]}")
>     print("    args:", list(t.args.keys()))
> resources = await client.get_resources("<server>")   # si expone resources
> ```

## Resumen
| Servidor | Tipo | Transporte | Tools | Resources | Prompts | Auth | Lección |
|---|---|---|---|---|---|---|---|
| `local_server` (`2.1_mcp_server.py`) | Propio (FastMCP) | `stdio` | 1 | 1 | 1 | Tavily key en `.env` | [M2.1 MCP](module-2/M2.1-mcp.md) |
| `mcp_server_time` | Terceros, local (PyPI) | `stdio` | 2 | 0 | 0 | Ninguna | [M2.1 MCP](module-2/M2.1-mcp.md) |
| Kiwi.com (`https://mcp.kiwi.com`) | Terceros, **remoto** | `streamable_http` | 2 | — | — | Ninguna | M2.1b Travel Agent |

---

## 1. `local_server` — servidor propio del curso
- **Archivo:** `notebooks/module-2/resources/2.1_mcp_server.py`
- **Construido con:** `FastMCP` del SDK oficial de MCP (no LangChain).
- **Conexión:**
```python
"local_server": {"transport": "stdio", "command": sys.executable, "args": ["resources/2.1_mcp_server.py"]}
```
| Tipo | Nombre | Parámetros | Qué hace |
|---|---|---|---|
| Tool | `search_web` | `query: str` | Busca en la web con Tavily y devuelve el dict completo (5 resultados) |
| Resource | `github://langchain-ai/langchain-mcp-adapters/main/README.md` (`github_file`) | — | Descarga el README de `langchain-mcp-adapters` desde GitHub |
| Prompt | `prompt` | — | System prompt de asistente experto en LangChain/LangGraph/LangSmith que rechaza otros temas |

- **Notas:** el prompt menciona `github_file` como si fuera una tool, pero es un resource. Devuelve resultados de Tavily sin recortar (≈2.000 tokens), lo que es lento en CPU. Mejora: `max_results=3`.

## 2. `mcp_server_time` — hora y zonas horarias
- **Paquete:** `mcp-server-time` (servidores de referencia del ecosistema MCP). Ya está en el `.venv`.
- **Conexión:**
```python
"time": {"transport": "stdio", "command": sys.executable,
         "args": ["-m", "mcp_server_time", "--local-timezone=America/Bogota"]}
```
- **Opción CLI:** `--local-timezone` cambia la zona horaria detectada del sistema.

| Tool | Parámetros (todos obligatorios) | Devuelve |
|---|---|---|
| `get_current_time` | `timezone: str` (IANA, ej. `America/Bogota`) | Zona, fecha y hora en ISO, y si está en horario de verano |
| `convert_time` | `source_timezone: str`, `time: str` (`HH:MM`, 24 h), `target_timezone: str` | Hora en ambas zonas y la diferencia |

- **Notas:** `timezone` es obligatorio. Si la pregunta no la dice ("What time is it?"), el modelo puede preguntar en vez de llamar la tool. Conviene preguntar "What time is it in America/Bogota?".

## 3. Kiwi.com — búsqueda de vuelos (remoto)
- **URL:** `https://mcp.kiwi.com`, sin API key.
- **Conexión:**
```python
"travel_server": {"transport": "streamable_http", "url": "https://mcp.kiwi.com"}
```
- **Tools listadas en mi lab (2026-10-04):**

| Tool | Qué hace |
|---|---|
| `search-flight` | Busca vuelos y devuelve una lista corta de "mejores opciones" con enlace de reserva en Kiwi.com |
| `feedback-to-devs` | Envía texto (feedback, bugs, pedidos) **a los desarrolladores de Kiwi**. Único arg: `text` |

**`search-flight`: 47 argumentos** agrupados:
| Grupo | Argumentos |
|---|---|
| Ruta y fechas | `flyFrom`, `flyTo`, `departureDate`, `departureDateFlexDays`, `departureDateTo`, `returnDate`, `returnDateFlexDays`, `returnDateTo` |
| Pasajeros y cabina | `adults`, `children`, `infants`, `cabinClass` |
| Formato | `currency`, `locale`, `sort`, `one_for_city` |
| Estancia | `nights_in_dst_from`, `nights_in_dst_to` |
| Precio y duración | `price_from`, `price_to`, `max_fly_duration` |
| Escalas | `max_sector_stopovers`, `stopover_from`, `stopover_to`, `stopover_airports`, `exclude_stopover_airports`, `stopover_countries`, `exclude_stopover_countries`, `allow_self_transfer`, `allow_overnight_stopovers`, `allow_diff_airport_connection` |
| Aerolíneas | `select_airlines`, `exclude_airlines` |
| Horarios ida / vuelta | `dtime_from`, `dtime_to`, `atime_from`, `atime_to`, `ret_dtime_from`, `ret_dtime_to`, `ret_atime_from`, `ret_atime_to`, `fly_days`, `ret_fly_days` |
| Equipaje | `adults_hold_bags`, `adults_hand_bags`, `children_hold_bags`, `children_hand_bags` |

- **Diseño del servidor** (según Kiwi): de los miles de vuelos que trae su API, devuelve solo unas decenas de "mejores" opciones, en tabla y con enlaces de reserva acortados para gastar menos tokens. Es buen ejemplo de **context engineering del lado del servidor**.
- **Notas para mi lab:**
  - **Tamaño de respuesta (medido):** una búsqueda BAQ→BOG devolvió 15 itinerarios; la llamada siguiente al modelo leyó **9.866 tokens** → requiere `num_ctx` ≥ 16–32K. Ver [M2.1b Travel Agent](module-2/M2.1b-travel-agent.md).
  - Los **47 argumentos entran en el prompt** como esquema de la tool, así que hay más tokens de entrada antes de empezar, lo que en CPU suma latencia.
  - ⚠️ **`feedback-to-devs` envía texto a un tercero.** Un agente con esta tool podría mandar parte de la conversación a Kiwi. En producción conviene **filtrar las tools** y pasar solo `search-flight`:
    ```python
    tools = [t for t in await client.get_tools() if t.name == "search-flight"]
    ```
  - La documentación pública de Kiwi habla de "una sola tool"; el listado real mostró dos. **Lo que vale es listar las tools en vivo**, no confiar en la doc.

---

## Plantilla para nuevos servidores
```markdown
## N. <nombre>
- **Qué es / quién lo mantiene:**
- **Conexión:** `{"transport": "...", ...}`
- **Auth:**
| Tipo | Nombre | Parámetros | Qué hace |
|---|---|---|---|
- **Notas (latencia, seguridad, trampas):**
- **Lección:** ...
```

## Enlaces
- [M2.1 MCP](module-2/M2.1-mcp.md) · M2.1b Travel Agent · 00 Glosario
- Kiwi MCP: https://www.kiwi.com/en/pages/mcp/ · Diseño: https://dev.to/alpic/behind-the-kiwicom-mcp-server-building-an-agentic-flight-booking-service-2pdd
- mcp-server-time: https://pypi.org/project/mcp-server-time/

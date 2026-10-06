# Guía de inicio en Windows (estudiante)

Para hacer el curso *Introduction to LangChain (Python)* con este repo en un **PC con Windows**:
- los modelos corren en un **servidor Ollama compartido** en la red de la casa;
- el tutor es **OpenCode** con un modelo gratuito.

Tiempo estimado de instalación: 30 a 45 minutos.

---

## 1 · Instalar las herramientas

Abre **PowerShell** (botón Inicio → escribe "PowerShell") y corre una línea a la vez:

```
winget install --id Git.Git -e
winget install --id astral-sh.uv -e
winget install --id OpenJS.NodeJS.LTS -e
```

Cierra PowerShell y ábrelo de nuevo para que reconozca los programas. Comprueba que estén instalados:

```
git --version
uv --version
node --version
```

## 2 · Descargar el repo

```
cd $HOME\Documents
git clone https://github.com/codeviloria/camino-lcae-langchain-local.git
cd camino-lcae-langchain-local
uv sync
```

`uv sync` instala Python y todas las librerías del curso. La primera vez tarda unos minutos.

## 3 · Crear tu `.env` (tus llaves)

```
copy .env.example .env
notepad .env
```

Llena estos valores y guarda:

| Variable | Qué poner |
|---|---|
| `OLLAMA_BASE_URL` | `http://<ip-del-servidor>:11434`. Pide la IP a quien administra el servidor |
| `OLLAMA_HOST` | La misma dirección |
| `TAVILY_API_KEY` | Tu llave gratis de tavily.com |
| `LANGSMITH_API_KEY` | Tu llave gratis de smith.langchain.com → Settings → API Keys |
| `LANGSMITH_PROJECT` | Un nombre tuyo, por ejemplo `lca-intro-estudiante` |

> 🔒 **Las llaves son como contraseñas.** No las pegues en chats ni en notebooks, y no las subas a internet. El archivo `.env` ya está protegido para que git no lo suba.

Sin espacios alrededor del `=` y sin comillas, por ejemplo: `LANGSMITH_PROJECT=lca-intro-estudiante`.

## 4 · Probar la conexión con el servidor

```
uv run python -c "from dotenv import load_dotenv; load_dotenv(); from local_model import get_model; print(get_model().invoke('di hola en 3 palabras').content)"
```

Si responde un saludo, todo funciona ✅. Si da `ConnectionError`, revisa la IP en `.env` y que el servidor esté encendido.

## 5 · El servidor es compartido: reglas de turno 🚦

El servidor Ollama solo tiene CPU: si dos personas lo usan a la vez, **todo va lentísimo** para las dos.

- Antes de empezar, la primera celda de cada notebook muestra el **semáforo**:
  - 🟢 libre;
  - 🟡 hay un modelo cargado;
  - 🔴 sin conexión.
- Ollama deja el modelo cargado unos **5 minutos** después de usarlo. Si sale 🟡 y fuiste tú, sigue tranquila.
- Si sale 🟡 y no fuiste tú, avisa por el chat de la casa y espera tu turno.

## 6 · Abrir los notebooks

```
uv run jupyter lab
```

Se abre el navegador. Ve a `notebooks/module-1-guiado/` y empieza por `M1.1_modelos_y_agentes.ipynb`. Corre las celdas **en orden** con `Shift + Enter`.

## 7 · El tutor: OpenCode

Instálalo una sola vez:

```
npm install -g opencode-ai
```

Ábrelo **dentro de la carpeta del repo**, en otra ventana de PowerShell:

```
cd $HOME\Documents\camino-lcae-langchain-local
opencode
```

- Escribe `/models` y elige un modelo **gratuito** de la lista. Para el tutor conviene uno en la nube: el servidor Ollama queda libre para los notebooks.
- Luego escribe: **"Quiero estudiar el módulo 1. Usa la skill tutor-lca-intro."**

El tutor está en `.agents/skills/tutor-lca-intro/`. Explica en español, hace preguntas y da **pistas**, pero no resuelve los ejercicios por ti: ese es el trato 😉.

## 8 · El certificado 🎓

El certificado lo entrega **LangChain Academy** (academy.langchain.com):

1. Crea tu cuenta y busca el curso **Introduction to LangChain (Python)**. Revisa en los términos si piden una edad mínima.
2. Ve las lecciones y completa los quizzes **en la plataforma**.
3. Usa este repo para practicar cada lección con modelos locales.

Ritmo sugerido: **un notebook por sesión**, en este orden:
1. ver el video en la Academy;
2. hacer el notebook guiado con el tutor;
3. completar el quiz en la Academy.

## Problemas frecuentes

| Síntoma | Causa probable | Solución |
|---|---|---|
| `uv` no se reconoce | PowerShell no se reinició | Ciérralo y ábrelo de nuevo |
| 🔴 en el semáforo | IP mal escrita o servidor apagado | Revisa `OLLAMA_BASE_URL` en `.env` |
| Tarda varios minutos | CPU, o alguien más está usando el servidor | Normal hasta 3 min; si es más, mira el semáforo |
| `does not support tools` | Ese modelo no sabe usar tools | Usa `get_model()` (qwen3:8b) o `gemma4:latest` |
| Tavily da error | Falta la llave | Revisa `TAVILY_API_KEY` en `.env` |
| Una celda muestra algo raro | Celdas corridas fuera de orden | Kernel → Restart, y córrelas en orden |

# Módulo 1 guiado: aprende agentes paso a paso

Versión **para aprender** del módulo 1 del curso *Introduction to LangChain (Python)* de LangChain Academy:

- explicaciones sencillas en español, con analogías;
- mnemotecnias;
- ejercicios "✍️ Tu turno";
- mini quizzes con las respuestas escondidas.

Todo corre con modelos **locales y gratis** (Ollama).

> Los notebooks de `../module-1/` son el laboratorio original adaptado (con experimentos y pruebas). Estos son la versión limpia para estudiar.

## Orden

| # | Notebook | Lección oficial | Idea clave |
|---|---|---|---|
| 1 | `M1.1_modelos_y_agentes.ipynb` | Foundational models | Modelo = chef; agente = chef con cocina |
| 2 | `M1.2_prompting.ipynb` | Prompting | System prompt = guion del actor (R-E-F) |
| 3 | `M1.3_tools.ipynb` | Tools | Tool = calculadora; el modelo la pide (N-D-A, P-P-R-R) |
| 4 | `M1.4_busqueda_web.ipynb` | Web search | Abrirle la ventana al estudiante encerrado |
| 5 | `M1.5_memoria.ipynb` | Memory | Checkpointer = libreta; thread_id = página |
| 6 | `M1.6_multimodal.ipynb` | Multimodal messages | Carta con fotos adjuntas |
| 7 | `M1.7_chef_personal.ipynb` | Personal chef (proyecto) | Agente = M-P-T-M |

## Antes de empezar
1. Sigue la [guía de instalación en Windows](../../docs/guia-estudiante-windows.md).
2. Abre Jupyter desde la raíz del repo: `uv run jupyter lab`.
3. Corre las celdas **en orden**. La primera revisa el **semáforo** del servidor Ollama, que es compartido.

## Convención de celdas
- 🔸 **ORIGINAL DEL CURSO**: el código de la lección oficial, comentado (usa APIs de pago).
- 🟢 **ADAPTADO LOCAL**: la versión que corres, con Ollama.

## Tutor
En OpenCode, dentro de la carpeta del repo, escribe:

> Quiero estudiar el módulo 1. Usa la skill tutor-lca-intro.

El tutor explica, hace preguntas y da **pistas**, pero no resuelve los ejercicios por ti.

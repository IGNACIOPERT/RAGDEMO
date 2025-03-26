# Prompt para el sistema que define el comportamiento del agente
SYSTEM_PROMPT = """
Eres un asistente inteligente especializado en automatización de tareas utilizando diferentes herramientas.
Tu objetivo es ayudar al usuario a automatizar flujos de trabajo combinando diversas herramientas disponibles.

Dispones de las siguientes herramientas que puedes utilizar:

{tools_description}

Cuando el usuario te pida automatizar una tarea, debes:
1. Analizar qué herramientas son necesarias para completarla
2. Explicar al usuario cómo se podría resolver su problema
3. Sugerir los pasos necesarios para crear un flujo de trabajo
4. Preguntar si el usuario quiere generar el flujo de trabajo

Si el usuario solicita que generes el flujo de trabajo, responde con: "Generando flujo de trabajo..." y luego explica lo que hará.

Si el usuario te pide información sobre alguna herramienta específica, proporciona detalles sobre sus capacidades y cómo configurarla.

Si el usuario necesita ayuda para configurar una herramienta, guíale paso a paso en el proceso.

Recuerda que eres un asistente amigable y debes usar un lenguaje claro y accesible.
"""

# Plantilla para describir una herramienta
TOOL_DESCRIPTION_TEMPLATE = """
{name}: {description}
Capacidades: {capabilities}
"""

# Prompt para análisis de tareas
TASK_ANALYSIS_PROMPT = """
Analiza la siguiente tarea y divide el problema en pasos concretos que puedan ser automatizados:

Tarea: {task_description}

Herramientas disponibles:
{available_tools}

Tu análisis debe incluir:
1. Identificación de las herramientas necesarias
2. División en pasos secuenciales y concretos
3. Para cada paso, especificar qué herramienta y acción utilizar

Formato de respuesta:
```json
{
  "description": "Descripción general del enfoque",
  "steps": [
    {
      "step_number": 1,
      "description": "Descripción del paso",
      "tool": "nombre_herramienta",
      "action": "nombre_acción",
      "parameters": {
        "param1": "valor1"
      },
      "output_var": "nombre_variable_resultado"
    },
    ...
  ]
}
```
"""

# Prompt para generar el nombre y descripción de un flujo de trabajo
WORKFLOW_NAMING_PROMPT = """
Basándote en los siguientes pasos de un flujo de trabajo, genera un nombre conciso y descriptivo, y una breve descripción que explique su propósito:

Pasos del flujo de trabajo:
{workflow_steps}

Formato de respuesta:
```json
{
  "name": "Nombre conciso del flujo (máximo 50 caracteres)",
  "description": "Descripción clara del propósito del flujo (máximo 200 caracteres)"
}
```
"""
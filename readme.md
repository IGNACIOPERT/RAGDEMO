rag-modular/
├── app.py # Aplicación Flask principal
├── config.py # Configuraciones del sistema
├── requirements.txt # Dependencias del proyecto
├── README.md # Documentación
│
├── static/ # Archivos estáticos
│ ├── css/
│ │ └── main.css # Estilos principales
│ ├── js/
│ │ ├── main.js # Scripts principales
│ │ ├── chat-interface.js # Interfaz de chat
│ │ └── flow-visualizer.js # Visualizador de flujos
│ └── img/ # Imágenes
│
├── templates/ # Plantillas HTML
│ ├── base.html # Plantilla base
│ ├── index.html # Página principal con chat
│ ├── modules.html # Configuración de módulos
│ └── workflows.html # Gestión de flujos guardados
│
├── agent/ # Agente principal
│ ├── **init**.py
│ ├── chat_agent.py # Agente de chat basado en GPT
│ └── prompt_templates.py # Plantillas para instrucciones a GPT
│
├── core/ # Núcleo del sistema
│ ├── **init**.py
│ ├── module_registry.py # Registro de módulos
│ ├── orchestrator.py # Orquestador de herramientas
│ ├── flow_generator.py # Generador de flujos de trabajo
│ └── executor.py # Motor de ejecución
│
├── modules/ # Módulos de herramientas
│ ├── **init**.py
│ ├── base_module.py # Clase base para módulos
│ ├── gmail_module.py # Módulo para Gmail
│ ├── whatsapp_module.py # Módulo para WhatsApp
│ ├── excel_module.py # Módulo para Excel
│ ├── vector_db_module.py # Módulo para BD vectorial
│ ├── chatgpt_module.py # Módulo para ChatGPT
│ └── embedding_module.py # Módulo para embeddings
│
└── data/ # Almacenamiento de datos
├── module_configs/ # Configuraciones de módulos
├── workflows/ # Flujos de trabajo guardados
└── user_data/ # Datos específicos del usuario

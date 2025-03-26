"""
Paquete central (core) del sistema RAG Modular.
Este módulo contiene los componentes principales del sistema, incluyendo:
- Registro de módulos
- Orquestador de herramientas
- Generador de flujos de trabajo
- Motor de ejecución
"""

from .module_registry import ModuleRegistry
from .orchestrator import Orchestrator
from .flow_generator import FlowGenerator
from .executor import Executor

__all__ = [
    'ModuleRegistry',
    'Orchestrator',
    'FlowGenerator',
    'Executor'
]
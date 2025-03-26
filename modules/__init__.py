import os
import importlib
import sys
from pathlib import Path

# Añadir directorio raíz al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

def get_module_class(module_type):
    """
    Obtiene la clase del módulo dado su tipo.
    
    Args:
        module_type (str): Tipo de módulo (ej: 'gmail', 'whatsapp')
        
    Returns:
        class: Clase del módulo o None si no existe
    """
    try:
        # Convertir el tipo de módulo a un nombre de clase
        # Ejemplo: 'gmail' -> 'GmailModule'
        class_name = module_type.capitalize() + "Module"
        
        # Importar el módulo dinámicamente
        module = importlib.import_module(f"modules.{module_type}_module")
        
        # Obtener la clase del módulo
        module_class = getattr(module, class_name)
        return module_class
    except (ImportError, AttributeError) as e:
        print(f"Error al cargar el módulo {module_type}: {e}")
        return None

def load_all_modules():
    """
    Carga todos los módulos disponibles.
    
    Returns:
        dict: Diccionario con instancias de todos los módulos disponibles
    """
    modules = {}
    for module_type in config.AVAILABLE_MODULES:
        module_class = get_module_class(module_type)
        if module_class:
            modules[module_type] = module_class()
    return modules

def get_module_by_type(module_type):
    """
    Obtiene una instancia de un módulo dado su tipo.
    
    Args:
        module_type (str): Tipo de módulo (ej: 'gmail', 'whatsapp')
        
    Returns:
        BaseModule: Instancia del módulo o None si no existe
    """
    module_class = get_module_class(module_type)
    if module_class:
        return module_class()
    return None

def discover_modules():
    """
    Descubre automáticamente todos los módulos disponibles en el directorio.
    
    Returns:
        list: Lista de tipos de módulos disponibles
    """
    module_types = []
    module_dir = Path(__file__).parent
    for file in module_dir.glob("*_module.py"):
        module_type = file.stem.replace("_module", "")
        if module_type != "base":
            module_types.append(module_type)
    return module_types
import os
import json
from pathlib import Path
import sys

# Añadir directorio raíz al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config
from modules import get_module_by_type, discover_modules

class ModuleRegistry:
    """
    Registro de módulos que gestiona la disponibilidad y configuración de módulos.
    """
    
    def __init__(self, config_dir=None):
        """
        Inicializa el registro de módulos.
        
        Args:
            config_dir (str, optional): Directorio donde se almacenan las configuraciones
        """
        self.config_dir = Path(config_dir) if config_dir else Path(config.MODULE_CONFIGS_DIR)
        self.modules = {}  # Instancias de módulos
        self.available_modules = []  # Tipos de módulos disponibles
        
        # Crear directorio de configuración si no existe
        self.config_dir.mkdir(parents=True, exist_ok=True)
        
        # Descubrir módulos disponibles
        self.discover_modules()
    
    def discover_modules(self):
        """
        Descubre los módulos disponibles y los carga.
        """
        # Obtener todos los tipos de módulo disponibles
        self.available_modules = discover_modules()
        
        # Inicializar módulos configurados
        for module_type in self.available_modules:
            config_file = self.config_dir / f"{module_type}.json"
            if config_file.exists():
                # El módulo está configurado, cargar instancia
                module = get_module_by_type(module_type)
                if module and module.is_configured:
                    self.modules[module_type] = module
    
    def get_available_modules(self):
        """
        Obtiene los tipos de módulos disponibles.
        
        Returns:
            list: Lista de tipos de módulos
        """
        return self.available_modules
    
    def get_configured_modules(self):
        """
        Obtiene los módulos que están configurados y listos para usar.
        
        Returns:
            dict: Diccionario con módulos configurados
        """
        return self.modules
    
    def get_module(self, module_type):
        """
        Obtiene un módulo específico.
        
        Args:
            module_type (str): Tipo de módulo
            
        Returns:
            BaseModule: Instancia del módulo o None si no existe o no está configurado
        """
        if module_type in self.modules:
            return self.modules[module_type]
        
        # Si el módulo no está en memoria pero está disponible, intentar cargarlo
        if module_type in self.available_modules:
            module = get_module_by_type(module_type)
            if module and module.is_configured:
                self.modules[module_type] = module
                return module
        
        return None
    
    def configure_module(self, module_type, config_data):
        """
        Configura un módulo.
        
        Args:
            module_type (str): Tipo de módulo
            config_data (dict): Datos de configuración
            
        Returns:
            bool: True si se configuró correctamente, False en caso contrario
        """
        if module_type not in self.available_modules:
            return False
        
        # Obtener o crear el módulo
        module = self.get_module(module_type)
        if not module:
            module = get_module_by_type(module_type)
            if not module:
                return False
        
        # Configurar el módulo
        success = module.save_config(config_data)
        if success:
            self.modules[module_type] = module
        
        return success
    
    def get_module_capabilities(self, module_type=None):
        """
        Obtiene las capacidades de un módulo o de todos los módulos configurados.
        
        Args:
            module_type (str, optional): Tipo de módulo específico
            
        Returns:
            dict: Diccionario con capacidades de los módulos
        """
        capabilities = {}
        
        if module_type:
            # Obtener capacidades de un módulo específico
            module = self.get_module(module_type)
            if module:
                capabilities[module_type] = module.get_capabilities()
        else:
            # Obtener capacidades de todos los módulos configurados
            for module_type, module in self.modules.items():
                capabilities[module_type] = module.get_capabilities()
        
        return capabilities
    
    def execute_module_action(self, module_type, action, params=None):
        """
        Ejecuta una acción en un módulo.
        
        Args:
            module_type (str): Tipo de módulo
            action (str): Nombre de la acción
            params (dict, optional): Parámetros para la acción
            
        Returns:
            dict: Resultado de la acción
        """
        module = self.get_module(module_type)
        if not module:
            return {"success": False, "error": f"Módulo '{module_type}' no disponible o no configurado"}
        
        return module.execute_action(action, params)
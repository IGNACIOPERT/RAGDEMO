from abc import ABC, abstractmethod
import json
from pathlib import Path
import sys
import os

# Añadir directorio raíz al path para importar config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

class BaseModule(ABC):
    """
    Clase base para todos los módulos del sistema.
    Define la interfaz común y la funcionalidad básica que todos los módulos deben implementar.
    """
    
    def __init__(self, module_type):
        """
        Inicializa un nuevo módulo.
        
        Args:
            module_type (str): Tipo de módulo (ej: 'gmail', 'whatsapp')
        """
        self.module_type = module_type
        self.config_file = Path(config.MODULE_CONFIGS_DIR) / f"{module_type}.json"
        self.is_configured = False
        self.config = {}
        
        # Cargar configuración si existe
        self.load_config()
    
    def load_config(self):
        """Carga la configuración del módulo desde el archivo JSON."""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    self.config = json.load(f)
                self.is_configured = self._validate_config()
            except Exception as e:
                print(f"Error al cargar configuración para {self.module_type}: {e}")
        return self.is_configured
    
    def save_config(self, config_data):
        """
        Guarda la configuración del módulo en un archivo JSON.
        
        Args:
            config_data (dict): Datos de configuración a guardar
            
        Returns:
            bool: True si se guardó correctamente, False en caso contrario
        """
        try:
            # Actualizar la configuración
            self.config = config_data
            
            # Asegurar que el directorio existe
            self.config_file.parent.mkdir(parents=True, exist_ok=True)
            
            # Guardar la configuración
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=4)
            
            # Validar la configuración guardada
            self.is_configured = self._validate_config()
            return self.is_configured
        except Exception as e:
            print(f"Error al guardar configuración para {self.module_type}: {e}")
            return False
    
    def _validate_config(self):
        """
        Valida que la configuración tenga todos los campos requeridos.
        
        Returns:
            bool: True si la configuración es válida, False en caso contrario
        """
        if self.module_type not in config.MODULE_CONFIGS:
            return False
        
        required_fields = config.MODULE_CONFIGS[self.module_type]['required_fields']
        for field in required_fields:
            if field not in self.config or not self.config[field]:
                return False
        return True
    
    def get_capabilities(self):
        """
        Devuelve una lista de capacidades que este módulo proporciona.
        
        Returns:
            list: Lista de strings describiendo las capacidades
        """
        return self._get_capabilities()
    
    def get_config_schema(self):
        """
        Devuelve el esquema de configuración para este módulo.
        
        Returns:
            dict: Diccionario con campos requeridos y opcionales
        """
        if self.module_type in config.MODULE_CONFIGS:
            return config.MODULE_CONFIGS[self.module_type]
        return {"required_fields": [], "optional_fields": []}
    
    def execute_action(self, action, params=None):
        """
        Ejecuta una acción específica del módulo.
        
        Args:
            action (str): Nombre de la acción a ejecutar
            params (dict, optional): Parámetros para la acción
            
        Returns:
            dict: Resultado de la acción
        """
        if not self.is_configured:
            return {"success": False, "error": "Módulo no configurado"}
        
        if not params:
            params = {}
        
        try:
            # Verificar si el método de acción existe
            if hasattr(self, action) and callable(getattr(self, action)):
                result = getattr(self, action)(**params)
                return {"success": True, "result": result}
            else:
                return {"success": False, "error": f"Acción '{action}' no disponible"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @abstractmethod
    def _get_capabilities(self):
        """
        Método abstracto que debe ser implementado por cada módulo.
        Devuelve una lista de capacidades del módulo.
        """
        pass
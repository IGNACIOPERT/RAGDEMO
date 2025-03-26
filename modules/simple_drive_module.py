from modules.base_module import BaseModule

class DriveModule(BaseModule):
    """Módulo simplificado para Google Drive."""
    
    def __init__(self):
        """Inicializa el módulo."""
        super().__init__("drive")
    
    def _get_capabilities(self):
        """Devuelve las capacidades del módulo."""
        return ["list_files", "download_file"]
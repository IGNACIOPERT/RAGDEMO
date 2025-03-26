from pathlib import Path
import os
import json
import requests
import io
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google.oauth2.credentials import Credentials
import sys

# Añadir directorio raíz al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from modules.base_module import BaseModule

class DriveModule(BaseModule):
    """Módulo para interactuar con Google Drive."""
    
    def __init__(self):
        """Inicializa el módulo de Google Drive."""
        super().__init__("drive")
        self.service = None
    
    def _get_capabilities(self):
        """
        Devuelve las capacidades del módulo de Google Drive.
        
        Returns:
            list: Lista de capacidades
        """
        return [
            "list_files",
            "download_file",
            "get_file_by_name",
            "upload_file"
        ]
    
    def _initialize_service(self):
        """
        Inicializa el servicio de Google Drive.
        
        Returns:
            bool: True si se inicializó correctamente, False en caso contrario
        """
        if self.service:
            return True
            
        try:
            # Usar las credenciales almacenadas en la configuración
            credentials = Credentials.from_authorized_user_info({
                "token": self.config.get("access_token"),
                "refresh_token": self.config.get("refresh_token"),
                "client_id": self.config.get("client_id"),
                "client_secret": self.config.get("client_secret"),
                "token_uri": "https://oauth2.googleapis.com/token"
            })
            
            # Construir el servicio
            self.service = build('drive', 'v3', credentials=credentials)
            return True
        except Exception as e:
            print(f"Error al inicializar servicio de Drive: {e}")
            return False
    
    def list_files(self, max_results=10, query=None):
        """
        Lista archivos de Google Drive.
        
        Args:
            max_results (int): Número máximo de resultados
            query (str): Consulta para filtrar archivos
            
        Returns:
            dict: Lista de archivos
        """
        if not self._initialize_service():
            return {"success": False, "error": "No se pudo inicializar el servicio de Drive"}
        
        try:
            # Preparar parámetros
            params = {
                'pageSize': max_results,
                'fields': "files(id, name, mimeType, webViewLink)"
            }
            
            if query:
                params['q'] = query
                
            # Ejecutar consulta
            results = self.service.files().list(**params).execute()
            files = results.get('files', [])
            
            return {
                "success": True,
                "files": files,
                "count": len(files)
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_file_by_name(self, file_name):
        """
        Busca un archivo por nombre.
        
        Args:
            file_name (str): Nombre del archivo a buscar
            
        Returns:
            dict: Información del archivo
        """
        # Crear consulta para buscar por nombre exacto
        query = f"name = '{file_name}'"
        
        # Usar la función list_files con la consulta
        result = self.list_files(max_results=1, query=query)
        
        if not result["success"]:
            return result
            
        files = result["files"]
        
        if not files:
            return {"success": False, "error": f"No se encontró el archivo '{file_name}'"}
        
        return {
            "success": True,
            "file": files[0]
        }
    
    def download_file(self, file_id, output_path=None):
        """
        Descarga un archivo de Google Drive.
        
        Args:
            file_id (str): ID del archivo a descargar
            output_path (str, optional): Ruta donde guardar el archivo
            
        Returns:
            dict: Resultado de la descarga
        """
        if not self._initialize_service():
            return {"success": False, "error": "No se pudo inicializar el servicio de Drive"}
        
        try:
            # Obtener metadatos del archivo
            file_metadata = self.service.files().get(fileId=file_id).execute()
            file_name = file_metadata.get('name', 'downloaded_file')
            
            # Si no se especifica ruta, usar un directorio temporal
            if not output_path:
                # Usar el directorio de datos de usuario
                temp_dir = Path("data/user_data/downloads")
                temp_dir.mkdir(parents=True, exist_ok=True)
                output_path = str(temp_dir / file_name)
                
            # Preparar la descarga
            request = self.service.files().get_media(fileId=file_id)
            file_content = io.BytesIO()
            downloader = MediaIoBaseDownload(file_content, request)
            
            # Descargar el archivo
            done = False
            while not done:
                status, done = downloader.next_chunk()
                
            # Guardar el archivo
            with open(output_path, 'wb') as f:
                f.write(file_content.getvalue())
                
            return {
                "success": True,
                "file_path": output_path,
                "file_name": file_name,
                "file_size": os.path.getsize(output_path)
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def upload_file(self, file_path, folder_id=None, mime_type=None):
        """
        Sube un archivo a Google Drive.
        
        Args:
            file_path (str): Ruta del archivo a subir
            folder_id (str, optional): ID de la carpeta destino
            mime_type (str, optional): Tipo MIME del archivo
            
        Returns:
            dict: Resultado de la subida
        """
        if not self._initialize_service():
            return {"success": False, "error": "No se pudo inicializar el servicio de Drive"}
        
        try:
            # Verificar que el archivo existe
            file = Path(file_path)
            if not file.exists():
                return {"success": False, "error": f"El archivo {file_path} no existe"}
            
            # Preparar metadatos
            file_metadata = {
                'name': file.name
            }
            
            # Si se especifica carpeta destino
            if folder_id:
                file_metadata['parents'] = [folder_id]
            
            # Preparar media
            from googleapiclient.http import MediaFileUpload
            media = MediaFileUpload(file_path, mimetype=mime_type)
            
            # Subir archivo
            file = self.service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id,name,webViewLink'
            ).execute()
            
            return {
                "success": True,
                "file_id": file.get('id'),
                "file_name": file.get('name'),
                "web_link": file.get('webViewLink')
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
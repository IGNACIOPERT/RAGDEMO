import requests
import json
from pathlib import Path
import sys
import os

# Añadir directorio raíz al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from modules.base_module import BaseModule

class WhatsAppModule(BaseModule):
    """Módulo para interactuar con WhatsApp Web API."""
    
    def __init__(self):
        """Inicializa el módulo de WhatsApp."""
        super().__init__("whatsapp")
    
    def _get_capabilities(self):
        """
        Devuelve las capacidades del módulo de WhatsApp.
        
        Returns:
            list: Lista de capacidades
        """
        return [
            "send_message",
            "send_file",
            "send_image",
            "create_group",
            "add_to_group"
        ]
    
    def send_message(self, phone_number, message):
        """
        Envía un mensaje de texto a un número de WhatsApp.
        
        Args:
            phone_number (str): Número de teléfono del destinatario
            message (str): Mensaje a enviar
            
        Returns:
            dict: Resultado de la operación
        """
        if not self.is_configured:
            return {"success": False, "error": "Módulo no configurado"}
        
        try:
            # URL de la API de WhatsApp
            api_url = "https://graph.facebook.com/v17.0/FROM_PHONE_NUMBER_ID/messages"
            
            # Reemplazar con el ID del número de teléfono del remitente
            api_url = api_url.replace("FROM_PHONE_NUMBER_ID", self.config.get("phone_number_id", ""))
            
            # Cabeceras de la solicitud
            headers = {
                "Authorization": f"Bearer {self.config.get('api_key', '')}",
                "Content-Type": "application/json"
            }
            
            # Datos del mensaje
            data = {
                "messaging_product": "whatsapp",
                "to": phone_number,
                "type": "text",
                "text": {
                    "body": message
                }
            }
            
            # En una implementación real, aquí se haría la llamada a la API
            # response = requests.post(api_url, headers=headers, json=data)
            # response_json = response.json()
            
            # Para simulación, devolvemos un resultado positivo
            # En implementación real, se analizaría la respuesta de la API
            
            return {
                "success": True,
                "message_id": "simulated_message_id_123456",
                "timestamp": "1633123456789",
                "recipient": phone_number
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def send_file(self, phone_number, file_path, caption=None):
        """
        Envía un archivo a un número de WhatsApp.
        
        Args:
            phone_number (str): Número de teléfono del destinatario
            file_path (str): Ruta al archivo a enviar
            caption (str, optional): Texto de acompañamiento
            
        Returns:
            dict: Resultado de la operación
        """
        if not self.is_configured:
            return {"success": False, "error": "Módulo no configurado"}
        
        try:
            # Verificar que el archivo existe
            file = Path(file_path)
            if not file.exists():
                return {"success": False, "error": f"El archivo {file_path} no existe"}
            
            # En una implementación real, aquí se haría la carga y envío del archivo
            # Para simulación, devolvemos un resultado positivo
            
            return {
                "success": True,
                "message_id": "simulated_file_message_id_123456",
                "timestamp": "1633123456789",
                "recipient": phone_number,
                "file": file_path
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def send_image(self, phone_number, image_path, caption=None):
        """
        Envía una imagen a un número de WhatsApp.
        
        Args:
            phone_number (str): Número de teléfono del destinatario
            image_path (str): Ruta a la imagen a enviar
            caption (str, optional): Texto de acompañamiento
            
        Returns:
            dict: Resultado de la operación
        """
        if not self.is_configured:
            return {"success": False, "error": "Módulo no configurado"}
        
        try:
            # Verificar que la imagen existe
            image = Path(image_path)
            if not image.exists():
                return {"success": False, "error": f"La imagen {image_path} no existe"}
            
            # En una implementación real, aquí se haría la carga y envío de la imagen
            # Para simulación, devolvemos un resultado positivo
            
            return {
                "success": True,
                "message_id": "simulated_image_message_id_123456",
                "timestamp": "1633123456789",
                "recipient": phone_number,
                "image": image_path
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def create_group(self, group_name, participants):
        """
        Crea un grupo de WhatsApp.
        
        Args:
            group_name (str): Nombre del grupo
            participants (list): Lista de números de teléfono
            
        Returns:
            dict: Resultado de la operación
        """
        if not self.is_configured:
            return {"success": False, "error": "Módulo no configurado"}
        
        try:
            # En una implementación real, aquí se haría la creación del grupo
            # Para simulación, devolvemos un resultado positivo
            
            return {
                "success": True,
                "group_id": "simulated_group_id_123456",
                "timestamp": "1633123456789",
                "group_name": group_name,
                "participants": participants
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def add_to_group(self, group_id, phone_numbers):
        """
        Añade participantes a un grupo de WhatsApp.
        
        Args:
            group_id (str): ID del grupo
            phone_numbers (list): Lista de números de teléfono
            
        Returns:
            dict: Resultado de la operación
        """
        if not self.is_configured:
            return {"success": False, "error": "Módulo no configurado"}
        
        try:
            # En una implementación real, aquí se añadirían los participantes
            # Para simulación, devolvemos un resultado positivo
            
            return {
                "success": True,
                "group_id": group_id,
                "timestamp": "1633123456789",
                "added_participants": phone_numbers
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
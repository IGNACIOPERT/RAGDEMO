import os
import json
import openai
import sys

# Añadir directorio raíz al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from modules.base_module import BaseModule

class ChatgptModule(BaseModule):
    """Módulo para interactuar con ChatGPT de OpenAI."""
    
    def __init__(self):
        """Inicializa el módulo de ChatGPT."""
        super().__init__("chatgpt")
        self.api_key = None
        self.model = "gpt-4o-mini"
    
    def _get_capabilities(self):
        """
        Devuelve las capacidades del módulo de ChatGPT.
        
        Returns:
            list: Lista de capacidades
        """
        return [
            "generate_text",
            "answer_question",
            "summarize_data",
            "translate_text",
            "analyze_sentiment"
        ]
    
    def _initialize_api(self):
        """
        Inicializa la API de OpenAI.
        
        Returns:
            bool: True si se inicializó correctamente, False en caso contrario
        """
        # Usar la clave de API almacenada en la configuración
        self.api_key = self.config.get("api_key")
        self.model = self.config.get("model", "gpt-4o-mini")
        
        if not self.api_key:
            return False
        
        openai.api_key = self.api_key
        return True
    
    def generate_text(self, prompt, max_tokens=500, temperature=0.7):
        """
        Genera texto utilizando ChatGPT.
        
        Args:
            prompt (str): Prompt para generar texto
            max_tokens (int, optional): Longitud máxima de la respuesta
            temperature (float, optional): Temperatura (aleatoriedad)
            
        Returns:
            dict: Texto generado
        """
        if not self._initialize_api():
            return {"success": False, "error": "No se pudo inicializar la API de OpenAI"}
        
        try:
            # Llamar a la API de ChatGPT
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Eres un asistente útil, conciso y claro."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_tokens,
                temperature=temperature
            )
            
            # Extraer texto generado
            generated_text = response.choices[0].message["content"]
            
            return {
                "success": True,
                "text": generated_text,
                "tokens_used": response.usage.total_tokens
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def answer_question(self, question, context=None, max_tokens=500):
        """
        Responde una pregunta utilizando ChatGPT.
        
        Args:
            question (str): Pregunta a responder
            context (str, optional): Contexto adicional para la pregunta
            max_tokens (int, optional): Longitud máxima de la respuesta
            
        Returns:
            dict: Respuesta a la pregunta
        """
        prompt = question
        
        # Si hay contexto, añadirlo al prompt
        if context:
            prompt = f"Contexto: {context}\n\nPregunta: {question}\n\nRespuesta:"
        
        # Usar generate_text para obtener la respuesta
        return self.generate_text(prompt, max_tokens, temperature=0.5)
    
    def summarize_data(self, data, format_type="text", max_tokens=300):
        """
        Resume y presenta datos en un formato legible.
        
        Args:
            data (dict/list): Datos a resumir
            format_type (str, optional): Tipo de formato (text, markdown, etc.)
            max_tokens (int, optional): Longitud máxima del resumen
            
        Returns:
            dict: Resumen de los datos
        """
        # Convertir datos a texto si no lo son
        if isinstance(data, (dict, list)):
            data_str = json.dumps(data, indent=2)
        else:
            data_str = str(data)
        
        # Crear prompt para resumir datos
        prompt = f"""
        Aquí hay unos datos para analizar y resumir:
        
        {data_str}
        
        Por favor, proporciona un resumen conciso de estos datos en formato {format_type}.
        Destaca los puntos clave y cualquier información relevante.
        """
        
        # Usar generate_text para obtener el resumen
        return self.generate_text(prompt, max_tokens, temperature=0.3)
    
    def translate_text(self, text, target_language, source_language=None):
        """
        Traduce texto a otro idioma.
        
        Args:
            text (str): Texto a traducir
            target_language (str): Idioma destino
            source_language (str, optional): Idioma origen
            
        Returns:
            dict: Texto traducido
        """
        # Crear prompt para traducción
        prompt = f"Traduce el siguiente texto al {target_language}:\n\n{text}"
        
        if source_language:
            prompt = f"Traduce el siguiente texto del {source_language} al {target_language}:\n\n{text}"
        
        # Usar generate_text para obtener la traducción
        return self.generate_text(prompt, max_tokens=len(text) * 2, temperature=0.3)
    
    def analyze_sentiment(self, text):
        """
        Analiza el sentimiento de un texto.
        
        Args:
            text (str): Texto a analizar
            
        Returns:
            dict: Resultado del análisis de sentimiento
        """
        # Crear prompt para análisis de sentimiento
        prompt = f"""
        Realiza un análisis de sentimiento del siguiente texto y clasifícalo como positivo, negativo o neutral.
        Proporciona un valor numérico entre -1 (muy negativo) y 1 (muy positivo).
        
        Texto: {text}
        
        Formato de respuesta:
        Clasificación: [positivo/negativo/neutral]
        Valor: [valor numérico]
        Explicación: [breve explicación]
        """
        
        # Usar generate_text para obtener el análisis
        result = self.generate_text(prompt, max_tokens=200, temperature=0.3)
        
        if not result["success"]:
            return result
        
        # Intentar extraer el valor numérico
        try:
            lines = result["text"].strip().split("\n")
            sentiment_value = 0.0
            sentiment_class = "neutral"
            
            for line in lines:
                if "Valor:" in line:
                    value_str = line.split("Valor:")[1].strip()
                    try:
                        sentiment_value = float(value_str)
                    except:
                        pass
                elif "Clasificación:" in line:
                    sentiment_class = line.split("Clasificación:")[1].strip()
            
            result["sentiment"] = {
                "classification": sentiment_class,
                "value": sentiment_value
            }
            
            return result
            
        except Exception as e:
            # Si hay error al parsear, devolver el resultado original
            return result
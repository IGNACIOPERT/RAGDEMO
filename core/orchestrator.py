import json
import sys
import os
import openai
<<<<<<< HEAD
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()
=======
>>>>>>> 28d0d3447ac7e388ed3e475a36f07fee63525e6f

# Añadir directorio raíz al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

class Orchestrator:
    """
    Orquestador que analiza tareas y coordina el uso de módulos.
    """
    
    def __init__(self, module_registry):
        """
        Inicializa el orquestador.
        
        Args:
            module_registry (ModuleRegistry): Registro de módulos disponibles
        """
        self.module_registry = module_registry
<<<<<<< HEAD
        
        # Obtener configuración desde variables de entorno
        self.openai_api_key = os.getenv("OPENAI_API_KEY", "")
        self.openai_model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        
        # Configurar API key para OpenAI
        openai.api_key = self.openai_api_key
        
        # Imprimir información para depuración
        api_key_status = "✅ Configurada" if self.openai_api_key else "❌ No encontrada"
        print(f"[Orchestrator] OPENAI_API_KEY: {api_key_status}")
        print(f"[Orchestrator] OPENAI_MODEL: {self.openai_model}")
=======
        self.openai_api_key = config.OPENAI_API_KEY
        self.openai_model = config.OPENAI_MODEL
        
        # Configurar API key para OpenAI
        openai.api_key = self.openai_api_key
>>>>>>> 28d0d3447ac7e388ed3e475a36f07fee63525e6f
    
    def get_available_tools(self):
        """
        Obtiene una lista de herramientas disponibles para el agente.
        
        Returns:
            list: Lista de herramientas con sus capacidades
        """
        tools = []
        
        # Obtener capacidades de todos los módulos configurados
        module_capabilities = self.module_registry.get_module_capabilities()
        
        for module_type, capabilities in module_capabilities.items():
            tool = {
                "name": module_type,
                "description": self._get_module_description(module_type),
                "capabilities": capabilities
            }
            tools.append(tool)
        
        return tools
    
    def analyze_task(self, task_description):
        """
        Analiza una tarea para determinar qué herramientas usar y cómo.
        
        Args:
            task_description (str): Descripción de la tarea
            
        Returns:
            dict: Análisis de la tarea con pasos y herramientas recomendadas
        """
        try:
            # Obtener herramientas disponibles
            available_tools = self.get_available_tools()
            
            # Si no hay herramientas configuradas, devolver error
            if not available_tools:
                return {
                    "success": False,
                    "error": "No hay herramientas configuradas",
                    "steps": []
                }
            
            # Crear prompt para el análisis de la tarea
            prompt = self._create_task_analysis_prompt(task_description, available_tools)
            
            # Llamar a la API de OpenAI para analizar la tarea
            response = openai.ChatCompletion.create(
                model=self.openai_model,
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": task_description}
                ],
                temperature=0.2,
                max_tokens=1000
            )
            
            # Extraer el análisis de la respuesta
            analysis_text = response.choices[0].message["content"]
            
            # Intentar convertir la respuesta a JSON
            try:
                # Primero intentar encontrar el JSON dentro del texto
                start_idx = analysis_text.find("{")
                end_idx = analysis_text.rfind("}")
                
                if start_idx >= 0 and end_idx > start_idx:
                    json_str = analysis_text[start_idx:end_idx+1]
                    analysis = json.loads(json_str)
                else:
                    # Si no se encuentra formato JSON válido, estructurar manualmente
                    analysis = {
                        "success": True,
                        "description": analysis_text,
                        "steps": []
                    }
            except json.JSONDecodeError:
                # Si hay error en el formato JSON, estructurar manualmente
                analysis = {
                    "success": True,
                    "description": analysis_text,
                    "steps": []
                }
            
            # Si el análisis no tiene pasos, hacer otro intento para obtenerlos
            if "steps" not in analysis or not analysis["steps"]:
                steps = self._extract_steps_from_text(analysis_text, available_tools)
                analysis["steps"] = steps
            
            analysis["success"] = True
            return analysis
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "steps": []
            }
    
    def _get_module_description(self, module_type):
        """
        Obtiene una descripción para un tipo de módulo.
        
        Args:
            module_type (str): Tipo de módulo
            
        Returns:
            str: Descripción del módulo
        """
        descriptions = {
            "gmail": "Envía y recibe correos electrónicos a través de Gmail",
            "whatsapp": "Envía mensajes y archivos a través de WhatsApp",
            "excel": "Lee, escribe y procesa archivos Excel",
            "vector_db": "Almacena y consulta datos en una base de datos vectorial",
            "chatgpt": "Genera texto y responde preguntas usando ChatGPT",
<<<<<<< HEAD
            "embedding": "Genera embeddings de texto para búsqueda semántica",
            "drive": "Accede y gestiona archivos en Google Drive"
=======
            "embedding": "Genera embeddings de texto para búsqueda semántica"
>>>>>>> 28d0d3447ac7e388ed3e475a36f07fee63525e6f
        }
        
        return descriptions.get(module_type, f"Módulo {module_type}")
    
    def _create_task_analysis_prompt(self, task_description, available_tools):
        """
        Crea un prompt para analizar una tarea.
        
        Args:
            task_description (str): Descripción de la tarea
            available_tools (list): Lista de herramientas disponibles
            
        Returns:
            str: Prompt para análisis de tarea
        """
        tools_text = "\n".join([
            f"- {tool['name']}: {tool['description']}. Capacidades: {', '.join(tool['capabilities'])}"
            for tool in available_tools
        ])
        
        prompt = f"""
        Eres un asistente experto en analizar tareas y dividirlas en pasos concretos que pueden ser ejecutados usando herramientas específicas.
        
        Tienes disponibles las siguientes herramientas:
        
        {tools_text}
        
        Dada una descripción de tarea, debes:
        1. Analizar qué herramientas son necesarias para completarla
        2. Dividir la tarea en pasos secuenciales y concretos
        3. Para cada paso, especificar qué herramienta usar y qué acción realizar
        
        Devuelve tu análisis en formato JSON con la siguiente estructura:
        {{
            "description": "Descripción breve de cómo abordas la tarea",
            "steps": [
                {{
                    "step_number": 1,
                    "description": "Descripción del paso",
                    "tool": "nombre_herramienta",
                    "action": "nombre_acción",
                    "parameters": {{
                        "param1": "valor1",
                        "param2": "valor2"
                    }}
                }},
                ...
            ]
        }}
        
        Asegúrate de que cada paso sea concreto y ejecutable, con parámetros específicos cuando sea posible.
        """
        
        return prompt
    
    def _extract_steps_from_text(self, text, available_tools):
        """
        Extrae pasos de un texto de análisis.
        
        Args:
            text (str): Texto de análisis
            available_tools (list): Lista de herramientas disponibles
            
        Returns:
            list: Lista de pasos extraídos
        """
        # Esta es una implementación simple para extraer pasos de un texto no estructurado
        steps = []
        
        # Lista de palabras clave que podrían indicar un paso
        step_keywords = ["paso", "step", "primero", "segundo", "tercero", "luego", "finalmente", "entonces"]
        
        # Dividir el texto en líneas
        lines = text.split("\n")
        
        current_step = None
        step_number = 0
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Verificar si la línea parece ser un nuevo paso
            is_new_step = False
            for keyword in step_keywords:
                if keyword.lower() in line.lower():
                    is_new_step = True
                    break
            
            # Si tenemos números en la línea, podría ser un paso numerado
            if line[0].isdigit() and "." in line[:5]:
                is_new_step = True
            
            if is_new_step:
                # Si hay un paso actual, guardarlo
                if current_step:
                    steps.append(current_step)
                
                # Crear un nuevo paso
                step_number += 1
                current_step = {
                    "step_number": step_number,
                    "description": line,
                    "tool": None,
                    "action": None,
                    "parameters": {}
                }
                
                # Intentar identificar herramienta y acción en la descripción del paso
                for tool in available_tools:
                    tool_name = tool["name"]
                    if tool_name.lower() in line.lower():
                        current_step["tool"] = tool_name
                        
                        # Intentar identificar una acción
                        for capability in tool["capabilities"]:
                            if capability.lower() in line.lower():
                                current_step["action"] = capability
                                break
                        break
            else:
                # Añadir línea a la descripción del paso actual
                if current_step:
                    current_step["description"] += " " + line
                    
                    # Seguir buscando herramienta y acción si no se han encontrado
                    if not current_step["tool"]:
                        for tool in available_tools:
                            tool_name = tool["name"]
                            if tool_name.lower() in line.lower():
                                current_step["tool"] = tool_name
                                break
                    
                    # Seguir buscando acción si no se ha encontrado
                    if current_step["tool"] and not current_step["action"]:
                        for tool in available_tools:
                            if tool["name"] == current_step["tool"]:
                                for capability in tool["capabilities"]:
                                    if capability.lower() in line.lower():
                                        current_step["action"] = capability
                                        break
                                break
        
        # Añadir el último paso si existe
        if current_step:
            steps.append(current_step)
        
        return steps
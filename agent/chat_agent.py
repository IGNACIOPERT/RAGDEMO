import os
import json
import time
import openai
import re
<<<<<<< HEAD
from dotenv import load_dotenv
from .prompt_templates import SYSTEM_PROMPT, TOOL_DESCRIPTION_TEMPLATE

# Cargar variables de entorno
load_dotenv()

=======
from .prompt_templates import SYSTEM_PROMPT, TOOL_DESCRIPTION_TEMPLATE

>>>>>>> 28d0d3447ac7e388ed3e475a36f07fee63525e6f
class ChatAgent:
    """
    Agente de chat basado en GPT que coordina el sistema.
    Analiza las instrucciones del usuario y decide qué herramientas utilizar.
    """
    
    def __init__(self, orchestrator, flow_generator, executor, model="gpt-4"):
        """
        Inicializa el agente de chat.
        
        Args:
            orchestrator: Orquestador de herramientas
            flow_generator: Generador de flujos de trabajo
            executor: Motor de ejecución
            model: Modelo de GPT a utilizar
        """
        self.orchestrator = orchestrator
        self.flow_generator = flow_generator
        self.executor = executor
<<<<<<< HEAD
        self.model = os.getenv("OPENAI_MODEL", model)
=======
        self.model = model
>>>>>>> 28d0d3447ac7e388ed3e475a36f07fee63525e6f
        
        # Intentar cargar la API key desde variables de entorno
        openai.api_key = os.getenv("OPENAI_API_KEY")
        
<<<<<<< HEAD
        # Imprimir estado para depuración
        api_key_status = "✅ Configurada" if openai.api_key else "❌ No encontrada"
        print(f"OPENAI_API_KEY: {api_key_status}")
        print(f"OPENAI_MODEL: {self.model}")
        
=======
>>>>>>> 28d0d3447ac7e388ed3e475a36f07fee63525e6f
        # Si no está disponible, se deberá configurar manualmente
        if not openai.api_key:
            print("⚠️ OPENAI_API_KEY no encontrada en variables de entorno")
    
    def set_api_key(self, api_key):
        """Establece la clave de API de OpenAI."""
        openai.api_key = api_key
    
    def process_message(self, message, chat_history=None):
        """
        Procesa un mensaje del usuario y genera una respuesta.
        
        Args:
            message: Mensaje del usuario
            chat_history: Historial de chat previo
            
        Returns:
            dict: Respuesta que incluye el mensaje para el usuario y opcionalmente un flujo de trabajo
        """
        if not chat_history:
            chat_history = []
        
<<<<<<< HEAD
        # Imprimir mensaje recibido para depuración
        print(f"\n[DEBUG] Mensaje recibido: {message}")
        print(f"[DEBUG] Historial de chat: {len(chat_history)} mensajes")
        
        # Verificar API key de nuevo
        if openai.api_key:
            print(f"[DEBUG] API Key en process_message: {openai.api_key[:5]}...")
        else:
            print("[DEBUG] API Key: No configurada")
        
        # Obtener herramientas disponibles
        available_tools = self.orchestrator.get_available_tools()
        print(f"[DEBUG] Herramientas disponibles: {len(available_tools)}")
=======
        # Obtener herramientas disponibles
        available_tools = self.orchestrator.get_available_tools()
>>>>>>> 28d0d3447ac7e388ed3e475a36f07fee63525e6f
        
        # Preparar la descripción de herramientas para el prompt
        tools_description = "\n".join([
            TOOL_DESCRIPTION_TEMPLATE.format(
                name=tool["name"],
                description=tool["description"],
                capabilities=", ".join(tool["capabilities"])
            ) for tool in available_tools
        ])
        
        # Preparar el sistema prompt con las herramientas disponibles
        system_prompt = SYSTEM_PROMPT.format(tools_description=tools_description)
        
        # Preparar los mensajes para la API de ChatGPT
        messages = [
            {"role": "system", "content": system_prompt},
        ]
        
        # Añadir historial de chat
        for chat_message in chat_history:
            messages.append({
                "role": chat_message["role"],
                "content": chat_message["content"]
            })
        
        # Añadir el mensaje actual si no está en el historial
        if not chat_history or chat_history[-1]["content"] != message:
            messages.append({"role": "user", "content": message})
        
<<<<<<< HEAD
        print(f"[DEBUG] Total de mensajes a enviar: {len(messages)}")
        
        try:
            # Configurar API key nuevamente para asegurar que esté disponible
            openai.api_key = os.getenv("OPENAI_API_KEY")
            
            # Imprimir información para depuración
            print(f"[DEBUG] Llamando a OpenAI API con modelo: {self.model}")
            
=======
        try:
>>>>>>> 28d0d3447ac7e388ed3e475a36f07fee63525e6f
            # Llamar a la API de ChatGPT
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=messages
            )
            
            # Obtener la respuesta
            assistant_message = response.choices[0].message["content"]
<<<<<<< HEAD
            print(f"[DEBUG] Respuesta recibida: {assistant_message[:50]}...")
            
            # Analizar si hay necesidad de crear un flujo de trabajo
            needs_workflow = self._needs_workflow(message, assistant_message)
            print(f"[DEBUG] ¿Necesita flujo de trabajo?: {needs_workflow}")
            
            if needs_workflow:
                # Pedir al orquestador que planifique un flujo de trabajo
                print("[DEBUG] Generando flujo de trabajo...")
=======
            
            # Analizar si hay necesidad de crear un flujo de trabajo
            needs_workflow = self._needs_workflow(message, assistant_message)
            
            if needs_workflow:
                # Pedir al orquestador que planifique un flujo de trabajo
>>>>>>> 28d0d3447ac7e388ed3e475a36f07fee63525e6f
                task_analysis = self.orchestrator.analyze_task(message)
                workflow = self.flow_generator.create_workflow(task_analysis)
                
                # Generar visualización para el flujo
                visualization = self.flow_generator.visualize_workflow(workflow)
                
                return {
                    "message": assistant_message,
                    "workflow": workflow,
                    "visualization": visualization
                }
            else:
                return {
                    "message": assistant_message
                }
                
        except Exception as e:
<<<<<<< HEAD
            import traceback
            print(f"[ERROR] Error al procesar el mensaje: {e}")
            print(traceback.format_exc())
            return {
                "message": f"Lo siento, ocurrió un error al procesar tu mensaje: {str(e)}",
                "error_details": traceback.format_exc()
=======
            print(f"Error al procesar el mensaje: {e}")
            return {
                "message": "Lo siento, ocurrió un error al procesar tu mensaje. Por favor, inténtalo de nuevo."
>>>>>>> 28d0d3447ac7e388ed3e475a36f07fee63525e6f
            }
    
    def _needs_workflow(self, user_message, assistant_message):
        """
        Determina si la interacción requiere crear un flujo de trabajo.
        
        Args:
            user_message: Mensaje del usuario
            assistant_message: Respuesta del asistente
            
        Returns:
            bool: True si se necesita un flujo de trabajo, False en caso contrario
        """
        # Palabras clave que sugieren la necesidad de un flujo de trabajo
        workflow_keywords = [
            "automatizar", "flujo", "secuencia", "pasos", "proceso",
            "enviar", "extraer", "procesar", "generar", "crear",
            "analizar", "combinar", "transformar"
        ]
        
        # Verificar si el mensaje del usuario contiene palabras clave
        for keyword in workflow_keywords:
            if keyword.lower() in user_message.lower():
                return True
        
        # Verificar si hay una petición explícita de generar un flujo
        generate_patterns = [
            r"generar\s+(?:un|el)\s+flujo",
            r"crear\s+(?:un|el)\s+flujo",
            r"hacer\s+(?:un|el)\s+flujo",
            r"construir\s+(?:un|el)\s+flujo",
            r"implementar\s+(?:un|el)\s+flujo",
            r"quiero\s+(?:un|el)\s+flujo",
            r"necesito\s+(?:un|el)\s+flujo",
            r"hazme\s+(?:un|el)\s+flujo",
            r"crear\s+(?:una|la)\s+automatización",
            r"generar\s+(?:una|la)\s+automatización"
        ]
        
        for pattern in generate_patterns:
            if re.search(pattern, user_message.lower()):
                return True
        
        # Verificar si el asistente sugiere generar un flujo
        if "Generando flujo de trabajo..." in assistant_message:
            return True
        
        return False
    
    def execute_workflow(self, workflow_id):
        """
        Ejecuta un flujo de trabajo y genera un resumen de la ejecución.
        
        Args:
            workflow_id: ID del flujo de trabajo a ejecutar
            
        Returns:
            dict: Resultado y resumen de la ejecución
        """
        # Obtener el flujo de trabajo
        # Nota: Esta implementación asume que el flujo está disponible en memoria
        # En una implementación real, habría que cargarlo desde algún almacenamiento
        
        # Ejecutar el flujo
        execution_result = self.executor.execute_workflow(workflow_id)
        
        # Generar un resumen de la ejecución
        if execution_result["success"]:
            summary = f"El flujo de trabajo se ejecutó correctamente en {execution_result['end_time'] - execution_result['start_time']:.2f} segundos."
            
            # Añadir resumen de pasos completados
            steps_summary = []
            for step_id, step_result in execution_result["steps_results"].items():
                status = "✅ Completado" if step_result["success"] else "❌ Fallido"
                steps_summary.append(f"- Paso {step_id}: {status}")
            
            if steps_summary:
                summary += "\n\nResumen de pasos:\n" + "\n".join(steps_summary)
            
            # Añadir resumen de resultados
            if execution_result["output"]:
                summary += "\n\nResultados:"
                for var_name, result in execution_result["output"].items():
                    if isinstance(result, dict) or isinstance(result, list):
                        result_str = json.dumps(result, indent=2)
                    else:
                        result_str = str(result)
                    summary += f"\n- {var_name}: {result_str[:200]}..."
        else:
            summary = f"⚠️ Error al ejecutar el flujo de trabajo: {execution_result.get('error', 'Error desconocido')}"
            
            # Añadir detalle del paso que falló
            for step_id, step_result in execution_result["steps_results"].items():
                if not step_result["success"]:
                    summary += f"\n\nError en paso {step_id}: {step_result.get('error', 'Error desconocido')}"
                    break
        
        return {
            "execution_result": execution_result,
            "summary": summary
        }
    
    def get_module_info(self, module_type):
        """
        Genera información detallada sobre un módulo específico.
        
        Args:
            module_type: Tipo de módulo
            
        Returns:
            str: Información detallada del módulo
        """
        # Obtener herramientas disponibles
        available_tools = self.orchestrator.get_available_tools()
        
        # Buscar el módulo solicitado
        module_info = None
        for tool in available_tools:
            if tool["name"] == module_type:
                module_info = tool
                break
        
        if not module_info:
            return f"No se encontró información para el módulo '{module_type}'."
        
        # Generar respuesta detallada sobre el módulo
        response = f"## Módulo: {module_info['name']}\n\n"
        response += f"{module_info['description']}\n\n"
        
        response += "### Capacidades:\n"
        for capability in module_info['capabilities']:
            response += f"- {capability}\n"
        
        # Obtener información de configuración requerida
        config_schema = self.orchestrator.module_registry.get_module(module_type).get_config_schema()
        
        response += "\n### Configuración requerida:\n"
        for field in config_schema.get('required_fields', []):
            response += f"- {field}\n"
        
        if config_schema.get('optional_fields', []):
            response += "\n### Configuración opcional:\n"
            for field in config_schema['optional_fields']:
                response += f"- {field}\n"
        
        return response
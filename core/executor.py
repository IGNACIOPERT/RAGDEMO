import time
import traceback
import json

class Executor:
    """
    Motor de ejecución de flujos de trabajo.
    """
    
    def __init__(self, module_registry):
        """
        Inicializa el motor de ejecución.
        
        Args:
            module_registry (ModuleRegistry): Registro de módulos disponibles
        """
        self.module_registry = module_registry
        self.execution_results = {}  # Resultados de ejecución por ID de flujo
    
    def execute_workflow(self, workflow):
        """
        Ejecuta un flujo de trabajo completo.
        
        Args:
            workflow (dict): Flujo de trabajo a ejecutar
            
        Returns:
            dict: Resultado de la ejecución
        """
        workflow_id = workflow.get("id", "unknown")
        steps = workflow.get("steps", [])
        
        start_time = time.time()
        
        # Inicializar el registro de resultados para este flujo
        execution_result = {
            "workflow_id": workflow_id,
            "status": "running",
            "start_time": start_time,
            "end_time": None,
            "steps_results": {},
            "success": True,
            "error": None,
            "output": {}
        }
        
        self.execution_results[workflow_id] = execution_result
        
        # Variables para almacenar resultados intermedios
        step_outputs = {}
        
        try:
            # Ejecutar cada paso secuencialmente
            for step in steps:
                step_id = step.get("id", "unknown")
                tool = step.get("tool")
                action = step.get("action")
                parameters = step.get("parameters", {})
                output_var = step.get("output_var")
                
                # Inicializar resultado del paso
                step_result = {
                    "step_id": step_id,
                    "tool": tool,
                    "action": action,
                    "start_time": time.time(),
                    "end_time": None,
                    "success": False,
                    "error": None,
                    "output": None
                }
                
                execution_result["steps_results"][step_id] = step_result
                
                # Verificar si el módulo y la acción existen
                if not tool or not action:
                    step_result["error"] = f"Herramienta o acción no especificada: {tool}/{action}"
                    execution_result["success"] = False
                    continue
                
                # Procesar parámetros para reemplazar referencias
                processed_params = {}
                for param_name, param_value in parameters.items():
                    if isinstance(param_value, dict) and param_value.get("type") == "reference":
                        ref_var = param_value.get("value")
                        if ref_var in step_outputs:
                            processed_params[param_name] = step_outputs[ref_var]
                        else:
                            step_result["error"] = f"Referencia no encontrada: {ref_var}"
                            execution_result["success"] = False
                            break
                    else:
                        processed_params[param_name] = param_value
                
                if step_result.get("error"):
                    continue
                
                try:
                    # Ejecutar la acción del módulo
                    action_result = self.module_registry.execute_module_action(
                        tool, action, processed_params
                    )
                    
                    # Registrar el resultado
                    step_result["success"] = action_result.get("success", False)
                    
                    if action_result.get("success", False):
                        step_result["output"] = action_result.get("result")
                        
                        # Guardar el resultado para referencias futuras
                        if output_var:
                            step_outputs[output_var] = action_result.get("result")
                    else:
                        step_result["error"] = action_result.get("error", "Error desconocido")
                        execution_result["success"] = False
                
                except Exception as e:
                    step_result["error"] = str(e)
                    step_result["traceback"] = traceback.format_exc()
                    execution_result["success"] = False
                
                # Registrar tiempo de finalización del paso
                step_result["end_time"] = time.time()
                
                # Si el paso falló y no se debe continuar, detener la ejecución
                if not step_result["success"] and step.get("stop_on_error", True):
                    break
            
            # Resultados finales
            execution_result["end_time"] = time.time()
            execution_result["status"] = "completed"
            
            # Si todos los pasos se ejecutaron correctamente, guardar salidas finales
            if execution_result["success"]:
                # Obtener resultados de los últimos pasos o pasos marcados como salida
                final_outputs = {}
                for step in steps:
                    if step.get("is_output", False) and step.get("output_var"):
                        output_var = step["output_var"]
                        if output_var in step_outputs:
                            final_outputs[output_var] = step_outputs[output_var]
                
                # Si no hay salidas marcadas explícitamente, usar la última
                if not final_outputs and steps and steps[-1].get("output_var"):
                    output_var = steps[-1]["output_var"]
                    if output_var in step_outputs:
                        final_outputs[output_var] = step_outputs[output_var]
                
                execution_result["output"] = final_outputs
            
        except Exception as e:
            execution_result["status"] = "failed"
            execution_result["success"] = False
            execution_result["error"] = str(e)
            execution_result["traceback"] = traceback.format_exc()
            execution_result["end_time"] = time.time()
        
        return execution_result
    
    def get_execution_result(self, workflow_id):
        """
        Obtiene el resultado de ejecución de un flujo específico.
        
        Args:
            workflow_id (str): ID del flujo de trabajo
            
        Returns:
            dict: Resultado de la ejecución o None si no existe
        """
        return self.execution_results.get(workflow_id)
    
    def get_step_result(self, workflow_id, step_id):
        """
        Obtiene el resultado de ejecución de un paso específico.
        
        Args:
            workflow_id (str): ID del flujo de trabajo
            step_id (str): ID del paso
            
        Returns:
            dict: Resultado del paso o None si no existe
        """
        execution_result = self.get_execution_result(workflow_id)
        if execution_result and "steps_results" in execution_result:
            return execution_result["steps_results"].get(step_id)
        return None
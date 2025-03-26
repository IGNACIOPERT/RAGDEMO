import json
import time
import uuid

class FlowGenerator:
    """
    Generador de flujos de trabajo a partir del análisis de tareas.
    """
    
    def __init__(self):
        """Inicializa el generador de flujos."""
        pass
    
    def create_workflow(self, task_analysis):
        """
        Crea un flujo de trabajo a partir del análisis de una tarea.
        
        Args:
            task_analysis (dict): Análisis de tarea con pasos
            
        Returns:
            dict: Flujo de trabajo estructurado
        """
        # Si no hay análisis exitoso, devolver flujo vacío
        if not task_analysis.get("success", False):
            return {
                "id": str(uuid.uuid4()),
                "name": "Flujo sin definir",
                "description": "No se pudo generar un flujo de trabajo",
                "created_at": int(time.time()),
                "steps": []
            }
        
        # Extraer pasos del análisis
        steps = task_analysis.get("steps", [])
        
        # Preparar los pasos del flujo
        workflow_steps = []
        
        # Variables para mapear salidas entre pasos
        output_vars = {}
        
        for i, step in enumerate(steps):
            # Crear una copia del paso para no modificar el original
            workflow_step = step.copy()
            
            # Asignar ID único al paso
            workflow_step["id"] = f"step_{i+1}"
            
            # Asignar una variable de salida para este paso
            if "output_var" not in workflow_step:
                workflow_step["output_var"] = f"result_{i+1}"
            
            # Registrar la variable de salida
            output_vars[workflow_step["output_var"]] = {
                "step_id": workflow_step["id"],
                "description": workflow_step.get("description", "")
            }
            
            # Analizar parámetros para reemplazar referencias a resultados anteriores
            if "parameters" in workflow_step:
                for param_name, param_value in workflow_step["parameters"].items():
                    if isinstance(param_value, str) and param_value in output_vars:
                        # El parámetro hace referencia a una salida anterior
                        workflow_step["parameters"][param_name] = {
                            "type": "reference",
                            "value": param_value
                        }
            
            workflow_steps.append(workflow_step)
        
        # Crear el flujo de trabajo
        workflow = {
            "id": str(uuid.uuid4()),
            "name": f"Flujo generado {time.strftime('%Y-%m-%d %H:%M')}",
            "description": task_analysis.get("description", "Flujo de trabajo generado automáticamente"),
            "created_at": int(time.time()),
            "steps": workflow_steps
        }
        
        return workflow
    
    def visualize_workflow(self, workflow):
        """
        Genera una visualización del flujo de trabajo en formato Mermaid.
        
        Args:
            workflow (dict): Flujo de trabajo
            
        Returns:
            str: Diagrama de flujo en formato Mermaid
        """
        # Si no hay pasos, devolver diagrama vacío
        if not workflow or not workflow.get("steps"):
            return "graph TD\n    A[Sin pasos definidos]"
        
        # Crear diagrama Mermaid
        mermaid = "graph TD\n"
        
        # Nodo inicial
        mermaid += "    Start[Inicio] --> Step1\n"
        
        # Añadir nodos para cada paso
        for i, step in enumerate(workflow["steps"]):
            step_id = step.get("id", f"step_{i+1}")
            tool = step.get("tool", "sin_herramienta")
            action = step.get("action", "sin_acción")
            description = step.get("description", "").replace("\n", " ")[:50]
            
            if i < len(workflow["steps"]) - 1:
                next_step_id = workflow["steps"][i+1].get("id", f"step_{i+2}")
                mermaid += f"    {step_id.replace('-', '_')}[{i+1}. {tool}: {action}] --> {next_step_id.replace('-', '_')}\n"
            else:
                mermaid += f"    {step_id.replace('-', '_')}[{i+1}. {tool}: {action}] --> End\n"
                
            # Añadir tooltip con descripción
            mermaid += f"    {step_id.replace('-', '_')}:::tooltip\n"
            
            # Añadir estilos según la herramienta
            mermaid += f"    class {step_id.replace('-', '_')} {tool}Style\n"
        
        # Nodo final
        mermaid += "    End[Fin]\n"
        
        # Añadir estilos
        mermaid += "    classDef gmailStyle fill:#D44638,color:white\n"
        mermaid += "    classDef whatsappStyle fill:#25D366,color:white\n"
        mermaid += "    classDef excelStyle fill:#217346,color:white\n"
        mermaid += "    classDef vector_dbStyle fill:#4285F4,color:white\n"
        mermaid += "    classDef chatgptStyle fill:#74AA9C,color:white\n"
        mermaid += "    classDef embeddingStyle fill:#FF6D00,color:white\n"
        mermaid += "    classDef tooltip title:\"Tooltip\"\n"
        
        return mermaid
    
    def update_workflow(self, workflow, changes):
        """
        Actualiza un flujo de trabajo con cambios específicos.
        
        Args:
            workflow (dict): Flujo de trabajo original
            changes (dict): Cambios a aplicar
            
        Returns:
            dict: Flujo de trabajo actualizado
        """
        # Crear una copia del flujo para no modificar el original
        updated_workflow = workflow.copy()
        
        # Actualizar metadatos si se proporcionan
        if "name" in changes:
            updated_workflow["name"] = changes["name"]
        
        if "description" in changes:
            updated_workflow["description"] = changes["description"]
        
        # Actualizar pasos si se proporcionan
        if "steps" in changes:
            # Acciones posibles: add, update, delete, reorder
            step_changes = changes["steps"]
            
            if "add" in step_changes:
                # Añadir nuevos pasos
                for new_step in step_changes["add"]:
                    # Asignar ID único si no tiene
                    if "id" not in new_step:
                        new_step["id"] = f"step_{len(updated_workflow['steps']) + 1}"
                    
                    # Añadir el paso
                    updated_workflow["steps"].append(new_step)
            
            if "update" in step_changes:
                # Actualizar pasos existentes
                for step_update in step_changes["update"]:
                    step_id = step_update.get("id")
                    if not step_id:
                        continue
                    
                    # Buscar el paso a actualizar
                    for i, step in enumerate(updated_workflow["steps"]):
                        if step.get("id") == step_id:
                            # Actualizar el paso
                            for key, value in step_update.items():
                                if key != "id":
                                    updated_workflow["steps"][i][key] = value
                            break
            
            if "delete" in step_changes:
                # Eliminar pasos
                step_ids_to_delete = step_changes["delete"]
                updated_workflow["steps"] = [
                    step for step in updated_workflow["steps"]
                    if step.get("id") not in step_ids_to_delete
                ]
            
            if "reorder" in step_changes:
                # Reordenar pasos
                new_order = step_changes["reorder"]
                
                # Crear un mapa de pasos por ID
                steps_map = {
                    step.get("id"): step
                    for step in updated_workflow["steps"]
                }
                
                # Crear la nueva lista de pasos según el orden
                updated_workflow["steps"] = [
                    steps_map[step_id]
                    for step_id in new_order
                    if step_id in steps_map
                ]
        
        # Actualizar timestamp de modificación
        updated_workflow["updated_at"] = int(time.time())
        
        return updated_workflow
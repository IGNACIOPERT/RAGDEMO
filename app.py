from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import os
import json
import time
from pathlib import Path
from dotenv import load_dotenv
import os
import json
# Cargar variables de entorno
load_dotenv()

# Importar componentes del sistema
from core.module_registry import ModuleRegistry
from core.orchestrator import Orchestrator
from core.flow_generator import FlowGenerator
from core.executor import Executor
from agent.chat_agent import ChatAgent
from modules import discover_modules

# Crear la aplicación Flask
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", os.urandom(24))

# Asegurar que existen los directorios necesarios
data_dir = Path("data")
module_configs_dir = data_dir / "module_configs"
workflows_dir = data_dir / "workflows"
user_data_dir = data_dir / "user_data"

for directory in [module_configs_dir, workflows_dir, user_data_dir]:
    directory.mkdir(parents=True, exist_ok=True)

# Inicializar componentes del sistema
module_registry = ModuleRegistry(str(module_configs_dir))
orchestrator = Orchestrator(module_registry)
flow_generator = FlowGenerator()
executor = Executor(module_registry)
chat_agent = ChatAgent(orchestrator, flow_generator, executor)

@app.route('/')
def index():
    """Página principal de la aplicación."""
    # Obtener módulos disponibles y configurados
    available_modules = module_registry.get_available_modules()
    configured_modules = module_registry.get_configured_modules()
    
    return render_template(
        'index.html',
        modules=available_modules,
        configured_modules=list(configured_modules.keys())
    )

@app.route('/chat', methods=['POST'])
def chat():
    """Endpoint para procesar mensajes de chat."""
<<<<<<< HEAD
    try:
        message = request.json.get('message', '')
        print(f"Mensaje recibido: {message}")
        
        # Obtener historial de chat de la sesión o inicializar
        chat_history = session.get('chat_history', [])
        print(f"Historial de chat: {len(chat_history)} mensajes")
        
        # Procesar con el agente de chat
        print("Procesando mensaje con el agente de chat...")
        response = chat_agent.process_message(message, chat_history)
        print(f"Respuesta generada: {response.get('message', '')[:50]}...")
        
        # Actualizar historial de chat
        if 'chat_history' not in session:
            session['chat_history'] = []
        
        session['chat_history'].append({"role": "user", "content": message})
        session['chat_history'].append({"role": "assistant", "content": response.get('message', '')})
        
        # Si el agente generó un flujo de trabajo, guardarlo en la sesión
        if 'workflow' in response:
            session['current_workflow'] = response['workflow']
            print("Se generó un flujo de trabajo")
        
        return jsonify(response)
    except Exception as e:
        import traceback
        print(f"Error en la función de chat: {e}")
        print(traceback.format_exc())
        return jsonify({
            "success": False,
            "message": f"Error al procesar el mensaje: {str(e)}",
            "error_details": traceback.format_exc()
        }), 500  # Código de estado HTTP 500 para indicar error del servidor
=======
    message = request.json.get('message', '')
    
    # Obtener historial de chat de la sesión o inicializar
    chat_history = session.get('chat_history', [])
    
    # Procesar con el agente de chat
    response = chat_agent.process_message(message, chat_history)
    
    # Actualizar historial de chat
    if 'chat_history' not in session:
        session['chat_history'] = []
    
    session['chat_history'].append({"role": "user", "content": message})
    session['chat_history'].append({"role": "assistant", "content": response.get('message', '')})
    
    # Si el agente generó un flujo de trabajo, guardarlo en la sesión
    if 'workflow' in response:
        session['current_workflow'] = response['workflow']
    
    return jsonify(response)

>>>>>>> 28d0d3447ac7e388ed3e475a36f07fee63525e6f
@app.route('/execute_workflow', methods=['POST'])
def execute_workflow():
    """Endpoint para ejecutar un flujo de trabajo."""
    data = request.json
    workflow_id = data.get('workflow_id')
    workflow = data.get('workflow')
    
    # Si se proporciona un ID pero no el flujo, intentar cargarlo
    if workflow_id and not workflow:
        workflow_path = workflows_dir / f"{workflow_id}.json"
        if workflow_path.exists():
            with open(workflow_path, 'r') as f:
                workflow = json.load(f)
        else:
            return jsonify({
                "success": False,
                "error": f"Flujo de trabajo con ID {workflow_id} no encontrado"
            })
    
    # Si no se proporciona el flujo, usar el guardado en la sesión
    if not workflow and 'current_workflow' in session:
        workflow = session['current_workflow']
    
    # Si aún no hay flujo, devolver error
    if not workflow:
        return jsonify({
            "success": False,
            "error": "No se ha proporcionado un flujo de trabajo para ejecutar"
        })
    
    # Ejecutar el flujo
    execution_result = executor.execute_workflow(workflow)
    
    # Generar un resumen de la ejecución
    summary = ""
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
    
    return jsonify({
        "success": execution_result["success"],
        "summary": summary,
        "execution_result": execution_result
    })

@app.route('/save_workflow', methods=['POST'])
def save_workflow():
    """Endpoint para guardar un flujo de trabajo."""
    data = request.json
    workflow = data.get('workflow')
    name = data.get('name', f"workflow_{int(time.time())}")
    
    if not workflow:
        return jsonify({
            "success": False,
            "error": "No se ha proporcionado un flujo de trabajo para guardar"
        })
    
    # Asegurarse de que el nombre es válido para un archivo
    name = "".join(c for c in name if c.isalnum() or c in "._- ")
    
    # Guardar metadatos
    workflow["name"] = data.get('name', workflow.get('name', name))
    workflow["description"] = data.get('description', workflow.get('description', ''))
    workflow["updated_at"] = int(time.time())
    
    # Guardar el flujo
    workflow_path = workflows_dir / f"{workflow['id']}.json"
    
    try:
        with open(workflow_path, 'w') as f:
            json.dump(workflow, f, indent=2)
        
        return jsonify({
            "success": True,
            "id": workflow['id'],
            "name": workflow['name']
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Error al guardar flujo de trabajo: {str(e)}"
        })

@app.route('/modules')
def modules_page():
    """Página para configurar módulos."""
    available_modules = module_registry.get_available_modules()
    configured_modules = module_registry.get_configured_modules()
    
    return render_template(
        'modules.html',
        modules=available_modules,
        configured_modules=list(configured_modules.keys())
    )

@app.route('/configure_module', methods=['POST'])
def configure_module():
    """Endpoint para configurar un módulo."""
    module_type = request.form.get('module_type')
    
    if not module_type:
        return jsonify({
            "success": False,
            "error": "Tipo de módulo no especificado"
        })
    
    # Recopilar configuración
    config = {k: v for k, v in request.form.items() if k != 'module_type'}
    
    # Guardar configuración
    success = module_registry.configure_module(module_type, config)
    
    return jsonify({
        "success": success,
        "module_type": module_type
    })

@app.route('/workflows')
def workflows_page():
    """Página para gestionar flujos de trabajo guardados."""
    workflows = []
    
    # Cargar todos los flujos guardados
    for workflow_file in workflows_dir.glob("*.json"):
        try:
            with open(workflow_file, 'r') as f:
                workflow = json.load(f)
                
                # Añadir información básica
                workflows.append({
                    "id": workflow["id"],
                    "name": workflow.get("name", workflow["id"]),
                    "description": workflow.get("description", ""),
                    "created_at": workflow.get("created_at", 0),
                    "updated_at": workflow.get("updated_at", workflow.get("created_at", 0))
                })
        except Exception as e:
            print(f"Error al cargar flujo de trabajo {workflow_file}: {e}")
    
    # Ordenar por fecha de actualización (más reciente primero)
    workflows.sort(key=lambda x: x["updated_at"], reverse=True)
    
    return render_template('workflows.html', workflows=workflows)

@app.route('/workflow/<workflow_id>')
def view_workflow(workflow_id):
    """Página para ver un flujo de trabajo específico."""
    workflow_path = workflows_dir / f"{workflow_id}.json"
    
    if not workflow_path.exists():
        return redirect(url_for('workflows_page'))
    
    try:
        with open(workflow_path, 'r') as f:
            workflow = json.load(f)
        
        # Generar visualización
        visualization = flow_generator.visualize_workflow(workflow)
        
        return render_template(
            'view_workflow.html',
            workflow=workflow,
            visualization=visualization
        )
    except Exception as e:
        print(f"Error al cargar flujo de trabajo {workflow_id}: {e}")
        return redirect(url_for('workflows_page'))

# API endpoints
@app.route('/api/module_config/<module_type>', methods=['GET'])
def get_module_config(module_type):
    """API para obtener configuración de un módulo."""
    module = module_registry.get_module(module_type)
    
    if not module:
        return jsonify({
            "success": False,
            "error": f"Módulo {module_type} no encontrado"
        })
    
    # Obtener esquema de configuración
    schema = module.get_config_schema()
    
    # Obtener capacidades
    capabilities = module.get_capabilities()
    
    return jsonify({
        "success": True,
        "config": module.config,
        "schema": schema,
        "capabilities": capabilities
    })

@app.route('/api/module_config/<module_type>', methods=['DELETE'])
def delete_module_config(module_type):
    """API para eliminar configuración de un módulo."""
    config_path = module_configs_dir / f"{module_type}.json"
    
    if not config_path.exists():
        return jsonify({
            "success": False,
            "error": f"Configuración de módulo {module_type} no encontrada"
        })
    
    try:
        config_path.unlink()
        
        # Recargar módulos
        module_registry.discover_modules()
        
        return jsonify({
            "success": True
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Error al eliminar configuración: {str(e)}"
        })

@app.route('/api/test_module/<module_type>', methods=['POST'])
def test_module(module_type):
    """API para probar configuración de un módulo."""
    config = request.json
    
    if not config:
        return jsonify({
            "success": False,
            "error": "No se ha proporcionado configuración para probar"
        })
    
    # En una implementación real, aquí se probaría la conexión del módulo
    # Para esta demo, simulamos una respuesta exitosa
    
    return jsonify({
        "success": True,
        "message": "Conexión exitosa al módulo"
    })

@app.route('/api/recent_workflows', methods=['GET'])
def get_recent_workflows():
    """API para obtener flujos de trabajo recientes."""
    workflows = []
    
    # Cargar todos los flujos guardados
    for workflow_file in workflows_dir.glob("*.json"):
        try:
            with open(workflow_file, 'r') as f:
                workflow = json.load(f)
                
                # Añadir información básica
                workflows.append({
                    "id": workflow["id"],
                    "name": workflow.get("name", workflow["id"]),
                    "created_at": workflow.get("created_at", 0)
                })
        except Exception as e:
            print(f"Error al cargar flujo de trabajo {workflow_file}: {e}")
    
    # Ordenar por fecha de creación (más reciente primero) y limitar a 5
    workflows.sort(key=lambda x: x["created_at"], reverse=True)
    workflows = workflows[:5]
    
    return jsonify({
        "success": True,
        "workflows": workflows
    })

@app.route('/api/workflow_diagram/<workflow_id>', methods=['GET'])
def get_workflow_diagram(workflow_id):
    """API para obtener diagrama de un flujo de trabajo."""
    workflow_path = workflows_dir / f"{workflow_id}.json"
    
    if not workflow_path.exists():
        return jsonify({
            "success": False,
            "error": f"Flujo de trabajo {workflow_id} no encontrado"
        })
    
    try:
        with open(workflow_path, 'r') as f:
            workflow = json.load(f)
        
        # Generar visualización
        visualization = flow_generator.visualize_workflow(workflow)
        
        return jsonify({
            "success": True,
            "diagram": f'<div class="mermaid">{visualization}</div>'
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Error al generar diagrama: {str(e)}"
        })

@app.route('/api/workflow/<workflow_id>', methods=['DELETE'])
def delete_workflow(workflow_id):
    """API para eliminar un flujo de trabajo."""
    workflow_path = workflows_dir / f"{workflow_id}.json"
    
    if not workflow_path.exists():
        return jsonify({
            "success": False,
            "error": f"Flujo de trabajo {workflow_id} no encontrado"
        })
    
    try:
        workflow_path.unlink()
        
        return jsonify({
            "success": True
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Error al eliminar flujo de trabajo: {str(e)}"
        })

<<<<<<< HEAD

@app.route('/test_api', methods=['GET'])
def test_api():
    """Endpoint de prueba para verificar la conexión con OpenAI."""
    try:
        # Cargar variables de entorno de nuevo
        from dotenv import load_dotenv
        load_dotenv()
        
        # Obtener y mostrar variables de entorno
        api_key = os.getenv("OPENAI_API_KEY", "")
        model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        
        # Configurar OpenAI con la API key
        openai.api_key = api_key
        
        # Realizar una llamada simple
        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "system", "content": "Eres un asistente útil."},
                {"role": "user", "content": "Responde solo con 'La API funciona correctamente'."}
            ]
        )
        
        # Extraer respuesta
        message = response.choices[0].message["content"]
        
        # Retornar estado exitoso
        return jsonify({
            "success": True,
            "message": message,
            "api_key_status": "Configurada correctamente",
            "model": model,
            "openai_version": openai.__version__
        })
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        
        # Retornar error
        return jsonify({
            "success": False,
            "error": str(e),
            "error_details": error_details,
            "api_key": api_key[:5] + "..." if api_key else "No configurada",
            "model": model,
            "openai_version": openai.__version__
        })
    

if __name__ == '__main__':
    port = int(os.getenv("PORT", 5000))
    debug = os.getenv("DEBUG", "True").lower() == "true"
    app.run(host='0.0.0.0', port=port, debug=debug)
=======
if __name__ == '__main__':
    port = int(os.getenv("PORT", 5000))
    debug = os.getenv("DEBUG", "True").lower() == "true"
    from flask import Flask, render_template, request, jsonify, session, redirect, url_for
>>>>>>> 28d0d3447ac7e388ed3e475a36f07fee63525e6f

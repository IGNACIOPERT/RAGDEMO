import sys
import importlib.metadata

try:
    # Obtener información sobre el paquete openai
    openai_version = importlib.metadata.version('openai')
    print(f"Versión de OpenAI: {openai_version}")
    
    # Verificar si estamos usando la versión antigua o nueva
    if openai_version.startswith('0.'):
        print("Estás usando la versión ANTIGUA de la API de OpenAI (v0.x)")
        print("Esta versión utiliza openai.ChatCompletion.create()")
        
        # Verificar si podemos importar el módulo correctamente
        import openai
        print("✅ Módulo OpenAI importado correctamente")
        
        # Verificar creación de ChatCompletion
        if hasattr(openai, 'ChatCompletion'):
            print("✅ openai.ChatCompletion está disponible")
        else:
            print("❌ openai.ChatCompletion no está disponible")
            
    else:
        print("Estás usando la versión NUEVA de la API de OpenAI (v1.x+)")
        print("Esta versión utiliza openai.OpenAI().chat.completions.create()")
        
        # Verificar si podemos importar el módulo correctamente
        import openai
        print("✅ Módulo OpenAI importado correctamente")
        
        # Verificar creación de chat completions
        if hasattr(openai, 'OpenAI'):
            print("✅ openai.OpenAI está disponible")
        else:
            print("❌ openai.OpenAI no está disponible")
    
    # Importar otros módulos relevantes para verificar su disponibilidad
    print("\nVerificando dependencias adicionales:")
    
    modules_to_check = [
        'flask', 'dotenv', 'json', 'pathlib'
    ]
    
    for module_name in modules_to_check:
        try:
            module = __import__(module_name)
            version = getattr(module, '__version__', 'Desconocida')
            print(f"✅ {module_name}: {version}")
        except ImportError:
            print(f"❌ {module_name}: No instalado")
    
    # Verificar Python
    print(f"\nVersión de Python: {sys.version}")
    
except Exception as e:
    print(f"Error al verificar la versión de OpenAI: {e}")
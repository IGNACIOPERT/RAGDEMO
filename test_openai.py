import os
from dotenv import load_dotenv
import openai

# Cargar variables de entorno
print("Cargando variables de entorno...")
load_dotenv()

# Obtener la API key de OpenAI
api_key = os.getenv("OPENAI_API_KEY")
print(f"API Key (primeros 10 caracteres): {api_key[:10]}...")

# Configurar la API key
openai.api_key = api_key

try:
    # Realizar una llamada simple
    print("Realizando llamada a OpenAI...")
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Eres un asistente útil."},
            {"role": "user", "content": "Di 'Hola, la API está funcionando!' para confirmar que todo está bien."}
        ]
    )
    
    # Mostrar la respuesta
    print("Respuesta recibida:")
    print(response.choices[0].message["content"])
    
    print("\n✅ La API de OpenAI funciona correctamente!")
    
except Exception as e:
    print(f"\n❌ Error al llamar a la API de OpenAI: {str(e)}")
    
    # Mostrar información adicional para depuración
    print("\nInformación de depuración:")
    print(f"Versión de openai: {openai.__version__}")
    print(f"API key configurada: {'Sí' if openai.api_key else 'No'}")
    
    # Comprobar si la API key tiene el formato correcto
    if api_key and not api_key.startswith('sk-'):
        print("⚠️ La API key no tiene el formato correcto. Debería comenzar con 'sk-'")
import os
import glob

def search_openai_api_key_in_files():
    # Patrones que queremos buscar
    patterns = ["openai.api_key", "OPENAI_API_KEY"]
    findings = []
    
    # Buscar todos los archivos Python en el directorio actual y subdirectorios
    python_files = glob.glob('./**/*.py', recursive=True)
    
    for file_path in python_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                
                # Verificar si alguno de los patrones está en el contenido
                for pattern in patterns:
                    if pattern in content:
                        findings.append({
                            'file': file_path,
                            'pattern': pattern
                        })
        except Exception as e:
            findings.append({
                'file': file_path,
                'error': str(e)
            })
    
    return findings

# Ejecutar la búsqueda
results = search_openai_api_key_in_files()

# Mostrar los resultados
if results:
    print("Archivos con referencias a la API key de OpenAI:")
    for result in results:
        if 'error' in result:
            print(f"  Error al analizar {result['file']}: {result['error']}")
        else:
            print(f"  {result['file']}: contiene '{result['pattern']}'")
else:
    print("No se encontraron referencias a la API key de OpenAI.")
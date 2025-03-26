import os
from dotenv import load_dotenv
import sys

# Añadir directorio raíz al path para estar seguros
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Cargar variables de entorno
print("Intentando cargar variables de entorno...")
load_dotenv()

print("\n===== Variables de OpenAI =====")
openai_key = os.getenv("OPENAI_API_KEY", "No encontrada")
openai_model = os.getenv("OPENAI_MODEL", "No encontrado")

print(f"OPENAI_API_KEY: {openai_key[:5]}{'*' * 20}")
print(f"OPENAI_MODEL: {openai_model}")

print("\n===== Variables de Google Drive =====")
gmail_client_id = os.getenv("GMAIL_CLIENT_ID", "No encontrado")
gmail_client_secret = os.getenv("GMAIL_CLIENT_SECRET", "No encontrado")
gmail_refresh_token = os.getenv("GMAIL_REFRESH_TOKEN", "No encontrado")
gmail_access_token = os.getenv("GMAIL_ACCESS_TOKEN", "No encontrado")

print(f"GMAIL_CLIENT_ID: {'Configurado' if gmail_client_id != 'No encontrado' else 'No encontrado'}")
print(f"GMAIL_CLIENT_SECRET: {'Configurado' if gmail_client_secret != 'No encontrado' else 'No encontrado'}")
print(f"GMAIL_REFRESH_TOKEN: {'Configurado' if gmail_refresh_token != 'No encontrado' else 'No encontrado'}")
print(f"GMAIL_ACCESS_TOKEN: {'Configurado' if gmail_access_token != 'No encontrado' else 'No encontrado'}")

print("\n===== Otras variables =====")
debug = os.getenv("DEBUG", "No encontrado")
port = os.getenv("PORT", "No encontrado")
secret_key = os.getenv("SECRET_KEY", "No encontrado")

print(f"DEBUG: {debug}")
print(f"PORT: {port}")
print(f"SECRET_KEY: {'Configurado' if secret_key != 'No encontrado' else 'No encontrado'}")

# Verificar ubicación del archivo .env
import pathlib
current_dir = pathlib.Path(__file__).parent.absolute()
env_path = current_dir / ".env"

print("\n===== Ubicación del archivo .env =====")
print(f"Directorio actual: {current_dir}")
print(f"Archivo .env: {'Existe' if env_path.exists() else 'No existe'} en {env_path}")

# Listar archivos en el directorio actual
print("\n===== Archivos en el directorio actual =====")
for file in current_dir.iterdir():
    if file.is_file() and (file.name.startswith('.env') or file.name == '.env'):
        print(f"- {file.name}")
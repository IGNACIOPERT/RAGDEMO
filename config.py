import os
from dotenv import load_dotenv
from pathlib import Path

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Directorio base del proyecto
BASE_DIR = Path(__file__).parent

# Configuración general
DEBUG = os.getenv('DEBUG', 'True') == 'True'
SECRET_KEY = os.getenv('SECRET_KEY', os.urandom(24))
PORT = int(os.getenv('PORT', 5000))

# Configuración de directorios
DATA_DIR = BASE_DIR / 'data'
MODULE_CONFIGS_DIR = DATA_DIR / 'module_configs'
WORKFLOWS_DIR = DATA_DIR / 'workflows'
USER_DATA_DIR = DATA_DIR / 'user_data'

# Asegurar que los directorios existan
for directory in [MODULE_CONFIGS_DIR, WORKFLOWS_DIR, USER_DATA_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# Configuración de OpenAI
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
OPENAI_MODEL = os.getenv('OPENAI_MODEL', 'gpt-4')

# Configuración de MongoDB (Para almacenar configuraciones y flujos de trabajo)
MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/')
MONGODB_DB = os.getenv('MONGODB_DB', 'rag_modular')

# Configuración de módulos
AVAILABLE_MODULES = [
    'gmail',
    'whatsapp',
    'excel',
    'vector_db',
    'chatgpt',
<<<<<<< HEAD
    'embedding',
    'drive'  # Nuestro nuevo módulo
=======
    'embedding'
>>>>>>> 28d0d3447ac7e388ed3e475a36f07fee63525e6f
]

# Configuración específica para módulos
MODULE_CONFIGS = {
    'gmail': {
        'required_fields': ['client_id', 'client_secret', 'refresh_token'],
        'optional_fields': ['user_email']
    },
    'whatsapp': {
        'required_fields': ['api_key'],
        'optional_fields': ['phone_number']
    },
    'excel': {
        'required_fields': [],
        'optional_fields': ['default_directory']
    },
    'vector_db': {
        'required_fields': ['connection_string'],
        'optional_fields': ['collection_name']
    },
    'chatgpt': {
        'required_fields': ['api_key'],
        'optional_fields': ['model']
    },
    'embedding': {
        'required_fields': ['api_key'],
        'optional_fields': ['model', 'dimension']
<<<<<<< HEAD
    },
    'drive': {
        'required_fields': ['client_id', 'client_secret', 'refresh_token', 'access_token'],
        'optional_fields': ['user_email']
=======
>>>>>>> 28d0d3447ac7e388ed3e475a36f07fee63525e6f
    }
}
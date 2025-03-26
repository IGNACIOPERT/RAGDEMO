import sys
from pathlib import Path
from modules import discover_modules, get_module_class

# Descubrir módulos
modules = discover_modules()
print(f"Módulos descubiertos: {modules}")

# Intentar cargar el módulo de Drive específicamente
if 'drive' in modules:
    try:
        drive_class = get_module_class('drive')
        print(f"Clase Drive: {drive_class}")
        if drive_class:
            drive_instance = drive_class()
            print(f"Instancia Drive creada: {drive_instance}")
            print(f"Capacidades: {drive_instance.get_capabilities()}")
    except Exception as e:
        print(f"Error al cargar el módulo Drive: {e}")
else:
    print("El módulo 'drive' no fue descubierto.")
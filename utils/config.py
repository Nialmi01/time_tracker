import os
import json

def load_config():
    """Carga la configuración de la aplicación"""
    config_path = 'config.json'
    
    # Si el archivo de configuración no existe, crear uno con valores por defecto
    if not os.path.exists(config_path):
        default_config = {
            'database_path': 'data/employee_tracker.db',
            'app_name': 'Employee Time Tracker',
            'refresh_interval': 30,  # segundos
            'auto_logout': 60  # minutos
        }
        
        with open(config_path, 'w') as f:
            json.dump(default_config, f, indent=4)
        
        return default_config
    
    # Leer configuración existente
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
        return config
    except Exception as e:
        print(f"Error al cargar configuración: {e}")
        return {
            'database_path': 'data/employee_tracker.db',
            'app_name': 'Employee Time Tracker',
            'refresh_interval': 30,
            'auto_logout': 60
        }
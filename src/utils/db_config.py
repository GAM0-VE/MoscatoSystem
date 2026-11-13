import os
import json
import logging
from src.utils.paths import get_project_root

CONFIG_FILE = os.path.join(get_project_root(), "db_config.json")
def load_db_config():
    """Carga la configuración de la base de datos y la aplica al entorno."""
    if not os.path.exists(CONFIG_FILE):
        logging.info("Archivo de configuración de base de datos no encontrado. Se usarán valores por defecto.")
        return

    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            config = json.load(f)
            for key, value in config.items():
                os.environ[key] = str(value)
        logging.info("Configuración de base de datos cargada exitosamente.")
    except Exception as e:
        logging.error(f"Error al cargar la configuración de la base de datos: {e}")

def get_current_config():
    """Obtiene la configuración actual (de variables de entorno o archivo)."""
    return {
        "host": os.getenv("DB_HOST", "127.0.0.1"),
        "port": os.getenv("DB_PORT", "3306"),
        "user": os.getenv("DB_USER", "root"),
        "password": os.getenv("DB_PASSWORD", ""),
        "database": os.getenv("DB_NAME", "moscato_db")
    }

def initialize_database():
    """Conecta a MySQL e inicializa la base de datos si no existe, usando moscato.sql."""
    import mysql.connector
    import sys
    
    config = get_current_config()
    db_name = config.pop("database")
    
    try:
        # Connect without specifying database to check/create it
        conn = mysql.connector.connect(**config, connection_timeout=4)
        cursor = conn.cursor()
        
        cursor.execute("SHOW DATABASES LIKE %s", (db_name,))
        if cursor.fetchone():
            logging.info(f"La base de datos '{db_name}' ya existe.")
            cursor.close()
            conn.close()
            return

        logging.info(f"La base de datos '{db_name}' no existe. Creando e inicializando desde moscato.sql...")
        
        # Locate moscato.sql
        if getattr(sys, 'frozen', False):
            sql_path = os.path.join(sys._MEIPASS, "moscato.sql")
        else:
            sql_path = os.path.join(get_project_root(), "moscato.sql")
            
        if not os.path.exists(sql_path):
            logging.error(f"No se encontró el archivo {sql_path} para inicializar la BD.")
            cursor.close()
            conn.close()
            return
            
        with open(sql_path, "r", encoding="utf-8") as file:
            sql_script = file.read()
            
        # Execute statements
        for statement in sql_script.split(';'):
            if statement.strip():
                try:
                    cursor.execute(statement)
                except Exception as e:
                    logging.warning(f"Error ejecutando consulta de inicialización: {e}")
                    
        conn.commit()
        cursor.close()
        conn.close()
        logging.info("Base de datos inicializada correctamente.")
    except Exception as e:
        logging.error(f"Error fatal durante la inicialización de la base de datos: {e}")

def save_db_config(host, port, user, password, database):
    """Guarda la configuración de la base de datos en un archivo JSON."""
    config = {
        "DB_HOST": host,
        "DB_PORT": port,
        "DB_USER": user,
        "DB_PASSWORD": password,
        "DB_NAME": database
    }
    
    try:
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=4)
        
        # Actualizar entorno inmediatamente
        for key, value in config.items():
            os.environ[key] = str(value)
        
        logging.info("Configuración de base de datos guardada exitosamente.")
        return True, "Configuración guardada correctamente."
    except Exception as e:
        logging.error(f"Error al guardar la configuración: {e}")
        return False, f"Error al guardar: {e}"


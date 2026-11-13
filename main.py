import logging
from src.core.app import MoscatoApp
from src.utils.db_config import load_db_config, initialize_database

import os
from src.utils.paths import get_project_root

def setup_logging() -> None:
    log_path = os.path.join(get_project_root(), "app.log")
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_path, mode="a", encoding="utf-8"),
            logging.StreamHandler()
        ]
    )

def main() -> None:
    setup_logging()
    logging.info("Iniciando aplicación Moscato...")
    
    # Cargar configuración de base de datos y LAN
    load_db_config()
    
    # Inicializar la base de datos si no existe
    initialize_database()

    app = MoscatoApp()
    app.mainloop()

if __name__ == "__main__":
    main()
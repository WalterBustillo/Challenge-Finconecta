from loguru import logger
import sys
from config.settings import settings

def configure_logging():
    """
    Configura el sistema de logging con Loguru
    """
    logger.remove()  # Remove default handler
    
    # Configuración básica del logger
    logger.add(
        sys.stderr,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
        level="INFO"
    )
    
    # Configuración de log a archivo
    logger.add(
        settings.LOG_FILE,
        rotation="10 MB",  # Rotar archivo cada 10MB
        retention="30 days",  # Conservar logs por 30 días
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
        level="DEBUG",
        encoding="utf-8"
    )
    
    return logger

# Inicializar el logger al importar el módulo
logger = configure_logging()

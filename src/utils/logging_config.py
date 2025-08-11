from loguru import logger
import sys
from config.settings import settings

def configure_logging():
    """
    Configura el sistema de logging con Loguru
    """
    logger.remove()  # Remove default handler
    
    # Configure basic handler
    logger.add(
        sys.stderr,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
        level="INFO"
    )
    
    # Configure log to file
    logger.add(
        settings.LOG_FILE,
        rotation="10 MB",  # rotate file 10mb
        retention="30 days",  # conserve log for 30 days
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
        level="DEBUG",
        encoding="utf-8"
    )
    
    return logger

# Lauch logger
logger = configure_logging()

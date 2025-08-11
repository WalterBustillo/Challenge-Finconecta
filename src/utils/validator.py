import pandas as pd
from datetime import datetime
from loguru import logger
from typing import Dict, List, Optional

class DataValidator:
    """
    Clase para validar datos durante el proceso ETL
    """
    
    def __init__(self, schema: Optional[Dict] = None):
        """
        Inicializa el validador con un esquema opcional
        """
        self.schema = schema or {}
    
    def validate_types(self, data: pd.DataFrame) -> bool:
        """
        Valida que los tipos de datos coincidan con el esquema
        
        Args:
            data: DataFrame a validar
            
        Returns:
            bool: True si todos los tipos coinciden, False en caso contrario
        """
        if not self.schema:
            logger.warning("No schema defined, skipping type validation")
            return True
            
        valid = True
        for column, expected_type in self.schema.items():
            if column not in data.columns:
                logger.error(f"Column {column} not found in data")
                valid = False
                continue
                
            actual_type = str(data[column].dtype)
            
            # Mapeo de tipos pandas a tipos simples
            type_mapping = {
                'object': 'str',
                'int64': 'int',
                'float64': 'float',
                'datetime64[ns]': 'datetime',
                'bool': 'bool'
            }
            
            actual_simple = type_mapping.get(actual_type, actual_type)
            
            if actual_simple != expected_type:
                logger.error(f"Type mismatch in column {column}: expected {expected_type}, got {actual_simple}")
                valid = False
                
        return valid
    

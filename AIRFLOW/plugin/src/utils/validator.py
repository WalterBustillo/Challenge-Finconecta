import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../plugin'))
import pandas as pd
from datetime import datetime
from loguru import logger
from typing import Dict, List, Optional

class DataValidator:
    
    #Class to validate data during ETL process
    
    def __init__(self, schema: Optional[Dict] = None):
    
        self.schema = schema or {}
    
    def validate_types(self, data: pd.DataFrame) -> bool:

        #Validate dato types
    
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
            
            # Data Type map
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
    

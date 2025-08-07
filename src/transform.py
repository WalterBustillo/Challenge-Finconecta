import pandas as pd
from datetime import datetime
from loguru import logger
from utils.logging_config import logger

def transform_data(data: pd.DataFrame) -> pd.DataFrame:
    """
    Transform the extracted data
  
    Returns:
        pandas.DataFrame: Transformed data
    """
    try:
        logger.info("Starting data transformation")
        
        # Make a copy to avoid SettingWithCopyWarning
        transformed = data.copy()
         
        # Convert string dates to datetime objects
        date_columns = [col for col in transformed.columns if 'date' in col.lower()]
        for col in date_columns:
            transformed[col] = pd.to_datetime(transformed[col], errors='coerce')
        
        # Normalize string columns (trim whitespace, lowercase, etc.)
        string_columns = transformed.select_dtypes(include=['object']).columns
        for col in string_columns:
            transformed[col] = transformed[col].str.strip().str.lower()
        
        # Convert numeric columns (handle non-numeric values)
        numeric_columns = [col for col in transformed.columns if 'amount' in col.lower() or 'price' in col.lower()]
        for col in numeric_columns:
            transformed[col] = pd.to_numeric(transformed[col], errors='coerce')
        
        # Add metadata
        transformed['etl_processed_at'] = datetime.now()
        
        logger.info("Data transformation completed successfully")
        return transformed
        
    except Exception as e:
        logger.error(f"Error during transformation: {str(e)}")
        raise

import pandas as pd
from config.settings import settings
from loguru import logger

def extract_data(file_path: str, file_type: str) -> pd.DataFrame:
    """
    Extract data from CSV
    
    Returns:
        pandas.DataFrame: Extracted data
    """
    try:
        logger.info(f"Extracting data from {file_path}")
        
        if file_type == 'csv':
            data = pd.read_csv(file_path)
        else:
            raise ValueError("Unsupported file type. Use 'csv'")
            
        logger.info(f"Successfully extracted {len(data)} records")
        return data
        
    except Exception as e:
        logger.error(f"Error during extraction: {str(e)}")
        raise

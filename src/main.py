from src.extract import extract_data
from src.transform import transform_data
from src.load import load_to_mongodb
from config.settings import settings
from loguru import logger
from src.utils.logging_config import logger

def run_etl_pipeline():
    """
    Main function to run the ETL pipeline
    """
    try:
        #logger.info("Starting ETL Pipeline")
        
        # Extract
        print(settings.INPUT_FILE)
        raw_data = extract_data(settings.INPUT_FILE, settings.FILE_TYPE)
        print (raw_data.head())
        """
        # Transform
        transformed_data = transform_data(raw_data)
        
        # Load
        load_result = load_to_mongodb(transformed_data)
        
        logger.info("ETL Pipeline completed successfully")
        
        return load_result
        """

    except Exception as e:
        #logger.error(f"ETL Pipeline failed: {str(e)}")
        raise

if __name__ == "__main__":
    run_etl_pipeline()

from pymongo import MongoClient
from pandas import DataFrame
import pandas as pd
from config.settings import settings
from loguru import logger
from src.utils.logging_config import logger

def load_to_mongodb(data: DataFrame, collection_name: str = None):
    """
    Load transformed data into MongoDB
    """
    try:
        logger.info("Starting data load to MongoDB")
        # Connect to MongoDB
        client = MongoClient(settings.MONGO_URI)
        db = client[settings.MONGO_DB]
        collection = db[collection_name or settings.MONGO_COLLECTION]
        
        # Convert DataFrame to dictionary records
        data = data.where(pd.notnull(data), None)
        records = data.to_dict('records')

        for record in records:
            for k, v in record.items():
                if pd.isna(v):  # catches both np.nan and pd.NaT
                    record[k] = None
        
        # Insert records
        result = collection.insert_many(records)
        
        logger.info(f"Successfully loaded {len(result.inserted_ids)} records to MongoDB")
        return result
        
    except Exception as e:
        logger.error(f"Error during MongoDB load: {str(e)}")
        raise
    finally:
        client.close()

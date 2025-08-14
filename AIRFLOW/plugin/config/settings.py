import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../plugin'))
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # MongoDB Configuration
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://172.27.48.1:27017/")
    MONGO_DB = os.getenv("MONGO_DB", "etl_database")
    MONGO_COLLECTION = os.getenv("MONGO_COLLECTION", "etl_collection")
    MONGO_COLLECTION_test = os.getenv("MONGO_COLLECTION_test", "test_collection")
    
    # File Configuration
    INPUT_FILE = os.getenv("INPUT_FILE", "plugin/data/sample_data.csv")
    FILE_TYPE = os.getenv("FILE_TYPE", "csv") 
    
    # Logging Configuration
    LOG_FILE = os.getenv("LOG_FILE", "etl_pipeline.log")

settings = Settings()

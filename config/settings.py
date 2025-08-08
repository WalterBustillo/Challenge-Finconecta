import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # MongoDB Configuration
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
    MONGO_DB = os.getenv("MONGO_DB", "etl_database")
    MONGO_COLLECTION = os.getenv("MONGO_COLLECTION", "etl_collection")
    
    # File Configuration
    INPUT_FILE = os.getenv("INPUT_FILE", "data/dirty_cafe_sales.csv")
    FILE_TYPE = os.getenv("FILE_TYPE", "csv") 
    
    # Logging Configuration
    LOG_FILE = os.getenv("LOG_FILE", "etl_pipeline.log")

settings = Settings()

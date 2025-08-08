import pandas as pd
import numpy as np
from datetime import datetime
from loguru import logger
from src.utils.logging_config import logger

def transform_data(data: pd.DataFrame) -> pd.DataFrame:
    """
    Transform the extracted data
  
    Returns:
        pandas.DataFrame: Transformed data
    """
    try:
        logger.info("Starting data transformation")
        
        # Make a copy 
        transformed = data.copy()

        # See the dataset info 
        print (transformed.info())

        # The columns header we will make all lower and replace the  spaces for "_"
        transformed.columns = transformed.columns.str.replace(' ', '_').str.lower()

        #Convert columns to correct types
        transformed["quantity"] = pd.to_numeric(transformed["quantity"],errors="coerce")
        transformed["price_per_unit"] = pd.to_numeric(transformed["price_per_unit"],errors="coerce",downcast='float')
        transformed["total_spent"] = pd.to_numeric(transformed["total_spent"],errors="coerce",downcast='float')
        transformed['transaction_date'] = pd.to_datetime(transformed['transaction_date'], errors='coerce')
        transformed['year'] = transformed['transaction_date'].dt.year
        transformed['month'] = transformed['transaction_date'].dt.month
        transformed['day'] = transformed['transaction_date'].dt.day
        transformed['dayofweek'] = transformed['transaction_date'].dt.dayofweek
        transformed['hour'] = transformed['transaction_date'].dt.hour
        
        for col in transformed.columns:
            if col == "item" or col == "payment_method" or col == "location":
                unique_names = transformed[col].unique()
                print(col,unique_names)  

        # Clean items column convert error and unknown to NaN 
        transformed.replace(['UNKNOWN','ERROR'],np.nan, inplace=True) 
 
        # to fill the blank or error in the columns item and price_per_unit we will create a dictionary this the unique values of item and the avg prices per unit
        dictdb = transformed.dropna(subset=["price_per_unit"])
        dictdb = dictdb.groupby("item")["price_per_unit"].unique()
        print(dictdb)
        dict = dictdb.to_dict()
        print(dict)

        unique_prices = dictdb.apply(lambda x: [p for p in x if not pd.isna(p)])
        multiple_prices = unique_prices[unique_prices.apply(len) > 1]

        print("Items with multiple unique prices:", multiple_prices)

        logger.info("Data transformation completed successfully")
        return transformed
        
    except Exception as e:
        logger.error(f"Error during transformation: {str(e)}")
        raise

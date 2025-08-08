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
        print("Before cleaning\n",transformed.isna().mean().sort_values(ascending=False))

        # The columns header we will make all lower and replace the  spaces for "_"
        transformed.columns = transformed.columns.str.replace(' ', '_').str.lower()

        #Convert columns to correct types
        transformed["quantity"] = pd.to_numeric(transformed["quantity"],errors="coerce")
        transformed["price_per_unit"] = pd.to_numeric(transformed["price_per_unit"],errors="coerce",downcast='float')
        transformed["total_spent"] = pd.to_numeric(transformed["total_spent"],errors="coerce",downcast='float')
        transformed['transaction_date'] = pd.to_datetime(transformed['transaction_date'], errors='coerce')
        
        for col in transformed.columns:
            if col == "item" or col == "payment_method" or col == "location":
                unique_names = transformed[col].unique()
                #print(col,unique_names)  

        # to fill the blank or error in the columns item and price_per_unit we will create a dictionary this the unique values of item and the avg prices per unit
        
        dict = {'Coffee': 2.0,
                'Tea': 1.5,
                'Sandwich': 4.0,
                'Salad': 5.0,
                'Cake': 3.0,
                'Cookie': 1.0,
                'Smoothie': 4.0,
                'Juice': 3.0}
        
        #Fill NaN data to price_per_unit with the dict
        #print("NaN Before in price_per_unit",transformed['price_per_unit'].isna().sum())
        transformed['price_per_unit'] = transformed['price_per_unit'].fillna(transformed['item'].map(dict))
        #print("NaN After in price_per_unit",transformed['price_per_unit'].isna().sum())

        #Fill NaN data to total_spent
        #print("NaN Before in total_spent",transformed['total_spent'].isna().sum())
        aux_total = transformed['total_spent'].isna() & transformed['quantity'].notna() & transformed['price_per_unit'].notna()
        transformed.loc[aux_total, 'total_spent'] = transformed.loc[aux_total, 'quantity'] * transformed.loc[aux_total, 'price_per_unit']
        #print("NaN after in total_spent",transformed['total_spent'].isna().sum())

        #Fill NaN data to quantity
        #print("NaN Before in quantity",transformed['quantity'].isna().sum())
        aux_quantity = transformed['quantity'].isna() & transformed['total_spent'].notna() & transformed['price_per_unit'].notna()
        transformed.loc[aux_quantity, 'quantity'] = transformed.loc[aux_quantity, 'total_spent'] / transformed.loc[aux_quantity, 'price_per_unit']
        #print("NaN after in quantity",transformed['quantity'].isna().sum())    
        
        #Fill NaN data to price_per_unit
        #print("NaN Before in price_per_unit",transformed['price_per_unit'].isna().sum())
        aux_quantity = transformed['price_per_unit'].isna() & transformed['total_spent'].notna() & transformed['quantity'].notna()
        transformed.loc[aux_quantity, 'price_per_unit'] = transformed.loc[aux_quantity, 'total_spent'] / transformed.loc[aux_quantity, 'quantity']
        #print("NaN after in price_per_unit",transformed['price_per_unit'].isna().sum()) 
        
        dict_item = {  2.0: 'Coffee',
                                1.5: 'Tea',
                                5.0: 'Salad',
                                1.0: 'Cookie'}

        #Fill NaN data to item with the dict_item
        #print("NaN Before in item",transformed['item'].isna().sum())
        transformed['item'] = transformed['item'].fillna(transformed['price_per_unit'].map(dict_item))
        #print("NaN After in item",transformed['item'].isna().sum())

        # Clean items column convert error and unknown to NaN 
        transformed['payment_method'] = transformed['payment_method'].replace(['UNKNOWN', 'ERROR'], np.nan)
        transformed['location'] = transformed['location'].replace(['UNKNOWN', 'ERROR'], np.nan)
        transformed['transaction_date'] = transformed['transaction_date'].replace(['UNKNOWN', 'ERROR'], np.nan)

        print("After Cleaning\n",transformed.isna().mean().sort_values(ascending=False))
        """
        #Add more info about date
        transformed['year'] = transformed['transaction_date'].dt.year
        transformed['month'] = transformed['transaction_date'].dt.month
        transformed['day'] = transformed['transaction_date'].dt.day
        transformed['dayofweek'] = transformed['transaction_date'].dt.dayofweek
        transformed['hour'] = transformed['transaction_date'].dt.hour
        """ 
        logger.info("Data transformation completed successfully")

        return transformed
        
    except Exception as e:
        logger.error(f"Error during transformation: {str(e)}")
        raise

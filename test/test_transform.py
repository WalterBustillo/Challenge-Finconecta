import pytest
import pandas as pd
import numpy as np
from datetime import datetime
from src.transform import transform_data

class TestTransform:
    def setup_method(self):
        """Configuración inicial para cada prueba"""
        self.raw_data = pd.DataFrame({
            'Transaction ID': ['TXN_1961373','TXN_4977031','TXN_4271903','TXN_7034554','TXN_3160411'],
            'Item': ['Coffee','Cake','Cookie','Salad','Coffee'],
            'Quantity': ['2','4','4','2','2'],
            'Price Per Unit':['2.0','3.0','1.0','5.0','2.0'],
            'Total Spent': ['4.0','12.0','ERROR','10.0','4.0'],
            'Payment Method': ['Credit Card','Cash','Credit Card','UNKNOWN','Digital Wallet'],
            'Location': ['Takeaway','In-store','In-store','UNKNOWN','In-store'],
            'Transaction Date': ['2023-09-08','2023-05-16','2023-07-19','2023-04-27','2023-06-11']})
        
    def test_transform_data_types(self):
        """Test para conversión de tipos"""
        transformed = transform_data(self.raw_data)
        # verify columns names
        assert list(transformed.columns) == ['transaction_id','item','quantity','price_per_unit','total_spent','payment_method','location','transaction_date']
        # Verificar tipos
        
        assert pd.api.types.is_string_dtype(transformed['transaction_id'])
        assert pd.api.types.is_string_dtype(transformed['item'])
        assert pd.api.types.is_numeric_dtype(transformed['quantity'])
        assert pd.api.types.is_numeric_dtype(transformed['price_per_unit'])
        assert pd.api.types.is_numeric_dtype(transformed['total_spent'])
        assert pd.api.types.is_string_dtype(transformed['payment_method'])
        assert pd.api.types.is_string_dtype(transformed['location'])
        assert pd.api.types.is_datetime64_any_dtype(transformed['transaction_date'])
        
    def test_transform_string_cleaning(self):
        """Test para limpieza de strings"""
        transformed = transform_data(self.raw_data)
        
        # Verificar que los espacios en blanco fueron removidos
        assert transformed['total_spent'].tolist() == [4.0,12.0,4.0,10.0,4.0]
        assert transformed['payment_method'].tolist() == ['Credit Card','Cash','Credit Card',np.nan,'Digital Wallet']
    def test_transform_date_conversion(self):
        """Test para conversión de fechas"""
        transformed = transform_data(self.raw_data)
        
    
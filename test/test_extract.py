import pytest
import pandas as pd
import os
from src.extract import extract_data
from config.settings import settings

class TestExtract:
    @classmethod
    def setup_class(cls):
        """Configuración inicial para las pruebas"""
        cls.test_csv = "data/test_data.csv"

        """Create a temporary CSV file for testing."""
        test_df = pd.DataFrame({
            'Transaction ID': ['TXN_1961373','TXN_4977031','TXN_4271903','TXN_7034554','TXN_3160411'],
            'Item': ['Coffee','Cake','Cookie','Salad','Coffee'],
            'Quantity': ['2','4','4','2','2'],
            'Price Per Unit':['2.0','3.0','1.0','5.0','2.0'],
            'Total Spent': ['4.0','12.0','ERROR','10.0','4.0'],
            'Payment Method': ['Credit Card','Cash','Credit Card','UNKNOWN','Digital Wallet'],
            'Location': ['Takeaway','In-store','In-store','UNKNOWN','In-store'],
            'Transaction Date': ['2023-09-08','2023-05-16','2023-07-19','2023-04-27','2023-06-11']})
        
        test_df.to_csv(cls.test_csv, index=False)

    @classmethod
    def teardown_class(cls):
        """Limpieza después de las pruebas"""
        if os.path.exists(cls.test_csv):
            os.remove(cls.test_csv)
    
    def test_extract_csv(self):
        """Test para extracción de CSV"""
        df = extract_data(self.test_csv, 'csv')
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 5
        assert list(df.columns) == ['Transaction ID','Item','Quantity','Price Per Unit','Total Spent','Payment Method','Location','Transaction Date']
    
    def test_extract_invalid_file(self):
        """Test para archivo no existente"""
        with pytest.raises(Exception):
            extract_data("nonexistent.csv", 'csv')
    
    def test_extract_invalid_type(self):
        """Test para tipo de archivo no soportado"""
        with pytest.raises(ValueError):
            extract_data(self.test_csv, 'xml')


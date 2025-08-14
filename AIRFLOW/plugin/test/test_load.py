import pytest
import pandas as pd
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../plugin'))
from pymongo import MongoClient
from src.load import load_to_mongodb
from config.settings import settings

class TestLoad:
    @classmethod
    def setup_class(cls):
        #Initial configuration for test
        cls.test_data = pd.DataFrame({
            'Transaction ID': ['TXN_1961373','TXN_4977031','TXN_4271903','TXN_7034554','TXN_3160411'],
            'Item': ['Coffee','Cake','Cookie','Salad','Coffee'],
            'Quantity': ['2','4','4','2','2'],
            'Price Per Unit':['2.0','3.0','1.0','5.0','2.0'],
            'Total Spent': ['4.0','12.0','ERROR','10.0','4.0'],
            'Payment Method': ['Credit Card','Cash','Credit Card','UNKNOWN','Digital Wallet'],
            'Location': ['Takeaway','In-store','In-store','UNKNOWN','In-store'],
            'Transaction Date': ['2023-09-08','2023-05-16','2023-07-19','2023-04-27','2023-06-11']})
        
        # Use test database
        cls.test_db = "etl_database"
        cls.test_collection = "test_collection"
        
        # Conection to MongoDB
        cls.client = MongoClient(settings.MONGO_URI)
        cls.db = cls.client[cls.test_db]
    
    @classmethod
    def teardown_class(cls):
        
        # Cleaning after test
        cls.db.drop_collection(cls.test_collection)
        cls.client.close()
    
    def test_load_to_mongodb(self):

        #test load data to MongoDB
       
        result = load_to_mongodb(self.test_data, self.test_db, self.test_collection)
        
        assert len(result.inserted_ids) == 5
        
        # Verify data in MOongoDB
        collection = self.db[self.test_collection]
        docs = list(collection.find({}))
        
        assert len(docs) == 5
        assert docs[0]['Transaction ID'] == 'TXN_1961373'
        assert docs[1]['Item'] == 'Cake'
        assert docs[2]['Quantity'] == '4'
        assert docs[3]['Price Per Unit'] == '5.0'
        assert docs[4]['Total Spent'] == '4.0'
        assert docs[0]['Payment Method'] == 'Credit Card'
        assert docs[1]['Location'] == 'In-store'
        assert docs[2]['Transaction Date'] == '2023-07-19'
    
    def test_load_empty_data(self):

        #Test for mpty dataset
        empty_df = pd.DataFrame()
        
        with pytest.raises(Exception):
            load_to_mongodb(empty_df, self.test_collection)
    
    def test_load_invalid_connection(self):
        #test for invalid conection to MongoDB
        original_uri = settings.MONGO_URI
        settings.MONGO_URI = "mongodb://invalid:27017"
        
        with pytest.raises(Exception):
            load_to_mongodb(self.test_data, self.test_collection)
        
        # Restart original URI
        settings.MONGO_URI = original_uri
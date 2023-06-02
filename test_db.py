import pandas as pd
from data_read_module.data_reader import DataReader
from data_preprocessing_module.data_preprocessor import DataPreprocessor

def test_data_reader():
    # Initialize DataReader
    data_reader = DataReader("root", "qwe123", "localhost", "wuliu")

    # Table names for testing
    tables = ['Grid', 'User', 'Product', 'Warehouse', 'WarehouseProduct', 'Transportation', 'TransportationProduct', 'Demand', 'DemandProduct']

    # Read data from each table
    for table in tables:
        data = data_reader.read_data(table)
        assert isinstance(data, pd.DataFrame)
        print(f"Data from {table}:", data.head())

def test_data_preprocessor():
    # Initialize DataReader
    data_reader = DataReader("root", "qwe123", "localhost", "wuliu")

    # Initialize DataPreprocessor
    data_preprocessor = DataPreprocessor()

    # Test preprocessing with data from each table
    tables = ['Grid', 'User', 'Product', 'Warehouse', 'WarehouseProduct', 'Transportation', 'TransportationProduct', 'Demand', 'DemandProduct']
    for table in tables:
        raw_data = data_reader.read_data(table)
        processed_data = data_preprocessor.preprocess(raw_data)
        
        # Assert data types and equality of raw and processed data shapes
        assert isinstance(processed_data, pd.DataFrame)
        assert raw_data.shape[0] == processed_data.shape[0]  # Assumes preprocessing doesn't drop rows
        print(f"Processed data from {table}:", processed_data.head())

if __name__ == "__main__":
    print("Testing DataReader...")
    test_data_reader()

    print("Testing DataPreprocessor...")
    test_data_preprocessor()

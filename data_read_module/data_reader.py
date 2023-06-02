from sqlalchemy import create_engine
import pandas as pd

class DataReader:
    def __init__(self, username, password, hostname, database):
        self.engine = create_engine(f'mysql+pymysql://{username}:{password}@{hostname}/{database}')

    def read_data(self, table_name):
        query = f"SELECT * FROM {table_name}"
        df = pd.read_sql(query, self.engine)
        return df

from sklearn.preprocessing import MinMaxScaler

class DataPreprocessor:
    def __init__(self):
        self.scaler = MinMaxScaler()

    def preprocess(self, df):
        # Verify data integrity and consistency
        self._verify_data(df)

        # Calculate and verify the coverage range of each warehouse
        self._calculate_coverage(df)

        # Calculate and generate the cost function
        self._calculate_cost(df)

        return df

    def _verify_data(self, df):
        # Handle missing values
        df = self._handle_missing_values(df)

        # Remove duplicates
        df = self._remove_duplicates(df)

        # Scale numerical features
        df = self._scale_numerical_features(df)
        pass

    def _calculate_coverage(self, df):
        # Add your code to calculate and verify the coverage range of each warehouse here
        pass

    def _calculate_cost(self, df):
        # Add your code to calculate and generate the cost function here
        pass

    def _handle_missing_values(self, df):
        # Fill numeric columns with the mean
        numeric_columns = df.select_dtypes(include=['int64', 'float64']).columns
        for col in numeric_columns:
            df[col].fillna(df[col].mean(), inplace=True)
        
        # Fill categorical columns with the mode
        categorical_columns = df.select_dtypes(include=['object']).columns
        for col in categorical_columns:
            df[col].fillna(df[col].mode()[0], inplace=True)

        return df

    def _remove_duplicates(self, df):
        df.drop_duplicates(inplace=True)
        return df

    def _scale_numerical_features(self, df):
        numeric_columns = df.select_dtypes(include=['int64', 'float64']).columns
        df[numeric_columns] = self.scaler.fit_transform(df[numeric_columns])

        return df

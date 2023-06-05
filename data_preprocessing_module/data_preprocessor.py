from sklearn.preprocessing import MinMaxScaler
# data_preprocessing_module/data_preprocessor.py

#Spdd类用于表示单个订单。使用它将有助于更容易地进行数据管理和操作，例如根据不同的属性对订单进行排序或过滤。
#定义了Spdd类之后，你可以在data_preprocessor.py文件中使用它将原始数据转换为Spdd对象的列表。然后，将这些预处理后的数据用作优化模型的输入。
class Spdd:
    def __init__(self, ddnm, qynm, spnm, sl, lg, zwdpwcsj):
        self.ddnm = ddnm  # 订单内码
        self.qynm = qynm  # 提交商品订单企业内码
        self.spnm = spnm  # 商品内码
        self.sl = sl  # 商品数量
        self.lg = lg  # 量纲
        self.zwdpwcsj = zwdpwcsj  # 最晚商品调配完成时间
    @classmethod
    def from_dict(cls, data):
        return cls(**data)

class DPTJ:
    """
    调配推荐类
    """
    def __init__(self, ckbh, yhbh, spsl):
        """
        初始化方法

        :param ckbh: 仓库编号 (ChangKuBianHao)
        :param yhbh: 用户编号 (YongHuBianHao)
        :param spsl: 商品数量 (ShangPinShuLiang)
        """
        self.ckbh = ckbh
        self.yhbh = yhbh
        self.spsl = spsl

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

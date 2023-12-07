import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler

class DataPreparation:
    """
    Overview:
        データの前処理を行うクラス。
    """

    def load_CSVdata(self, file_path):
        """
        Overview:
            CSVからデータを読み込む。
        Parameters:
            file_path - CSVファイルのパス。
        Returns:
            データフレーム。
        """
        df = pd.read_csv(file_path)
        df['Date'] = pd.to_datetime(df['Date'])
        df = df.sort_values(by='Date')
        return df

    def preprocess_data(self, df):
        """
        Overview:
            データを標準化
        Parameters:
            df - データフレーム。
        Returns:
            標準化データ、スケーラー、元データ。
        """
        # 数値データの列だけを選択してカンマを削除し、float型に変換
        numerical_columns = df.select_dtypes(include=[object]).columns.difference(['Date'])
        df[numerical_columns] = df[numerical_columns].replace({',': ''}, regex=True).astype(float)

        dataset = df.select_dtypes(include=[np.number])

        if dataset.empty:
            print("This DataFrame is empty. Please check your data^^")
            return None,None,None

        scaler = StandardScaler()
        standardized_data = pd.DataFrame(scaler.fit_transform(dataset), columns=dataset.columns)
        return standardized_data, scaler

    def create_training_data(self, scaled_data, window_size=60):
        """
        Overview:
            訓練データを作成。
        Parameters:
            scaled_data - 正規化されたデータ。
            window_size - ウィンドウサイズ。
        Returns:
            x_train, y_train, 訓練データ長
        """
        train_data_len = int(np.ceil(len(scaled_data) * .8))
        train_data = scaled_data.values[0:int(train_data_len), :]
        x_train, y_train = [], []

        for i in range(window_size, len(train_data)):
            x_train.append(train_data[i-window_size:i, 1:])
            y_train.append(train_data[i, 1])

        x_train, y_train = np.array(x_train), np.array(y_train)

        return x_train, y_train, train_data_len


    def create_test_data(self, scaled_data, train_data_len, window_size=60):
        """
        Overview:
            テストデータを作成する
        Parameters:
            scaled_data - 正規化されたデータ。
            dataset - 元のデータセット。
            scaler - データを標準化するためのスケーラー。
            training_data_len - 訓練データの長さ。
            window_size - ウィンドウサイズ（デフォルトは60）。
        Returns:
            テストデータ（x_test, y_test）
        """
        scaled_data_np = scaled_data.to_numpy()
        test_data = scaled_data_np[train_data_len - window_size:, :]
        x_test = []

        y_test = scaled_data_np[train_data_len:, 1]

        for i in range(window_size, len(test_data)):
            x_test.append(test_data[i-window_size:i, 1:])

        x_test = np.array(x_test)

        return x_test, y_test






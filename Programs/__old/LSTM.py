"""
PlotLearning クラス:
    Overview:
        訓練中の学習曲線をリアルタイムでプロット。

DataPreparation クラス:
    load_CSVdata(file_path):
        Overview:
            CSVからデータを読み込む。
        Parameters:
            file_path - CSVファイルのパス。
        Returns:
            データフレーム。

    preprocess_data(df):
        Overview:
            データを正規化。
        Parameters:
            df - データフレーム。
        Returns:
            正規化データ、スケーラー、元データ。

    create_training_data(scaled_data, window_size=60):
        Overview:
            訓練データを作成。
        Parameters:
            scaled_data - 正規化されたデータ。
            window_size - ウィンドウサイズ。
        Returns:
            x_train, y_train, 訓練データ長。

ModelBuilder クラス:
    build_and_train_model(x_train, y_train):
        Overview:
            LSTMモデルを構築・訓練。
        Parameters:
            x_train, y_train - 訓練データ。
        Returns:
            訓練済みモデル。

ModelEvaluation クラス:
    make_predictions(model, x_test, scaler):
        Overview:
            予測を行う。
        Parameters:
            model - 訓練済みモデル。
            x_test - テストデータ。
            scaler - データスケーラー。
        Returns:
            予測値。

    calculate_rmse_and_r2(y_test, predictions):
        Overview:
            RMSEとR2スコアを計算。
        Parameters:
            y_test, predictions - 実際の値と予測値。
        Returns:
            RMSE, R2スコア。

DataVisualization クラス:
    plot_initial_data(df):
        Overview:
            初期データをプロット。
        Parameters:
            df - データフレーム。
        Returns:
            None。

    plot_data(train, valid, start_date, end_date):
        Overview:
            訓練・検証・予測データをプロット。
        Parameters:
            train, valid - 訓練データと検証データ。
            start_date, end_date - プロットする期間。
        Returns:
            None。

FuturePrediction クラス:
    predict_future_prices(model, latest_data, scaler, future_days=10, window_size=60):
        Overview:
            未来の価格を予測。
        Parameters:
            model - 訓練済みモデル。
            latest_data - 最新のデータ。
            scaler - データスケーラー。
            future_days - 予測する未来の日数。
            window_size - ウィンドウサイズ。
        Returns:
            未来の価格リスト。
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from datetime import datetime, timedelta
from sklearn.metrics import r2_score
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense, LSTM, Dropout
from keras.callbacks import Callback

class PlotLearning(Callback):
    """
    Overview:
        訓練中の学習曲線をリアルタイムでプロット。
    """

    def on_train_begin(self, logs={}):
        self.i = 0
        self.x = []
        self.losses = []
        self.val_losses = []
        self.errors = []
        self.val_errors = []
        self.fig = plt.figure(figsize=(16, 9))
        self.logs = []

    def on_epoch_end(self, epoch, logs={}):
        self.logs.append(logs)
        self.x.append(self.i)
        self.losses.append(logs.get('loss'))
        self.val_losses.append(logs.get('val_loss'))
        self.errors.append(logs.get('error'))
        self.val_errors.append(logs.get('val_error'))
        self.i += 1

        plt.clf()

        plt.subplot(1, 2, 1)
        plt.plot(self.x, self.losses, label="Train Loss (Cost)")
        plt.plot(self.x, self.val_losses, label="Validation Loss (Cost)")
        plt.legend()
        plt.title('Train and Validation Loss (Cost)')

        plt.subplot(1, 2, 2)
        plt.plot(self.x, self.errors, label="Train Error")
        plt.plot(self.x, self.val_errors, label="Validation Error")
        plt.legend()
        plt.title('Train and Validation Error')

        plt.draw()
        plt.pause(0.001)

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
        df.set_index('Date', inplace=True)

        df = df.sort_index()
        return df

    def preprocess_data(self, df):
        """
        Overview:
            データを正規化。
        Parameters:
            df - データフレーム。
        Returns:
            正規化データ、スケーラー、元データ。
        """
        data = df['Close'].str.replace(',', '').astype(float)
        dataset = data.values.reshape(-1, 1)
        scaler = MinMaxScaler(feature_range=(0,1))
        scaled_data = scaler.fit_transform(dataset)
        return scaled_data, scaler, dataset

    def create_training_data(self, scaled_data, window_size=60):
        """
        Overview:
            訓練データを作成。
        Parameters:
            scaled_data - 正規化されたデータ。
            window_size - ウィンドウサイズ。
        Returns:
            x_train, y_train, 訓練データ長。
        """
        training_data_len = int(np.ceil(len(scaled_data) * .8))
        train_data = scaled_data[0:int(training_data_len), :]
        x_train, y_train = [], []
        for i in range(window_size, len(train_data)):
            x_train.append(train_data[i-window_size:i, 0])
            y_train.append(train_data[i, 0])
        x_train, y_train = np.array(x_train), np.array(y_train)
        x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))
        return x_train, y_train, training_data_len

class ModelBuilder:
    """
    Overview:
        モデルの構築と訓練を行うクラス。
    """

    def build_and_train_model(self, x_train, y_train):
        """
        Overview:
            LSTMモデルを構築・訓練。
        Parameters:
            x_train, y_train - 訓練データ。
        Returns:
            訓練済みモデル。
        """
        model = Sequential()
        model.add(LSTM(units=50, return_sequences=True, input_shape=(x_train.shape[1], 1)))
        model.add(Dropout(0.2))
        model.add(LSTM(units=50, return_sequences=True))
        model.add(Dropout(0.2))
        model.add(LSTM(units=50, return_sequences=True))
        model.add(Dropout(0.2))
        model.add(LSTM(units=50))
        model.add(Dropout(0.2))
        model.add(Dense(units=1))
        model.compile(optimizer='adam', loss='mean_squared_error')

        plot_learning = PlotLearning()

        model.fit(x_train, y_train, batch_size=32, epochs=100, validation_split=0.2, callbacks=[plot_learning])
        return model

class ModelEvaluation:
    """
    Overview:
        モデルの評価を行うクラス。
    """

    def make_predictions(self, model, x_test, scaler):
        """
        Overview:
            予測を行う。
        Parameters:
            model - 訓練済みモデル。
            x_test - テストデータ。
            scaler - データスケーラー。
        Returns:
            予測値。
        """
        predictions = model.predict(x_test)
        predictions = scaler.inverse_transform(predictions)
        return predictions

    def calculate_rmse_and_r2(self, y_test, predictions):
        """
        Overview:
            RMSEとR2スコアを計算。
        Parameters:
            y_test, predictions - 実際の値と予測値。
        Returns:
            RMSE, R2スコア。
        """
        rmse = np.sqrt(np.mean(((predictions - y_test) ** 2)))
        r2 = r2_score(y_test, predictions)
        return rmse, r2

class DataVisualization:
    """
    Overview:
        データの可視化を行うクラス。
    """

    def plot_initial_data(self, df):
        """
        Overview:
            初期データをプロット。
        Parameters:
            df - データフレーム。
        Returns:
            None。
        """
        plt.figure(figsize=(16,6))
        plt.title('JPY/BTC Close Price History')
        plt.plot(df['Close'].str.replace(',', '').astype(float))
        plt.xlabel('Date', fontsize=14)
        plt.ylabel('Close Price JPY', fontsize=14)
        plt.show()


    def plot_data(self, train, valid, start_date, end_date):
        """
        Overview:
            訓練・検証・予測データをプロット。
        Parameters:
            train, valid - 訓練データと検証データ。
            start_date, end_date - プロットする期間。
        Returns:
            None。
        """
        train_filtered = train.loc[start_date:end_date]
        valid_filtered = valid.loc[start_date:end_date]
        plt.figure(figsize=(16,6))
        plt.title('Model')
        plt.xlabel('Date', fontsize=14)
        plt.ylabel('Close Price JPY', fontsize=14)
        plt.plot(train_filtered)
        plt.plot(valid_filtered[['Close', 'Predictions']])
        plt.legend(['Train', 'Val', 'Predictions'], loc='lower right')
        plt.show()

class FuturePrediction:
    """
    Overview:
        未来の価格を予測するクラス。
    """

    def predict_future_prices(self, model, latest_data, scaler, future_days=10, window_size=60):
        """
        Overview:
            未来の価格を予測。
        Parameters:
            model - 訓練済みモデル。
            latest_data - 最新のデータ。
            scaler - データスケーラー。
            future_days - 予測する未来の日数。
            window_size - ウィンドウサイズ。
        Returns:
            未来の価格リスト。
        """
        future_prices = []
        for _ in range(future_days):
            scaled_latest_data = scaler.transform(latest_data.reshape(-1, 1))
            x_future = []
            x_future.append(scaled_latest_data[-window_size:])
            x_future = np.array(x_future)
            x_future = np.reshape(x_future, (x_future.shape[0], x_future.shape[1], 1))
            future_price_scaled = model.predict(x_future)
            future_price = scaler.inverse_transform(future_price_scaled)
            future_prices.append(future_price[0][0])
            latest_data = np.append(latest_data, future_price)
            latest_data = latest_data[1:]
        return future_prices

def main():
    data_prep = DataPreparation()
    model_builder = ModelBuilder()
    model_eval = ModelEvaluation()
    data_viz = DataVisualization()

    file_path = 'D:\\Program\\仮想通貨情報収集\\CSV\\price-data.csv'
    save_path = 'D:\\Program\\仮想通貨情報収集\\model'

    # Load and preprocess data
    df = data_prep.load_data(file_path)
    scaled_data, scaler, dataset = data_prep.preprocess_data(df)

    # Create training data
    x_train, y_train, training_data_len = data_prep.create_training_data(scaled_data)

    # Build and train the model
    model = model_builder.build_and_train_model(x_train, y_train)

    # Save the trained model (Optional)
    # save_model(model, save_path)

    # Create test data
    x_test, y_test = data_prep.create_test_data(scaled_data, dataset, training_data_len)

    # Make predictions
    predictions = model_eval.make_predictions(model, x_test, scaler)

    # Calculate RMSE and R2 score
    rmse, r2s = model_eval.calculate_rmse_and_r2(y_test, predictions)
    print(f"RMSE: {rmse}")
    print(f"R2 Score: {r2s}")

    # Prepare data for plotting
    train = df['Close'].str.replace(',', '').astype(float)[:training_data_len]
    valid = df['Close'].str.replace(',', '').astype(float)[training_data_len:]
    valid = valid.to_frame()
    valid['Predictions'] = predictions

    # Plotting the final data
    start_date = '2023-01-01'
    end_date = '2023-08-31'
    data_viz.plot_data(train, valid, start_date, end_date)

if __name__ == "__main__":
    main()

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from datetime import datetime
from sklearn.metrics import r2_score
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense, LSTM, Dropout
from keras.callbacks import Callback

class PlotLearning(Callback):
    def on_train_begin(self, logs={}):
        self.i = 0
        self.x = []
        self.losses = []
        self.val_losses = []
        plt.ion()
        self.fig = plt.figure(figsize=(16, 9))
        self.logs = []

    def on_epoch_end(self, epoch, logs={}):

        self.logs.append(logs)
        self.x.append(self.i)
        self.losses.append(logs.get('loss'))
        self.val_losses.append(logs.get('val_loss'))
        self.i += 1

        plt.clf()

        plt.subplot(1, 2, 1)
        plt.plot(self.x, self.losses, label="Train Loss")
        plt.plot(self.x, self.val_losses, label="Validation Loss")
        plt.legend()
        plt.title('Train Loss and Validation Loss')

        plt.draw()
        plt.pause(0.001)



#------------------------------------------------------
#
# 概要   ：CSVファイルからデータを読み込む
# input  ：CSVファイルのパス
# return :データフレーム
#
#------------------------------------------------------
def load_data(file_path):
    df = pd.read_csv(file_path)
    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index('Date', inplace=True)
    df = df.sort_index()
    return df

#------------------------------------------------------
#
# 概要   ：データの前処理を行う
# input  ：データフレーム
# return :正規化されたデータ, スケーラー, 元のデータセット
#
#------------------------------------------------------
def preprocess_data(df):
    data = df['Close'].str.replace(',', '').astype(float)
    dataset = data.values.reshape(-1, 1)
    scaler = MinMaxScaler(feature_range=(0,1))
    scaled_data = scaler.fit_transform(dataset)
    return scaled_data, scaler, dataset

#------------------------------------------------------
#
# 概要   ：訓練データを作成する
# input  ：正規化されたデータ, ウィンドウサイズ（デフォルトは60）
# return :訓練データ（x_train, y_train）, 訓練データの長さ
#
#------------------------------------------------------
def create_training_data(scaled_data, window_size=60):
    training_data_len = int(np.ceil(len(scaled_data) * .8))
    train_data = scaled_data[0:int(training_data_len), :]
    x_train, y_train = [], []
    for i in range(window_size, len(train_data)):
        x_train.append(train_data[i-window_size:i, 0])
        y_train.append(train_data[i, 0])
    x_train, y_train = np.array(x_train), np.array(y_train)
    x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))
    return x_train, y_train, training_data_len

#------------------------------------------------------
#
# 概要   ：LSTMモデルを構築し訓練する
# input  ：訓練データ（x_train, y_train）
# return :訓練済みモデル
#
#------------------------------------------------------
def build_and_train_model(x_train, y_train):
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

    model.fit(x_train, y_train, batch_size=32, epochs=100, callbacks=[plot_learning])
    return model

#------------------------------------------------------
#
# 概要   ：学習済みモデルを保存する
# input  ：モデル, 保存先のパス
# return :なし
#
#------------------------------------------------------
def save_model(model, save_path):
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    model.save(f"{save_path}\LSTM_{timestamp}.h5")


#------------------------------------------------------
#
# 概要   ：データをプロットする
# input  ：訓練データ, 検証データ, 開始日, 終了日
# return :なし
#
#------------------------------------------------------
def plot_data(train, valid, start_date, end_date):
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

#------------------------------------------------------
#
# 概要   ：テストデータを作成する
# input  ：正規化されたデータ, 元のデータセット, 訓練データの長さ, ウィンドウサイズ（デフォルトは60）
# return :テストデータ（x_test, y_test）
#
#------------------------------------------------------
def create_test_data(scaled_data, dataset, training_data_len, window_size=60):
    test_data = scaled_data[training_data_len - window_size: , :]
    x_test = []
    y_test = dataset[training_data_len:, :]
    for i in range(window_size, len(test_data)):
        x_test.append(test_data[i-window_size:i, 0])
    x_test = np.array(x_test)
    x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))
    return x_test, y_test

#------------------------------------------------------
#
# 概要   ：予測を行う
# input  ：モデル, テストデータ, スケーラー
# return :予測値
#
#------------------------------------------------------
def make_predictions(model, x_test, scaler):
    predictions = model.predict(x_test)
    predictions = scaler.inverse_transform(predictions)
    return predictions

# Main program
file_path = 'D:\\Program\\仮想通貨情報収集\\CSV\\price-data.csv'
save_path = 'D:\Program\仮想通貨情報収集\model'

df = load_data(file_path)
scaled_data, scaler, dataset = preprocess_data(df)

# Plot initial data
plt.figure(figsize=(16,6))
plt.title('JPY/BTC Close Price History')
plt.plot(df['Close'].str.replace(',', '').astype(float))
plt.xlabel('Date', fontsize=14)
plt.ylabel('Close Price JPY', fontsize=14)
plt.show()

x_train, y_train, training_data_len = create_training_data(scaled_data)
model = build_and_train_model(x_train, y_train)

# Save the trained model
save_model(model, save_path)

# Create test data and make predictions
x_test, y_test = create_test_data(scaled_data, dataset, training_data_len)
predictions = make_predictions(model, x_test, scaler)

# Calculate RMSE and R2 score
rmse = np.sqrt(np.mean(((predictions - y_test) ** 2)))
print(f"RMSE: {rmse}")

r2s = r2_score(y_test, predictions)
print(f"R2 Score: {r2s}")

# Prepare data for plotting
train = df['Close'].str.replace(',', '').astype(float)[:training_data_len]
valid = df['Close'].str.replace(',', '').astype(float)[training_data_len:]
valid = valid.to_frame()
valid['Predictions'] = predictions

# Plotting the final data
start_date = '2023-01-01'
end_date = '2023-08-31'
plot_data(train, valid, start_date, end_date)
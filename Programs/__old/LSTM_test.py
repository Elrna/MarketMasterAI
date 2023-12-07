import numpy as np
import pandas as pd
from sklearn.metrics import r2_score
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense, LSTM, Dropout
import matplotlib.pyplot as plt

# CSVファイルからデータを読み込む
df = pd.read_csv('D:\\Program\\仮想通貨情報収集\\CSV\\price-data.csv')
df['Date'] = pd.to_datetime(df['Date'])
df.set_index('Date', inplace=True)
df = df.sort_index()

# データの可視化
plt.figure(figsize=(16,6))
plt.title('JPY/BTC Close Price History')
plt.plot(df['Close'].str.replace(',', '').astype(float))
plt.xlabel('Date', fontsize=14)
plt.ylabel('Close Price JPY', fontsize=14)
plt.show()

# データの前処理
data = df['Close'].str.replace(',', '').astype(float)
dataset = data.values.reshape(-1, 1)
scaler = MinMaxScaler(feature_range=(0,1))
scaled_data = scaler.fit_transform(dataset)

training_data_len = int(np.ceil( len(dataset) * .8 ))
window_size = 60

train_data = scaled_data[0:int(training_data_len), :]

x_train, y_train = [], []
for i in range(window_size, len(train_data)):
    x_train.append(train_data[i-window_size:i, 0])
    y_train.append(train_data[i, 0])

x_train, y_train = np.array(x_train), np.array(y_train)
x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

# モデルの構築と訓練
model = Sequential()
model.add(LSTM(units=50,return_sequences=True,input_shape=(x_train.shape[1], 1)))
model.add(Dropout(0.2))
model.add(LSTM(units=50,return_sequences=True))
model.add(Dropout(0.2))
model.add(LSTM(units=50,return_sequences=True))
model.add(Dropout(0.2))
model.add(LSTM(units=50))
model.add(Dropout(0.2))
model.add(Dense(units=1))

model.compile(optimizer='adam', loss='mean_squared_error')
history = model.fit(x_train, y_train, batch_size=32, epochs=100)

# テストデータと予測
test_data = scaled_data[training_data_len - window_size: , :]
x_test = []
y_test = dataset[training_data_len:, :]
for i in range(window_size, len(test_data)):
    x_test.append(test_data[i-window_size:i, 0])

x_test = np.array(x_test)
x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1 ))

predictions = model.predict(x_test)
predictions = scaler.inverse_transform(predictions)

rmse = np.sqrt(np.mean(((predictions - y_test) ** 2)))
print(rmse)

r2s = r2_score(y_test, predictions)
print(r2s)

train = data[:training_data_len]
valid = data[training_data_len:]
valid = valid.to_frame()
valid['Predictions'] = predictions


# 既存のコードの後にこの部分を追加または変更します。
start_date = '2023-01-01'
end_date = '2023-08-31'

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


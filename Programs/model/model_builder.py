import os
import matplotlib.pyplot as plt

from datetime import datetime
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

class ModelBuilder:
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
        model.add(LSTM(units=50, return_sequences=True, input_shape=(x_train.shape[1], x_train.shape[2])))
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
        callbacks=[plot_learning]
        model.fit(x_train, y_train, batch_size=32, epochs=100, validation_split=0.2)
        return model

    def save_model(self, model, save_path):
        """
        Overview:
            学習済みモデルを保存する。
        Parameters:
            model - 訓練済みのモデル。
            save_path - モデルを保存するパス。
        Returns:
            None。
        """
        if not os.path.exists(save_path):
            os.makedirs(save_path)

        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        model.save(f"{save_path}\\LSTM_{timestamp}.h5")

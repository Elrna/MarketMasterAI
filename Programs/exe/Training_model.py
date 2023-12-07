import os
import logging
import json
import numpy as np
import pandas as pd
from keras.models import load_model, Sequential
from keras.layers import Dense, LSTM, Dropout



def LSTM_model(x_train, y_train):
    """
    overview:
        LSTMモデルを構築・訓練
    Parameters:
        x_train, y_train - 訓練データ
    Returns:
        訓練済みモデル
    """
    try:
        model = Sequential()
        model.add(LSTM(units=50, return_sequences=True, input_shape=(x_train.shape[1], 4)))
        model.add(Dropout(0.2))
        model.add(LSTM(units=50, return_sequences=True))
        model.add(Dropout(0.2))
        model.add(LSTM(units=50, return_sequences=True))
        model.add(Dropout(0.2))
        model.add(LSTM(units=50))
        model.add(Dropout(0.2))
        model.add(Dense(units=1))
        model.compile(optimizer='adam', loss='mean_squared_error')

        history = model.fit(x_train, y_train, batch_size=32, epochs=100, validation_split=0.2)

        final_loss = history.history['loss'][-1]
        final_val_loss = history.history['val_loss'][-1]
        logging.info(f"Training completed. Final loss: {final_loss}, Final validation loss: {final_val_loss}")

        return model

    except Exception as e:
        logging.error(f"Error in LSTM_model : {e}")
        raise

def retrain_model(model, x_train, y_train):
    """
    Overview:
        既存のモデルを新しいデータセットで再トレーニングする。
    Parameters:
        model - 再トレーニングするモデル。
        x_train, y_train - 新しいトレーニングデータ。
    Returns:
        再トレーニングされたモデル。
    """
    try:
        history = model.fit(x_train, y_train, batch_size=1024, epochs=100, validation_split=0.2)

        final_loss = history.history['loss'][-1]
        final_val_loss = history.history['val_loss'][-1]
        logging.info(f"Training completed. Final loss: {final_loss}, Final validation loss: {final_val_loss}")

        return model
    except Exception as e:
        logging.error(f"Error in retrain_model : {e}")
        raise

def save_Trained_model(model, model_path):
    """
    Overview:
        学習済みモデルを保存する。
    Parameters:
        model - 訓練済みのモデル。
        save_path - モデルを保存するパス。
    Returns:
        None。
    """
    try:
        model.save(f'{model_path}')
        logging.info(f"Model saved successfully at {model_path}")
    except Exception as e:
        logging.error(f"Error in save_Trained_model : {e}")
        raise

def create_training_data(file_path, window_size=60):
    """
    Overview:
        訓練データを作成。
    Parameters:
        file_path - 正規化されたデータのファイルパス。
        window_size - ウィンドウサイズ。
    Returns:
        x_train, y_train, 訓練データ長
    """
    try:
        scaled_data = pd.read_csv(file_path)

        scaled_data = scaled_data.iloc[:, 1:-1]

        train_data_len = int(np.ceil(len(scaled_data) * .8))

        train_data = scaled_data.values[0:int(train_data_len), :]
        x_train, y_train = [], []

        for i in range(window_size, len(train_data)):
            x_train.append(train_data[i-window_size:i, :])
            y_train.append(train_data[i, 0])

        x_train = np.array(x_train).astype('float64')
        y_train = np.array(y_train).astype('float64')

        logging.info("Training data created successfully.")
        return x_train, y_train
    except Exception as e:
        logging.error(f"Error in create_training_data: {e}")
        raise

def loading_model(model_path):
    try:
        model = load_model(model_path)

        logging.info("loading LSTM model successfully.")

        return model

    except Exception as e:
        logging.error(f"Error in loading_model: {e}")

def model_exists(model_path):
    """
    Overview:
        モデルファイルが存在するかをチェックする。
    Parameters:
        model_path - モデルファイルのパス。
    Returns:
        モデルが存在する場合はTrue、そうでない場合はFalse。
    """
    return os.path.exists(model_path)

def get_last_timestamp(file_path):
    """
    Overview:
        トレーニングデータの最後のタイムスタンプを取得する。
    Parameters:
        file_path - データファイルのパス。
    Returns:
        最後のタイムスタンプ。
    """
    try:
        data = pd.read_csv(file_path)

        last_timestamp = data.iloc[-1]['timestamp']

        return last_timestamp
    except Exception as e:
        logging.error(f"Error in get_last_timestamp: {e}")
        raise

def save_last_timestamp(timestamp, json_path):
    """
    Overview:
        タイムスタンプをJSONファイルに保存する。
    Parameters:
        timestamp - 保存するタイムスタンプ。
        json_path - JSONファイルのパス。
    Returns:
        None。
    """
    try:
        with open(json_path, 'w') as file:
            json.dump({'last_timestamp': timestamp}, file)
        logging.info(f"Last timestamp saved successfully in {json_path}")
    except Exception as e:
        logging.error(f"Error in save_last_timestamp: {e}")
        raise

def main():
    try:
        with open('D:\MarketMasterAI\Def\Path.json', 'r') as file:
            paths = json.load(file)
            log_path = paths['log_paths']['Training_model']
            model_paths = [ paths['model_paths']['5min_model_save'],
                            paths['model_paths']['15min_model_save'],
                            paths['model_paths']['30min_model_save'],
                            paths['model_paths']['1hr_model_save'],
                            paths['model_paths']['4hr_model_save'],
                            paths['model_paths']['1d_model_save'],]

            train_datas = [ paths['csv_paths']['5min_training'],
                            paths['csv_paths']['15min_training'],
                            paths['csv_paths']['30min_training'],
                            paths['csv_paths']['1hr_training'],
                            paths['csv_paths']['4hr_training'],
                            paths['csv_paths']['1d_training'],]

            retrain_datas = [   paths['csv_paths']['5min_retrain'],
                                paths['csv_paths']['15min_retrain'],
                                paths['csv_paths']['30min_retrain'],
                                paths['csv_paths']['1hr_retrain'],
                                paths['csv_paths']['4hr_retrain'],
                                paths['csv_paths']['1d_retrain'],]

            timestamp_json = paths["json_paths"]["Last_timestamp"]


        logging.basicConfig(filename=log_path,
                            level=logging.INFO,
                            format='%(asctime)s:%(levelname)s:%(message)s')
        models = []

        for i, model_path in enumerate(model_paths):
            if model_exists(model_path):
                x_train, y_train = create_training_data(retrain_datas[i])
                model = loading_model(model_path)
                retrained_model = retrain_model(model, x_train, y_train)
                models.append(retrained_model)
                last_timestamp = get_last_timestamp(retrain_datas[i])
                save_last_timestamp(last_timestamp, timestamp_json)
            else:
                x_train, y_train = create_training_data(train_datas[i])
                model = LSTM_model(x_train, y_train)
                models.append(model)
                last_timestamp = get_last_timestamp(train_datas[i])
                save_last_timestamp(last_timestamp, timestamp_json)

        # 学習済みモデルの保存
        for i, model in enumerate(models):
            save_Trained_model(model, model_paths[i])

        logging.info("Main function executed successfully.")

    except Exception as e:
        logging.error(f"Error in main: {e}")

if __name__ == "__main__":
    main()
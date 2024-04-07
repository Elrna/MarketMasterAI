from keras.models import load_model
import numpy as np
import pandas as pd
import json
from datetime import timedelta

with open('D:/MarketMasterAI/Def/Path.json', 'r') as file:
    paths = json.load(file)
    model_path = paths['model_paths']['5min_model_save']
    train_data = paths['csv_paths']['5min_training']
    scaler_params = paths['json_paths']['scaler_param']
    lstm_output = paths['csv_paths']['LSTM_output']

def predict_future_prices(model, last_window, future_periods, window_size, last_timestamp):
    future_predictions = []
    current_window = last_window

    for i in range(future_periods):
        # 現在のウィンドウから次の価格を予測
        current_window_without_volume = current_window[:, :4]
        predicted_price = model.predict(np.array([current_window_without_volume]))
        future_predictions.append(predicted_price[0, 0])

        # 新しい予測値をウィンドウに追加し、最古のデータを削除
        current_window = np.append(current_window, predicted_price)[1:].reshape(window_size, -1)

        # タイムスタンプを4時間進める
        last_timestamp += timedelta(hours=4)

    # 予測価格とタイムスタンプを含むDataFrameを作成
    df = pd.DataFrame({
        'timestamp': pd.date_range(start=last_timestamp, periods=future_periods, freq='4H').strftime('%Y/%m/%d %H:%M'),
        'close': future_predictions
    })

    return df

def main():

    # モデルの読み込み
    model = load_model(model_path)

    # 最後のウィンドウデータを準備（ウィンドウサイズに合わせて調整）
    window_size = 60
    historical_data = pd.read_csv(train_data)
    last_window = historical_data.iloc[-window_size:, 1:].values # 最後のウィンドウデータ
    last_timestamp = pd.to_datetime(historical_data.iloc[-1, 0])  # 最後のタイムスタンプ
    with open(scaler_params, 'r') as file:
        scaler_param = json.load(file)

    mean_close = scaler_param['means'][1]
    scale_close = scaler_param['scales'][1]

    # 未来の価格を予測
    future_periods = 126
    predicted_df = predict_future_prices(model, last_window, future_periods, window_size, last_timestamp)

    predicted_df['close'] = predicted_df['close'] * scale_close + mean_close
    # DataFrameをCSVファイルに出力
    predicted_df.to_csv(lstm_output, index=False)

if __name__ == '__main__':
    main()
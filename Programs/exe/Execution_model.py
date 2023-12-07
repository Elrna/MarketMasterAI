from keras.models import load_model
import numpy as np
import pandas as pd
import json

with open('D:/MarketMasterAI/Def/Path.json', 'r') as file:
    paths = json.load(file)
    model_path = paths['model_paths']['model_save']
    train_data = paths['csv_paths']['training_data']

def predict_future_prices(model, last_window, future_periods, window_size):
    future_predictions = []
    current_window = last_window

    for _ in range(future_periods):
        # 現在のウィンドウから次の価格を予測
        predicted_price = model.predict(np.array([current_window]))
        future_predictions.append(predicted_price[0, 0])

        # 新しい予測値をウィンドウに追加し、最古のデータを削除
        current_window = np.append(current_window, predicted_price)[1:].reshape(window_size, -1)

    return future_predictions


def main():

    # モデルの読み込み
    model = load_model(model_path)

    # 最後のウィンドウデータを準備（ウィンドウサイズに合わせて調整）
    window_size = 60
    historical_data = pd.read_csv(train_data)
    last_window = historical_data.iloc[-window_size:, 1:].values # 最後のウィンドウデータ

    # 未来の価格を予測
    future_periods = 30 # 未来30時点分の価格を予測
    predicted_prices = predict_future_prices(model, last_window, future_periods, window_size)

    # 予測結果をDataFrameに変換（必要に応じてフォーマットを調整）
    predicted_df = pd.DataFrame(predicted_prices, columns=['Predicted_Price'])
    print(predicted_df)


if __name__ == '__main__':
    main()
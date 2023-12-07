import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from datetime import timedelta

from Data_preparation.data_loader import DataPreparation
from model.model_builder import ModelBuilder
from model.model_evaluation import ModelEvaluation
from visualization.data_visualization import DataVisualization
from future_prediction.future_prediction import FuturePrediction
from Data_preparation.data_updater import DataUpdater
from Data_preparation.dataset_manager import DatasetManager



def main():
    data_prep = DataPreparation()
    model_builder = ModelBuilder()
    model_eval = ModelEvaluation()
    data_viz = DataVisualization()
    future_pred = FuturePrediction()

    file_path = 'CSV\price-data.csv'
    save_path = 'model'

    df = data_prep.load_CSVdata(file_path)
    print(df.columns)
    data_updater = DataUpdater(df)
    dataset_manager = DatasetManager(df)
    dataset_manager.save_history()
    new_data = data_updater.fetch_new_data()
    updated_dataset = data_updater.update_dataset(new_data)

    # 更新されたデータセットを保存（または次の処理ステップに渡す）
    updated_dataset.to_csv(file_path, index=False)

    scaled_data, scaler = data_prep.preprocess_data(updated_dataset)

    # 訓練データを作成
    x_train, y_train, training_data_len = data_prep.create_training_data(scaled_data)

    # テストデータを作成
    x_test, y_test = data_prep.create_test_data(scaled_data, training_data_len)

    # モデルを構築しトレーニング
    model = model_builder.build_and_train_model(x_train, y_train)

    # トレーニング済のモデルを保存
    model_builder.save_model(model, save_path)



    # 予測を行う
    predictions = model_eval.make_predictions(model, x_test, updated_dataset)

    # RMSEおよびR2スコアを計算
    rmse, r2s = model_eval.calculate_rmse_and_r2(y_test, predictions)
    print(f"RMSE: {rmse}")
    print(f"R2 Score: {r2s}")

    # データの型を確認して、必要に応じてカンマを削除してfloat型に変換
    if updated_dataset['Close'].dtype == 'object':
        train = updated_dataset['Close'].str.replace(',', '').astype(float)[:training_data_len]
        valid = updated_dataset['Close'].str.replace(',', '').astype(float)[training_data_len:]
    else:
        train = updated_dataset['Close'][:training_data_len]
        valid = updated_dataset['Close'][training_data_len:]

    valid = valid.to_frame()
    valid['Predictions'] = predictions

    # Plotting the final data
    start_date = '2023-01-01'
    end_date = '2023-09-30'
    data_viz.plot_data(train, valid, start_date, end_date)

    # 1次元配列に整形
    y_train_reshaped = y_train[-60:].reshape(-1, 1)
    y_test_reshaped = y_test.reshape(-1, 1)

    # 結合
    latest_data = np.concatenate((y_train_reshaped, y_test_reshaped))

    # 未来の10日間の価格を予測
    future_prices = future_pred.predict_future_prices(model, latest_data, scaled_data, future_days=10)

    # スケーリングを逆転させる
    future_prices = scaler.inverse_transform(future_prices.reshape(-1, 1)).flatten()

    # 最後の日付を取得
    last_date = pd.to_datetime(df.index[-1])

    # 未来の日付を生成
    future_dates = [last_date + timedelta(days=i) for i in range(1, 11)]

    # 未来の価格をデータフレームに追加
    future_df = pd.DataFrame(future_prices, index=future_dates, columns=['Future Predictions'])

    # 現在のデータと未来の予測をプロット
    data_viz.plot_future_predictions(df, future_df, future_dates)

    # モデルを保存
    model_builder.save_model(model, save_path)

if __name__ == "__main__":
    main()

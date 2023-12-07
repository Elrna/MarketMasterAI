import numpy as np

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

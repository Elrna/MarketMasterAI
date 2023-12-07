from sklearn.preprocessing import StandardScaler
from sklearn.metrics import r2_score
import numpy as np

class ModelEvaluation():
    """
    Overview:
        モデルの評価を行うクラス。予測値を生成し、RMSE（Root Mean Square Error）と
        R2スコア（決定係数）を計算する。
    """
    def make_predictions(self, model, x_test, dataset):
        """
        Overview:
            予測を行う
        Parameters:
            model - 訓練済みモデル
            x_test - テストデータ
            dataset - 元のデータセット
        Returns:
            予測値。
        """
        predictions = model.predict(x_test)

        # 'Close'の列だけを取得してスケーラをフィットさせる
        close_scaler = StandardScaler()
        close_scaler.fit(dataset[['Close']])

        # 逆標準化を行う
        predictions = close_scaler.inverse_transform(predictions)
        return predictions

    def calculate_rmse_and_r2(self, y_test, predictions, scaler=None):
        """
        Overview:
            RMSEとR2スコアを計算。
        Parameters:
            y_test, predictions - 実際の値と予測値。
            scaler - スケーラーインスタンス（もし必要な場合）
        Returns:
            RMSE, R2スコア。
        """
        if scaler is not None:
            y_test = scaler.inverse_transform(y_test.reshape(-1, 1)).flatten()
            predictions = scaler.inverse_transform(predictions.reshape(-1, 1)).flatten()

        rmse = np.sqrt(np.mean((y_test - predictions) ** 2))
        r2 = r2_score(y_test, predictions)
        return rmse, r2

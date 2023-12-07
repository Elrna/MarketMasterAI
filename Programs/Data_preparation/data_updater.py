import pandas as pd
import ccxt
from datetime import datetime, timedelta

class DataUpdater:
    """
    データセットを更新するためのクラス。
    """

    def __init__(self, existing_dataset: pd.DataFrame):
        """
        コンストラクタ。

        Parameters:
            existing_dataset (pd.DataFrame): 既存のデータセット。
        """
        self.existing_dataset = existing_dataset



    def fetch_new_data(self) -> pd.DataFrame:
        """
        新しいデータを取得する。

        Returns:
            pd.DataFrame: 新しく取得したデータ。
        """
        # 現在の日付を取得
        current_date = datetime.now()

        # 30日前の日付を計算
        thirty_days_ago = current_date - timedelta(days=30)

        # ccxtを使用して、Binanceから30日前から現在までのBTC/USDTのデータを取得
        binance = ccxt.binance({
            'rateLimit': 1200,
            'enableRateLimit': True,
        })

        ohlcv = binance.fetch_ohlcv('BTC/USDT', '1d', binance.parse8601(thirty_days_ago.strftime('%Y-%m-%dT%H:%M:%SZ')), limit=30)
        new_data = pd.DataFrame(ohlcv, columns=['timestamp', 'Open', 'High', 'Low', 'Close', 'Volume'])

        # タイムスタンプを日付に変換
        new_data['Date'] = pd.to_datetime(new_data['timestamp'], unit='ms').dt.strftime('%Y-%m-%d')

        # 必要な列のみを取得
        new_data = new_data[['Date', 'Close', 'Open', 'High', 'Low']]

        return new_data

    def update_dataset(self, new_data: pd.DataFrame) -> pd.DataFrame:
        """
        既存のデータセットを更新する。

        Parameters:
            new_data (pd.DataFrame): 新しく取得したデータ。

        Returns:
            pd.DataFrame: 更新されたデータセット。
        """

        last_date_in_existing = pd.to_datetime(self.existing_dataset['Date']).max()
        first_date_in_new = pd.to_datetime(new_data['Date']).min()

        if first_date_in_new > last_date_in_existing:
            updated_dataset = pd.concat([self.existing_dataset, new_data])
            return updated_dataset.reset_index(drop=True)
        else:
            return self.existing_dataset

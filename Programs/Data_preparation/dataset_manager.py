import os
import pandas as pd
from datetime import datetime

class DatasetManager:
    """
    データセットの保存と更新を管理するクラス。
    """

    def __init__(self, existing_dataset: pd.DataFrame):
        """
        コンストラクタ。

        Parameters:
            existing_dataset (pd.DataFrame): 既存のデータセット。
        """
        self.existing_dataset = existing_dataset

    def save_history(self):
        """
        既存のデータセットを履歴として保存する。
        """
        timestamp = datetime.now().strftime("%Y%m%d%H%M")
        history_path = f"CSV\History\\dataset_{timestamp}.csv"
        self.existing_dataset.to_csv(history_path, index=False)

    def update_and_save(self, updated_dataset: pd.DataFrame):
        """
        更新されたデータセットを保存する。

        Parameters:
            updated_dataset (pd.DataFrame): 更新されたデータセット。
        """
        updated_path = "CSV\price-data.csv"
        updated_dataset.to_csv(updated_path, index=False)


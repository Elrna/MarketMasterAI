import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
import pandas as pd
from datetime import timedelta

class DataVisualization:
    """
    Overview:
        データの可視化を行うクラス。
    """
    def plot_initial_data(self, df):
        """
        Overview:
            初期データをプロット。
        Parameters:
            df - データフレーム。
        Returns:
            None。
        """
        plt.figure(figsize=(16,6))
        plt.title('JPY/BTC Close Price History')
        plt.plot(df['Close'].str.replace(',', '').astype(float))
        plt.xlabel('Date', fontsize=14)
        plt.ylabel('Close Price USD', fontsize=14)
        plt.show()

    def plot_data(self, train, valid, start_date, end_date):
        """
        Overview:
            訓練・検証・予測データをプロット。
        Parameters:
            train, valid - 訓練データと検証データ。
            start_date, end_date - プロットする期間。
        Returns:
            None。
        """
        train_filtered = train.loc[start_date:end_date]
        valid_filtered = valid.loc[start_date:end_date]
        fig, ax = plt.subplots(figsize=(16,6))
        ax.set_title('Model')
        ax.set_xlabel('Date', fontsize=14)
        ax.set_ylabel('Close Price USD', fontsize=14)
        ax.plot(train_filtered)
        ax.plot(valid_filtered[['Close', 'Predictions']])
        ax.legend(['Train', 'Val', 'Predictions'], loc='lower right')

        # グラフを表示するウィンドウを作成
        root = tk.Tk()
        canvas = FigureCanvasTkAgg(fig, master=root)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        tk.mainloop()

    def plot_future_predictions(self, df, future_df, future_dates):
        """
        Overview:
            現在のデータと未来の予測をプロット。
        Parameters:
            df - 現在のデータフレーム。
            future_df - 未来の価格予測を含むデータフレーム。
            future_dates - 未来の日付リスト。
        Returns:
            None。
        """
        plt.figure(figsize=(16,6))
        plt.title('Model with Future Predictions')
        plt.xlabel('Date', fontsize=14)
        plt.ylabel('Close Price JPY', fontsize=14)

        # 現在のデータと未来のデータを結合
        combined_df = pd.concat([df['Close'].str.replace(',', '').astype(float), future_df['Future Predictions']])

        # 最終日から30日前までのデータをプロット
        start_date = future_dates[-1] - timedelta(days=30)
        end_date = future_dates[-1]
        plt.plot(combined_df.loc[start_date:end_date])
        plt.legend(['Combined'], loc='lower right')
        plt.show()
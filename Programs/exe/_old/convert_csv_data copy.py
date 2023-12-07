import pandas as pd
import json
import logging
import Standardization as stand

#pathの読み込み
with open('D:\MarketMasterAI\Def\Path.json', 'r') as file:
    paths = json.load(file)
    log = paths['log_paths']['convert']

    Def = paths['file']['Def']

    csv_5T = paths['csv_paths']['5min_BTC_price']
    csv_15T = paths['csv_paths']['15min_BTC_price']
    csv_30T = paths['csv_paths']['30min_BTC_price']
    csv_1H = paths['csv_paths']['1hr_BTC_price']
    csv_4H = paths['csv_paths']['4hr_BTC_price']
    csv_1D = paths['csv_paths']['1d_BTC_price']

    train_5T = paths['csv_paths']['5min_training']
    train_15T = paths['csv_paths']['15min_training']
    train_30T = paths['csv_paths']['30min_training']
    train_1H = paths['csv_paths']['1hr_training']
    train_4H = paths['csv_paths']['4hr_training']
    train_1D = paths['csv_paths']['1d_training']

# ログ設定

logging.basicConfig(filename=log, level=logging.INFO, 
                    format='%(asctime)s:%(levelname)s:%(message)s')

def read_csv(file_path):
    """
    CSVファイルを読み込む。
    """
    try:
        data = pd.read_csv(file_path, index_col='timestamp', parse_dates=True)
        logging.info("CSVファイルの読み込みに成功しました。")
        return data
    except Exception as e:
        logging.error(f"CSVファイルの読み込み中にエラーが発生しました: {e}")
        raise

def resample_data(data, interval):
    """
    データを指定された間隔で再サンプリングする。
    """
    try:
        resampled_data = data.resample(interval).agg({'open': 'first', 
                                                      'high': 'max',
                                                      'low': 'min',
                                                      'close': 'last',
                                                      'volume': 'sum'})
        logging.info(f"{interval}間隔でのデータ再サンプリングに成功しました。")
        return resampled_data
    except Exception as e:
        logging.error(f"データ再サンプリング中にエラーが発生しました: {e}")
        raise

def save_to_csv(data, file_name):
    """
    データをCSVファイルに保存する。
    """
    try:
        data.to_csv(file_name)
        logging.info(f"{file_name}にデータを保存しました。")
    except Exception as e:
        logging.error(f"CSVファイルの保存中にエラーが発生しました: {e}")
        raise

def main():
    file_path = csv_5T
    intervals = ['15T', '30T', '1H', '4H', '1D']

    try:
        data = read_csv(file_path)
        for interval in intervals:
            resampled_data = resample_data(data, interval)
            output_file_name = f"{Def}BTCUSDT_{interval}.csv"
            save_to_csv(resampled_data, output_file_name)
            
        logging.info("すべての間隔でのデータ処理が完了しました。")

        stand.standardize_and_save_csv(csv_5T, train_5T, '5T')
        stand.standardize_and_save_csv(csv_15T, train_15T, interval[0])
        stand.standardize_and_save_csv(csv_30T, train_30T, interval[1])
        stand.standardize_and_save_csv(csv_1H, train_1H, interval[2])
        stand.standardize_and_save_csv(csv_4H, train_4H, interval[3])
        stand.standardize_and_save_csv(csv_1D, train_1D, interval[4])

        logging.info("すべての間隔での標準化処理が完了しました。")
        



    except Exception as e:
        logging.error(f"メイン処理中にエラーが発生しました: {e}")

if __name__ == "__main__":
    main()

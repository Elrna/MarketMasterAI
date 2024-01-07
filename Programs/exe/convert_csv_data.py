import pandas as pd
import json
import logging
import Standardization as stand

def load_paths():
    """
    JSONファイルからパスを読み込む。
    """
    try:
        with open('D:/MarketMasterAI/Def/Path.json', 'r') as file:
            return json.load(file)
    except Exception as e:
        logging.exception("パスの読み込み中にエラーが発生しました")
        raise

def resample_data(data, interval):
    """
    データを指定された間隔で再サンプリングする。
    """
    try:
        resampled_data = data.resample(interval).agg(
            {   'open'  : 'first',
                'high'  : 'max',
                'low'   : 'min',
                'close' : 'last',
                'volume': 'sum'
            })

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

def read_csv(file_path):
    """
    CSVファイルを読み込む。
    """
    try:
        data = pd.read_csv(file_path, index_col='timestamp', dtype={'timestamp': 'object'})

        data.index = pd.to_datetime(data.index, format='%Y/%m/%d %H:%M')

        logging.info("CSVファイルの読み込みに成功しました。")
        return data
    except Exception as e:
        logging.error(f"CSVファイルの読み込み中にエラーが発生しました: {e}")
        raise

def process_and_standardize_data(file_path, interval, output_def, standardize_func, is_retrain=False):
    resampled_data = resample_data(read_csv(file_path), interval)
    retrain_prefix = 'retrain_' if is_retrain else ''
    output_file_name = f"{output_def}{retrain_prefix}BTCUSDT_{interval}.csv"
    save_to_csv(resampled_data, output_file_name)

    output_file = f"{output_def}Standrd_{retrain_prefix}BTCUSDT_{interval}.csv"
    standardize_func(output_file_name, output_file, interval)

def retrain_process_data(file_path, interval, output_def, standardize_func):
    """
    データの処理と標準化を行う。
    """
    resampled_data = resample_data(read_csv(file_path), interval)
    output_file_name = f"{output_def}retrain_BTCUSDT_{interval}.csv"
    save_to_csv(resampled_data, output_file_name)

    output_file = f"{output_def}Standrd_retrain_BTCUSDT_{interval}.csv"
    standardize_func(output_file_name, output_file, interval)

def main():
    paths = load_paths()
    logging.basicConfig(filename=paths['log_paths']['convert'], level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

    intervals = ['5T', '15T', '30T', '1H', '4H', '1D']
    try:
        for interval in intervals:
            process_and_standardize_data(paths['csv_paths']['clean_BTC_price'], interval, paths['file']['Def'], stand.standardize_and_save_csv)

        logging.info("すべての間隔でのデータ処理と標準化が完了しました。")
    except Exception as e:
        logging.exception("メイン処理中にエラーが発生しました")

if __name__ == "__main__":
    main()

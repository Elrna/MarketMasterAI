import pandas as pd
from sklearn.preprocessing import StandardScaler
import json

def standardize_data(data, columns_to_scale):
    """
    データを標準化する
    """
    scaler = StandardScaler()
    data[columns_to_scale] = scaler.fit_transform(data[columns_to_scale])

    return data, scaler


def save_data_to_csv(data, file_path):
    """
    データをCSVファイルに保存する。
    """
    try:
        data.to_csv(file_path, index=False)
    except Exception as e:
        raise Exception(f"CSVファイルの保存中にエラーが発生しました: {e}")

def standardize_and_save_csv(input_file_path, output_file_path, interval):
    try:
        data = pd.read_csv(input_file_path)

        timestamp_data = data['timestamp']
        # OCHLとVolumeを別々に標準化
        ochl_columns = ['open', 'close', 'high', 'low']
        volume_columns = ['volume']

        ochl_data, ochl_scaler = standardize_data(data, ochl_columns)
        volume_data, volume_scaler = standardize_data(data, volume_columns)

        # 標準化されたデータの結合
        standardized_data = pd.concat([timestamp_data, ochl_data[ochl_columns], volume_data[volume_columns]], axis=1)

        save_data_to_csv(standardized_data, output_file_path)

        # スケーラーパラメータの保存
        scaler_parameter_to_json(ochl_scaler.mean_, ochl_scaler.scale_, interval, 'ochl')
        scaler_parameter_to_json(volume_scaler.mean_, volume_scaler.scale_, interval, 'volume')

    except Exception as e:
        raise Exception(f"標準化処理中にエラーが発生しました: {e}")

def scaler_parameter_to_json(means, scales, interval, data_type):
    scaler_params = {
        'means' : means.tolist(),
        'scales': scales.tolist()
    }

    with open(f'D:/MarketMasterAI/bin/{interval}_{data_type}_scaler_parameters.json', 'w') as f:
        json.dump(scaler_params, f, indent=4)


def retrain_standardize_and_save_csv(input_file_path, output_file_path, interval):
    try:
        data = pd.read_csv(input_file_path)

        ochl_columns = ['open', 'close', 'high', 'low']
        volume_columns = ['volume']

        ochl_data, ochl_scaler = standardize_data(data, ochl_columns)
        volume_data, volume_scaler = standardize_data(data, volume_columns)

        # 標準化されたデータの結合
        standardized_data = pd.concat([ochl_data, volume_data[volume_columns]], axis=1)

        save_data_to_csv(standardized_data, output_file_path)

        retrain_scaler_parameter_to_json(ochl_scaler.mean_, ochl_scaler.scale_, interval, 'ochl')
        retrain_scaler_parameter_to_json(volume_scaler.mean_, volume_scaler.scale_, interval, 'volume')
    except Exception as e:
        raise Exception(f"標準化処理中にエラーが発生しました: {e}")

def retrain_scaler_parameter_to_json(means, scales, interval, data_type):
    scaler_params = {
        'means' : means.tolist(),
        'scales': scales.tolist()
    }

    with open(f'D:/MarketMasterAI/bin/retrain_{interval}_{data_type}__scaler_parameters.json', 'w') as f:
        json.dump(scaler_params, f, indent=4)





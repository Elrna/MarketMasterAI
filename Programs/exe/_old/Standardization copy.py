import pandas as pd
from sklearn.preprocessing import StandardScaler
import json



def standardize_and_save_csv(input_file_path, output_file_path, interval):
    # データを読み込む
    data = pd.read_csv(input_file_path)

    # 標準化を行うカラムを選択
    columns_to_scale = ['open', 'close', 'high', 'low', 'volume']

    # StandardScalerを使ってデータを標準化
    scaler = StandardScaler()
    data[columns_to_scale] = scaler.fit_transform(data[columns_to_scale])

    # 標準化されたデータを新しいCSVファイルに保存
    data.to_csv(output_file_path, index=False)

    scaler_parameter_to_json(scaler.mean_, scaler.scale_, interval)

    return data

def scaler_parameter_to_json(means, scales, interval):
    scaler_params = {
        'means' : means.tolist(),
        'scales': scales.tolist()
    }

    with open(f'D:/MarketMasterAI/bin/{interval}_scaler_parameters.json', 'w') as f:
        json.dump(scaler_params, f, indent=4)



def inverse_standardize_csv(LSTM_output_filepath, output_file_path, scaler_json_path):
    # JSONファイルから平均値と標準偏差を読み込む
    with open(scaler_json_path, 'r') as f:
        scaler_params = json.load(f)
    
    # StandardScalerオブジェクトを再構築
    scaler = StandardScaler()
    scaler.mean_ = scaler_params['means']
    scaler.scale_ = scaler_params['scales']

    # 標準化されたデータを読み込む
    standardized_data = pd.read_csv(LSTM_output_filepath)

    # 標準化されたデータのカラムを選択
    columns_to_inverse = ['open', 'close', 'high', 'low', 'volume']

    # inverse_transformを使用して元のスケールに戻す
    standardized_data[columns_to_inverse] = scaler.inverse_transform(standardized_data[columns_to_inverse])

    # 元のスケールに戻したデータを新しいCSVファイルに保存
    standardized_data.to_csv(output_file_path, index=False)

    return standardized_data
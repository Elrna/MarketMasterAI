import pandas as pd
import logging
import json

def initialize(output_path):
    """既存のCSVファイルを初期化する"""
    df = pd.read_csv(output_path, nrows=0)
    df.to_csv(output_path, index=False)

def clean_and_export_csv(csv_path, output_path):
    """CSVデータをクリーンアップして出力する"""
    try:
        initialize(output_path) #二重追記防止
        chunksize = 10000
        chunks = pd.read_csv(csv_path, chunksize=chunksize, usecols=['timestamp', 'open', 'high', 'low', 'close', 'volume'])

        for i, chunk in enumerate(chunks):
            cleaned_chunk = clean_data(chunk)
            header = i == 0
            cleaned_chunk.to_csv(output_path, mode='a', header=header, index=False)


            logging.info('\n')
            logging.info(f'Chunk {i} done.')

    except Exception as e:
        logging.error(f'Error: {e}')

def clean_data(chunk):
    """データをクリーンアップする"""
    timestamp = chunk[['timestamp']]
    volume = chunk[['volume']]
    ochl = chunk[['open', 'high', 'low', 'close']]

    ochl = ochl.replace('', pd.NA).replace(0, pd.NA)

    ochl.dropna(subset=['open', 'high', 'low', 'close'], inplace=True)

    return pd.concat([timestamp, ochl, volume], axis=1)

def main():
    logging.basicConfig(filename='D:/MarketMasterAI/Log/DataCleaner.log',
                        level=logging.INFO,
                        format='%(asctime)s:%(levelname)s:%(message)s')
    
    with open("D:/MarketMasterAI/Def/Path.json", 'r') as file:
        data = json.load(file)
        csv_path = data['csv_paths']['5min_BTC_price']
        output = data['csv_paths']['clean_BTC_price']
    
    clean_and_export_csv(csv_path, output)

if __name__ == '__main__':
    main()
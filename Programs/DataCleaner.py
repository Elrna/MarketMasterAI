import pandas as pd
import logging
import json

def main():
    logging.basicConfig(filename='D:/MarketMasterAI/Log/DataCleaner.log',
                    level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')

    with open("D:/MarketMasterAI/Def/Path.json", 'r') as file:
        data = json.load(file)
        csv_path = data['csv_paths']['5min_BTC_price']

    try:
        chunksize = 10

        chunks = pd.read_csv(csv_path, chunksize=chunksize, usecols=['timestamp', 'open', 'high', 'low', 'close', 'volume'])

        first_chunk = True

        for chunk in chunks:
            timestamp = chunk[['timestamp']]
            ochlv = chunk.drop('timestamp', axis=1)

            ochlv.replace('', pd.NA, inplace=True)
            #ochlv.replace(0, pd.NA, inplace=True)

            ochlv.dropna(subset=['open', 'high', 'low', 'close', 'volume'], inplace=True)

            cleaned_chunk = pd.concat([timestamp, ochlv], axis=1)

            if first_chunk:
                cleaned_chunk.to_csv(csv_path, index=False)
                first_chunk = False
            else:
                cleaned_chunk.to_csv(csv_path, mode='a', header=False, index=False)

        logging.info('DataCleaner.py finished successfully.')

    except Exception as e:
        logging.error(f'Error: {e}')

if __name__ == '__main__':
    main()
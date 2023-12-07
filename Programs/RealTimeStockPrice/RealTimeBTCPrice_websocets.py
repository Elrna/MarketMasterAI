import asyncio
import websockets
import json
import pandas as pd
from datetime import datetime

# グローバル変数
bybit_price = None
bybit_timestamp = None

# JSONファイルにデータを保存
def save_to_json(data, filepath):
    with open(filepath, 'w') as file:
        json.dump(data, file)

# CSVファイルにデータを追加
def save_to_csv(price, timestamp, csv_filepath):
    df = pd.DataFrame({'Timestamp': [timestamp], 'Price': [price]})
    df.to_csv(csv_filepath, mode='a', header=False, index=False)

# リアルタイム価格データの取得
async def fetch_bybit_price(csv_filepath, json_filepath):
    global bybit_price, bybit_timestamp

    async with websockets.connect('wss://stream.bybit.com/v5/public/linear') as bybit_ws:
        bybit_payload = {"op": "subscribe", "args": ["tickers.BTCUSDT"]}
        await bybit_ws.send(json.dumps(bybit_payload))
        
        while True:
            response = await bybit_ws.recv()
            data = json.loads(response)

            if "data" in data and "lastPrice" in data["data"]:
                bybit_price = float(data["data"]["lastPrice"])
                bybit_timestamp = float(data["ts"])

                # CSVファイルに5分間隔で保存
                if datetime.now().minute % 5 == 0:
                    save_to_csv(bybit_price, bybit_timestamp, csv_filepath)

                # JSONファイルにリアルタイムで保存
                save_to_json(bybit_price, json_filepath)


                #print(f'Bybit: Price: {bybit_price}, Timestamp: {bybit_timestamp}')

# CSVとJSONファイルのパス
csv_filepath = 'realtime_price.csv'
json_filepath = 'realtime_data.json'



# 実行
asyncio.run(fetch_bybit_price(csv_filepath, json_filepath))

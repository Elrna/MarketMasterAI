import json
import logging
import asyncio
import aiohttp
import pandas as pd
import numpy as np
import time

# ロギングの設定
logging.basicConfig(filename="D:\\MarketMasterAI\\Log\\RealTimeBTCPrice.log", level=logging.INFO)

# APIからデータを非同期で取得する関数
async def fetch_data(session, url, params):
    async with session.get(url, params=params) as response:
        response_json = await response.json()
        print(response_json)  # APIレスポンスボディの確認
        return await response.json()

# データをPandas DataFrameに変換する関数
def process_data(data):
    df = pd.DataFrame(data)
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
    df.set_index('timestamp', inplace=True)
    for col in ['open', 'high', 'low', 'close', 'volume']:
        df[col] = df[col].astype(float)
    return df

# 移動平均を計算する関数
def calculate_sma(df, period=14):
    df['SMA'] = df['close'].rolling(window=period).mean()
    return df

# ATRを計算する関数
def calculate_atr(df, period=14):
    high_low = df['high'] - df['low']
    high_close = np.abs(df['high'] - df['close'].shift())
    low_close = np.abs(df['low'] - df['close'].shift())
    ranges = pd.concat([high_low, high_close, low_close], axis=1)
    true_range = np.max(ranges, axis=1)
    df['ATR'] = true_range.rolling(window=period).mean()
    return df

# RSIを計算する関数
def calculate_rsi(df, period=14):
    delta = df['close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))
    return df

# MACDを計算する関数
def calculate_macd(df, fast_period=12, slow_period=26, signal_period=9):
    df['MACD'] = df['close'].ewm(span=fast_period, adjust=False).mean() - df['close'].ewm(span=slow_period, adjust=False).mean()
    df['MACD_signal'] = df['MACD'].ewm(span=signal_period, adjust=False).mean()
    df['MACD_hist'] = df['MACD'] - df['MACD_signal']
    return df

# データをファイルに保存する関数
def save_data(data, filepath):
    with open(filepath, 'w') as file:
        json.dump(data, file, default=str)

# メインの非同期処理関数
async def main():
    filepath = "D:\\MarketMasterAI\\bin\\BTC_PriceData.json"
    url = "https://api.bybit.com/public/linear/kline?symbol=BTCUSDT&interval=D"
    current_timestamp = int(time.time())
    params = {
            'symbol': 'BTCUSDT',
        'interval': 'D',
        'from': current_timestamp - 86400 * 30  # 30日前からのデータを取得
    }

    try:
        async with aiohttp.ClientSession() as session:
            response = await fetch_data(session, url, params)
            df = process_data(response['result'])
            df = calculate_sma(df)
            df = calculate_atr(df)
            df = calculate_rsi(df)
            df = calculate_macd(df)
            save_data(df.to_dict('records'), filepath)
            logging.info(f"Data successfully fetched and processed. Saved to {filepath}")
    except Exception as e:
        logging.error(f"Error occurred: {e}")

# スクリプトの実行
if __name__ == "__main__":
    asyncio.run(main())

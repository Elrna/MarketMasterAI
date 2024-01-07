from aiohttp import ClientSession, ClientTimeout, ClientOSError
import asyncio
import pandas as pd
from datetime import datetime, timedelta
import logging
import json

# ロガーの設定
logging.basicConfig(filename='D:/MarketMasterAI/Log/RealTimeBTCPrice.log',
                    level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')

with open("D:/MarketMasterAI/Def/Path.json", 'r') as file:
    data = json.load(file)
    csv_path = data['csv_paths']['5min_BTC_price']
    retrain_csv = data['csv_paths']['5min_retrain']


async def fetch(session, url, retry_count=0, max_retries=3):
    """
    非同期でHTTP GETリクエストを実行する。リトライロジックを含む。
    """
    timeout = ClientTimeout(total=10)
    try:
        async with session.get(url, timeout=timeout) as response:
            if response.status != 200:
                raise Exception(f"HTTP Error: {response.status}")
            content_type = response.headers.get('Content-Type', '')
            return await response.json() if 'application/json' in content_type else await response.text()
    except (asyncio.TimeoutError, ClientOSError, Exception) as e:
        if retry_count < max_retries:
            logging.warning(f"Error: {e}. Retrying... ({retry_count + 1}/{max_retries})")
            await asyncio.sleep(2 ** retry_count)  # Exponential backoff
            return await fetch(session, url, retry_count + 1, max_retries)
        else:
            logging.error(f"Failed to retrieve data after {max_retries} retries. Error: {e}")
            raise


async def fetch_ohlcv(session, symbol, interval, start, end):
    url = f'https://api.bybit.com/v2/public/kline/list?symbol={symbol}&interval={interval}&from={start}&to={end}&limit=200'
    response = await fetch(session, url)
    data = response.get('result', [])
    if not data:
        return pd.DataFrame()

    df = pd.DataFrame(data)
    df['timestamp'] = pd.to_datetime(df['open_time'], unit='s')
    df['timestamp'] = df['timestamp'].dt.strftime('%Y/%m/%d %H:%M')
    return df[['timestamp', 'open', 'high', 'low', 'close', 'volume']]

def get_timedelta(interval):
    """
    指定された間隔に応じたtimedeltaを返す。
    """
    if interval == '5':
        return timedelta(minutes=1000)
    elif interval == '15':
        return timedelta(minutes=3000)
    elif interval == '30':
        return timedelta(minutes=6000)
    elif interval == '60':
        return timedelta(minutes=12000)
    elif interval == '240':
        return timedelta(minutes=48000)
    else:
        raise ValueError("Invalid interval")

async def update_data(symbol, interval, start, end):
    async with ClientSession() as session:
        start_timestamp = int(start.timestamp())
        end_timestamp = int(end.timestamp())
        df = await fetch_ohlcv(session, symbol, interval, start_timestamp, end_timestamp)
        return df

# 必要なヘルパー関数の定義
def get_last_timestamp():
    try:
        df = pd.read_csv(csv_path)
        return convert_to_utc(df['timestamp'].iloc[-1]) + timedelta(minutes=5)
    except (FileNotFoundError, pd.errors.EmptyDataError):
        logging.info("CSVファイルが見つからないか、データがありません。新しいデータ取得を開始します。")
        return datetime.utcnow()

def convert_to_utc(timestamp):
    last_timestamp = pd.to_datetime(timestamp, utc=False)
    return last_timestamp.tz_localize('Asia/Tokyo').tz_convert('UTC').replace(tzinfo=None)

def adjust_to_interval(now):
    return (now - timedelta(minutes=now.minute % 5, seconds=now.second, microseconds=now.microsecond)).replace(tzinfo=None)

def save_data(df, interval):
    df['timestamp'] = pd.to_datetime(df['timestamp']).dt.tz_localize('UTC').dt.tz_convert('Asia/Tokyo')
    df['timestamp'] = df['timestamp'].dt.strftime('%Y/%m/%d %H:%M')
    df.to_csv(csv_path, mode='a', header=False, index=False, lineterminator='\n')


async def main(symbol, intervals):

    sleep_flag = False

    while True:
        for interval in intervals:
            try:
                last_timestamp = get_last_timestamp()
                end = adjust_to_interval(datetime.utcnow())
                if last_timestamp < end:
                    df = await update_data(symbol, interval, last_timestamp, end)
                    save_data(df, interval)

                time_diff = end - last_timestamp
                if time_diff.total_seconds() < 300:
                    sleep_flag = True

            except Exception as e:
                logging.error(f"Error occurred during data update for interval {interval}: {e}")

        if sleep_flag:
            logging.info("No new data to update. Sleep 5min.")
            sleep_flag = False
            await asyncio.sleep(300)

if __name__ == "__main__":
    symbol = 'BTCUSD'
    intervals = ['5']
    asyncio.run(main(symbol, intervals))

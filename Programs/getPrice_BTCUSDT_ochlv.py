from aiohttp import ClientSession, ClientTimeout, ClientOSError
import asyncio
import pandas as pd
from datetime import datetime, timedelta
import logging
import json
import pytz

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

def read_last_timestamp():
    """
    JSONファイルから最後のタイムスタンプを読み込む。
    """
    with open("D:/MarketMasterAI/bin/Last_timestamp.json", 'r') as file:
        data = json.load(file)
        return pd.to_datetime(data['last_timestamp'])

def load_data_from_csv(file_path, start_data, end_date):
    """
    CSVファイルから特定の期間のデータを読み込む関数

    :param file_path: CSVファイルのパス
    :param start_date: 開始日時（文字列）
    :param end_date: 終了日時（文字列）
    :return: フィルタリングされたデータフレーム
    """
    df = pd.read_csv(file_path, parse_dates=['timestamp'])

    df['timestamp'] = df['timestamp'].apply(lambda x: x.tz_localize('UTC').tz_convert('Asia/Tokyo'))
    timestamp = pd.to_datetime(add_jst_timezone(df['timestamp']))
    filtered_df = df[(timestamp >= start_data) & (timestamp <= end_date)]

    return filtered_df

def convert_utc_to_jst(utc_datetime):
    """
    UTCの日時を日本時間（JST）に変換する。

    :param utc_datetime: UTCの日時（datetimeオブジェクト）
    :return: JSTに変換された日時（datetimeオブジェクト）
    """
    # UTCとJSTのタイムゾーンを定義
    utc_zone = pytz.timezone('UTC')
    jst_zone = pytz.timezone('Asia/Tokyo')

    # UTC日時をタイムゾーン付きの日時に変換
    utc_datetime = utc_zone.localize(utc_datetime)

    # JSTに変換
    jst_datetime = utc_datetime.astimezone(jst_zone)

    return jst_datetime

def add_jst_timezone(naive_datetime):
    """
    tz-naiveな日時にJSTのタイムゾーン情報を付加する。
    
    :param naive_datetime: タイムゾーン情報を持たない日時（datetimeオブジェクト）
    :return: JSTタイムゾーン情報を持つ日時（datetimeオブジェクト）
    """
    jst_zone = pytz.timezone('Asia/Tokyo')
    localized_datetime = jst_zone.localize(naive_datetime)
    return pd.Timestamp(localized_datetime)


async def main(symbol, intervals):
    while True:
        sleep_flg = True
        for interval in intervals:
            try:
                last_timestamp = get_last_timestamp()
                end = adjust_to_interval(datetime.utcnow())
                if last_timestamp < end:
                    df = await update_data(symbol, interval, last_timestamp, end)
                    save_data(df, interval)
                    sleep_flg = False

                    lstm_last_timestamp = add_jst_timezone(read_last_timestamp())
                    dataset_last_timestamp = convert_utc_to_jst(last_timestamp)
                    if lstm_last_timestamp < dataset_last_timestamp:
                        retrain_csvdata = load_data_from_csv(csv_path, lstm_last_timestamp, dataset_last_timestamp)
                        retrain_csvdata.to_csv(retrain_csv, mode='w', index=False)

            except Exception as e:
                logging.error(f"Error occurred during data update for interval {interval}: {e}")

        if sleep_flg:
            await asyncio.sleep(300)


if __name__ == "__main__":
    symbol = 'BTCUSD'
    intervals = ['5']
    asyncio.run(main(symbol, intervals))

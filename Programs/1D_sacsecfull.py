import aiohttp
import asyncio
import pandas as pd
from datetime import datetime, timedelta

async def fetch(session, url):
    """
    非同期でHTTP GETリクエストを実行する。
    """
    async with session.get(url) as response:
        return await response.json()

async def fetch_ohlcv(symbol, start, end):
    """
    特定の期間のOHLCVデータを非同期で取得する。
    """
    async with aiohttp.ClientSession() as session:
        url = f'https://api.bybit.com/v2/public/kline/list?symbol={symbol}&interval=D&from={start}&to={end}'
        response = await fetch(session, url)
        data = response.get('result', [])
        if not data:
            return pd.DataFrame()  # 空のDataFrameを返す

        df = pd.DataFrame(data)
        df['timestamp'] = pd.to_datetime(df['open_time'], unit='s')
        return df[['timestamp', 'open', 'high', 'low', 'close', 'volume']]

async def main(symbol, start_date, end_date):
    """
    指定された期間にわたってOHLCVデータを取得し、結合する。
    """
    start = datetime.strptime(start_date, '%Y-%m-%d')
    end = datetime.strptime(end_date, '%Y-%m-%d')

    # データ取得タスクを作成
    tasks = []
    while start < end:
        next_end = start + timedelta(days=30)  # 30日ごとのデータを取得
        if next_end > end:
            next_end = end
        start_timestamp = int(start.timestamp())
        end_timestamp = int(next_end.timestamp())
        task = fetch_ohlcv(symbol, start_timestamp, end_timestamp)
        tasks.append(task)
        start = next_end

    # 非同期でデータ取得を実行
    dataframes = await asyncio.gather(*tasks)
    return pd.concat(dataframes)

# 実行部分
start_date = '2018-01-01'
end_date = '2023-11-24'
symbol = 'BTCUSD'

df = asyncio.run(main(symbol, start_date, end_date))
df.to_csv('bybit_ohlcv_async.csv', index=False)

import time
import datetime
import math
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pybit import usdt_perpetual
from pandas import json_normalize

count = 5 #過去データ200件を何回分取得するか

session_unauth = usdt_perpetual.HTTP(
    endpoint="https://api-testnet.bybit.com"
)

period = 4 * 200 * 60 * 60 # 4H * 200item * 60(m) * 60(s)

ts0 = time.time()
print(ts0)

df_list = [] #取得データの一時保存リスト

for i in range(1, count):
    ts = ts0 - period*i
    ts = math.floor(ts)

    #時間確認
    print(ts)
    dt = datetime.datetime.fromtimestamp(ts)
    print(dt.strftime("%Y-%m-%d %H:%M:%S"))

    #ローソク足取得
    result = session_unauth.query_kline(
        symbol="BTCUSDT",
        limit=200, #上限200
        interval=240, #4h
        from_time=ts
    )

    df = json_normalize(result['result'])
    df_list.insert(0, df) #先頭に追加


df = pd.concat(df_list, ignore_index=True)

# ファイル保存
df.to_csv("4h.csv", index=False)

# -------------------以下テスト---------------------

# ファイル読み込み
data = pd.read_csv('4h.csv')

#グラフ
fig, axes = plt.subplots(1, 1, figsize=(18, 4), tight_layout=True)
plt.plot(data[['close', 'open', 'high', 'low']])
plt.legend(['close', 'open', 'high', 'low'])
plt.show()

fig, axes = plt.subplots(1, 1, figsize=(18, 2), tight_layout=True)
plt.plot(data[['volume']], label='volume')
plt.legend()
plt.show()


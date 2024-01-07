#MarketMasterAI/bin

ここはpythonスクリプトをexe化したものと、python上で使用するデータがjsonファイルとして保管されています。

## プロジェクト構造

### EXEファイル
- getPrice_BTCUSDT_ochlv.exe：Bybitから現在日時までの5分間隔のデータを取得し、CSVへ出力する。
- getNews.exe：CoinPostからニュースのデータを取得し、jsonファイルへ出力する。
- convert_cav_data.exe：getPrice_BTCUSDT_ochlv.exeで作成された、CSVを参照し、間隔別のCSVファイルを出力する。（15T、30T、1H、4H、1D）
- Technical.exe：BTCUSDTの価格情報を参照し、テクニカル指標を用いて相場を評価する。それぞれの指標の結果はjsonファイルに出力される。


### Jsonファイル

- 5T_ochl_scaler_parameters.json   ：5分間隔のBTC/USDTの"OCHLデータ"を標準化した際のパラメータを保管
- 5T_volume_scaler_parameters.json ：5分間隔のBTC/USDTの"Volumeデータ"を標準化した際のパラメータを保管
- 15T_ochl_scaler_parameters.json  ：15分間隔のBTC/USDTの"OCHLデータ"を標準化した際のパラメータを保管
- 15T_volume_scaler_parameters.json：15分間隔のBTC/USDTの"Volumeデータ"を標準化した際のパラメータを保管
- 30T_ochl_scaler_parameters.json  ：30分間隔のBTC/USDTの"OCHLデータ"を標準化した際のパラメータを保管
- 30T_volume_scaler_parameters.json：30分間隔のBTC/USDTの"Volumeデータ"を標準化した際のパラメータを保管
- 1H_ochl_scaler_parameters.json   ：1時間間隔のBTC/USDTの"OCHLデータ"を標準化した際のパラメータを保管
- 1H_volume_scaler_parameters.json ：1時間間隔のBTC/USDTの"Volumeデータ"を標準化した際のパラメータを保管
- 4H_ochl_scaler_parameters.json   ：4時間間隔のBTC/USDTの"OCHLデータ"を標準化した際のパラメータを保管
- 4H_volume_scaler_parameters.json ：4時間間隔のBTC/USDTの"Volumeデータ"を標準化した際のパラメータを保管
- 1D_ochl_scaler_parameters.json   ：1日間隔のBTC/USDTの"OCHLデータ"を標準化した際のパラメータを保管
- 1D_volume_scaler_parameters.json ：1日間隔のBTC/USDTの"Volumeデータ"を標準化した際のパラメータを保管

- retrain_5T_ochl_scaler_parameters.json   ：5分間隔のBTC/USDTの"OCHLデータ"を標準化した際のパラメータを保管
- retrain_5T_volume_scaler_parameters.json ：5分間隔のBTC/USDTの"Volumeデータ"を標準化した際のパラメータを保管
- retrain_15T_ochl_scaler_parameters.json  ：15分間隔のBTC/USDTの"OCHLデータ"を標準化した際のパラメータを保管
- retrain_15T_volume_scaler_parameters.json：15分間隔のBTC/USDTの"Volumeデータ"を標準化した際のパラメータを保管
- retrain_30T_ochl_scaler_parameters.json  ：30分間隔のBTC/USDTの"OCHLデータ"を標準化した際のパラメータを保管
- retrain_30T_volume_scaler_parameters.json：30分間隔のBTC/USDTの"Volumeデータ"を標準化した際のパラメータを保管
- retrain_1H_ochl_scaler_parameters.json   ：1時間間隔のBTC/USDTの"OCHLデータ"を標準化した際のパラメータを保管
- retrain_1H_volume_scaler_parameters.json ：1時間間隔のBTC/USDTの"Volumeデータ"を標準化した際のパラメータを保管
- retrain_4H_ochl_scaler_parameters.json   ：4時間間隔のBTC/USDTの"OCHLデータ"を標準化した際のパラメータを保管
- retrain_4H_volume_scaler_parameters.json ：4時間間隔のBTC/USDTの"Volumeデータ"を標準化した際のパラメータを保管
- retrain_1D_ochl_scaler_parameters.json   ：1日間隔のBTC/USDTの"OCHLデータ"を標準化した際のパラメータを保管
- retrain_1D_volume_scaler_parameters.json ：1日間隔のBTC/USDTの"Volumeデータ"を標準化した際のパラメータを保管

- Last_timestamp.json：LSTMが学習に使用したデータセットの最後のタイムスタンプを保管

- trending_news.json：取得したニュースのデータを保管（Title, Link, MainText）

- Technical.json：テクニカル指標と、その指標がonかoffかの情報が保管されている。
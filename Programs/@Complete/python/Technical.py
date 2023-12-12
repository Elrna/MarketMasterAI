import pandas as pd
import json
import logging

def setup_logging():
    """
    ログの設定を行い、ログファイルに出力する。
    """
    logging.basicConfig(filename='D:/MarketMasterAI/Log/Technical.log', 
                        level=logging.INFO, 
                        format='%(asctime)s:%(levelname)s:%(message)s')

def load_data(file_path):
    """
    CSVファイルからBTCUSDTの市場データを読み込む。
    """
    try:
        return pd.read_csv(file_path, parse_dates=['timestamp'])
    except Exception as e:
        logging.error(f"Failed to load data from {file_path}: {e}")
        raise

def calculate_sma(data, period):
    """
    指定された期間の単純移動平均（SMA）を計算する。
    """
    try:
        return data.rolling(window=period).mean()
    except Exception as e:
        logging.error(f"Failed to calculate SMA: {e}")
        raise

def calculate_rsi(data, period=14):
    """
    相対力指数（RSI）を計算する。
    """
    try:
        delta = data.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        return 100 - (100 / (1 + rs))
    except Exception as e:
        logging.error(f"Failed to calculate RSI: {e}")
        raise

def calculate_bollinger_bands(data, period=20, num_std_dev=2):
    """
    ボリンジャーバンドを計算する。
    """
    try:
        sma = data.rolling(window=period).mean()
        std_dev = data.rolling(window=period).std()
        upper_band = sma + (std_dev * num_std_dev)
        lower_band = sma - (std_dev * num_std_dev)
        return upper_band, sma, lower_band
    except Exception as e:
        logging.error(f"Failed to calculate Bollinger Bands: {e}")
        raise

def calculate_macd(data, short_period=12, long_period=26, signal_period=9):
    """
    MACD（Moving Average Convergence Divergence）を計算する。
    """
    try:
        short_ema = data.ewm(span=short_period, adjust=False).mean()
        long_ema = data.ewm(span=long_period, adjust=False).mean()
        macd = short_ema - long_ema
        signal = macd.ewm(span=signal_period, adjust=False).mean()
        return macd, signal
    except Exception as e:
        logging.error(f"Failed to calculate MACD: {e}")
        raise

def read_paths_from_json(json_path):
    """
    JSONファイルからCSVのパスと出力先のJSONファイルのパスを読み込む。
    """
    try:
        with open(json_path, 'r') as file:
            data = json.load(file)
            csv_path = data['csv_paths']['5min_BTC_price']
            output_json_path = data['json_paths']['Technical']
            return csv_path, output_json_path
    except Exception as e:
        logging.error(f"Failed to read paths from JSON: {e}")
        raise

def determine_market_trend(sma, rsi, upper_band, lower_band, macd, signal, adx, stochastic_k, stochastic_d, vwap, fibonacci_levels, latest_close):
    """
    各テクニカル指標に基づいて市場のトレンドを判断する。

    Args:
    sma (pandas.Series): 単純移動平均。
    rsi (pandas.Series): 相対力指数。
    upper_band (pandas.Series): ボリンジャーバンドの上限。
    lower_band (pandas.Series): ボリンジャーバンドの下限。
    macd (pandas.Series): MACDライン。
    signal (pandas.Series): MACDのシグナルライン。
    adx (pandas.Series): 平均方向指数。
    stochastic_k (pandas.Series): ストキャスティクスオシレータの%K。
    stochastic_d (pandas.Series): ストキャスティクスオシレータの%D。
    vwap (pandas.Series): 出来高加重平均価格。
    fibonacci_levels (Dict[str, float]): フィボナッチリトレースメントレベル。
    latest_close (float): 最新のクローズ価格。

    Returns:
    Dict[str, bool]: 各テクニカル指標に基づく市場のトレンド。
    """    
    try:
        latest_sma = sma.iloc[-1]
        latest_rsi = rsi.iloc[-1]
        latest_upper_band = upper_band.iloc[-1]
        latest_lower_band = lower_band.iloc[-1]
        latest_macd = macd.iloc[-1]
        latest_signal = signal.iloc[-1]
        latest_adx = adx.iloc[-1]
        latest_stochastic_k = stochastic_k.iloc[-1]
        latest_stochastic_d = stochastic_d.iloc[-1]
        latest_vwap = vwap.iloc[-1]

        trends = {
            "SMA": bool(latest_sma > 0),
            "RSI": bool(latest_rsi < 70 and latest_rsi > 30),
            "Bollinger": bool(latest_upper_band > 0 and latest_lower_band < 0),
            "MACD": bool(latest_macd > latest_signal),
            "ADX": bool(latest_adx > 25),
            "Stochastic": bool(latest_stochastic_k > 20 and latest_stochastic_k < 80 and latest_stochastic_k > latest_stochastic_d),
            "VWAP": bool(latest_close > latest_vwap),
            "Fibonacci": bool(latest_close > fibonacci_levels["0.618"])
        }
        return trends
    except Exception as e:
        logging.error(f"Failed to determine market trend: {e}")
        raise

def write_to_json(data, json_path):
    """
    分析結果をJSONファイルに書き込む。
    """
    try:
        with open(json_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
    except Exception as e:
        logging.error(f"Failed to write to JSON file: {e}")
        raise


def calculate_adx(data, period=14):
    """
    平均方向指数（ADX）を計算する。

    Args:
    data (pandas.DataFrame): 価格データ。'high', 'low', 'close'カラムが必要。
    period (int): ADXの計算期間。

    Returns:
    pandas.Series: ADXの値。
    """
    try:
        high = data['high']
        low = data['low']
        close = data['close']

        plus_dm = high.diff()
        minus_dm = low.diff()
        plus_dm[plus_dm < 0] = 0
        minus_dm[minus_dm > 0] = 0

        tr = pd.concat([high - low, abs(high - close.shift()), abs(low - close.shift())], axis=1).max(axis=1)
        atr = tr.rolling(window=period).mean()

        plus_di = 100 * (plus_dm.rolling(window=period).mean() / atr)
        minus_di = abs(100 * (minus_dm.rolling(window=period).mean() / atr))

        adx = abs((plus_di - minus_di) / (plus_di + minus_di)) * 100
        adx = adx.rolling(window=period).mean()

        return adx
    except Exception as e:
        logging.error(f"Failed to calculate ADX: {e}")
        raise

def calculate_stochastic_oscillator(data, k_period=14, d_period=3):
    """
    ストキャスティクスオシレータを計算する。

    Args:
    data (pandas.DataFrame): 価格データ。'high', 'low', 'close'カラムが必要。
    k_period (int): %Kの計算期間。
    d_period (int): %Dの計算期間。

    Returns:
    Tuple[pandas.Series, pandas.Series]: %Kと%Dの値。
    """
    try:
        low_min = data['low'].rolling(window=k_period).min()
        high_max = data['high'].rolling(window=k_period).max()

        k = 100 * ((data['close'] - low_min) / (high_max - low_min))
        d = k.rolling(window=d_period).mean()

        return k, d
    except Exception as e:
        logging.error(f"Failed to calculate Stochastic Oscillator: {e}")
        raise

def calculate_vwap(data):
    """
    出来高加重平均価格（VWAP）を計算する。

    Args:
    data (pandas.DataFrame): 価格データ。'high', 'low', 'close', 'volume'カラムが必要。

    Returns:
    pandas.Series: VWAPの値。
    """
    try:
        vwap = (data['volume'] * (data['high'] + data['low'] + data['close']) / 3).cumsum() / data['volume'].cumsum()
        return vwap
    except Exception as e:
        logging.error(f"Failed to calculate VWAP: {e}")
        raise

def calculate_fibonacci_retracement(data):
    """
    フィボナッチリトレースメントレベルを計算する。

    Args:
    data (pandas.Series): 価格データ。

    Returns:
    Dict[str, float]: フィボナッチリトレースメントレベル。
    """
    try:
        max_price = data.max()
        min_price = data.min()
        difference = max_price - min_price
        first_level = max_price - 0.236 * difference
        second_level = max_price - 0.382 * difference
        third_level = max_price - 0.618 * difference

        levels = {
            "0.236": first_level,
            "0.382": second_level,
            "0.618": third_level
        }

        return levels
    except Exception as e:
        logging.error(f"Failed to calculate Fibonacci Retracement levels: {e}")
        raise

def main():
    setup_logging()
    try:
        # パスの読み込み
        csv_path, output_json_path = read_paths_from_json("D:/MarketMasterAI/Def/Path.json")
        logging.info("Successfully read paths from JSON.")

        # データの読み込み
        market_data = load_data(csv_path)
        logging.info(f"Successfully loaded market data from {csv_path}.")

        # 各テクニカル指標の計算
        sma = calculate_sma(market_data['close'], 20)
        rsi = calculate_rsi(market_data['close'])
        upper_band, middle_band, lower_band = calculate_bollinger_bands(market_data['close'])
        macd, signal = calculate_macd(market_data['close'])
        adx = calculate_adx(market_data, 14)
        stochastic_k, stochastic_d = calculate_stochastic_oscillator(market_data, 14, 3)
        vwap = calculate_vwap(market_data)
        fibonacci_levels = calculate_fibonacci_retracement(market_data['close'])
        logging.info("Successfully calculated technical indicators.")

        # 市場トレンドの判断
        latest_close = market_data['close'].iloc[-1]
        trends = determine_market_trend(sma, rsi, upper_band, lower_band, macd, signal, adx, stochastic_k, stochastic_d, vwap, fibonacci_levels, latest_close)
        logging.info("Successfully determined market trends.")

        # 結果をJSONファイルに書き込む
        write_to_json(trends, output_json_path)
        logging.info(f"Successfully wrote analysis results to {output_json_path}.")

    except Exception as e:
        logging.error(f"An error occurred in the main process: {e}")
if __name__ == '__main__':
    main()



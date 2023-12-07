import requests
import json
import pandas as pd
from datetime import datetime
import logging
import ccxt

# BybitのAPIキーとシークレット（環境変数から取得することを推奨）
API_KEY = 'your_api_key'
API_SECRET = 'your_api_secret'

bybit = ccxt.bybit({"apiKey": API_KEY, "secret": API_SECRET})

with open("D:\MarketMasterAI\Def\Path.json", 'r') as file:
    data = json.load(file)
    m_csv = data["csv_paths"]["Portfolio"]
    m_json = data["json_paths"]["Portfolio"]
    m_log = data["log_paths"]["Portfolio"]

logging.basicConfig(filename=m_log, level=logging.INFO,
                        format='%(asctime)s:%(levelname)s:%(message)s')



def get_acquisition_price(api_key, api_secret):
    """
    Bybit APIを使用してBTCUSDTの取得単価を取得する

    Parameters:
    api_key (str): APIキー
    api_secret (str): APIシークレット

    Returns:
    float: 取得単価
    """
    try:
        # Bybit APIのエンドポイント
        endpoint = 'https://api.bybit.com/v2/private/position/list'
        params = {
            'api_key': api_key,
            'symbol': 'BTCUSDT',
            # ここに追加のパラメータ（署名など）を追加
        }
        response = requests.get(endpoint, params=params)
        data = response.json()

        # 取得単価の計算（デモコードでは単純化しています）
        acquisition_price = data['result']['entry_price']
        logging.info("Acquisition price retrieved successfully.")
        return acquisition_price

    except Exception as e:
        logging.error(f"Error in getting acquisition price: {e}")
        raise

def get_total_assets(api_key, api_secret):
    """
    Bybit APIを使用して自身の資産総額を取得する。

    Parameters:
    api_key (str): APIキー
    api_secret (str): APIシークレット

    Returns:
    float: 資産総額
    """
    try:
        # Bybit APIのエンドポイント
        endpoint = 'https://api.bybit.com/v2/private/wallet/balance'
        params = {
            'api_key': api_key,
            # ここに追加のパラメータ（署名など）を追加
        }
        response = requests.get(endpoint, params=params)
        data = response.json()

        # 資産総額の計算（デモコードでは単純化しています）
        total_assets = data['result']['BTC']['wallet_balance']
        logging.info("Total assets retrieved successfully.")
        return total_assets
    except Exception as e:
        logging.error(f"Error in getting total assets: {e}")
        raise

def calculate_profit(total_assets, acquisition_price):
    """
    資産総額から取得単価を引いて、利益を算出する。

    Parameters:
    total_assets (float): 資産総額
    acquisition_price (float): 取得単価

    Returns:
    float: 利益
    """
    try:
        profit = total_assets - acquisition_price
        logging.info("Profit calculated successfully.")
        return profit
    except Exception as e:
        logging.error(f"Error in calculating profit: {e}")
        raise

def calculate_tax(profit, tax_rate):
    """
    利益に基づいて税金を計算する。

    Parameters:
    profit (float): 利益
    tax_rate (float): 税率（例：0.2は20%）

    Returns:
    float: 税金
    """
    try:
        tax = profit * tax_rate
        logging.info("Tax calculated successfully.")
        return tax
    except Exception as e:
        logging.error(f"Error in calculating tax: {e}")
        raise

def export_to_files(data, json_file, csv_file):
    """
    情報をJSONファイルおよびCSVファイルに出力する。

    Parameters:
    data (dict): 出力するデータ
    json_file (str): JSONファイルのパス
    csv_file (str): CSVファイルのパス

    Returns:
    None
    """
    try:
        # JSONに出力
        with open(json_file, 'w') as file:
            json.dump(data, file)

        # CSVに出力
        df = pd.DataFrame([data])
        df.to_csv(csv_file, index=False)
        logging.info("Data exported to files successfully.")
    except Exception as e:
        logging.error(f"Error in exporting to files: {e}")
        raise

def main():
    try:
        acquisition_price = get_acquisition_price(API_KEY, API_SECRET)
        total_assets = get_total_assets(API_KEY, API_SECRET)
        profit = calculate_profit(total_assets, acquisition_price)
        tax_rate = 0.2  # 税率は例として20%
        tax = calculate_tax(profit, tax_rate)

        data = {
            'acquisition_price': acquisition_price,
            'total_assets': total_assets,
            'profit': profit,
            'tax': tax,
            'timestamp': datetime.now().isoformat()
        }

        export_to_files(data, m_json, m_csv)
        logging.info("Main function executed successfully.")
    except Exception as e:
        logging.error(f"Error in main function: {e}")
if __name__ == '__main__':
    main()

import requests
import logging
import pandas as pd
from api_keys import *

# Set up logging configuration to add timestamps and log levels
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def get_hourly_crypto_data(symbol, to_ts=None, limit=2000):
    logging.info("Starting to fetch hourly crypto date.")
    url = 'https://min-api.cryptocompare.com/data/v2/histohour'
    parameters = {
        'fsym': symbol,
        'tsym': 'USD',
        'limit': limit,
        'api_key': API_KEY
    }
    if to_ts:
        parameters['toTs'] = to_ts
    response = requests.get(url, params=parameters)
    data = response.json()
    if response.status_code == 200 and data.get('Response') == 'Success':
        df = pd.DataFrame(data['Data']['Data'])
        df['time'] = pd.to_datetime(df['time'], unit='s')
        df = df[['time', 'open', 'close', 'high', 'low', 'volumefrom', 'volumeto']]
        df.rename(columns={'time': 'datetime', 'volumefrom': 'volume'}, inplace=True)
        logging.info("Successfully fetched data on hourly crypto date.")
        return df
    else:
        print("Error fetching data:", data.get('Message', 'No error message'))
        logging.info("Unsuccessfully fetched data on hourly crypto date.")
        return pd.DataFrame()


def append_data_for_period(symbol, total_hours=24 * 365 * 2):
    logging.info("Starting search all data for our period")
    all_data = pd.DataFrame()
    hours_retrieved = 0
    to_ts = None
    while hours_retrieved < total_hours:
        limit = min(2000, total_hours - hours_retrieved)
        df = get_hourly_crypto_data(symbol, to_ts=to_ts, limit=limit)
        if df.empty:
            break
        all_data = pd.concat([df, all_data], ignore_index=True)
        to_ts = int(df['datetime'].iloc[0].timestamp()) - 1
        hours_retrieved += len(df)
        logging.info(f"Retrieved {hours_retrieved} hours of data for {symbol}.")
    logging.info("Successfully searched all data for our period")
    return all_data


def fetch_top_cryptos_by_market_cap(limit=10):
    """Retrieve a list of the top cryptocurrencies by market cap."""
    logging.info("Starting to fetch top cryptocurrencies ranked by market capitalization.")
    url = 'https://api.coingecko.com/api/v3/coins/markets'
    parameters = {
        'vs_currency': 'usd',
        'order': 'market_cap_desc',  # Sorted by market cap in descending order
        'per_page': limit,
        'page': 1,
        'sparkline': False
    }
    response = requests.get(url, params=parameters)
    cryptocurrencies = response.json()
    logging.info("Successfully fetched data on top market cap cryptocurrencies.")
    return cryptocurrencies


def fetch_top_cryptos_by_volume(limit=10):
    """Retrieve a list of the top cryptocurrencies by trading volume over the last 24 hours."""
    logging.info("Starting to fetch the most traded cryptocurrencies over the past 24 hours.")
    url = 'https://api.coingecko.com/api/v3/coins/markets'
    parameters = {
        'vs_currency': 'usd',
        'order': 'volume_desc',  # Sorted by trading volume in descending order
        'per_page': limit,
        'page': 1,
        'sparkline': False
    }
    response = requests.get(url, params=parameters)
    cryptocurrencies = response.json()
    logging.info("Successfully fetched data on top volume cryptocurrencies.")
    return cryptocurrencies


def fetch_global_market_cap():
    """Fetch the total market capitalization of the entire cryptocurrency market."""
    logging.info("Fetching the total market capitalization for all cryptocurrencies.")
    url = 'https://api.coingecko.com/api/v3/global'
    response = requests.get(url)
    market_data = response.json()
    logging.info("Successfully fetched global market cap data.")
    return market_data['data']['total_market_cap']['usd']

def print_base_info():
    try:
        # Get data for top cryptocurrencies by market cap and volume
        top_cryptos_by_market_cap = fetch_top_cryptos_by_market_cap()
        top_cryptos_by_volume = fetch_top_cryptos_by_volume()
        entire_market_cap = fetch_global_market_cap()

        print("Top cryptocurrencies by market capitalization:")
        for crypto in top_cryptos_by_market_cap:
            formatted_market_cap = f"{crypto['market_cap']:,}".replace(",", ".")
            print(f"{crypto['name']} (Symbol: {crypto['symbol']}) - Market Cap: ${formatted_market_cap}")

        print("\nTop cryptocurrencies by trading volume in the past 24 hours:")
        for crypto in top_cryptos_by_volume:
            formatted_volume = f"{crypto['total_volume']:,}".replace(",", ".")
            print(f"{crypto['name']} (Symbol: {crypto['symbol']}) - Volume: ${formatted_volume}")

        formatted_total_market_cap = f"{entire_market_cap:,}".replace(",", ".")
        print(f"\nTotal cryptocurrency market cap worldwide: ${formatted_total_market_cap}\n")
    except Exception as error:
        logging.error("An error occurred while fetching cryptocurrency data.", exc_info=True)

def get_prices():
    try:
        # Get hourly data for BTC and ETH
        hourly_data_btc = append_data_for_period("BTC")[['datetime', 'open', 'high', 'low', 'close', 'volume']].copy()
        hourly_data_eth = append_data_for_period("ETH")[['datetime', 'open', 'high', 'low', 'close', 'volume']].copy()
        hourly_data_btc['name'] = 'BTC'
        hourly_data_eth['name'] = 'ETH'
        combined_hourly_data = pd.concat([hourly_data_btc, hourly_data_eth], ignore_index=True)

        # for debug
        # print("Hourly crypto data")
        # for index, row in combined_hourly_data.iterrows():
        #     name = row['name']
        #     date = row['datetime'].strftime('%Y-%m-%d')
        #     open_price = row['open']
        #     high_price = row['high']
        #     low_price = row['low']
        #     close_price = row['close']
        #     volume = row['volume']
        #     print(f"Валюта: {name}, Дата: {date}, Цена открытия: {open_price}, Максимальная цена: {high_price}, "
        #           f"Минимальная цена: {low_price}, Цена закрытия: {close_price}, Объем: {volume}")

        return combined_hourly_data
    except Exception as error:
        logging.error("An error occurred while fetching cryptocurrency data.", exc_info=True)

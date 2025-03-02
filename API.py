import requests
import logging

# Set up logging configuration to add timestamps and log levels
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

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
    print(f"\nTotal cryptocurrency market cap worldwide: ${formatted_total_market_cap}")

except Exception as error:
    logging.error("An error occurred while fetching cryptocurrency data.", exc_info=True)
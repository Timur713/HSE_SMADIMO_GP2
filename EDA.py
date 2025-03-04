import logging

import pandas as pd
import json
from datetime import datetime
import numpy as np

import API

# Set up logging configuration to add timestamps and log levels
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# for debug
# pd.set_option('display.max_columns', None)
# pd.set_option('display.max_rows', None)
# pd.set_option('display.width', None)

# get base data
logging.info('Start getting base data about cryptocurrencies')

base_data = None
advance_data = None


try:
    base_data = API.get_prices()
    logging.info('Successfully finished getting base data about cryptocurrencies')
except Exception as error:
    logging.error("An error occurred while API.get_prices()", exc_info=True)

# json files
file_paths = [
    'scrapping_json_data/cost-per-transaction.json',
    'scrapping_json_data/fees-usd-per-transaction.json',
    'scrapping_json_data/hash-rate.json',
    'scrapping_json_data/mvrv.json',
    'scrapping_json_data/n-payments-per-block.json',
    'scrapping_json_data/n-transactions-per-block.json',
    'scrapping_json_data/n-unique-addresses.json',
    'scrapping_json_data/nvt.json',
    'scrapping_json_data/nvts.json',
    'scrapping_json_data/trade-volume.json'
]

advance_data_dfs = {}
# To fix result of sample(1) func
np.random.seed(42)

logging.info('Start prepare advance data about cryptocurrencies to merge')
try:
    for file_path in file_paths:
        with open(file_path, 'r') as file:
            json_data = json.load(file)

            metric1 = json_data['metric1']

            df = pd.DataFrame(json_data[metric1])

            # Convert timestamp to date
            df['date'] = pd.to_datetime(df['x'], unit='ms').dt.date

            # Sample one row per date without the grouping columns (date)
            df = df.groupby('date', group_keys=False).apply(lambda x: x.sample(1)).reset_index(drop=True)

            # Set date as index and rename column
            df.set_index('date', inplace=True)
            df = df.rename(columns={'y': metric1}).drop(columns='x')

            advance_data_dfs[metric1] = df
    logging.info('Successfully finished prepare advance data about cryptocurrencies to merge')
except Exception as error:
    logging.error("An error occurred while API.get_prices()", exc_info=True)

# Merge all advance_data_dfs
try:
    logging.info('Start merging advance data about cryptocurrencies to each other')
    advance_data = pd.DataFrame(index=pd.Index([], name='date'))  # Initialize empty df
    for df in advance_data_dfs.values():
        advance_data = advance_data.join(df, how='outer')
    logging.info('Successfully finished merging advance data about cryptocurrencies to each other')
except Exception as error:
    logging.error("An error occurred while API.get_prices()", exc_info=True)

print(base_data.head())
print(advance_data.head())

# save to csv for future analytics
base_data.to_csv('base_data.csv', index=True, index_label='Date', sep=',')
advance_data.to_csv('advance_data.csv', index=True, index_label='Date', sep=',')
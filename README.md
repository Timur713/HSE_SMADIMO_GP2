# HSE_SMADIMO_GP2

Group project 2 by Timur Isanbirdin, Andrey Anokhin, Vladislav Staritsyn and Ignat Gurtovoj

## Getting started
1. Get `API_KEY` from `https://developers.coindesk.com/`
2. Create `api_keys.py` file and save this `API_KEY`

# Description
## Get base info by API
`API.py` contains two usefull functions:
- `print_base_info()` # base information about crypto market and top currencies
- `get_prices()` # history prices of BTC and ETH
#### We will use this functions in `EDA.py` file

## Get advance info by web-scrapping (for BTC only)
0. This project already has downloaded files, but you can overwrite them doing next steps
1. First of all, you should run script `web_scrapping.py` to download jsons with advance information about Bitcoin

## EDA
All EDA process is in `EDA.py` file
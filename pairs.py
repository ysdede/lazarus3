from binance.client import Client
from jesse import import_candles

api_key = "x"
api_secret = "x"
sd = '2017-01-01'
exch = 'Binance'
skc = True

client = Client(api_key, api_secret)
exchange_info = client.get_exchange_info()

from jesse.config import config
config['app']['trading_mode'] = 'import-candles'

from jesse.services import db

from jesse.modes import import_candles_mode
print(exchange_info)
for s in exchange_info['symbols']:
    if s['status'] == 'TRADING' and (s['quoteAsset'] == 'USDT' or s['quoteAsset'] == 'BUSD') and s['isSpotTradingAllowed']:
        sym = s['symbol'].replace('USDT', '-USDT')
        print(sym)
        import_candles_mode.run(exch, sym, sd, skc)

db.close_connection()

# import_candles(exchange: str, symbol: str, start_date: str, skip_confirmation: bool)
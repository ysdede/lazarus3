# -*- coding: utf-8 -*-

import os
import sys
import ccxt  # noqa: E402
#
from jesse.config import config
config['app']['trading_mode'] = 'import-candles'
from jesse.services import db
from jesse.modes import import_candles_mode
#


root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root + '/python')
print('CCXT Version:', ccxt.__version__)

# exch, exchccxt = 'Binance Futures', 'future'
exch, exchccxt = 'Binance', 'spot'

sd = '2017-01-01'   # Start date
skc = True          # Skip confirmation

exchange = ccxt.binance({
    'apiKey': 'YOUR_API_KEY',
    'secret': 'YOUR_SECRET',
    'enableRateLimit': True, # required https://github.com/ccxt/ccxt/wiki/Manual#rate-limit
    'options': {
        'defaultType': exchccxt,
    },
})

markets = exchange.load_markets()
exchange.verbose = True  # UNCOMMENT THIS AFTER LOADING THE MARKETS FOR DEBUGGING


def is_active_symbol(exchange, symbol):
    return ((symbol.endswith('USDT') or symbol.endswith('BUSD')) and '.' not in symbol)\
           and (('active' not in exchange.markets[symbol]) or (exchange.markets[symbol]['active']))


for s in exchange.symbols:
    if is_active_symbol(exchange, s):
        symb = s.replace('/', '-')
        print(symb)
        import_candles_mode.run(exch, symb, sd, skc)

db.close_connection()

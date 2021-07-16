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

exch, exchccxt = 'Bitfinex', 'spot'

sd = '2013-01-01'   # Start date
skc = True          # Skip confirmation

exchange = ccxt.bitfinex2({
    'rateLimit': 10000,
    'enableRateLimit': True,
    # 'verbose': True,
})


markets = exchange.load_markets()
exchange.verbose = True  # UNCOMMENT THIS AFTER LOADING THE MARKETS FOR DEBUGGING

blacklist = '1INCH/USD 1INCH/USDT AAVE/USD AAVE/USDT'

def is_active_symbol(exchange, symbol):
    return exchange.markets[symbol]['quote'] == 'USD' and ' ' not in symbol\
           and (('active' not in exchange.markets[symbol]) or (exchange.markets[symbol]['active']))\
           and exchange.markets[symbol]['type'] == 'futures'
           # and symbol not in blacklist

print(exchange.symbols)
# print(exchange.markets)
print(f'Importing {exch} candles...')
print('-'*30)

for s in exchange.symbols:
    if is_active_symbol(exchange, s):
        symb = s.replace('/', '-')
        print(symb)
        import_candles_mode.run(exch, symb, sd, skc)

db.close_connection()

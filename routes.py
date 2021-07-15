# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Make sure to read the docs about routes if you haven't already:
# https://docs.jesse.trade/docs/routes.html
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

from jesse.utils import anchor_timeframe

# trading routes
routes = [
    ('Binance Futures', '1000SHIB-USDT', '2h', 'lazarus3'),
    # ('Binance', 'ETH-USDT', '2h', 'lazarus31'),
    # ('Binance', 'BNB-USDT', '2h', 'lazarus31'),
    # ('Binance', 'LTC-USDT', '2h', 'lazarus31'),
    # ('Binance', 'ETH-USDT', '2h', 'lazarus3'),
    # ('Binance', 'LTC-USDT', '2h', 'lazarus3'),
]

# in case your strategy requires extra candles, timeframes, ...
extra_candles = [
    # ('Binance', 'BTC-USDT', anchor_timeframe('2h')),
]


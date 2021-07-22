# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Make sure to read the docs about routes if you haven't already:
# https://docs.jesse.trade/docs/routes.html
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

from jesse.utils import anchor_timeframe

# trading routes
routes = [
    ('Binance', 'BTC-USDT', '30m', 'lazarusdyn'),
    # ('Binance', 'BNB-USDT', '2h', 'lazarus3'),
    # ('Bitfinex', 'ETH-USD', '1h', 'lazarusdyn'),
    # ('Bitfinex', 'LTC-USD', '2h', 'lazarus3'),
    # ('Bitfinex', 'ETC-USD', '2h', 'lazarus3'),

]

# in case your strategy requires extra candles, timeframes, ...
extra_candles = [
    # ('Bitfinex', 'BTC-USD', '2h'),
]


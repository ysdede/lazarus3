from jesse.strategies import Strategy, cached
from jesse import utils
import jesse.indicators as ta
from jesse.services.selectors import get_all_trading_routes
from optvars import cl

class lazarusdyn(Strategy):
    def __init__(self):
        super().__init__()
        self.losecount = 0
        self.wincount = 0
        self.winlimit = 2
        self.lastwasprofitable = False
        self.targetprice = 0
        self.multiplier = 1
        self.incr = True            # Martingale like aggressive position sizing.
        self.donchianfilterenabled = False
        self.skipenabled = False    # If last trade was profitable, skip next trade
        self.dnaindex = 1

    def hyperparameters(self):
        return [
            {'name': 'atrlen', 'type': int, 'min': 5, 'max': 120, 'default': 14},
            {'name': 'atrpnl', 'type': int, 'min': 10, 'max': 220, 'default': 201},  # = atrpnl/10, 20.1
            {'name': 'atrstop', 'type': int, 'min': 5, 'max': 60, 'default': 51},   # = atrstop/10, 5.1
            # {'name': 'donchlen', 'type': int, 'min': 2, 'max': 200, 'default': 77},     # Donchian Channel Len.
            # {'name': 'pmpsize', 'type': int, 'min': 10, 'max': 50, 'default': 47},    # /10
            # {'name': 'fast', 'type': int, 'min': 2, 'max': 8, 'default': 6},
            # {'name': 'slow', 'type': int, 'min': 20, 'max': 48, 'default': 44},
            # {'name': 'clindex', 'type': int, 'min': 0, 'max': 134, 'default': 96},

        ]

    @property
    def atrpnl(self):
        return self.hp['atrpnl'] / 10

    @property
    def atrstop(self):
        return self.hp['atrstop'] / 10

    @property
    def atrlen(self):
        return self.hp['atrlen']

    @property
    def donchianlen(self):
        return 77  # self.hp['donchlen']

    @property
    def pumpsize(self):
        return 47  # .hp['pmpsize']

    @property
    def ewofast(self):
        return 6  # self.hp['fast']

    @property
    def ewoslow(self):
        return 44  # self.hp['slow']

    @property
    def limit(self):
        return 4  # cl[self.hp['clindex']][0]

    @property
    def carpan(self):
        return 0.66  # cl[self.hp['clindex']][1] / 50

    @property
    def pumplookback(self):
        return 3


    @property
    @cached
    def positionsize(self):
        numberofroutes = len(get_all_trading_routes())
        return 8 * numberofroutes

    @property
    @cached
    def atr(self):
        return ta.atr(self.candles, self.atrlen)

    @property
    @cached
    def entry_donchian(self):
        return ta.donchian(self.candles, self.donchianlen, sequential=False)

    @property
    @cached
    def slow_ema(self):
        return ta.ema(self.candles, self.ewoslow, sequential=True)

    @property
    @cached
    def fast_ema(self):
        return ta.ema(self.candles, self.ewofast, sequential=True)

    @cached
    def isdildo(self, index):
        open = self.candles[:, 1][index]
        close = self.candles[:, 2][index]
        return abs(open - close) * 100 / open > self.pumpsize / 10

    @property
    @cached
    def dumpump(self):
        open = self.candles[:, 1][-self.pumplookback]
        close = self.candles[:, 2][-1]
        multibardildo = abs(open - close) * 100 / open > self.pumpsize / 10
        return self.isdildo(-1) or self.isdildo(-2) or self.isdildo(-3) or self.isdildo(-4) or multibardildo

    def should_long(self) -> bool:
        dc = True
        if self.donchianfilterenabled:
            dc = self.close >= self.entry_donchian[1]
        return utils.crossed(self.fast_ema, self.slow_ema, direction='above', sequential=False) and not self.dumpump and dc

    def should_short(self) -> bool:
        dc = True
        if self.donchianfilterenabled:
            dc = self.close <= self.entry_donchian[1]
        return utils.crossed(self.fast_ema, self.slow_ema, direction='below', sequential=False) and not self.dumpump and dc

    @property
    def calcqty(self):
        if self.incr and not self.lastwasprofitable and self.losecount <= self.limit:
            return (self.capital / self.positionsize) * self.multiplier
        return self.capital / self.positionsize

    def go_long(self):
        sl = self.price - (self.atrstop * self.atr)
        tp = self.price + (self.atrpnl * self.atr)
        # print('long price: ', self.price, 'sl: ', sl, 'take profit: ', tp, 'atr: ', self.atr, 'atrpnl: ', self.atrpnl)
        qty = utils.size_to_qty(self.calcqty, self.price, fee_rate=self.fee_rate) * self.leverage

        self.buy = qty, self.price
        self.stop_loss = qty, sl
        self.take_profit = qty, tp
        self.targetprice = tp

    def go_short(self):
        sl = self.price + (self.atrstop * self.atr)
        tp = self.price - (self.atrpnl * self.atr)
        # print('short price: ', self.price, 'sl: ', sl, 'take profit: ', tp, 'atr: ', self.atr, 'atrpnl: ', self.atrpnl)
        qty = utils.size_to_qty(self.calcqty, self.price, fee_rate=self.fee_rate) * self.leverage

        self.sell = qty, self.price
        self.stop_loss = qty, sl
        self.take_profit = qty, tp
        self.targetprice = tp

    def update_position(self):
        # if self.position.pnl_percentage / self.position.leverage > (self.targetpnl / 10):
        if self.is_long and self.price >= self.targetprice:
            self.liquidate()

        if self.is_short and self.price <= self.targetprice:
            self.liquidate()

        # c. Emergency exit! Close position at trend reversal
        if utils.crossed(self.fast_ema, self.slow_ema, sequential=False):
            self.liquidate()

    def on_stop_loss(self, order):
        self.lastwasprofitable = False
        self.losecount += 1
        self.wincount = 0
        self.multiplier = self.multiplier * (1 + self.carpan)  # = 1 + 0.66

    def on_take_profit(self, order):
        self.lastwasprofitable = True
        self.wincount += 1
        self.losecount = 0
        self.multiplier = 1

    def filters(self):
        return [
            self.skipfilter
        ]

    def skipfilter(self):
        if self.skipenabled and self.lastwasprofitable:
            self.lastwasprofitable = False
            return False
        return True

    def before(self):
        pass

    def should_cancel(self) -> bool:
        return True

    def on_open_position(self, order):
        pass

from jesse.strategies import Strategy, cached
from jesse import utils
import jesse.indicators as ta
from optvars import cl


class lazarus3(Strategy):
    def __init__(self):
        super().__init__()
        self.losecount = 0
        self.wincount = 0
        self.winlimit = 2
        self.lastwasprofitable = False
        self.multiplier = 1
        self.incr = True            # Martingale like aggressive position sizing.
        self.donchianfilterenabled = False
        self.skipenabled = False    # If last trade was profitable, skip next trade

        # Test period: 2021-05-01 2021-07-13 - Bitfinex BTC-USD 5x Lev. w/ Binance fee rate
        self.positionsize, self.targetpnl, self.targetstop, self.donchianlen, self.pumpsize, self.ewofast, self.ewoslow, self.pumplookback = \
            8, 296, 87, 183, 47, 6, 44, 3  # vaJpp;g   + 2.58    92.98   6.07    %96.65  %-29.14 --> vaJpC;g *****
        # 8, 253, 87, 183, 26, 3, 41, 3     #   vXJp.._   + 3.48    156.66  11.19   %103.69 %-20.69 *
        # 8, 253, 87, 183, 33, 3, 41, 3     #   vXJp5._   + 3.15    99.97   7.56    %95.77  %-26.48 ** High DD
        # 8, 258, 172, 178, 33, 4, 42, 3    #   sYon51`   + 2.64    53.78   5.95    %75.75  %-28.15 ** High DD
        # 8, 310, 151, 183, 33, 3, 21, 3    #   vdfp5.)   - 2.46    44.74   4.52    %66.18  %-25.14 High DD
        # 8, 281, 87, 183, 50, 4, 44, 3     #   v^JpF/g   + 2.59    70.64   6.06    %94.28  %-36.05
        # 8, 258, 128, 178, 33, 4, 42, 3    #   vY\n51`   + 2.64    53.78   5.95    %75.75  %-28.15 **
        # 8, 281, 87, 183, 50, 4, 39, 3     #   Z^JpF/Y   + 2.98    123.77  7.6     %99.78  %-23.73 **

        # 8, 310, 151, 183, 33, 7, 46, 3    #   vdfp5@l *   1.62    8.35    3.69    %35     %-42
        # 8, 310, 147, 190, 33, 6, 46, 3    #   vdds59l *   1.78    12.18   3.6     %34     %-26.82
        # 8, 243, 87, 25, 30, 3, 41, 3      #   vVJ/2._   + 3.32    144.8   10.74   %102.34 %-21.64 - 2021
        # 8, 205, 35, 71, 59, 3, 44, 3      #   vN3BO,f *   2.45    38.49   4.84    %70     %-33
        # 8, 310, 172, 190, 33, 7, 46, 3    #   vdos5>l *   1.62    8.35    3.69    %35     %-42
        # 8, 338, 35, 64, 92, 4, 46, 3      #   vj3?o1l *   0.76    -       1.31    --
        # 8, 372, 172, 183, 63, 3, 40, 3    #   vqopR,] *** 2.43    41.57   4.5     %74     %-34.58
        # 8, 296, 103, 183, 54, 6, 44, 3    #   vaQpJ;g *** 2.48    76.15   5.82    %89     %-29
        # 8, 310, 49, 64, 39, 4, 33, 3      #   kd9?;1H *** 2.46    32.03   6.52    %63     %-32
        # 8, 281, 87, 183, 50, 4, 38, 3     #   v^JpF/U   + 2.65    65.75   6.49    %81.89  %-27.56 ***
        # 8, 296, 156, 183, 54, 6, 44, 3    #   vahpJ;g   + 2.48    76.15   5.82    %89.11  %-29.11 ***
        # 8, 296, 87, 183, 47, 6, 44, 3     #   vaJpC;g   + 2.58    92.98   6.07    %96.65  %-29.14 *****

    def hyperparameters(self):
        return [
            {'name': 'optindex', 'type': int, 'min': 0, 'max': 134, 'default': 96},  # Multiplier fine tuning
        ]

    @property
    def limit(self):
        return cl[self.hp['optindex']][0]

    @property
    def carpan(self):
        return cl[self.hp['optindex']][1]

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
        sl = self.targetstop / 1000
        qty = utils.size_to_qty(self.calcqty, self.price, fee_rate=self.fee_rate) * self.leverage

        self.buy = qty, self.price
        self.stop_loss = qty, self.price - (self.price * sl)

    def go_short(self):
        sl = self.targetstop / 1000
        qty = utils.size_to_qty(self.calcqty, self.price, fee_rate=self.fee_rate) * self.leverage

        self.sell = qty, self.price
        self.stop_loss = qty, self.price + (self.price * sl)

    def update_position(self):
        if self.position.pnl_percentage / self.position.leverage > (self.targetpnl / 10):
            self.liquidate()

        # c. Emergency exit! Close position at trend reversal
        if utils.crossed(self.fast_ema, self.slow_ema, sequential=False):
            self.liquidate()

    def on_stop_loss(self, order):
        self.lastwasprofitable = False
        self.losecount += 1
        self.wincount = 0
        self.multiplier = self.multiplier * (1 + (self.carpan/50))

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

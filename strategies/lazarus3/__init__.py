from jesse.strategies import Strategy, cached
from jesse import utils
import jesse.indicators as ta


class lazarus3(Strategy):
    def __init__(self):
        super().__init__()
        self.losecount = 0
        self.wincount = 0
        self.winlimit = 2
        self.lastwasprofitable = False
        self.multiplier = 1
        self.positionsize = 10
        self.incr = True
        self.targetpnl = 296
        self.targetstop = 87
        self.pumpsize = 47
        self.pumplookback = 3
        self.ewofast = 6
        self.ewoslow = 44

    def hyperparameters(self):
        return [
            {'name': 'carpan', 'type': int, 'min': 5, 'max': 75, 'default': 66},  # Multiplier fine tuning
            {'name': 'raiselimit', 'type': int, 'min': 2, 'max': 5, 'default': 4},  # Limit
        ]

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
        return utils.crossed(self.fast_ema, self.slow_ema, direction='above', sequential=False) and not self.dumpump

    def should_short(self) -> bool:
        return utils.crossed(self.fast_ema, self.slow_ema, direction='below', sequential=False) and not self.dumpump

    @property
    def calcqty(self):
        if self.incr and not self.lastwasprofitable and self.losecount <= self.hp['raiselimit']:
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
        self.multiplier = self.multiplier * (1 + (self.hp['carpan']/100))

    def on_take_profit(self, order):
        self.lastwasprofitable = True
        self.wincount += 1
        self.losecount = 0
        self.multiplier = 1

    def before(self):
        pass

    def should_cancel(self) -> bool:
        return True

    def on_open_position(self, order):
        pass

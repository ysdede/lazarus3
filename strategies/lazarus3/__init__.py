from jesse.strategies import Strategy, cached
from jesse import utils
import jesse.indicators as ta
import custom_indicators as cta

class lazarus3(Strategy):
    def __init__(self):
        super().__init__()
        self.losecount = 0
        self.wincount = 0
        self.winlimit = 2
        self.lastwasprofitable = False
        self.multiplier = 1
        self.positionsize = 8
        self.incr = True
        self.targetpnl = 296
        self.targetstop = 87
        self.pumpsize = 47
        self.pumplookback = 3
        self.ewofast = 6
        self.ewoslow = 44
        self.partialexitenabled = True
        self.increasepositionenabled = False
        self.obl = 53
        self.osl = -53
        self.initialqty = 0
        self.exitcounter = 0
        self.exitpoints = [0.05, 0.35, 0.10]

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
    def is_dildo(self, index):
        open = self.candles[:, 1][index]
        close = self.candles[:, 2][index]
        return abs(open - close) * 100 / open > self.pumpsize / 10

    @property
    @cached
    def dump_pump(self):
        open = self.candles[:, 1][-self.pumplookback]
        close = self.candles[:, 2][-1]
        multibardildo = abs(open - close) * 100 / open > self.pumpsize / 10
        return self.is_dildo(-1) or self.is_dildo(-2) or self.is_dildo(-3) or self.is_dildo(-4) or multibardildo

    # Wavetrend funcs. -------------->
    @property
    @cached
    def wt(self):
        return ta.wt(self.candles, wtchannellen=9, wtaveragelen=12, wtmalen=3,
                            oblevel=self.obl, oslevel=self.osl,
                            source_type="close", sequential=True)

    @property
    @cached
    def wt_crossed(self):
        return utils.crossed(self.wt.wt1, self.wt.wt2, direction=None, sequential=False)

    @property
    def wt_cross_up(self):
        return self.wt.wtCrossUp[-1]

    @property
    def wt_cross_down(self):
        return self.wt.wtCrossDown[-1]

    @property
    def wt_oversold(self):
        return self.wt.wtOversold[-1]

    @property
    def wt_overbought(self):
        return self.wt.wtOverbought[-1]

    @property
    def wt_buy(self):
        return self.wt_oversold and self.wt_cross_up and self.wt_crossed

    @property
    def wt_sell(self):
        return self.wt_crossed and self.wt_cross_down and self.wt_overbought
    # END of Wavetrend funcs. <--------------

    def should_long(self) -> bool:
        return utils.crossed(self.fast_ema, self.slow_ema, direction='above', sequential=False) and not self.dump_pump

    def should_short(self) -> bool:
        return utils.crossed(self.fast_ema, self.slow_ema, direction='below', sequential=False) and not self.dump_pump

    @property
    def calc_qty(self):
        if self.incr and not self.lastwasprofitable and self.losecount <= self.hp['raiselimit']:
            return (self.capital / self.positionsize) * self.multiplier
        return self.capital / self.positionsize

    def go_long(self):
        sl = self.targetstop / 1000
        qty = utils.size_to_qty(self.calc_qty, self.price, fee_rate=self.fee_rate) * self.leverage

        self.buy = qty, self.price
        self.stop_loss = qty, self.price - (self.price * sl)
        self.initialqty = qty
        self.exitcounter = 0

    def go_short(self):
        sl = self.targetstop / 1000
        qty = utils.size_to_qty(self.calc_qty, self.price, fee_rate=self.fee_rate) * self.leverage

        self.sell = qty, self.price
        self.stop_loss = qty, self.price + (self.price * sl)
        self.initialqty = qty
        self.exitcounter = 0

    def update_position(self):
        # a. Profit target hit. Close Position
        if self.position.pnl_percentage / self.position.leverage > (self.targetpnl / 10):
            self.liquidate()

        # b. Take profit at wavetrend buy sell signals
        if self.partialexitenabled:
            if self.is_long and self.wt_sell:
                self.partial_liq()

            if self.is_short and self.wt_buy:
                self.partial_liq()

        # c. Emergency exit! Close position at trend reversal
        if utils.crossed(self.fast_ema, self.slow_ema, sequential=False):
            self.liquidate()

        # d. Increase position. TODO: Update stoploss
        if self.increasepositionenabled:
            if self.is_long and self.wt_buy:
                qty = utils.size_to_qty(self.capital / 15, self.price, fee_rate=self.fee_rate) * self.leverage
                self.buy = qty, self.price

            if self.is_short and self.wt_sell:
                qty = utils.size_to_qty(self.capital / 15, self.price, fee_rate=self.fee_rate) * self.leverage
                self.sell = qty, self.price

    # Partial Exit Func.
    def partial_liq(self):
        if self.exitcounter < len(self.exitpoints) - 1:
            if self.position.pnl > 0:
                self.take_profit = self.initialqty * self.exitpoints[self.exitcounter], self.position.current_price
                self.exitcounter += 1
    # -----------------

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

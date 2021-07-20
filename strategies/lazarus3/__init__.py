from jesse.strategies import Strategy, cached
from jesse import utils
import jesse.indicators as ta


class lazarus32(Strategy):
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

        self.dnas = {
            1: {"dna": 'vaJpC;g', "tpnl": 296, "tstop": 87, "donlen": 183, "pmpsize": 47, "fast": 6, "slow": 44},
            2: {"dna": 'vaJpp;g', "tpnl": 296, "tstop": 87, "donlen": 183, "pmpsize": 93, "fast": 6, "slow": 44},
            3: {"dna": 'vXJp.._', "tpnl": 253, "tstop": 87, "donlen": 183, "pmpsize": 26, "fast": 3, "slow": 41},
            4: {"dna": 'vXJp5._', "tpnl": 253, "tstop": 87, "donlen": 183, "pmpsize": 33, "fast": 3, "slow": 41},
            5: {"dna": 'sYon51`', "tpnl": 258, "tstop": 172, "donlen": 178, "pmpsize": 33, "fast": 4, "slow": 42},
            6: {"dna": 'vdfp5.)', "tpnl": 310, "tstop": 151, "donlen": 183, "pmpsize": 33, "fast": 3, "slow": 21},
            7: {"dna": 'v^JpF/g', "tpnl": 281, "tstop": 87, "donlen": 183, "pmpsize": 50, "fast": 4, "slow": 44},
            8: {"dna": 'vY\\n51`', "tpnl": 258, "tstop": 128, "donlen": 178, "pmpsize": 33, "fast": 4, "slow": 42},
            9: {"dna": 'Z^JpF/Y', "tpnl": 281, "tstop": 87, "donlen": 183, "pmpsize": 50, "fast": 4, "slow": 39},
            10: {"dna": 'kd9?;1H', "tpnl": 310, "tstop": 49, "donlen": 64, "pmpsize": 39, "fast": 4, "slow": 33},
            11: {"dna": 'vdfp5@l', "tpnl": 310, "tstop": 151, "donlen": 183, "pmpsize": 33, "fast": 7, "slow": 46},
            12: {"dna": 'vdds59l', "tpnl": 310, "tstop": 147, "donlen": 190, "pmpsize": 33, "fast": 6, "slow": 46},
            13: {"dna": 'vVJ/2._', "tpnl": 243, "tstop": 87, "donlen": 25, "pmpsize": 30, "fast": 3, "slow": 41},
            14: {"dna": 'vN3BO,f', "tpnl": 205, "tstop": 35, "donlen": 71, "pmpsize": 59, "fast": 3, "slow": 44},
            15: {"dna": 'vdos5>l', "tpnl": 310, "tstop": 172, "donlen": 190, "pmpsize": 33, "fast": 7, "slow": 46},
            16: {"dna": 'vj3?o1l', "tpnl": 338, "tstop": 35, "donlen": 64, "pmpsize": 92, "fast": 4, "slow": 46},
            17: {"dna": 'vqopR,]', "tpnl": 372, "tstop": 172, "donlen": 183, "pmpsize": 63, "fast": 3, "slow": 40},
            18: {"dna": 'vaQpJ;g', "tpnl": 296, "tstop": 103, "donlen": 183, "pmpsize": 54, "fast": 6, "slow": 44},
            19: {"dna": 'v^JpF/U', "tpnl": 281, "tstop": 87, "donlen": 183, "pmpsize": 50, "fast": 4, "slow": 38},
            20: {"dna": 'vahpJ;g', "tpnl": 296, "tstop": 156, "donlen": 183, "pmpsize": 54, "fast": 6, "slow": 44}
        }

    def hyperparameters(self):
        return [
            {'name': 'dnaindex', 'type': int, 'min': 1, 'max': 20, 'default': 1}
        ]

    @property
    def targetpnl(self):
        return self.dnas[self.hp['dnaindex']]['tpnl']

    @property
    def targetstop(self):
        return self.dnas[self.hp['dnaindex']]['tstop']

    @property
    def donchianlen(self):
        return self.dnas[self.hp['dnaindex']]['donlen']

    @property
    def pumpsize(self):
        return self.dnas[self.hp['dnaindex']]['pmpsize']

    @property
    def ewofast(self):
        return self.dnas[self.hp['dnaindex']]['fast']

    @property
    def ewoslow(self):
        return self.dnas[self.hp['dnaindex']]['slow']

    @property
    def limit(self):
        return 4

    @property
    def carpan(self):
        return 33

    @property
    def pumplookback(self):
        return 3

    @property
    def positionsize(self):
        return 8

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

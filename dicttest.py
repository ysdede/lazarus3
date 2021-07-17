dnas = {
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

print(dnas[1])
x = 1
print(dnas[1]['fast'])

# 8, 296, 87, 183, 47, 6, 44, 3     #   vaJpp;g   + 2.58    92.98   6.07    %96.65  %-29.14 --> vaJpC;g *****
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
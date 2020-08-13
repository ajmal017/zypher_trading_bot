from ib_insync import IB, util
from ib_insync.contract import *
from ibtest import runstrategy


def run(strategy, **kwargs):
    print("ZYPHER_TRADING_BOT")
    runstrategy(contracts, strategy, **kwargs)

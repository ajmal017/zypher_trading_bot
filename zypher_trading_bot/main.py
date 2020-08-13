from ib_insync import IB
from ib_helper import runstrategy
from teststrategy import TestStrategy


def run(strategy, **kwargs):
    runstrategy(strategy, **kwargs)


if __name__ == "__main__":
    run(
        TestStrategy,
        data0="EUR.USD-CASH-IDEALPRO",
        port=7497,
        timeframe="Minutes",
        compression=5,
    )

from ib_insync import IB, util
from ib_insync.contract import *


def run(contracts, ip="127.0.0.1", port=7496):
    ib = IB()
    ib.connect(ip, port, clientId=1)


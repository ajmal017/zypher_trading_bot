from __future__ import absolute_import, division, print_function, unicode_literals

import argparse
import datetime

# The above could be sent to an independent module
import backtrader as bt
from backtrader.utils import flushfile  # win32 quick stdout flushing


def runstrategy(strategy, **kwargs):
    # Create a cerebro
    cerebro = bt.Cerebro()

    storekwargs = dict(
        host=kwargs.get("host", "127.0.0.1"),
        port=kwargs.get("port", 7496),
        clientId=kwargs.get("clientId", None),
        timeoffset=not kwargs.get("no_timeoffset", None),
        reconnect=kwargs.get("reconnect", 3),
        timeout=kwargs.get("timeout", 3.0),
        notifyall=kwargs.get("notifyall", None),
        _debug=kwargs.get("debug", None),
    )

    ibstore = bt.stores.IBStore(**storekwargs)
    broker = ibstore.getbroker()

    cerebro.setbroker(broker)

    timeframe = bt.TimeFrame.TFrame(kwargs.get("timeframe", "Minutes"))
    # Manage data1 parameters
    tf1 = kwargs.get("timeframe1", None)
    tf1 = bt.TimeFrame.TFrame(tf1) if tf1 is not None else timeframe
    cp1 = kwargs.get("compression1", None)
    cp1 = cp1 if cp1 is not None else kwargs.get("compression", 1)

    if kwargs.get("resample", None) or kwargs.get("replay", None):
        datatf = datatf1 = bt.TimeFrame.Ticks
        datacomp = datacomp1 = 1
    else:
        datatf = timeframe
        datacomp = kwargs.get("compression", 1)
        datatf1 = tf1
        datacomp1 = cp1

    fromdate = None
    if kwargs.get("fromdate", None):
        dtformat = "%Y-%m-%d" + ("T%H:%M:%S" * ("T" in kwargs.get("fromdate", None)))
        fromdate = datetime.datetime.strptime(kwargs.get("fromdate", None), dtformat)
        print(fromdate)

    datakwargs = dict(
        timeframe=datatf,
        compression=datacomp,
        historical=kwargs.get("historical", None),
        fromdate=fromdate,
        rtbar=kwargs.get("rtbar", False),
        qcheck=kwargs.get("qcheck", 0.5),
        what=kwargs.get("what", None),
        backfill_start=not kwargs.get("no_backfill_start", None),
        backfill=not kwargs.get("no_backfill", None),
        latethrough=kwargs.get("latethrough", None),
        tz=kwargs.get("timezone", None),
    )

    data0 = ibstore.getdata(dataname=kwargs.get("data0", None), **datakwargs)

    data1 = None
    if kwargs.get("data1", None) is not None:
        if kwargs.get("data1", None) != kwargs.get("data0", None):
            datakwargs["timeframe"] = datatf1
            datakwargs["compression"] = datacomp1
            data1 = ibstore.getdata(dataname=kwargs.get("data1", None), **datakwargs)
        else:
            data1 = data0

    rekwargs = dict(
        timeframe=timeframe,
        compression=kwargs.get("compression", 1),
        bar2edge=not kwargs.get("no_bar2edge", None),
        adjbartime=not kwargs.get("no_adjbartime", None),
        rightedge=not kwargs.get("no_rightedge", None),
        takelate=not kwargs.get("no_takelate", None),
    )

    if kwargs.get("replay", None):
        cerebro.replaydata(data0, **rekwargs)

        if data1 is not None:
            rekwargs["timeframe"] = tf1
            rekwargs["compression"] = cp1
            cerebro.replaydata(data1, **rekwargs)

    elif kwargs.get("resample", None):
        cerebro.resampledata(data0, **rekwargs)

        if data1 is not None:
            rekwargs["timeframe"] = tf1
            rekwargs["compression"] = cp1
            cerebro.resampledata(data1, **rekwargs)

    else:
        cerebro.adddata(data0)
        if data1 is not None:
            cerebro.adddata(data1)

    if kwargs.get("valid", None) is None:
        valid = None
    else:
        valid = datetime.timedelta(seconds=kwargs.get("valid", None))
    # Add the strategy
    cerebro.addstrategy(
        strategy,
        smaperiod=kwargs.get("smaperiod", 5),
        trade=kwargs.get("trade", None),
        exectype=bt.Order.ExecType(kwargs.get("exectype", bt.Order.ExecTypes[0])),
        stake=kwargs.get("stake", 10),
        stopafter=kwargs.get("stopafter", 0),
        valid=valid,
        cancel=kwargs.get("cancel", 0),
        donotsell=kwargs.get("donotsell", None),
        stoptrail=kwargs.get("stoptrail", None),
        stoptraillimit=kwargs.get("traillimit", None),
        trailamount=kwargs.get("trailamount", None),
        trailpercent=kwargs.get("trailpercent", None),
        limitoffset=kwargs.get("limitoffset", None),
        oca=kwargs.get("oca", None),
        bracket=kwargs.get("bracket", None),
    )

    # Live data ... avoid long data accumulation by switching to "exactbars"
    cerebro.run(exactbars=kwargs.get("exactbars", 1))

    if kwargs.get("plot", None) and kwargs.get("exactbars", 1) < 1:  # plot if possible
        cerebro.plot()


# def parse_args():
#     parser = argparse.ArgumentParser(
#         formatter_class=argparse.ArgumentDefaultsHelpFormatter,
#         description="Test Interactive Brokers integration",
#     )

#     parser.add_argument(
#         "--exactbars",
#         default=1,
#         type=int,
#         required=False,
#         action="store",
#         help="exactbars level, use 0/-1/-2 to enable plotting",
#     )

#     parser.add_argument(
#         "--plot", required=False, action="store_true", help="Plot if possible"
#     )

#     parser.add_argument(
#         "--stopafter",
#         default=0,
#         type=int,
#         required=False,
#         action="store",
#         help="Stop after x lines of LIVE data",
#     )

#     parser.add_argument(
#         "--usestore", required=False, action="store_true", help="Use the store pattern"
#     )

#     parser.add_argument(
#         "--notifyall",
#         required=False,
#         action="store_true",
#         help="Notify all messages to strategy as store notifs",
#     )

#     parser.add_argument(
#         "--debug",
#         required=False,
#         action="store_true",
#         help="Display all info received form IB",
#     )

#     parser.add_argument(
#         "--host",
#         default="127.0.0.1",
#         required=False,
#         action="store",
#         help="Host for the Interactive Brokers TWS Connection",
#     )

#     parser.add_argument(
#         "--qcheck",
#         default=0.5,
#         type=float,
#         required=False,
#         action="store",
#         help=("Timeout for periodic " "notification/resampling/replaying check"),
#     )

#     parser.add_argument(
#         "--port",
#         default=7496,
#         type=int,
#         required=False,
#         action="store",
#         help="Port for the Interactive Brokers TWS Connection",
#     )

#     parser.add_argument(
#         "--clientId",
#         default=None,
#         type=int,
#         required=False,
#         action="store",
#         help="Client Id to connect to TWS (default: random)",
#     )

#     parser.add_argument(
#         "--no-timeoffset",
#         required=False,
#         action="store_true",
#         help=(
#             "Do not Use TWS/System time offset for non "
#             "timestamped prices and to align resampling"
#         ),
#     )

#     parser.add_argument(
#         "--reconnect",
#         default=3,
#         type=int,
#         required=False,
#         action="store",
#         help="Number of recconnection attempts to TWS",
#     )

#     parser.add_argument(
#         "--timeout",
#         default=3.0,
#         type=float,
#         required=False,
#         action="store",
#         help="Timeout between reconnection attempts to TWS",
#     )

#     parser.add_argument(
#         "--data0",
#         default=None,
#         required=True,
#         action="store",
#         help="data 0 into the system",
#     )

#     parser.add_argument(
#         "--data1",
#         default=None,
#         required=False,
#         action="store",
#         help="data 1 into the system",
#     )

#     parser.add_argument(
#         "--timezone",
#         default=None,
#         required=False,
#         action="store",
#         help="timezone to get time output into (pytz names)",
#     )

#     parser.add_argument(
#         "--what",
#         default=None,
#         required=False,
#         action="store",
#         help="specific price type for historical requests",
#     )

#     parser.add_argument(
#         "--no-backfill_start",
#         required=False,
#         action="store_true",
#         help="Disable backfilling at the start",
#     )

#     parser.add_argument(
#         "--latethrough",
#         required=False,
#         action="store_true",
#         help=(
#             "if resampling replaying, adjusting time "
#             "and disabling time offset, let late samples "
#             "through"
#         ),
#     )

#     parser.add_argument(
#         "--no-backfill",
#         required=False,
#         action="store_true",
#         help="Disable backfilling after a disconnection",
#     )

#     parser.add_argument(
#         "--rtbar",
#         default=False,
#         required=False,
#         action="store_true",
#         help="Use 5 seconds real time bar updates if possible",
#     )

#     parser.add_argument(
#         "--historical",
#         required=False,
#         action="store_true",
#         help="do only historical download",
#     )

#     parser.add_argument(
#         "--fromdate",
#         required=False,
#         action="store",
#         help=(
#             "Starting date for historical download "
#             "with format: YYYY-MM-DD[THH:MM:SS]"
#         ),
#     )

#     parser.add_argument(
#         "--smaperiod",
#         default=5,
#         type=int,
#         required=False,
#         action="store",
#         help="Period to apply to the Simple Moving Average",
#     )

#     pgroup = parser.add_mutually_exclusive_group(required=False)

#     pgroup.add_argument(
#         "--replay",
#         required=False,
#         action="store_true",
#         help="replay to chosen timeframe",
#     )

#     pgroup.add_argument(
#         "--resample",
#         required=False,
#         action="store_true",
#         help="resample to chosen timeframe",
#     )

#     parser.add_argument(
#         "--timeframe",
#         default=bt.TimeFrame.Names[0],
#         choices=bt.TimeFrame.Names,
#         required=False,
#         action="store",
#         help="TimeFrame for Resample/Replay",
#     )

#     parser.add_argument(
#         "--compression",
#         default=1,
#         type=int,
#         required=False,
#         action="store",
#         help="Compression for Resample/Replay",
#     )

#     parser.add_argument(
#         "--timeframe1",
#         default=None,
#         choices=bt.TimeFrame.Names,
#         required=False,
#         action="store",
#         help="TimeFrame for Resample/Replay - Data1",
#     )

#     parser.add_argument(
#         "--compression1",
#         default=None,
#         type=int,
#         required=False,
#         action="store",
#         help="Compression for Resample/Replay - Data1",
#     )

#     parser.add_argument(
#         "--no-takelate",
#         required=False,
#         action="store_true",
#         help=(
#             "resample/replay, do not accept late samples "
#             "in new bar if the data source let them through "
#             "(latethrough)"
#         ),
#     )

#     parser.add_argument(
#         "--no-bar2edge",
#         required=False,
#         action="store_true",
#         help="no bar2edge for resample/replay",
#     )

#     parser.add_argument(
#         "--no-adjbartime",
#         required=False,
#         action="store_true",
#         help="no adjbartime for resample/replay",
#     )

#     parser.add_argument(
#         "--no-rightedge",
#         required=False,
#         action="store_true",
#         help="no rightedge for resample/replay",
#     )

#     parser.add_argument(
#         "--broker", required=False, action="store_true", help="Use IB as broker"
#     )

#     parser.add_argument(
#         "--trade",
#         required=False,
#         action="store_true",
#         help="Do Sample Buy/Sell operations",
#     )

#     parser.add_argument(
#         "--donotsell",
#         required=False,
#         action="store_true",
#         help="Do not sell after a buy",
#     )

#     parser.add_argument(
#         "--exectype",
#         default=bt.Order.ExecTypes[0],
#         choices=bt.Order.ExecTypes,
#         required=False,
#         action="store",
#         help="Execution to Use when opening position",
#     )

#     parser.add_argument(
#         "--stake",
#         default=10,
#         type=int,
#         required=False,
#         action="store",
#         help="Stake to use in buy operations",
#     )

#     parser.add_argument(
#         "--valid",
#         default=None,
#         type=int,
#         required=False,
#         action="store",
#         help="Seconds to keep the order alive (0 means DAY)",
#     )

#     pgroup = parser.add_mutually_exclusive_group(required=False)
#     pgroup.add_argument(
#         "--stoptrail",
#         required=False,
#         action="store_true",
#         help="Issue a stoptraillimit after buy( do not sell",
#     )

#     pgroup.add_argument(
#         "--traillimit",
#         required=False,
#         action="store_true",
#         help="Issue a stoptrail after buying (do not sell",
#     )

#     pgroup.add_argument(
#         "--oca",
#         required=False,
#         action="store_true",
#         help="Test oca by putting 2 orders in a group",
#     )

#     pgroup.add_argument(
#         "--bracket",
#         required=False,
#         action="store_true",
#         help="Test bracket orders by issuing high/low sides",
#     )

#     pgroup = parser.add_mutually_exclusive_group(required=False)
#     pgroup.add_argument(
#         "--trailamount",
#         default=None,
#         type=float,
#         required=False,
#         action="store",
#         help="trailamount for StopTrail order",
#     )

#     pgroup.add_argument(
#         "--trailpercent",
#         default=None,
#         type=float,
#         required=False,
#         action="store",
#         help="trailpercent for StopTrail order",
#     )

#     parser.add_argument(
#         "--limitoffset",
#         default=None,
#         type=float,
#         required=False,
#         action="store",
#         help="limitoffset for StopTrailLimit orders",
#     )

#     parser.add_argument(
#         "--cancel",
#         default=0,
#         type=int,
#         required=False,
#         action="store",
#         help=(
#             "Cancel a buy order after n bars in operation,"
#             " to be combined with orders like Limit"
#         ),
#     )

#     return parser.parse_args()

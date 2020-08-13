import backtrader as bt


class TestStrategy(bt.Strategy):
    params = dict(
        smaperiod=5,
        trade=False,
        stake=10,
        exectype=bt.Order.Market,
        stopafter=0,
        valid=None,
        cancel=0,
        donotsell=False,
        stoptrail=False,
        stoptraillimit=False,
        trailamount=None,
        trailpercent=None,
        limitoffset=None,
        oca=False,
        bracket=False,
    )

    def __init__(self):
        # To control operation entries
        self.orderid = list()
        self.order = None

        self.counttostop = 0
        self.datastatus = 0

        # Create SMA on 2nd data
        self.sma = bt.indicators.MovAv.SMA(self.data, period=self.p.smaperiod)

        print("--------------------------------------------------")
        print("Strategy Created")
        print("--------------------------------------------------")

    def notify_data(self, data, status, *args, **kwargs):
        print("*" * 5, "DATA NOTIF:", data._getstatusname(status), *args)
        if status == data.LIVE:
            self.counttostop = self.p.stopafter
            self.datastatus = 1

    def notify_store(self, msg, *args, **kwargs):
        print("*" * 5, "STORE NOTIF:", msg)

    def notify_order(self, order):
        if order.status in [order.Completed, order.Cancelled, order.Rejected]:
            self.order = None

        print("-" * 50, "ORDER BEGIN", datetime.datetime.now())
        print(order)
        print("-" * 50, "ORDER END")

    def notify_trade(self, trade):
        print("-" * 50, "TRADE BEGIN", datetime.datetime.now())
        print(trade)
        print("-" * 50, "TRADE END")

    def prenext(self):
        self.next(frompre=True)

    def next(self, frompre=False):
        txt = list()
        txt.append("Data0")
        txt.append("%04d" % len(self.data0))
        dtfmt = "%Y-%m-%dT%H:%M:%S.%f"
        txt.append("{}".format(self.data.datetime[0]))
        txt.append("%s" % self.data.datetime.datetime(0).strftime(dtfmt))
        txt.append("{}".format(self.data.open[0]))
        txt.append("{}".format(self.data.high[0]))
        txt.append("{}".format(self.data.low[0]))
        txt.append("{}".format(self.data.close[0]))
        txt.append("{}".format(self.data.volume[0]))
        txt.append("{}".format(self.data.openinterest[0]))
        txt.append("{}".format(self.sma[0]))
        print(", ".join(txt))

        if len(self.datas) > 1 and len(self.data1):
            txt = list()
            txt.append("Data1")
            txt.append("%04d" % len(self.data1))
            dtfmt = "%Y-%m-%dT%H:%M:%S.%f"
            txt.append("{}".format(self.data1.datetime[0]))
            txt.append("%s" % self.data1.datetime.datetime(0).strftime(dtfmt))
            txt.append("{}".format(self.data1.open[0]))
            txt.append("{}".format(self.data1.high[0]))
            txt.append("{}".format(self.data1.low[0]))
            txt.append("{}".format(self.data1.close[0]))
            txt.append("{}".format(self.data1.volume[0]))
            txt.append("{}".format(self.data1.openinterest[0]))
            txt.append("{}".format(float("NaN")))
            print(", ".join(txt))

        if self.counttostop:  # stop after x live lines
            self.counttostop -= 1
            if not self.counttostop:
                self.env.runstop()
                return

        if not self.p.trade:
            return

        if self.datastatus and not self.position and len(self.orderid) < 1:
            exectype = self.p.exectype if not self.p.oca else bt.Order.Limit
            close = self.data0.close[0]
            price = round(close * 0.90, 2)
            self.order = self.buy(
                size=self.p.stake,
                exectype=exectype,
                price=price,
                valid=self.p.valid,
                transmit=not self.p.bracket,
            )

            self.orderid.append(self.order)

            if self.p.bracket:
                # low side
                self.sell(
                    size=self.p.stake,
                    exectype=bt.Order.Stop,
                    price=round(price * 0.90, 2),
                    valid=self.p.valid,
                    transmit=False,
                    parent=self.order,
                )

                # high side
                self.sell(
                    size=self.p.stake,
                    exectype=bt.Order.Limit,
                    price=round(close * 1.10, 2),
                    valid=self.p.valid,
                    transmit=True,
                    parent=self.order,
                )

            elif self.p.oca:
                self.buy(
                    size=self.p.stake,
                    exectype=bt.Order.Limit,
                    price=round(self.data0.close[0] * 0.80, 2),
                    oco=self.order,
                )

            elif self.p.stoptrail:
                self.sell(
                    size=self.p.stake,
                    exectype=bt.Order.StopTrail,
                    # price=round(self.data0.close[0] * 0.90, 2),
                    valid=self.p.valid,
                    trailamount=self.p.trailamount,
                    trailpercent=self.p.trailpercent,
                )

            elif self.p.stoptraillimit:
                p = round(self.data0.close[0] - self.p.trailamount, 2)
                # p = self.data0.close[0]
                self.sell(
                    size=self.p.stake,
                    exectype=bt.Order.StopTrailLimit,
                    price=p,
                    plimit=p + self.p.limitoffset,
                    valid=self.p.valid,
                    trailamount=self.p.trailamount,
                    trailpercent=self.p.trailpercent,
                )

        elif self.position.size > 0 and not self.p.donotsell:
            if self.order is None:
                self.order = self.sell(
                    size=self.p.stake // 2,
                    exectype=bt.Order.Market,
                    price=self.data0.close[0],
                )

        elif self.order is not None and self.p.cancel:
            if self.datastatus > self.p.cancel:
                self.cancel(self.order)

        if self.datastatus:
            self.datastatus += 1

    def start(self):
        if self.data0.contractdetails is not None:
            print(
                "Timezone from ContractDetails: {}".format(
                    self.data0.contractdetails.m_timeZoneId
                )
            )

        header = [
            "Datetime",
            "Open",
            "High",
            "Low",
            "Close",
            "Volume",
            "OpenInterest",
            "SMA",
        ]
        print(", ".join(header))

        self.done = False

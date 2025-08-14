from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import SMA, STDEV
from surmount.data import Asset
import pandas as pd

class TradingStrategy(Strategy):
    def __init__(self):
        self.ticker = "AAPL"

    @property
    def interval(self):
        # Analysis interval
        return "1day"

    @property
    def assets(self):
        # Assets to include in the strategy
        return [self.ticker]

    @property
    def data(self):
        # Additional data requirements are listed here
        # Observing the base example, only
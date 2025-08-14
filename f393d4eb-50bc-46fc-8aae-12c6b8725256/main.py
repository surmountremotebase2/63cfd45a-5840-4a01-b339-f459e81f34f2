from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import SMA, STDEV
from surmount.data import Asset
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        self.tickers = ["AAPL"]

    @property
    def interval(self):
        return "1day"  # Adjust based on preference

    @property
    def assets(self):
        return self.tickers

    @property
    def data(self):
        # Only OHLCV data is automatically fetched; no need to add to data_list
        return []
    
    def run(self, data):
        closing_prices = [d["AAPL"]["close"] for d in data["ohlcv"]]
        opening_prices = [d["AAPL"]["open"] for d in data["ohlcv"]]
        volumes = [d["AAPL"]["volume"] for d in data["ohlcv"]]

        # Moving averages for support/resistance
        short_term_ma = SMA("AAPL", opening_prices, 14)  # 14 days for short-term trend
        long_term_ma = SMA("AAPL", closing_prices, 50)  # 50 days for long-term trend
        price_std_dev = STDEV("AAPL", closing_prices, 20)  # 20 days standard deviation

        allocation = 0  # Default to no allocation

        # Basic Strategy Logic
        if len(short_term_ma) > 0 and len(long_term_ma) > 0:
            current_short_term_ma = short_term_ma[-1]
            current_long_term_ma = long_term_ma[-1]
            current_price = closing_prices[-1]
            current_volume = volumes[-1]
            volume_price_spread = current_volume * current_price  # Not a typical indicator
            
            # Buy signal: if current price above short MA and short MA above long MA
            # and high volume-price spread indicating strong buying interest
            if current_price > current_short_term_ma and current_short_term_ma > current_long_term_ma:
                if volume_price_spread > (sum(volumes) / len(volumes)) * current_price:  # Average volume * price
                    allocation = min(1, (price_std_dev[-1]/current_price) + 0.5)  # Adjust based on volatility
            
            # Sell signal: if current price below short MA and short MA below long MA
            elif current_price < current_short_term_ma and current_short_term_ma < current_long_term_ma:
                allocation = 0  # Sell everything
            
            # Adjust allocation based on standard deviation as a risk management measure
            # Higher volatility = lower allocation
            allocation = max(0, min(allocation - (price_std_dev[-1]/current_price), 1))

        return TargetAllocation({"AAPL": allocation})
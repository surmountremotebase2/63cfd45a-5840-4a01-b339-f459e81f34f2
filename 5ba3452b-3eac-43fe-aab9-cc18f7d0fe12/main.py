from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import SMA, STDEV
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        self.ticker = "AAPL"
    
    @property
    def interval(self):
        return "1day"

    @property
    def assets(self):
        return [self.ticker]

    @property
    def data(self):
        return []

    def run(self, data):
        # Load daily opening and closing prices
        open_prices = [d[self.ticker]["open"] for d in data["ohlcv"]]
        close_prices = [d[self.ticker]["close"] for d in data["ohlcv"]]
        
        # Calculate moving averages for open and close prices
        sma_open = SMA(self.ticker, data["ohlcv"], length=20, price_key="open")
        sma_close = SMA(self.ticker, data["ohlcv"], length=20, price_key="close")
        
        # Calculate standard deviation for closing prices to understand volatility
        std_dev_close = STDEV(self.ticker, data["ohlcv"], length=20, price_key="close")
        
        # Assume last price is the latest closing price
        last_price = close_prices[-1] if close_prices else 0
        
        # Calculating the spread difference between price and volume (simplified)
        # Note: This is a basic example. Real trading strategies might involve more complex calculations.
        volume = [d[self.ticker]["volume"] for d in data["ohlcv"]]
        price_volume_spread = last_price * sum(volume[-5:]) # Last 5 days as an example
        
        # Decide to buy if the last closing price is above the moving average of closing prices
        # and the standard deviation is not too high (indicating less volatility)
        # Also, considering the price-volume spread as an additional condition
        allocation = 0 # Default to holding no position
        if last_price > sma_close[-1] and std_dev_close[-1] < 5 and price_volume_spread > 1000000:
            allocation = 1  # Buy
        elif last_price < sma_close[-1] or std_dev_close[-1] > 5:
            allocation = 0  # Sell or stay out
        
        return TargetAllocation({self.ticker: allocation})
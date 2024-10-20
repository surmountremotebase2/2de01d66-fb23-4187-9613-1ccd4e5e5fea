
from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import SMA
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        # Define the ticker we're interested in
        self.ticker = "LUNR"
        # Length of the moving average window
        self.sma_length = 2

    @property
    def assets(self):
        # The assets method returns a list of tickers we're interested in
        return [self.ticker]

    @property
    def interval(self):
        # Define the interval for data points (1 day in this case)
        return "1hour"

    def run(self, data):
        # Calculate the simple moving average (SMA) for the specified length
        # for our ticker LUNR
        sma = SMA(self.ticker, data["ohlcv"], self.sma_length)
        
        if not sma or len(sma) < self.sma_length:
            # If SMA can't be calculated or we don't have enough data,
            # don't allocate any capital
            return TargetAllocation({})
        
        # Get the latest available closing price for LUNR
        current_price = data["ohlcv"][-1][self.ticker]["close"]
        
        # Determine allocation based on mean reversion principle
        allocation_dict = {}
        if current_price < sma[-1]:  # Price is below the average, consider it undervalued
            # Buy LUNR, allocating a certain percentage of the portfolio to it
            allocation_dict[self.ticker] = 1.0  # Example: 100% of the portfolio allocated
        elif current_price > sma[-1]:  # Price is above the average, consider it overvalued
            # Sell or avoid buying LUNR
            allocation_dict[self.ticker] = 0.0  # No allocation
            
        # Log the allocation decision for analysis
        log(f"Allocating {allocation_dict[self.ticker]*100}% to {self.ticker}")
        
        return TargetAllocation(allocation_dict)

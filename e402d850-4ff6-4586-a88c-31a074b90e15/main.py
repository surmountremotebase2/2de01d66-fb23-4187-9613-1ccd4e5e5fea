from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import SMA
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        self.ticker = "ASTS"  # Define the ticker we are interested in.
        # No additional data needed from surmount.data as we are only using price data.
        
    @property
    def assets(self):
        return [self.ticker]  # List containing the ticker of interest, used by Surmount to fetch relevant market data.

    @property
    def interval(self):
        return "1min"  # Use 1min interval for high-frequency trading strategy.
        
    def run(self, data):
        # Calculate SMA for 1 minute and 5 minutes intervals
        sma_1min = SMA(self.ticker, data["ohlcv"], 1)  # SMA for the past 1 minute.
        sma_5min = SMA(self.ticker, data["ohlcv"], 5)  # SMA for the past 5 minutes.
        
        # Initialize the allocation with 0, represents no position
        allocation = 0

        # Ensure we have enough data for both SMAs to make a decision.
        if len(sma_1min) > 0 and len(sma_5min) > 0:
            # Fetch the last calculated SMA value for 1min and 5min intervals
            last_sma_1min = sma_1min[-1]
            last_sma_5min = sma_5min[-1]

            # If the 1min SMA is less than the 5min SMA by more than $0.50, set allocation to buy (1).
            if current_price < (last_sma_5min - 0.25):
                log("Buying signal: 1min SMA is significantly lower than 5min SMA.")
                allocation = 1  # Buy signal

            # If the 1min SMA is greater than the 5min SMA by more than $1, set allocation to sell (0).
            elif current_price > (last_sma_5min + 0.5):
                log("Selling signal: 1min SMA is significantly higher than 5min SMA.")
                allocation = 0  # Sell signal / take no position
        
        # Return the target allocation; in this case, it could be 0 (no position) or 1 (full position).
        return TargetAllocation({self.ticker: allocation})
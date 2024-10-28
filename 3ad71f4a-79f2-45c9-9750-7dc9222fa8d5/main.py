
from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import SMA
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        # Initialize with the relevant ticker
        self.tickers = ["ASTS"]

    @property
    def interval(self):
        # Use 1min interval as the strategy revolves around quick changes
        return "5min"

    @property
    def assets(self):
        # Operate on ASTS
        return self.tickers

    def run(self, data):
        # Data for ASTS from the 1min OHLCV data
        asts_data = data["ohlcv"]
        # Check if we have enough data for SMA calculation, though this example implicitly assumes presence
        if len(asts_data) < 2:  # Simple check, might need to adjust based on SMA calculation requirements
            return TargetAllocation({"ASTS": 0})
        
        # Calculate the 1 minute SMA for ASTS
        asts_sma = SMA("ASTS", asts_data, 5)[-1]  # Using the last SMA value
        asts_sma_1 = SMA("ASTS", asts_data, 1)[-1]  # Using the last SMA value
        current_price = asts_data[-1]["ASTS"]["close"]  # Get the most recent closing price

        allocation = 0

        # Define threshold values
        sell_above = 0.50  # Sell when price is more than 50 cents above the SMA
        buy_below = 0.25  # Buy when price is more than 25 cents below the SMA

        # Decision logic
        if current_price < (asts_sma - buy_below):
            # The larger the gap, the higher the allocation, up to a maximum of 1
            difference = asts_sma - current_price
            allocation = min(1, difference)  # Example formula, adjust based on desired sensitivity
        elif current_price > (asts_sma_1 + sell_above):
            # Selling strategy, could be a negative allocation to indicate short-selling or just 0 to avoid action
            allocation = 0
            
        # Logging for debugging and insight
        log(f"ASTS Current Price: {current_price}, SMA: {asts_sma}, Allocation: {allocation}")

        return TargetAllocation({"ASTS": allocation})

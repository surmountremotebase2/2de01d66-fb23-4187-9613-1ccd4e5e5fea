from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import SMA
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        self.tickers = ["RKLB"]

    @property
    def interval(self):
        # Defines the data interval to be used for the strategy
        return "5min"

    @property
    def assets(self):
        # List of assets the strategy will consider trading
        return self.tickers

    # The run method is called when data is available to be processed.
    def run(self, data):
        ticker = self.tickers[0]  # Assuming only one ticker is used in this strategy
        ohlcv_data = data["ohlcv"]
        
        if len(ohlcv_data) > 20:  # Ensures there's enough data to calculate SMA
            sma20 = SMA(ticker, ohlcv_data, length=2)  # Calculates 20 periods SMA
            
            current_price = ohlcv_data[-1][ticker]["close"]
            last_sma_value = sma20[-1]
            
            if current_price - last_sma_value <= -0.01:
                # Current price is below the 20-day SMA, indicating a potential buy signal
                log(f"Buying signal for {ticker}: current price {current_price} is lower than 20-day SMA of {last_sma_value}.")
                allocation = 1  # Sets allocation to 100%
            elif current_price - last_sma_value >= 0.02:
                # Current price is above the 20-day SMA, indicating a potential sell signal
                log(f"Selling signal for {ticker}: current price {current_price} is higher than 20-day SMA of {last_sma_value}.")
                allocation = 0  # Sets allocation to 0%
            else:
                allocation = 0  # Default allocation in case the price equals the SMA
        else:
            log("Not enough data to calculate SMA.")
            allocation = 0  # Default allocation if not enough data

        return TargetAllocation({ticker: allocation})
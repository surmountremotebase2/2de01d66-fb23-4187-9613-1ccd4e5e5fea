from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import SMA
from surmount.logging import log
from surmount.data import OHLCV  # Importing OHLCV even if we don't add it to data_list directly

class TradingStrategy(Strategy):
    def __init__(self):
        self.ticker = "CLOV"
        
    @property
    def assets(self):
        return [self.ticker]

    @property
    def interval(self):
        # Ensuring the strategy checks the price every minute
        return "1min"

    @property
    def data(self):
        # Not adding OHLCV data to data_list as instructed.
        return []

    def run(self, data):
        # Access the latest minute's close price data for CLOV
        clov_data = data["ohlcv"]
        current_price = clov_data[-1][self.ticker]["close"]
        
        # Calculate the 5-minute SMA for CLOV. Length is set to 5 for the 5-minute SMA.
        clov_sma_5min = SMA(self.ticker, clov_data, 5)
        
        if len(clov_sma_5min) == 0:
            # If we do not have enough data to calculate SMA, we do not return any allocation
            return TargetAllocation({})
        
        # The last value from clov_sma_5min gives us the latest SMA value
        sma_5min_current = clov_sma_5min[-1]
        
        allocation = 0
        
        if current_price < sma_5min_current:
            # Current price is below the 5-minute SMA, setting allocation to buy (1)
            log(f'Current price of {self.ticker} below 5min SMA, buying')
            allocation = 1
        elif current_price > sma_5min_current + 0.03:
            # Current price is above the 5-minute SMA by more than 3 cents, setting allocation to sell (0)
            log(f'Current price of {self.ticker} above 5min SMA by more than 0.03, selling')
            allocation = 0
        else:
            log(f'{self.ticker} price is within threshold of 5min SMA, holding position')
            
        # Returning the target allocation based on the logic above
        return TargetAllocation({self.ticker: allocation})
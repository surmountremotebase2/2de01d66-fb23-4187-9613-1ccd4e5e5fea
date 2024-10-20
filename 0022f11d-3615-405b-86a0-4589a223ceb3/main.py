from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import MACD
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        self.tickers = ["RXRX"]  # Define the ticker we are interested in
        self.ticker = tickers[0]  # Define the ticker we are interested in

    @property
    def interval(self):
        return "5min"  # Set the interval for MACD calculation

    @property
    def assets(self):
        return self.tickers  # Specify the assets involved in the strategy

    def run(self, data):
        allocation = 0  # Default to no allocation
        rxrx_data = data["ohlcv"]  # Extract ohlcv data for calculations

        # Calculate MACD for RXRX
        macd = MACD(ticker, rxrx_data, fast=3, slow=26)
        
        macd_line = macd["MACD_3_26_9"]
        signal_line = macd["MACDs_3_26_9"]
            

        # Extract MACD and Signal line lists. macd["MACD"] would give us the MACD line, whereas macd["signal"] would give us the Signal line.
        
        if len(macd_line) > 1 and len(signal_line) > 1:
            last_close_price = rxrx_data[-1]["RXRX"]["close"]  # Get the latest closing price
            prev_close_price = rxrx_data[-2]["RXRX"]["close"]  # Get the previous closing price

            log(f"-2 macd_line value - signal_line value = {macd_line[-2] - signal_line[-2]}")
            log(f"-1 macd_line value - signal_line value = {macd_line[-1] - signal_line[-1]}")

            # Buy condition: if the MACD line crosses below the signal line
            if macd_line[-2] > signal_line[-2] and macd_line[-1] < signal_line[-1]:
                log("Buying signal triggered")
                allocation = 1  # Full allocation
            
            # Sell condition: if the MACD line crosses above the signal line
            elif macd_line[-2] < signal_line[-2] and macd_line[-1] > signal_line[-1]:
                log("Selling signal triggered")
                allocation = 0  # No allocation due to selling
        
        # Return the allocation decision for RXRX
        return TargetAllocation({"RXRX": allocation})
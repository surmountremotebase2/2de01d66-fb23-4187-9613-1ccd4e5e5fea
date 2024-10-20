from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import MACD
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        self.tickers = ["RXRX"]  # Define the ticker we are interested in

    @property
    def interval(self):
        return "1day"  # Set the interval for MACD calculation

    @property
    def assets(self):
        return self.tickers  # Specify the assets involved in the strategy

    def run(self, data):
        allocation = 0  # Default to no allocation
        rxrx_data = data["ohlcv"]  # Extract ohlcv data for calculations
        log(str(rxrx_data))

        # Calculate MACD for RXRX
        macd = MACD("RXRX", rxrx_data, fast=12, slow=26)
        # Extract MACD and Signal line lists. macd["MACD"] would give us the MACD line, whereas macd["signal"] would give us the Signal line.
        macd_line, signal_line = macd["MACD"], macd["signal"]
        
        if len(macd_line) > 1 and len(signal_line) > 1:
            last_close_price = rxrx_data[-1]["RXRX"]["close"]  # Get the latest closing price
            prev_close_price = rxrx_data[-2]["RXRX"]["close"]  # Get the previous closing price

            # Buy condition: if the MACD line crosses above the signal line and the price is down by at least 3 cents from the previous close
            if macd_line[-2] < signal_line[-2] and macd_line[-1] > signal_line[-1] and (prev_close_price - last_close_price) >= 0.03:
                log("Buying signal triggered")
                allocation = 1  # Full allocation
            
            # Sell condition: if the MACD line crosses below the signal line and the price is up by at least 5 cents from the previous close
            elif macd_line[-2] > signal_line[-2] and macd_line[-1] < signal_line[-1] and (last_close_price - prev_close_price) >= 0.05:
                log("Selling signal triggered")
                allocation = 0  # No allocation due to selling
        
        # Return the allocation decision for RXRX
        return TargetAllocation({"RXRX": allocation})
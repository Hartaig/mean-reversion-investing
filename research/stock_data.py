import pandas as pd
import yfinance as yf

class StockData:
    def get_price_history(self, ticker: str, start_dt: str, end_dt: str,
                          interval: str) -> pd.DataFrame:
        """
        """
        return yf.download(tickers=ticker, start=start_dt, end=end_dt,
                           interval=interval).reset_index()
    
    def get_bb(self, df: pd.DataFrame, periods: int,
               num_std: int) -> pd.DataFrame:
        """
        periods: number of periods to use
        num_std: number of standard deviations for upper and lower bands
        """
        df_out = df.copy()
        # Calculate the rolling mean and standard deviation
        rolling_mean = df_out['Close'].rolling(window=periods).mean()
        rolling_std = df_out['Close'].rolling(window=periods).std()
        # Calculate the upper and lower Bollinger Bands
        ub = rolling_mean + (rolling_std * num_std)
        lb = rolling_mean - (rolling_std * num_std)
        # Create a DataFrame to store the Bollinger Bands
        df_out['ub'] = ub
        df_out['ma'] = rolling_mean
        df_out['lb'] = lb
        return df_out
    


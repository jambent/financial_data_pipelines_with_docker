import yfinance as yf
import pandas as pd
from datetime import datetime as dt

if __name__ == '__main__':
    target_time = dt.fromisoformat('2024-02-29T16:15:00Z')

    def generate_empty_dataframe_for_equity_index_data(dataframe_columns):
        """
        Generates empty DataFrame to which equity index data will be appended

        Args:
            dataframe_columns: column names for generated DataFrame
        Returns:
            Empty DataFrame with required column names
        Raises:
            TypeError if dataframe_columns is not a list
        """
        if not isinstance(dataframe_columns, list):
            raise TypeError(
                ('dataframe_columns must be a list: equity index DataFrame'))

        df = pd.DataFrame(columns=(dataframe_columns))
        return df
    

    def find_target_batch_time():
        """
        Determine required batch time by comparing time when function invoked
        to list of required BATCH_TIMES, and select most recent BATCH_TIME

        Returns:
            String of required batch time, to match index format
                of yfinance DataFrame
            file_key to be used when writing to s3 bucket
        """
        time_now = dt.now()
        date_today = str(time_now.date())

        batch_time_string = '2024-02-29' + 'T16:15:00Z'
        
        target_batch_dt_object = dt.fromisoformat(batch_time_string)

        file_key = (date_today + '/' + '16'
                    + '30' + '/' + 'yfinance_Equity_Index')

        return target_batch_dt_object, file_key


    TICKER_LIST = [
        '^FTSE',
        '^GSPC',
        '^DJI',
        '^IXIC',
        '^GDAXI',
        '^FCHI'
    ]

    DATAFRAME_COLUMNS = [
        'Open',
        'High',
        'Low',
        'Close',
        'Volume',
        'Dividends',
        'Stock Splits',
        'Ticker']

    BATCH_TIMES = [
        '16:30:00',
        '20:00:00'
    ]

    df = generate_empty_dataframe_for_equity_index_data(DATAFRAME_COLUMNS)
    target_batch_string, file_key = find_target_batch_time()
 
    for ticker in TICKER_LIST:
        ticker_data = yf.Ticker(ticker)
        ticker_df = ticker_data.history(period='2d', interval='15m')
        filtered_ticker_df = ticker_df.loc[[target_batch_string]]
        filtered_ticker_df['Ticker'] = ticker
        df = pd.concat([df, filtered_ticker_df])

    print(df.head(50))
    print(target_batch_string)
    print(file_key)



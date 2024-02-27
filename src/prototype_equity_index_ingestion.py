import yfinance as yf
import pandas as pd
from datetime import datetime as dt

if __name__ == '__main__':
    target_time = dt.fromisoformat('2024-02-26T16:15:00Z')

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

    # df = generate_empty_dataframe_for_equity_index_data(DATAFRAME_COLUMNS)

    df = pd.DataFrame(
        columns=(
            'Open',
            'High',
            'Low',
            'Close',
            'Volume',
            'Dividends',
            'Stock Splits',
            'Ticker'))
    for ticker in TICKER_LIST:
        ticker_data = yf.Ticker(ticker)
        ticker_df = ticker_data.history(period='2d', interval='15m')
        filtered_ticker_df = ticker_df.loc[[target_time]]
        filtered_ticker_df['Ticker'] = ticker
        df = pd.concat([df, filtered_ticker_df])

    print(df.head(50))

    # def generate_empty_dataframe_for_equity_index_data(dataframe_columns):
    #     """
    #     Generates empty DataFrame to which equity index data will be appended

    #     Args:
    #         dataframe_columns: column names for generated DataFrame
    #     Returns:
    #         Empty DataFrame with required column names
    #     Raises:
    #         TypeError if dataframe_columns is not a list
    #     """
    #     if not isinstance(dataframe_columns, list):
    #         raise TypeError(
    #             ('dataframe_columns must be a list: equity index DataFrame'))

    #     df = pd.DataFrame(columns=(dataframe_columns))
    #     return df

import os

from load_equity_index_data import load_equity_index_data


from df_to_parquet import dataframe_to_parquet


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
    '16:15:00'
]


def lambda_handler(event, context):
    """
    Lambda handler function for yfinance Equity Index data ingestion
    """
    equity_index_df, key = load_equity_index_data(TICKER_LIST)
    bucket = os.environ['S3_LANDING_ID']

    dataframe_to_parquet(equity_index_df, bucket, key)

    return {'statusCode': 200}

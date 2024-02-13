import os

from load_fx_data import load_fx_data


from df_to_parquet import dataframe_to_parquet


TICKER_LIST = [
    'EURUSD=X',
    'GBPUSD=X',
    'GBPEUR=X',
    'JPY=X',
    'GBP=X',
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
    '06:00:00',
    '16:30:00',
    '20:00:00'
]


def lambda_handler(event, context):
    """
    Lambda handler function for yfinance FX data ingestion
    """
    fx_df, key = load_fx_data(TICKER_LIST)
    bucket = os.environ['S3_LANDING_ID']

    dataframe_to_parquet(fx_df, bucket, key)

    return {'statusCode': 200}

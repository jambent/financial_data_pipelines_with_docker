import awswrangler as wr
import pandas as pd


def dataframe_to_parquet(df, bucket, key):
    """
    Converts DataFrame to parquet file

    Args:
        df: target DataFrame
        bucket: target s3 bucket for resulting parquet file
        key: filename for resulting parquet file
    Returns:
        Parquet file
    Raises:
        TypeError if input not a DataFrame
    """
    if not isinstance(df, pd.DataFrame):
        raise TypeError('Input to dataframe_to_parquet() must be a dataframe')

    try:
        wr.s3.to_parquet(
            df=df,
            path=f's3://{bucket}/{key}.parquet'
        )

    except Exception:
        print('Writing of parquet file to landing bucket failed')

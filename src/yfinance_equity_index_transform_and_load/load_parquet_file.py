import awswrangler as wr


def load_parquet(bucket, key):
    """
    Loads specific parquet file from s3 bucket and converts
    to DataFrame

    Args:
        bucket: name of s3 bucket that target parquet file lies in
        key: remaining filepath of target parquet file within s3 bucket
                , including ".parquet"
    Returns:
        DataFrame
    Raises:
        TypeError if bucket or key input not a string
    """
    if not isinstance(bucket, str):
        raise TypeError('bucket name must be a string')
    if not isinstance(key, str):
        raise TypeError('key must be a string')
    if not key.endswith('.parquet', len(key) - 8):
        raise TypeError('File to load must be a .parquet file')

    try:
        df = wr.s3.read_parquet(path='s3://' + bucket + '/' + key)
        return df
    except Exception as e:
        print(f'Parquet file s3://{bucket}/{key} could not be read: {e}')

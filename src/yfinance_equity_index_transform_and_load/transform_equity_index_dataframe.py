def transform_equity_index_dataframe(equity_index_dataframe, key):
    """
    Transforms Equity Index dataframe, loaded from s3 parquet file,
    to match columns of target val_equity_index database table

    Args:
        equity_index_dataframe: dataframe corresponding to Equity Index data,
                                loaded by load_parquet_file function
        key: filepath of target parquet file within s3 bucket
                , including ".parquet", but not including bucket name,
                e.g., '2024-02-26/1615/yfinance_Equity_Index.parquet'
    Returns:
        DataFrame
    """
    df = equity_index_dataframe.copy(deep=True)

    def extract_equity_index_name(row):
        "Extracts index name from yfinance Equity Index Ticker"
        return row['Ticker'][1:]

    df['equity_index'] = df.apply(extract_equity_index_name, axis=1)

    key_info = key.split('/')
    date = key_info[0]
    batch = key_info[1]
    df['date'] = date
    df['batch'] = batch
    df['index_level'] = df['Close']

    (df.drop(columns=['Volume', 'Dividends', 'Stock_Splits', 'Ticker',
                      'Open', 'High', 'Low', 'Close'], inplace=True))

    df = (df[['date', 'batch'] + [col_name for col_name in df.columns
             if col_name not in ['date', 'batch']]])

    return df

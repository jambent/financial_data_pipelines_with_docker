def transform_fx_dataframe(fx_dataframe, key):
    """
    Transforms FX dataframe, loaded from s3 parquet file, to match columns
    of target val_fx database table

    Args:
        fx_dataframe: dataframe corresponding to FX data,
                       loaded by load_parquet_file function
        key: filepath of target parquet file within s3 bucket
                , including ".parquet", but not including bucket name,
                e.g., '2024-02-08/1630/yfinance_FX.parquet'
    Returns:
        DataFrame
    """
    df = fx_dataframe.copy(deep=True)

    def obtain_domestic_ccy(row):
        "Extracts domestic currency from yfinance FX Ticker"
        ccy_info = row['Ticker'].split('=')[0]
        if len(ccy_info) == 3:
            return 'USD'
        elif len(ccy_info) == 6:
            return ccy_info[0:3]

    def obtain_foreign_ccy(row):
        "Extracts foreign currency from yfinance FX Ticker"
        ccy_info = row['Ticker'].split('=')[0]
        return ccy_info[-3:]

    df['domestic_ccy'] = df.apply(obtain_domestic_ccy, axis=1)
    df['foreign_ccy'] = df.apply(obtain_foreign_ccy, axis=1)

    key_info = key.split('/')
    date = key_info[0]
    batch = key_info[1]
    df['date'] = date
    df['batch'] = batch
    df['fx_rate'] = df['Close']

    (df.drop(columns=['Volume', 'Dividends', 'Stock_Splits', 'Ticker',
                      'Open', 'High', 'Low', 'Close'], inplace=True))

    df = (df[['date', 'batch'] + [col_name for col_name in df.columns
             if col_name not in ['date', 'batch']]])

    return df

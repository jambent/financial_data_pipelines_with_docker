import pandas as pd

def transform_dataframe(dataframe):
    df = dataframe.copy(deep=True)
    df.drop(columns=['Volume','Dividends','Stock Splits'])

    return df
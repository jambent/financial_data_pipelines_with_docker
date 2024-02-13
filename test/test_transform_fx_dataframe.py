import pandas as pd

from src.yfinance_fx_transform_and_load.transform_fx_dataframe \
    import transform_dataframe


def test_that_dataframe_returned_and_is_not_the_same_as_the_input():
    df = pd.DataFrame()
    result = transform_dataframe(df)

    assert isinstance(result, pd.DataFrame)
    assert result is not df


def test_that_input_dataframe_is_not_mutated():
    df = pd.DataFrame()
    df_copy = df.copy(deep=True)
    transform_dataframe(df)

    assert df.equals(df_copy)
    assert df is not df_copy

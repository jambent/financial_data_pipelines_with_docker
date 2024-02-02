import pytest
import pandas as pd
import copy

from src.yfinance_fx_ingestion.load_fx_data import (
    generate_empty_dataframe_for_fx_data, load_fx_data, find_target_batch_time)

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


def test_that_dataframe_returned_from_generate_empty_dataframe_for_fx_data():
    result = generate_empty_dataframe_for_fx_data(DATAFRAME_COLUMNS)

    assert isinstance(result, pd.DataFrame)


def test_generate_empty_dataframe_for_fx_data_returns_df_with_right_columns():
    result = generate_empty_dataframe_for_fx_data(DATAFRAME_COLUMNS)
    columns_list = list(result)
    assert columns_list == DATAFRAME_COLUMNS


def test_that_type_error_raised_if_df_columns_not_passed_as_list():
    with pytest.raises(TypeError, match=r'dataframe_columns must be a list'):
        generate_empty_dataframe_for_fx_data({'Open': 'Open', 'High': 'High'})


def test_that_exception_raised_if_empty_df_not_generated():
    with pytest.raises(Exception):
        generate_empty_dataframe_for_fx_data(DATAFRAME_COLUMNS, 2)


def test_that_dataframe_returned_from_load_fx_data():
    result, key = load_fx_data(TICKER_LIST)

    assert isinstance(result, pd.DataFrame)
    assert isinstance(key, str)


def test_that_ticker_list_not_mutated():
    ticker_list_copy = copy.deepcopy(TICKER_LIST)
    load_fx_data(ticker_list_copy)

    assert ticker_list_copy == TICKER_LIST
    assert ticker_list_copy is not TICKER_LIST


def test_that_type_error_raised_if_ticker_list_not_passed_as_list():
    with pytest.raises(TypeError, match=r'ticker_list must be a list'):
        load_fx_data({'EURUSD=X': 'EURUSD=X', 'GBPUSD=X': 'GBPUSD=X'})


def test_that_exception_raised_if_fx_df_not_returned():
    with pytest.raises(Exception):
        load_fx_data(TICKER_LIST, 2)


def test_that_target_batch_time_returned_as_string():
    result, key = find_target_batch_time()

    assert isinstance(result, str)
    assert isinstance(key, str)

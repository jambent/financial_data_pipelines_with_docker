import pytest
import pandas as pd
import boto3
from moto import mock_s3
from unittest.mock import patch

from src.yfinance_fx_transform_and_load.load_parquet_file import load_parquet


@mock_s3
@patch('src.yfinance_fx_transform_and_load.load_parquet_file.load_parquet',
       return_value=pd.DataFrame())
def test_that_dataframe_returned(patched_load_parquet):
    bucket = 'test-bucket'
    key = '/2023-12-18/0600/test.parquet'
    client = boto3.client('s3')
    client.create_bucket(
        Bucket=bucket,
        CreateBucketConfiguration={'LocationConstraint': 'eu-west-2'}
    )
    result = patched_load_parquet(bucket, key)

    assert isinstance(result, pd.DataFrame)


@mock_s3
@patch('src.yfinance_fx_transform_and_load.load_parquet_file.wr.s3')
def test_that_awswrangler_func_called_with_right_arguments(
        patched_parquet_load):
    bucket = 'test-bucket'
    key = '2023-12-18/0600/test.parquet'
    client = boto3.client('s3')
    client.create_bucket(
        Bucket=bucket,
        CreateBucketConfiguration={'LocationConstraint': 'eu-west-2'}
    )
    load_parquet(bucket, key)

    patched_parquet_load.read_parquet.assert_called_with(
        path='s3://test-bucket/2023-12-18/0600/test.parquet')


def test_that_type_error_raised_if_inputs_not_strings_or_file_not_parquet():
    with pytest.raises(TypeError):
        load_parquet(85, 'this_is_a_test_file.txt')
        load_parquet('test-bucket', True)
        load_parquet('test-bucket', 'this_is_a_test_file.txt')

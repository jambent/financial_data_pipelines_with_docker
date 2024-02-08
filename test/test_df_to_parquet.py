import pytest
import pandas as pd
import boto3
import awswrangler as wr
from moto import mock_aws
from unittest.mock import patch

from src.yfinance_fx_ingestion.df_to_parquet import dataframe_to_parquet


@mock_aws
def test_that_input_dataframe_not_mutated():
    df = pd.DataFrame()
    df_copy = df.copy(deep=True)
    bucket = 'test-bucket'
    key = 'test_df'
    client = boto3.client('s3')
    client.create_bucket(
        Bucket=bucket,
        CreateBucketConfiguration={'LocationConstraint': 'eu-west-2'}
    )

    dataframe_to_parquet(df, bucket, key)

    assert df.equals(df_copy)
    assert df is not df_copy


@mock_aws
def test_that_type_error_thrown_for_non_dataframe_input():
    with pytest.raises(TypeError, match=r'must be a dataframe'):
        bucket = 'test-bucket'
        key = 'test_df'
        client = boto3.client('s3')
        client.create_bucket(
            Bucket=bucket,
            CreateBucketConfiguration={'LocationConstraint': 'eu-west-2'}
        )
        dataframe_to_parquet("hello", bucket, key)


@mock_aws
@patch('src.yfinance_fx_ingestion.df_to_parquet.dataframe_to_parquet',
       side_effect=(Exception
                    ('Writing of parquet file to landing bucket failed')))
def test_that_exception_thrown_for_invalid_arguments(
    patched_dataframe_to_parquet
):
    df = pd.DataFrame(data={'col1': [1, 2], 'col2': [3, 4]})
    bucket = 'test-bucket'
    key = 'test_df'
    client = boto3.client('s3')
    client.create_bucket(
        Bucket=bucket,
        CreateBucketConfiguration={'LocationConstraint': 'eu-west-2'}
    )
    with pytest.raises(Exception) as e:
        patched_dataframe_to_parquet(df, 'no-test-bucket', key)
        assert str(
            e.value) == 'Writing of parquet file to landing bucket failed'
        assert e.type == Exception


@mock_aws
def test_that_input_dataframe_is_recoverable_from_parquet_file():
    df = pd.DataFrame(data={'col1': [1, 2], 'col2': [3, 4]})
    bucket = 'test-bucket'
    key = 'test_df'
    client = boto3.client('s3')
    client.create_bucket(
        Bucket=bucket,
        CreateBucketConfiguration={'LocationConstraint': 'eu-west-2'}
    )

    dataframe_to_parquet(df, bucket, key)

    recovered_df = wr.s3.read_parquet(
        path='s3://test-bucket/test_df.parquet'
    )

    recovered_df = recovered_df.astype(int)
    pd.testing.assert_frame_equal(df, recovered_df)

import boto3
import json
import pytest

from src.get_db_credentials import get_db_credentials
from moto import mock_aws


@mock_aws
def test_get_db_credentials_returns_stored_json():
    sm = boto3.client("secretsmanager", region_name="eu-west-2")
    secret = {
        "endpoint": "a",
        "port": "5432",
        "database": "b",
        "username": "c",
        "password": "d"
    }
    json_secret = json.dumps(secret)
    sm.create_secret(Name="test_credentials", SecretString=json_secret)
    
    response = get_db_credentials("test_credentials")
    
    assert response == json_secret

@pytest.mark.skip
@mock_aws
def test_get_db_credentials_raises_exeption_if_secret_not_found():
    with pytest.raises(botocore.exceptions.ResourceNotFoundException):
        get_db_credentials("this_is_not_a_secret")

@pytest.mark.skip
@mock_aws
def test_get_db_credentials_raises_error_if_secret_not_json():
    sm = boto3.client("secretsmanager", region_name="eu-west-2")
    secret = "secret_credentials"
    sm.create_secret(Name="test_credentials", SecretString=secret)
    with pytest.raises(ResourceNotFoundException):
        get_db_credentials("test_credentials")

@pytest.mark.skip
@mock_aws
def test_get_db_credentials_raises_error_if_required_fields_missing():
    sm = boto3.client("secretsmanager", region_name="eu-west-2")
    secret = {
        "hostname": "a",
        "port": "5432",
        "database": "b",
    }
    sm.create_secret(Name="test_credentials", SecretString=json.dumps(secret))

    with pytest.raises(CredentialRetrievalError):
        get_db_credentials("test_credentials")

@pytest.mark.skip
@mock_aws
def test_get_db_credentials_raises_runtime_error_for_anything_else():
    with pytest.raises(RuntimeError):
        get_db_credentials(44)
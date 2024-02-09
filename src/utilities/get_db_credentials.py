import boto3
from botocore.exceptions import ClientError
import json


def get_db_credentials(secret_name):

    region_name = "eu-west-2"

    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        raise e
    except client.exceptions.ResourceNotFoundException as e:
        print(f"Credentials not found: '{e.response}'")

    secret = json.loads(get_secret_value_response['SecretString'])

    return secret

if __name__ == '__main__':
    creds = get_db_credentials("db_credentials_val_data")
    print(creds)

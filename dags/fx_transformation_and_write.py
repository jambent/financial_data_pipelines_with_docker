from airflow.models import DAG
from airflow.models.connection import Connection
from airflow.exceptions import AirflowFailException
from datetime import datetime, timedelta
from airflow.utils.dates import days_ago
from airflow.operators.python import PythonOperator
from airflow.providers.amazon.aws.sensors.s3 import S3KeySensor
from airflow.hooks.S3_hook import S3Hook
import boto3
import os
import json

#os.environ['AWS_PROFILE'] = 'default'
#os.environ['REGION_NAME'] = 'eu-west-2'
# os.environ['AWS_PROFILE'] = "dev"
# os.environ['AWS_DEFAULT_REGION'] = "eu-west-2"

# def _create_connection(**context):
#     """
#     AWS connection
#     """
#     AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
#     AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
#     AWS_SESSION_TOKEN = os.getenv("AWS_SESSION_TOKEN")
#     REGION_NAME = os.getenv("REGION_NAME")
#     credentials = [
#         AWS_SESSION_TOKEN,
#         AWS_ACCESS_KEY_ID,
#         AWS_SECRET_ACCESS_KEY,
#         REGION_NAME,
#     ]
#     if not credentials or any(not credential for credential in credentials):
#         raise AirflowFailException("Environment variables were not passed")

#     extras = json.dumps(
#         dict(
#             aws_session_token=AWS_SESSION_TOKEN,
#             aws_access_key_id=AWS_ACCESS_KEY_ID,
#             aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
#             region_name=REGION_NAME,
#         ),
#     )
#     try:
#         aws_conn = Connection(
#             conn_id="s3_con",
#             conn_type="S3",
#             extra=extras,
#         )
#     except Exception as e:
#         raise AirflowFailException(
#             f"Error creating connection to Airflow :{e}",
#         )


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': days_ago(1),
    'max_active_runs': 1,
    'email_on_retry': False,
    'retry_delay': timedelta(minutes=5)
}

dg = DAG('FX_s3_sensor',
          schedule_interval='00 * * * *',
          default_args=default_args,
          catchup=True
          )
#s3_conn = S3Hook.get_conn()
s3_client = boto3.client('s3')
# s3_client = boto3.client('s3', aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'],region_name=os.environ['AWS_DEFAULT_REGION']
# )

buckets = s3_client.list_buckets()
bucket_names = [bucket['Name'] for bucket in buckets['Buckets']]

matched_bucket_name = [match for match in bucket_names if "landing" in match]
s3_bucket_name = matched_bucket_name[0]

s3_key = 'test.txt'

s3_sensor = S3KeySensor(
    task_id='s3_FX_file_check',
    poke_interval=60,
    timeout=180,
    soft_fail=False,
    retries=2,
    bucket_key=s3_key,
    bucket_name=s3_bucket_name,
    aws_conn_id='aws_default',
    dag=dg)


def processing_func(**kwargs):
    print("Reading the file")
    s3 = boto3.client('s3')
    obj = s3.get_object(Bucket=s3_bucket_name, Key=s3_key)
    lin = obj['Body'].read().decode("utf-8")
    print(lin)


func_task = PythonOperator(
    task_id='a_task_using_fx_file',
    python_callable=processing_func,
    dag=dg)

s3_sensor >> func_task
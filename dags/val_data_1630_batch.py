from airflow.models import DAG
from airflow.models.connection import Connection
from airflow.exceptions import AirflowFailException
from datetime import timedelta
from airflow.utils.dates import days_ago
from airflow.operators.python import PythonOperator
from airflow.providers.amazon.aws.sensors.s3 import S3KeySensor
from airflow.hooks.S3_hook import S3Hook
import os
# import ssl
# import awswrangler as wr
from datetime import datetime as dt
from datetime import timedelta
# from pg8000.native import literal

from src.yfinance_fx_transform_and_load.load_parquet_file \
    import load_parquet
from src.yfinance_fx_transform_and_load.transform_fx_dataframe \
    import transform_fx_dataframe
from src.yfinance_fx_transform_and_load.insert_into_val_fx \
    import insert_into_val_fx
from src.yfinance_batch_completion.get_val_batch_insertion_string \
    import get_val_batch_insertion_string
from src.utilities.get_db_connection import new_db_connection


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

dg = DAG('FX_1630_s3_sensor',
          schedule_interval='51 16 * * 1-5',
          default_args=default_args,
          catchup=True
          )
#s3_conn = S3Hook.get_conn()
# s3_client = boto3.client('s3')
# s3_client = boto3.client('s3', aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'],region_name=os.environ['AWS_DEFAULT_REGION']
# )

# buckets = s3_client.list_buckets()
# bucket_names = [bucket['Name'] for bucket in buckets['Buckets']]

# matched_bucket_name = [match for match in bucket_names if "landing" in match]
# s3_bucket_name = matched_bucket_name[0]
s3_landing_bucket = os.environ['S3_LANDING_ID']

time_now = dt.now()
date_today = str(time_now.date())
fx_1630_s3_key = date_today + '/' + '1630' + '/' + 'yfinance_FX.parquet'

fx_1630_s3_sensor = S3KeySensor(
    task_id = 'fx_1630_s3_file_check',
    poke_interval = 60,
    timeout = 180,
    soft_fail = False,
    retries = 2,
    bucket_key = fx_1630_s3_key,
    bucket_name = s3_landing_bucket,
    aws_conn_id = 'aws_default',
    dag = dg)


def write_to_val_fx():
    fx_df = load_parquet(s3_landing_bucket, fx_1630_s3_key)
    transformed_fx_df = transform_fx_dataframe(fx_df, fx_1630_s3_key)
    # ssl_context = ssl.SSLContext()
    # conn = wr.postgresql.connect(secret_id="db_credentials_val_data",ssl_context=ssl_context)
    conn = new_db_connection()
    try:
        insert_into_val_fx(transformed_fx_df, conn)
        # wr.postgresql.to_sql(
        #     df=transformed_fx_df,
        #     table='val_fx',
        #     schema='public',
        #     con=conn,
        #     mode='upsert',
        #     index=False,
        #     use_column_names=True,
        #     upsert_conflict_columns=['id']
        # )
    finally:
        conn.close()



def write_1630_to_val_batch():
    # ssl_context = ssl.SSLContext()
    # conn = wr.postgresql.connect(
    #     secret_id="db_credentials_val_data",
    #     ssl_context=ssl_context)
    conn = new_db_connection()
    cursor = conn.cursor()

    try:
        batch_complete_string = get_val_batch_insertion_string(date_today,'1630')
        # activate_1630_val_batch = f"""INSERT INTO val_batch 
        # (date, batch, batch_ready)
        # VALUES
        # ({literal(date_today)}, '1630', true);"""

        # cursor.execute(activate_1630_val_batch)
        cursor.execute(batch_complete_string)
        conn.commit()
    finally:
        conn.close()



write_fx_1630_data_to_val_fx = PythonOperator(
    task_id = 'Process_1630_FX_file',
    python_callable = write_to_val_fx,
    dag = dg)


activate_1630_batch_in_val_batch = PythonOperator(
    task_id = 'Activate_1630_batch',
    python_callable = write_1630_to_val_batch,
    dag = dg)



fx_1630_s3_sensor >> write_fx_1630_data_to_val_fx

[write_fx_1630_data_to_val_fx] >> activate_1630_batch_in_val_batch
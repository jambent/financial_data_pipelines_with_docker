from airflow.models import DAG
from airflow.utils.dates import days_ago
from airflow.operators.python import PythonOperator
from airflow.providers.amazon.aws.sensors.s3 import S3KeySensor
import boto3
from datetime import datetime as dt
from datetime import timedelta

# from src.yfinance_fx_transform_and_load.load_parquet_file \
#     import load_parquet
from src.yfinance_fx_transform_and_load.transform_fx_dataframe \
    import transform_fx_dataframe
from src.yfinance_fx_transform_and_load.insert_into_val_fx \
    import insert_into_val_fx

# from src.yfinance_equity_index_transform_and_load.load_parquet_file \
#     import load_parquet
from src.yfinance_equity_index_transform_and_load.\
    transform_equity_index_dataframe import transform_equity_index_dataframe
from src.yfinance_equity_index_transform_and_load.\
    insert_into_val_equity_index import insert_into_val_equity_index

from src.yfinance_batch_completion.get_val_batch_insertion_string \
    import get_val_batch_insertion_string

from src.utilities.get_db_connection import new_db_connection
from src.utilities.load_parquet_file import load_parquet


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': days_ago(1),
    'max_active_runs': 1,
    'email_on_retry': False,
    'retry_delay': timedelta(minutes=5)
}

# fx_0600_dg = DAG('FX_0600_s3_sensor',
#                  schedule_interval='21 06 * * 1-5',
#                  default_args=default_args,
#                  catchup=True
#                  )

# fx_1630_dg = DAG('FX_1630_s3_sensor',
#                  schedule_interval='51 16 * * 1-5',
#                  default_args=default_args,
#                  catchup=True
#                  )

# equity_index_1615_dg = DAG('Equity_Index_1615_s3_sensor',
#                            schedule_interval='36 16 * * 1-5',
#                            default_args=default_args,
#                            catchup=True
#                            )

# fx_2000_dg = DAG('FX_2000_s3_sensor',
#                  schedule_interval='21 20 * * 1-5',
#                  default_args=default_args,
#                  catchup=True
#                  )

s3_client = boto3.client('s3')
buckets = s3_client.list_buckets()
bucket_names = [bucket['Name'] for bucket in buckets['Buckets']]
matched_bucket_name = [match for match in bucket_names if "landing" in match]
s3_landing_bucket = matched_bucket_name[0]


time_now = dt.now()
date_today = str(time_now.date())
fx_0600_s3_key = date_today + '/' + '0600' + '/' + 'yfinance_FX.parquet'
fx_1630_s3_key = date_today + '/' + '1630' + '/' + 'yfinance_FX.parquet'
equity_index_1615_s3_key = date_today + '/' + \
    '1615' + '/' + 'yfinance_Equity_Index.parquet'
fx_2000_s3_key = date_today + '/' + '2000' + '/' + 'yfinance_FX.parquet'


with DAG(
    '1630_val_data_batch',
    schedule_interval='31 16 * * 1-5',
    default_args=default_args,
    catchup=True
):



# fx_0600_s3_sensor = S3KeySensor(
#     task_id='fx_0600_s3_file_check',
#     poke_interval=60,
#     timeout=180,
#     soft_fail=False,
#     retries=2,
#     bucket_key=fx_0600_s3_key,
#     bucket_name=s3_landing_bucket,
#     aws_conn_id='aws_default',
#     dag=fx_0600_dg)

    equity_index_1615_s3_sensor = S3KeySensor(
    task_id='equity_index_1615_s3_file_check',
    poke_interval=60,
    timeout=600,
    soft_fail=False,
    # retries=2,
    bucket_key=equity_index_1615_s3_key,
    bucket_name=s3_landing_bucket,
    aws_conn_id='aws_default',
    # dag=equity_index_1615_dg
    )

    fx_1630_s3_sensor = S3KeySensor(
    task_id='fx_1630_s3_file_check',
    poke_interval=60,
    timeout=960,
    soft_fail=False,
    # retries=2,
    bucket_key=fx_1630_s3_key,
    bucket_name=s3_landing_bucket,
    aws_conn_id='aws_default',
    # dag=fx_1630_dg
    )

# fx_2000_s3_sensor = S3KeySensor(
#     task_id='fx_2000_s3_file_check',
#     poke_interval=60,
#     timeout=180,
#     soft_fail=False,
#     retries=2,
#     bucket_key=fx_2000_s3_key,
#     bucket_name=s3_landing_bucket,
#     aws_conn_id='aws_default',
#     dag=fx_2000_dg)


# def write_0600_to_val_fx():
#     "Insert 0600 FX data into val_fx"
#     fx_df = load_parquet(s3_landing_bucket, fx_0600_s3_key)
#     transformed_fx_df = transform_fx_dataframe(fx_df, fx_0600_s3_key)
#     conn = new_db_connection()
#     try:
#         insert_into_val_fx(transformed_fx_df, conn)
#     finally:
#         conn.close()


    def write_1615_to_val_equity_index():
        "Insert 1615 Equity Index data into val_equity_index"
        equity_index_df = load_parquet(s3_landing_bucket, equity_index_1615_s3_key)
        transformed_equity_index_df = transform_equity_index_dataframe(
            equity_index_df, equity_index_1615_s3_key)
        conn = new_db_connection()
        try:
            insert_into_val_equity_index(transformed_equity_index_df, conn)
        finally:
            conn.close()


    def write_1630_to_val_fx():
        "Insert 1630 FX data into val_fx"
        fx_df = load_parquet(s3_landing_bucket, fx_1630_s3_key)
        transformed_fx_df = transform_fx_dataframe(fx_df, fx_1630_s3_key)
        conn = new_db_connection()
        try:
            insert_into_val_fx(transformed_fx_df, conn)
        finally:
            conn.close()


# def write_2000_to_val_fx():
#     "Insert 2000 FX data into val_fx"
#     fx_df = load_parquet(s3_landing_bucket, fx_2000_s3_key)
#     transformed_fx_df = transform_fx_dataframe(fx_df, fx_2000_s3_key)
#     conn = new_db_connection()
#     try:
#         insert_into_val_fx(transformed_fx_df, conn)
#     finally:
#         conn.close()


# def write_0600_to_val_batch():
#     """
#     Activate the 0600 batch for current date,
#     once ALL 0600 data has been inserted
#     """
#     conn = new_db_connection()
#     cursor = conn.cursor()
#     try:
#         batch_complete_string = \
#             get_val_batch_insertion_string(date_today, '0600')
#         cursor.execute(batch_complete_string)
#         conn.commit()
#     finally:
#         conn.close()


    def write_1630_to_val_batch():
        """
        Activate the 1630 batch for current date,
        once ALL 1630 data has been inserted
        """
        conn = new_db_connection()
        cursor = conn.cursor()
        try:
            batch_complete_string = \
                get_val_batch_insertion_string(date_today, '1630')
            cursor.execute(batch_complete_string)
            conn.commit()
        finally:
            conn.close()


# def write_2000_to_val_batch():
#     """
#     Activate the 2000 batch for current date,
#     once ALL 2000 data has been inserted
#     """
#     conn = new_db_connection()
#     cursor = conn.cursor()
#     try:
#         batch_complete_string = \
#             get_val_batch_insertion_string(date_today, '2000')
#         cursor.execute(batch_complete_string)
#         conn.commit()
#     finally:
#         conn.close()


# write_fx_0600_data_to_val_fx = PythonOperator(
#     task_id='Process_0600_FX_file',
#     python_callable=write_0600_to_val_fx
# )

    write_equity_index_1615_data_to_val_equity_index = PythonOperator(
        task_id='Process_1615_Equity_Index_file',
        python_callable=write_1615_to_val_equity_index)

    write_fx_1630_data_to_val_fx = PythonOperator(
        task_id='Process_1630_FX_file',
        python_callable=write_1630_to_val_fx
    )

# write_fx_2000_data_to_val_fx = PythonOperator(
#     task_id='Process_2000_FX_file',
#     python_callable=write_2000_to_val_fx
# )


# activate_0600_batch_in_val_batch = PythonOperator(
#     task_id='Activate_0600_batch',
#     python_callable=write_0600_to_val_batch
# )

    activate_1630_batch_in_val_batch = PythonOperator(
        task_id='Activate_1630_batch',
        python_callable=write_1630_to_val_batch
    )

# activate_2000_batch_in_val_batch = PythonOperator(
#     task_id='Activate_2000_batch',
#     python_callable=write_2000_to_val_batch
# )


    # fx_0600_s3_sensor >> write_fx_0600_data_to_val_fx
    equity_index_1615_s3_sensor >> write_equity_index_1615_data_to_val_equity_index
    fx_1630_s3_sensor >> write_fx_1630_data_to_val_fx
    # fx_2000_s3_sensor >> write_fx_2000_data_to_val_fx

    # [write_fx_0600_data_to_val_fx] >> activate_0600_batch_in_val_batch
    #[write_equity_index_1615_data_to_val_equity_index,write_fx_1630_data_to_val_fx] >> activate_1630_batch_in_val_batch
    write_equity_index_1615_data_to_val_equity_index >> activate_1630_batch_in_val_batch
    write_fx_1630_data_to_val_fx >> activate_1630_batch_in_val_batch
    # [write_fx_2000_data_to_val_fx] >> activate_2000_batch_in_val_batch

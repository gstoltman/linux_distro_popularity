import os
import pyarrow.csv as pv
import pyarrow.parquet as pq
from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.providers.google.cloud.operators.bigquery import BigQueryCreateExternalTableOperator


from google.cloud import storage
# from schema import schema

default_args = {
    'owner': 'airflow'
}

AIRFLOW_HOME = os.environ.get('AIRFLOW_HOME', '/opt/airflow')

URL = 'https://raw.githubusercontent.com/gstoltman/linux_distro_popularity/main/exports/rank_by_years.csv'
CSV_FILENAME = 'rank_by_years.csv'
PARQUET_FILENAME = CSV_FILENAME.replace('csv', 'parquet')

CSV_OUTFILE = f'{AIRFLOW_HOME}/{CSV_FILENAME}'
PARQUET_OUTFILE = f'{AIRFLOW_HOME}/{PARQUET_FILENAME}'
TABLE_NAME = 'rank_by_year'

GCP_PROJECT_ID = os.environ.get('GCP_PROJECT_ID')
GCP_GCS_BUCKET = os.environ.get('GCP_GCS_BUCKET')
#BIQQUERY_DATASET = os.environ.get('BIGQUERY_DATASET', '###PLACEHOLDER###')

def convert_to_parquet(csv_file, parquet_file):
    if not csv_file.endswith('csv'):
        raise ValueError('The input file is not in csv format')
    
    table=pv.read_csv(csv_file)
    pq.write_table(table, parquet_file)

def upload_to_gcs(file_path, bucket_name, blob_name):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    
    blob = bucket.blob(blob_name)
    blob.upload_from_filename(file_path)

with DAG(
    dag_id = f'load_data_dag',
    default_args = default_args,
    schedule_interval="@once",
    start_date=datetime(2023,11,7),
    end_date=datetime(2023,11,7),
    catchup=True,
    tags=['ldp']
) as dag:
    
    download_data_file_task = BashOperator(
        task_id = "download_data_file",
        bash_command = f"curl -o {CSV_OUTFILE} {URL}"
    )

    convert_to_parquet_task = PythonOperator(
        task_id = 'convert_to_parquet',
        python_callable = convert_to_parquet,
        op_kwargs = {
            'csv_file' : CSV_OUTFILE,
            'parquet_file' : PARQUET_OUTFILE
        }
    )

    upload_to_gcs_task = PythonOperator(
        task_id = 'upload_to_gcs',
        python_callable = upload_to_gcs,
        op_kwargs = {
            'file_path': PARQUET_OUTFILE,
            'bucket_name': GCP_GCS_BUCKET,
            'blob_name': f'{TABLE_NAME}/{PARQUET_FILENAME}'
        }
    )

    remove_files_from_local_task=BashOperator(
        task_id='remove_files_from_local',
        bash_command=f'rm {CSV_OUTFILE} {PARQUET_OUTFILE}'
    )

    download_data_file_task >> convert_to_parquet_task >> upload_to_gcs_task >> remove_files_from_local_task
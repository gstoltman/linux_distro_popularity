from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
from google.cloud import storage

def upload_to_gcp(**kwargs):
    source_file_path = '/home/space/projects/data_eng/linux_distro_popularity/exports/2002_export.csv'
    destination_bucket_name = 'ldp-bucket-1'
    destination_blob_name = "file.csv"

    client = storage.Client()
    bucket = client.get_bucket(destination_bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_path)

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 11, 3),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 3,
}

dag = DAG(
    'send_csvs_to_gcp',
    default_args=default_args,
    schedule_interval=None,
    dagrun_timeout=timedelta(minutes=60),
)

t1 = PythonOperator(
    task_id='send_csvs_to_gcp',
    python_callable=upload_to_gcp,
    provide_context=True,
    dag=dag,
)
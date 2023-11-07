from datetime import datetime
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.contrib.operators.gcs_to_bq import GoogleCloudStorageToBigQueryOperator
from airflow.providers.google.cloud.transfers.local_to_gcs import LocalFilesystemToGCSOperator
import os

def upload_to_gcs(export_folder, gcs_path, **kwargs):
    export_folder = export_folder
    bucket_name = 'ldp-bucket-1'
    gcs_conn_id = 'google_cloud_default'

    csv_files = [file for file in os.listdir(export_folder)]

    for csv_file in csv_files:
        local_file_path = os.path.join(export_folder, csv_file)
        gcs_file_path = f"{gcs_path}/{csv_file}"

        upload_task = LocalFilesystemToGCSOperator(
            task_id = f'upload_to_gcs',
            src=local_file_path,
            dst=gcs_file_path,
            bucket=bucket_name,
            gcp_conn_id=gcs_conn_id,
        )
        upload_task.execute(context=kwargs)

dag = DAG(
    'upload_files_to_gcs',
    start_date=datetime(2023, 10, 6),
    schedule_interval=None,
    catchup=False,
)

upload_to_gcs = PythonOperator(
    task_id='upload_to_gcs',
    python_callable=upload_to_gcs,
    op_args=['/home/space/projects/data_eng/linux_distro_popularity/exports/', 'ldp/exports'],
    provide_context=True,
    dag=dag,
)

upload_to_gcs
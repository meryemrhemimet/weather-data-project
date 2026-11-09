from airflow import DAG  
from datetime import datetime, timedelta
from airflow.operators.python import PythonOperator
from airflow.providers.docker.operators.docker import DockerOperator
from docker.types import Mount
import os
import sys 
sys.path.append('/opt/airflow/api-requests')
from insert_records import main

default_args = {
    'description': 'A DAG to orchestrate the weather data pipeline',      
    'start_date': datetime(2026, 10, 26),
    'catchup': False,  
}
dag = DAG(
    dag_id='weather-api-dbt-orchestrator',
    default_args=default_args,
    schedule=timedelta(minutes=1)
    )
with dag:
    task1 =PythonOperator(
        task_id='ingest_weather_data',
        python_callable=main
    )
    task2 = DockerOperator(
        task_id='transform_data_task',
        image='ghcr.io/dbt-labs/dbt-postgres:1.9.0',
        command='run',
        working_dir='/usr/app',
        mounts=[
    Mount(
        source=os.path.join(os.environ["WEATHER_PROJECT_ROOT"], "dbt/my_project"),
        target='/usr/app',
        type='bind'
    ),
    Mount(
        source=os.path.join(os.environ["WEATHER_PROJECT_ROOT"], "dbt/profiles"),
        target='/root/.dbt',
        type='bind'
    )
],
        network_mode=os.environ["WEATHER_DOCKER_NETWORK"],
        environment={
            "POSTGRES_HOST": os.environ["POSTGRES_HOST"],
            "POSTGRES_PORT": os.environ["POSTGRES_PORT"],
            "POSTGRES_DB": os.environ["POSTGRES_DB"],
            "POSTGRES_USER": os.environ["POSTGRES_USER"],
            "POSTGRES_PASSWORD": os.environ["POSTGRES_PASSWORD"],
        },
        docker_url='unix://var/run/docker.sock',
        auto_remove='success'
    )
 
task1 >> task2
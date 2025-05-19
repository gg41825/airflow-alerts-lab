import os
import sys

from airflow.sdk import DAG
from airflow.providers.standard.operators.python import PythonOperator

import pendulum

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PROJECT_ROOT)

from utils.currency_rate_fetcher import get_eur_twd_rate
from utils.email_alert import send_rate_info_email

default_args = {
    'owner': 'Ginny',
    'start_date': pendulum.datetime(2025, 5, 17, tz="Asia/Taipei"),
    'retries': 1
}

with DAG(
    dag_id='eur_twd_rate_alert',
    default_args=default_args,
    schedule="30 15 * * *", # every day at 15:30, Sino Bank Ex rate late update time
    tags=['currency', 'email']
) as dag:
    
    get_rate = PythonOperator(
        task_id='get_rate',
        python_callable=get_eur_twd_rate
    )

    send_email = PythonOperator(
        task_id='send_email',
        python_callable=send_rate_info_email
    )
    get_rate >> send_email
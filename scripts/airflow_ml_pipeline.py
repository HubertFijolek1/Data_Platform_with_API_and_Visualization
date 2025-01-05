from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash_operator import BashOperator

default_args = {
    "owner": "you",
    "depends_on_past": False,
    "start_date": datetime(2025, 1, 10),
    "retries": 1,
    "retry_delay": timedelta(minutes=5)
}

with DAG(
    dag_id="ml_pipeline_example",
    default_args=default_args,
    schedule_interval="@daily",  # or any cron expression
    catchup=False
) as dag:

    # Step 1: Data extraction (dummy example)
    extract_data = BashOperator(
        task_id="extract_data",
        bash_command="echo 'Extracting data...'"
    )

    # Step 2: Train model
    #   We call the train_models.py script or some CLI command from inside BashOperator
    train_model_task = BashOperator(
        task_id="train_model",
        bash_command="cd /app && python scripts/train_models.py"
    )

    # Step 3: Evaluate / store metrics (dummy example)
    store_metrics = BashOperator(
        task_id="store_metrics",
        bash_command="echo 'Storing metrics...'"
    )

    extract_data >> train_model_task >> store_metrics
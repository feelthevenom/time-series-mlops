"""
Time Series Forecasting DAG
"""
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys
import os

# Add parent directory to sys.path to make src visible - this is a light operation
sys.path.insert(0, '/app')

# Define the DAG first, before any heavy imports
with DAG(
    dag_id="data_ingestion_test",
    start_date=datetime(2024, 1, 1),
    schedule="*/2 * * * *",
    catchup=False,
    default_args={
        'retries': 1,
        'retry_delay': timedelta(seconds=30),
    },
    tags=["test", "ingestion"]
) as dag:
    
    # Define a callable function to be used by the task
    # This is crucial - only import heavy modules inside the function
    def run_data_ingestion(**kwargs):
        # Import components here inside the function, not at the top level
        # This way imports are only processed when the task actually runs
        from src.components.data_ingetion import DataIngestion
        from src.entity.config_entity import DataIngestionConfig, TrainingPipelineConfig
        
        # Execute data ingestion logic
        pipeline_config = TrainingPipelineConfig()
        ingestion_config = DataIngestionConfig(pipeline_config)
        ingestor = DataIngestion(ingestion_config)
        ingestor.initiate_data_ingestion()
    
    # Create the task
    ingest_task = PythonOperator(
        task_id="run_data_ingestion",
        python_callable=run_data_ingestion
    )

# The DAG object needs to be accessible at the module level
# No heavy processing or imports should happen after this point
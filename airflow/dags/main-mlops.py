# root/airflow/dags/main-mlops.py

"""
Time Series Forecasting DAG with enhanced error handling
"""
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import os
import logging
import subprocess

# Configure logging
logger = logging.getLogger(__name__)

# Get the absolute path to the project root directory
PROJECT_ROOT = "/app"

# Function to check DVC status
def check_dvc_status():
    """Check DVC status and report issues"""
    try:
        os.chdir(PROJECT_ROOT)
        status_output = subprocess.check_output(["dvc", "status"]).decode('utf-8')
        logger.info(f"DVC Status:\n{status_output}")
        return True
    except Exception as e:
        logger.error(f"Error checking DVC status: {str(e)}")
        return False

# Define the DAG
with DAG(
    dag_id="mlops_pipeline",
    start_date=datetime(2024, 1, 1),
    schedule="*/20 * * * *",  # every 20 minutes
    catchup=False,
    default_args={
        'retries': 7, # Number of Retries
        'retry_delay': timedelta(minutes=2), # Delay between retries
        'email_on_failure': False,
        'email_on_retry': False,
        'execution_timeout': timedelta(minutes=30),  # Add timeout
    },
    tags=["dvc", "pipeline"]
) as dag:


    # Task to check DVC status
    check_dvc = PythonOperator(
        task_id="check_dvc",
        python_callable=check_dvc_status,
    )

    # Common bash command prefix to ensure we're in the right directory with error handling
    cmd_prefix = f"cd {PROJECT_ROOT} && "
    
    # Enhanced bash script with better error handling
    bash_script_template = """
set -e  # Exit on any error
set -o pipefail  # Pipeline fails on any command failure

cd {project_root}
echo "Starting {task_name} at $(date)"

# Check if DVC is properly initialized
if [ ! -d ".dvc" ]; then
  echo "ERROR: DVC not initialized in this directory"
  exit 1
fi

# Run the command and capture output
echo "Running: dvc repro --force {stage_name}"
dvc repro --force {stage_name} 2>&1 | tee /tmp/dvc_output.log

# Check exit status
if [ $? -ne 0 ]; then
  echo "ERROR: DVC command failed for {stage_name}"
  echo "Last 20 lines of output:"
  tail -n 20 /tmp/dvc_output.log
  exit 1
fi

echo "Successfully completed {task_name} at $(date)"
"""

    data_ingestion = BashOperator(
        task_id="data_ingestion",
        bash_command=bash_script_template.format(
            project_root=PROJECT_ROOT,
            task_name="data_ingestion",
            stage_name="data_ingestion"
        ),
    )

    data_validation = BashOperator(
        task_id="data_validation",
        bash_command=bash_script_template.format(
            project_root=PROJECT_ROOT,
            task_name="data_validation",
            stage_name="data_validation"
        ),
    )

    data_transformation = BashOperator(
        task_id="data_transformation",
        bash_command=bash_script_template.format(
            project_root=PROJECT_ROOT,
            task_name="data_transformation",
            stage_name="data_transformation"
        ),
    )

    model_training = BashOperator(
        task_id="model_training",
        bash_command=bash_script_template.format(
            project_root=PROJECT_ROOT,
            task_name="model_training",
            stage_name="model_training"
        ),
    )

    model_evaluation = BashOperator(
        task_id="model_evaluation",
        bash_command=bash_script_template.format(
            project_root=PROJECT_ROOT,
            task_name="model_evaluation",
            stage_name="model_evaluation"
        ),
    )

    # Define the task dependencies
    check_dvc >> data_ingestion >> data_validation >> data_transformation >> model_training >> model_evaluation

# The DAG object needs to be accessible at the module level
dag 
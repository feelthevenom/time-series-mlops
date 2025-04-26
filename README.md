# time-series-mlops

# Installation Process and Run

## Install uv using pip (in global system)
     pip install uv


## Open project and Create env and activate (it shows how to start in terminal itself)
     uv venv

## install dependencies and libraries 
     uv add -r requirements.txt

## Run the Application 
     python app.py

# Complete MLOPS project using Docker and Apache Airflow 

# Data Ingetion

Ingest data from source data and convert the data into train and test

# Data Validation 
Check the train and test data columns are same 

# Data Tranformation 
Normalize the data in to numpy and save it as pkl file.

# Model Training
Define the model and train the model using Tensofrlow for Model register and push to main model folder path

# Model Evaluation
Evaluate the model and push only if the model is valid to production 

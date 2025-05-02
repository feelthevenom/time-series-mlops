# time-series-mlops

# Installation Process and Run

## Clone the Github Repo

# Run using Docker

## Build the docker file
     docker compose build
## Run the docker file (Remove -d to view the service logs)
     docker compose up -d
## If something went wrong or you want to down and rerun 
     docker compose down -v
## Remove the following file
     .dvc/cache
     .dvc/temp
     dvc.lock
# Apache airflow
![Alt text](/images/apache-airflow-dag.png "a Apache airflow 3.0 UI") 
### Open the browser and paste the url
     http://localhost:8080/
### Login username is admin and password is presented inside project ariflow/simple_auth_manager_passwords.json.generated
### You can see the DAG and select, then it may be started or scheduled to run. 

# Influx DB setup
![Alt text](/images/InfluxDB.png "a InfluxDB UI testing UI") 
### 1. Enter the url in the browser
     http://localhost:8086/
### 2. Select the Data Explorer
### 3. Choose the buck here it is TimeseriesRetailDB
### 4. Choose SCRIPT EDITOR on right side and paste this
     from(bucket: "TimeseriesRetailDB")
       |> range(start: 0)
       |> filter(fn: (r) => r._measurement == "time_series_retail_sales")


# Complete MLOPS project using Docker and Apache Airflow 
![Alt text](/images/sales_prediction_mlops_arch.png "Complete Architecture")

# Real time data generation 
A raw csv dataset is stored in InfluxDB, initially 40% of the data is ingested to DB to initial model training and other csv data points data are stored for each seconds.
To train the model schedule. So this process make it as real-time data to replicate.

# Data Ingetion
Ingest data from source data influxDB bucket and stores the data into feature as csv and split the data into train and test.

# Data Validation 
Check the train and test data columns are contains same number of columns and validate feature csv has correct schema as we defined in yaml file.

# Data Tranformation 
Normalize the data in to numpy and save it as pkl file. which contains train, test and timestamp.

# Model Training
Define the model and train the model using Tensofrlow for Model register and push to main model folder path

# Model Evaluation
Evaluate the model and push only if the model is valid to production and save the plot of the test as png file in artifact.


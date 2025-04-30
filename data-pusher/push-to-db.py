import pandas as pd
import os
import time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
import requests
from src.logging.logger import logging

# InfluxDB Connection Details
INFLUX_URL   = "http://storedata-db:8086"
# INFLUX_TOKEN = os.getenv("DOCKER_INFLUXDB_INIT_ADMIN_TOKEN")
# INFLUX_ORG   = os.getenv("DOCKER_INFLUXDB_INIT_ORG")
# INFLUX_BUCKET= os.getenv("DOCKER_INFLUXDB_INIT_BUCKET")
INFLUX_TOKEN = "RahulSuperSecretToken2024"
INFLUX_ORG   = "Rahul-Personal"
INFLUX_BUCKET= "TimeseriesRetailDB"
MEASUREMENT  = "time_series_retail_sales"


CSV_FILE = os.path.join(os.path.dirname(__file__), "retail_sales.csv")

logger = logging.getLogger(__name__)

def wait_for_influxdb(url, timeout=60):
    start = time.time()
    while time.time() - start < timeout:
        try:
            r = requests.get(url + "/health")
            if r.status_code == 200:
                logger.info("InfluxDB is ready!")
                return True
        except Exception:
            pass
        logger.info("Waiting for InfluxDB to be ready...")
        time.sleep(2)
    raise Exception("InfluxDB did not become ready in time.")

class DataPusher:
    def __init__(self):
        self.client = InfluxDBClient(url=INFLUX_URL, token=INFLUX_TOKEN)
        self.measurement = MEASUREMENT
        self.write_api = self.client.write_api(write_options=SYNCHRONOUS)

    def read_data(self, file_path):
        """
        Read data from a CSV file and return a pandas DataFrame.

        Args:
            file_path (str): The path to the CSV file.

        Returns:
        
        """
        df = pd.read_csv(file_path)
        return df

    def initialize_push_to_db(self):
        """
        Push 40% of data to a database immediately, then append the remaining 60% one row per second.
        """
        df = self.read_data(CSV_FILE)
        df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%y %H:%M')
        n_rows = len(df)
        n_40 = int(0.4 * n_rows)

        logger.info(f"Loaded {n_rows} rows. Pushing first 40% ({n_40} rows)...")

        for index, row in df.iloc[:n_40].iterrows():
            try:
                logger.info(f"[{index+1}] Writing row - Date: {row['Date']}, Sales: {row['Sales']}")
                point = Point(self.measurement).time(row['Date'], WritePrecision.S).field("sales", row['Sales'])
                self.write_api.write(bucket=INFLUX_BUCKET, org=INFLUX_ORG, record=point)
            except Exception as e:
                logger.error(f"[ERROR] Failed to write row {index+1}: {e}")

        logger.info("✅ Finished writing 40%. Now writing 1 row/sec for remaining 60%...")

        for index, row in df.iloc[n_40:].iterrows():
            try:
                logger.info(f"[{index+1}] Writing row - Date: {row['Date']}, Sales: {row['Sales']}")
                point = Point(self.measurement).time(row['Date'], WritePrecision.S).field("sales", row['Sales'])
                self.write_api.write(bucket=INFLUX_BUCKET, org=INFLUX_ORG, record=point)
                time.sleep(1)
            except Exception as e:
                logger.error(f"[ERROR] Failed to write row {index+1}: {e}")

if __name__ == "__main__":
    wait_for_influxdb(INFLUX_URL)
    data_pusher = DataPusher()
    data_pusher.initialize_push_to_db()



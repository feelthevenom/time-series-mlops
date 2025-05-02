import sys
import os
import pandas as pd
from influxdb_client import InfluxDBClient
import warnings
from influxdb_client.client.warnings import MissingPivotFunction
from datetime import datetime, timedelta

# Suppress the missing pivot function warning
warnings.simplefilter("ignore", MissingPivotFunction)

from src.exception.exception import CustomException
from src.logging.logger import logging

from src.entity.artifact_entity import DataingestionArtifact
from src.entity.config_entity import DataIngestionConfig

from sklearn.model_selection import train_test_split

logger = logging.getLogger(__name__)

class DataIngestion:
    def __init__(self, data_ingestion_config: DataIngestionConfig):
        self.data_ingestion_config = data_ingestion_config
        
    def extract_data_from_influxdb(self):
        """
        Extract all historical data from InfluxDB, merge with existing data if needed,
        and return a comprehensive DataFrame with columns 'Date' and 'Sales'.
        """
        try:
            client = InfluxDBClient(
                url=self.data_ingestion_config.influxdb_url,
                token=self.data_ingestion_config.influxdb_token,
                org=self.data_ingestion_config.influxdb_org
            )
            
            # Query for ALL available data
            query = f'''
            from(bucket: "{self.data_ingestion_config.influxdb_bucket}") 
            |> range(start: 0)  
            |> filter(fn: (r) => r["_measurement"] == "{self.data_ingestion_config.influxdb_measurement}") 
            |> filter(fn: (r) => r["_field"] == "{self.data_ingestion_config.influxdb_field}")
            |> keep(columns: ["_time", "_value"])
            '''
            
            query_api = client.query_api()
            result = query_api.query_data_frame(query)
            
            # Handle potentially empty results
            if result is None or (isinstance(result, list) and len(result) == 0):
                logger.warning("Query returned no data from InfluxDB")
                df_new = pd.DataFrame(columns=["Date", "Sales"])
            else:
                # Convert result to DataFrame if it's a list
                df_new = result if isinstance(result, pd.DataFrame) else pd.concat(result)
                
                # Clean up the DataFrame
                if not df_new.empty:
                    # Keep only necessary columns
                    keep_cols = ["_time", "_value"]
                    df_new = df_new[[col for col in keep_cols if col in df_new.columns]]
                    # Rename columns for clarity
                    df_new.rename(columns={"_time": "Date", "_value": "Sales"}, inplace=True)
                    # Ensure correct types
                    df_new["Date"] = pd.to_datetime(df_new["Date"])
                    df_new["Sales"] = pd.to_numeric(df_new["Sales"], errors="coerce")
            
            # Check if there's existing data to merge with
            feature_store_path = self.data_ingestion_config.feature_store_file_path
            df_existing = None
            
            if os.path.exists(feature_store_path) and os.path.getsize(feature_store_path) > 0:
                try:
                    logger.info(f"Loading existing data from {feature_store_path}")
                    df_existing = pd.read_csv(feature_store_path)
                    # Ensure Date column is properly formatted
                    if 'Date' in df_existing.columns:
                        df_existing['Date'] = pd.to_datetime(df_existing['Date'])
                        logger.info(f"Loaded {len(df_existing)} existing records")
                except Exception as e:
                    logger.warning(f"Error reading existing feature store: {str(e)}. Will create new file.")
            
            # Merge existing data with new data if needed
            if df_existing is not None and not df_existing.empty:
                if 'Date' in df_new.columns and not df_new.empty:
                    df_new['Date'] = pd.to_datetime(df_new['Date'])
                df_combined = pd.concat([df_existing, df_new])
                df_combined = df_combined.drop_duplicates(subset=['Date'], keep='last')
                df_combined = df_combined.sort_values('Date')
                logger.info(f"Combined dataset has {len(df_combined)} records")
                df = df_combined
            else:
                df = df_new
                logger.info(f"Using only new data with {len(df)} records")
            
            # Ensure the directory exists before saving
            os.makedirs(os.path.dirname(feature_store_path), exist_ok=True)
            
            # Save DataFrame to CSV
            if not df.empty:
                df.to_csv(feature_store_path, index=False)
                logger.info(f"Feature store file saved at {feature_store_path} with {len(df)} records")
            else:
                pd.DataFrame(columns=["Date", "Sales"]).to_csv(feature_store_path, index=False)
                logger.warning(f"Empty feature store file created at {feature_store_path}")
            
            return df
            
        except Exception as e:
            logger.error(f"Error in extract_data_from_influxdb: {str(e)}")
            raise CustomException(e, sys)

    def split_data_into_train_test(self, df: pd.DataFrame):
        """
        Split the data into train and test sets and save them to the specified paths.
        Handles empty dataframes gracefully. Expects columns 'Date' and 'Sales'.
        """
        try:
            logger.info(f"Splitting data into train and test sets.")
            
            # Check if DataFrame is empty or has insufficient rows for meaningful split
            if df.empty or len(df) < 2:
                logger.warning("DataFrame is empty or has insufficient rows for splitting.")
                if df.empty:
                    columns = ["Date", "Sales"]
                    current_time = datetime.now()
                    dummy_data = {
                        "Date": [current_time - timedelta(days=4),
                                 current_time - timedelta(days=3),
                                 current_time - timedelta(days=2),
                                 current_time - timedelta(days=1),
                                 current_time],
                        "Sales": [0, 0, 0, 0, 0]
                    }
                    fallback_df = pd.DataFrame(dummy_data)
                    logger.warning("Created fallback data for empty dataset")
                    train, test = train_test_split(fallback_df, test_size=0.2, shuffle=False)
                else:
                    fallback_df = pd.concat([df, df])
                    logger.warning("Duplicated single row to allow for data splitting")
                    train, test = train_test_split(fallback_df, test_size=0.2, shuffle=False)
            else:
                train, test = train_test_split(df, test_size=0.2, shuffle=False)
            logger.info(f"Train shape: {train.shape}")
            logger.info(f"Test shape: {test.shape}")
            os.makedirs(self.data_ingestion_config.ingested_data_dir_path, exist_ok=True)
            train.to_csv(self.data_ingestion_config.train_file_path, index=False)
            test.to_csv(self.data_ingestion_config.test_file_path, index=False)
            logger.info("Train and test files saved successfully.")
            return train, test
        except Exception as e:
            logger.error(f"Error in split_data_into_train_test: {str(e)}")
            raise CustomException(e, sys)
    
    def initiate_data_ingestion(self):
        """
        Initiate the data ingestion process.
        This method reads the source data, splits it into train and test sets,
        then returns the path for data validation.
        """
        try:
            # Extract data, merging with existing data if available
            df = self.extract_data_from_influxdb()
            
            # Check if data was retrieved
            if df.empty:
                logger.warning("No data was retrieved from InfluxDB or existing files. Using fallback mechanism.")
            
            # Split data - our improved function handles empty/insufficient DataFrames
            self.split_data_into_train_test(df=df)
            logger.info("Data ingestion completed successfully.")

            # Create and return artifact
            dataingetionartifact = DataingestionArtifact(
                feature_store_path = self.data_ingestion_config.feature_store_file_path,
                train_file_path = self.data_ingestion_config.train_file_path,
                test_file_path = self.data_ingestion_config.test_file_path
            )
            return dataingetionartifact
            
        except Exception as e:
            logger.error(f"Error in initiate_data_ingestion: {str(e)}")
            raise CustomException(e, sys)
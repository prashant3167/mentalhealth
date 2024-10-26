from dagster import resource, InitResourceContext
import pandas as pd
import os
from typing import List

class DbResource:
    def __init__(self):
        self.base_path = os.getenv("DB_PATH") 

    def write_to_parquet(self, data: pd.DataFrame, table: str, partition_cols: List[str] = None):
        """Write a DataFrame to a Parquet file."""
        output_folder = os.path.join(self.base_path, table)
        # output_file = os.path.join(self.base_path, sub_folder, file_name)
        os.makedirs(output_folder, exist_ok=True)
        data.to_parquet(output_folder,partition_cols=partition_cols, index=False, existing_data_behavior='delete_matching')

    def read_from_parquet(self, table: str, partition: List[str] = None) -> pd.DataFrame:
        """Read all DataFrames from Parquet files"""
        # Construct the full path to the sub-folder
        folder_path = os.path.join(self.base_path, table)
        if partition:
            folder_path = folder_path + "/" + partition
        dataframes = pd.read_parquet(folder_path)
        return dataframes




@resource(config_schema={})
def pandas_resource(init_context: InitResourceContext) -> DbResource:
    base_path = os.getenv("DB_PATH") 
    if not os.path.exists(base_path):
        os.makedirs(base_path)

    return DbResource()

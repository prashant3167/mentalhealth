import ray
import pandas as pd
import os
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder, MinMaxScaler
import joblib
BASE_PATH =  "/Users/prashant/project/kaggle/remote_health/"

import sys

def start_ray(dashboard=True):
    """Start Ray cluster

    Args:
        dashboard (bool, optional): Boolean to start the dashboard. Defaults to True.
    """
    ray.init(include_dashboard=dashboard, runtime_env={"working_dir": BASE_PATH}, logging_level = DEBUG)

def shutdown_ray():
    """Shutdown Ray cluster

    """
    ray.shutdown()


def check_file_present(filename):
    return os.path.isfile(filename)

def load_encoder(encoder_path):
    return joblib.load(encoder_path)
    

@ray.remote
def encode_column(column, data):
    """One hot encoding for categorical column

    Args:
        column ([String]): Column name
        data ([Dataframe]): Column data

    Returns:
        [Datframe]: Encodeded Datset
    """

    encoder_path = f"{BASE_PATH}/resources/{column}_encoder.joblib"
    encoder = None
    # print(data.head())
    if check_file_present(encoder_path):
        encoder = load_encoder(encoder_path)
    else:
        encoder = OneHotEncoder(sparse_output=False, drop='first')
        encoder.fit(data[[column]])
        joblib.dump(encoder, encoder_path)
    
    one_hot_encoded = encoder.transform(data[[column]])
    
    encoded_df = pd.DataFrame(one_hot_encoded, columns=[f"{column}_{cat}" for cat in encoder.categories_[0][1:]])

    return encoded_df



@ray.remote
def encode_ordinal_column(column, data, custom_order=None):
    """Ordinal encoding for categorical column with optional custom order.

    Args:
        column (str): Column name to encode.
        data (pd.DataFrame): DataFrame containing the data.
        custom_order (list of list, optional): Custom order for encoding categories.

    Returns:
        pd.DataFrame: Encoded DataFrame with the encoded dataframe.
    """
    
    encoder_path = f"{BASE_PATH}/resources/{column}_encoder.joblib"
    encoder = None
    if custom_order!=None:
        custom_order = [custom_order]

    # https://psycnet.apa.org/record/2018-70020-001
    data[column].fillna(custom_order[0][-1], inplace=True)


    if check_file_present(encoder_path):
        encoder = load_encoder(encoder_path)
    else:
        if custom_order is not None:
            encoder = OrdinalEncoder(categories=custom_order)
        else:
            encoder = OrdinalEncoder()
        
        encoder.fit(data[[column]])
        joblib.dump(encoder, encoder_path)

    encoded_values = encoder.transform(data[[column]])
    # breakpoint()
    encoded_df = pd.DataFrame(encoded_values, columns=[column])

    # encoded_data = pd.concat([data, encoded_df], axis=1)

    return column, encoded_df



@ray.remote
def scale_features(column, data):
    """Ordinal encoding for categorical column with optional custom order.

    Args:
        column (str): Column name to encode.
        data (pd.DataFrame): DataFrame containing the data.
        custom_order (list of list, optional): Custom order for encoding categories.

    Returns:
        pd.DataFrame: Encoded DataFrame with the encoded dataframe.
    """
    
    scaler_path = f"{BASE_PATH}/resources/{column}_scaler.joblib"
    scaler = None



    if check_file_present(scaler_path):
        scaler = load_encoder(scaler_path)
    else:
        scaler = MinMaxScaler(feature_range=(0, 1))
        scaler.fit(data[[column]])
        joblib.dump(scaler, scaler_path)

    encoded_values = scaler.transform(data[[column]])
    # breakpoint()
    encoded_df = pd.DataFrame(encoded_values, columns=[column])

    # encoded_data = pd.concat([data, encoded_df], axis=1)

    return column, encoded_df


# @ray.remote
# def scale_and_save(column_data, column_name, save_path):
#     """Scale a column using Min-Max Scaling and save the scaler."""
#     scaler = MinMaxScaler()
#     scaled_values = scaler.fit_transform(column_data.values.reshape(-1, 1))
    
#     # Save the scaler
#     joblib.dump(scaler, save_path)
    
#     return pd.DataFrame(scaled_values, columns=[column_name])


def read_dataset(path):
    return pd.read_csv(path)


# def fill_na()

def clean_dataset(dataset):
    dataset = dataset[dataset["Age"]-dataset["Years_of_Experience"]>=18]
    return dataset

def encode_categorical_dataset(dataset, features, drop_columns = True):
    futures = [encode_column.remote(column, dataset) for column in features]
    results = ray.get(futures)

    for encoded_df in results:
        # print(encoded_df.head())
        dataset = pd.concat([dataset.reset_index(drop=True), encoded_df.reset_index(drop=True)], axis=1)
    if drop_columns:
        dataset.drop(columns=features, inplace=True)
    return dataset

def encode_ordinal_dataset(dataset, features, drop_columns = True):
    futures = [encode_ordinal_column.remote(column = column, data = dataset, custom_order = custom_order) for column, custom_order in features.items()]
    results = ray.get(futures)
    for column, encoded_df in results:
        dataset[column] = encoded_df
    return dataset



def scale_dataset(dataset, features):
    futures = [scale_features.remote(column = column, data = dataset) for column in features]
    results = ray.get(futures)
    for column, encoded_df in results:
        dataset[column] = encoded_df
    return dataset


# import wandb
import os
import joblib  # For loading the model
import pandas as pd

# # Initialize a new WandB run

# def download_artifactory(name):
#     """ Download artifactory from Weight and Biases
#     """
#     run = wandb.init(project="pacific31-xsor-capital")

#     artifact = run.use_artifact(f"pacific31-xsor-capital/os.getenv('ENV')/{name}:v0")
#     artifact_dir = artifact.download(f"/tmp/")
#     return artifact_dir


def load_encoder(encoder_path):
    return joblib.load(encoder_path)


def encode_categorical_column(column, data):
    """One hot encoding for categorical column
    """
    encoder_path = f"model_resources/{column}_encoder.joblib"
    encoder = load_encoder(encoder_path)
    one_hot_encoded = encoder.transform(data[[column]])
    encoded_df = pd.DataFrame(one_hot_encoded, columns=[f"{column}_{cat}" for cat in encoder.categories_[0][1:]])
    return encoded_df



def encode_ordinal_column(column, data, custom_order=None,context=None):
    """Ordinal encoding for categorical column with optional custom order.

    Args:
        column (str): Column name to encode.
        data (pd.DataFrame): DataFrame containing the data.
        custom_order (list of list, optional): Custom order for encoding categories.

    Returns:
        pd.DataFrame: Encoded DataFrame with the encoded dataframe.
    """
    
    if custom_order!=None:
        custom_order = [custom_order]
        # https://psycnet.apa.org/record/2018-70020-001
        data[column].fillna(custom_order[0][-1], inplace=True)

    encoder_path = f"model_resources/{column}_encoder.joblib"
    encoder = load_encoder(encoder_path)

    encoded_values = encoder.transform(data[[column]])
    # context.log.info(f"{type(encoded_values)}")
    
    encoded_df = pd.DataFrame(encoded_values, columns=[column])
    return encoded_df[column]



def scale_feature(column, data):
    """Ordinal encoding for categorical column with optional custom order.

    Args:
        column (str): Column name to encode.
        data (pd.DataFrame): DataFrame containing the data.
        custom_order (list of list, optional): Custom order for encoding categories.

    Returns:
        pd.Series: Encoded Series
    """
    
    scaler_path = f"model_resources/{column}_scaler.joblib"
    scaler = load_encoder(scaler_path)
    encoded_values = scaler.transform(data[[column]])
    # breakpoint()
    encoded_df = pd.DataFrame(encoded_values, columns=[column])

    # encoded_data = pd.concat([data, encoded_df], axis=1)

    return encoded_df[column]# import wandb
import os
import joblib  # For loading the model
import pandas as pd

# # Initialize a new WandB run

# def download_artifactory(name):
#     """ Download artifactory from Weight and Biases
#     """
#     run = wandb.init(project="pacific31-xsor-capital")

#     artifact = run.use_artifact(f"pacific31-xsor-capital/os.getenv('ENV')/{name}:v0")
#     artifact_dir = artifact.download(f"/tmp/")
#     return artifact_dir


def load_encoder(encoder_path):
    return joblib.load(encoder_path)


def encode_categorical_column(column, data):
    """One hot encoding for categorical column
    """
    encoder_path = f"model_resources/{column}_encoder.joblib"
    encoder = load_encoder(encoder_path)
    one_hot_encoded = encoder.transform(data[[column]])
    encoded_df = pd.DataFrame(one_hot_encoded, columns=[f"{column}_{cat}" for cat in encoder.categories_[0][1:]])
    return encoded_df



def encode_ordinal_column(column, data, custom_order=None,context=None):
    """Ordinal encoding for categorical column with optional custom order.

    Args:
        column (str): Column name to encode.
        data (pd.DataFrame): DataFrame containing the data.
        custom_order (list of list, optional): Custom order for encoding categories.

    Returns:
        pd.DataFrame: Encoded DataFrame with the encoded dataframe.
    """
    
    if custom_order!=None:
        custom_order = [custom_order]
        # https://psycnet.apa.org/record/2018-70020-001
        data[column].fillna(custom_order[0][-1], inplace=True)

    encoder_path = f"model_resources/{column}_encoder.joblib"
    encoder = load_encoder(encoder_path)

    encoded_values = encoder.transform(data[[column]])
    # context.log.info(f"{type(encoded_values)}")
    
    encoded_df = pd.DataFrame(encoded_values, columns=[column])
    return encoded_df[column]



def scale_feature(column, data):
    """Ordinal encoding for categorical column with optional custom order.

    Args:
        column (str): Column name to encode.
        data (pd.DataFrame): DataFrame containing the data.
        custom_order (list of list, optional): Custom order for encoding categories.

    Returns:
        pd.Series: Encoded Series
    """
    
    scaler_path = f"model_resources/{column}_scaler.joblib"
    scaler = load_encoder(scaler_path)
    encoded_values = scaler.transform(data[[column]])
    # breakpoint()
    encoded_df = pd.DataFrame(encoded_values, columns=[column])

    # encoded_data = pd.concat([data, encoded_df], axis=1)

    return encoded_df[column]
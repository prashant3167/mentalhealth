import pandas as pd
from utils.data_processing import load_encoder
import yaml
import os
import xgboost
import numpy as np


def get_prediction(context, features) -> pd.Series:
    with open(
        f'{os.getenv("DAGSTER_MENTAL_PATH")}/config_files/mental_health.yaml'
    ) as f:
        config = yaml.load(f, Loader=yaml.SafeLoader)
        target = config["target"]
    predictor = load_encoder(f"model_resources/{target}_predict.pkl")
    feature_order = predictor.feature_names_in_
    features = features[feature_order]
    predict = predictor.predict(features)
    decoder = load_encoder(f"model_resources/{target}_encoder.joblib")
    if predict.ndim == 1:
        predict = predict.reshape(-1, 1)
    
    predicted_data = decoder.inverse_transform(predict)
    if isinstance(predicted_data, np.ndarray) and predicted_data.ndim == 2:
        predicted_data = predicted_data.flatten() 
    return pd.Series(predicted_data)
            
from dagster import (
    Definitions,
    ScheduleDefinition,
    resource,
    job,
    op,
    Out,
    graph,
    AssetMaterialization,
    MetadataValue,
    Output,
)
from utils.data_processing import (
    encode_categorical_column,
    encode_ordinal_column,
    scale_feature,
)
from utils.predict import get_prediction
from datetime import datetime, timedelta
import pandas as pd
import os
import yaml
from yaml.loader import SafeLoader
from datetime import datetime


def flatten_document(doc):
    """Flatten the document for easy storage in Parquet format."""
    flattened_doc = {}
    for key, value in doc.items():
        if isinstance(value, dict):
            for sub_key, sub_value in value.items():
                flattened_doc[f"{key}.{sub_key}"] = sub_value
        else:
            flattened_doc[key] = value
    return flattened_doc


@op(
    out={"branch_1": Out(is_required=False), "branch_2": Out(is_required=False)},
    required_resource_keys={"mongo", "db"},
)
def pull_data_from_mongo(context):
    """Pull data partition daily"""
    db = context.resources.mongo
    parquet_writer = context.resources.db
    collection = db["medical_responses"]

    created_at_partition = context.partition_key

    created_at_start = datetime.strptime(created_at_partition, "%Y-%m-%d")
    created_at_end = created_at_start + timedelta(days=1)

    context.log.info(f"Date {created_at_start}")

    distinct_companies = collection.distinct(
        "company", {"created_at": {"$gte": created_at_start, "$lt": created_at_end}}
    )

    company_data = {}
    documents = collection.find(
        {
            "created_at": {"$gte": created_at_start, "$lt": created_at_end},
        },
        {"_id": 0},
    )
    form_data = []
    for doc in documents:
        flattened_doc = flatten_document(doc)
        form_data.append(flattened_doc)
    final_df = pd.DataFrame(form_data)

    # Check if DataFrame is empty
    if final_df.empty:
        context.log.info(
            "No data found for the given partition. Marking the run as successful."
        )
        # Stop the run and mark it as successful
        # context.step.success()
        yield Output("No data is created for patitition {context.partition_key}", "branch_2")

    if not final_df.empty:
        final_df["created_date"] = final_df["created_at"].dt.date
        parquet_writer.write_to_parquet(
            final_df, "raw_form_responses", ["company", "created_date"]
        )
        #  return final_df
        yield Output(final_df, "branch_1")


@op(out={"dataframe": Out(is_required=False), "no_data": Out(is_required=False)})
def clean_dataset(context, input_data):
    with open(
        f'{os.getenv("DAGSTER_MENTAL_PATH")}/config_files/mental_health.yaml'
    ) as f:
        data = yaml.load(f, Loader=SafeLoader)
        ordinal_features = list(data["encoding_features"]["ordinal"].keys())
        numerical_features = data["encoding_features"]["numerical"]
        features = numerical_features
    for feature in features:
        input_data[feature] = input_data[feature].astype(int)

    context.log.info(f"features: {features}")

    dataset = input_data[input_data["Age"] - input_data["Years_of_Experience"] >= 18]
    context.log.info(f"Total Dataset: len(input_data)")
    context.log.info(f"Removed Dataset: len(input_data)-len(dataset)")
    if dataset.empty:
        context.log.info(
            "No data found for the given partition. Marking the run as successful."
        )
        # Stop the run and mark it as successful
        # context.step.success()
        yield Output("No data is left after cleaning", "no_data")
    yield Output(dataset, "dataframe")


@op(required_resource_keys={"mongo"})
def process_categorical_data(context, input_data):
    with open(
        f'{os.getenv("DAGSTER_MENTAL_PATH")}/config_files/mental_health.yaml'
    ) as f:
        data = yaml.load(f, Loader=SafeLoader)
        categorical_features = data["encoding_features"]["categorical"]

    context.log.info(f"Processing ordinal data: {input_data}")
    categorical_data = pd.DataFrame()
    for column in categorical_features:
        try:
            encoded_data = encode_categorical_column(column, input_data)
            categorical_data = pd.concat(
                [
                    categorical_data.reset_index(drop=True),
                    encoded_data.reset_index(drop=True),
                ],
                axis=1,
            )
        except:
            pass
    return categorical_data


@op(required_resource_keys={"mongo"})
def process_ordinal_data(context, input_data) -> pd.DataFrame:
    with open(
        f'{os.getenv("DAGSTER_MENTAL_PATH")}/config_files/mental_health.yaml'
    ) as f:
        config = yaml.load(f, Loader=SafeLoader)
        ordinal_features = config["encoding_features"]["ordinal"]
        # if config["target"] in ordinal_features:
        #     ordinal_features.remove(config["target"])

    ordinal_data = pd.DataFrame()
    for column, ordinal_order in ordinal_features.items():
        if column != config["target"]:
            ordinal_data[column] = encode_ordinal_column(
                column, input_data, custom_order=ordinal_order, context=context
            )
    return ordinal_data


@op
def scale_dataset(context, ordinal_data, clean_dataset) -> pd.DataFrame:
    with open(
        f'{os.getenv("DAGSTER_MENTAL_PATH")}/config_files/mental_health.yaml'
    ) as f:
        data = yaml.load(f, Loader=SafeLoader)
        numerical_features = data["encoding_features"]["numerical"]

    scaled_features = pd.DataFrame()
    features = numerical_features + list(ordinal_data.columns)
    for feature in features:
        if feature in ordinal_data.columns:
            scaled_features[feature] = scale_feature(feature, ordinal_data)
        else:
            scaled_features[feature] = scale_feature(feature, clean_dataset)
    return scaled_features


@op
def merge_dataset(context, scale_data, categorical_data, clean_dataset) -> pd.DataFrame:
    """Merge clean dataset for prediction"""
    for feature in scale_data.columns:
        clean_dataset[feature] = scale_data[feature]
    for feature in categorical_data.columns:
        clean_dataset[feature] = categorical_data[feature]
    context.log_event(
        AssetMaterialization(
            asset_key="Final merge dataset",
            description="Clean and scaled data",
            metadata={
                "data_sample": MetadataValue.text(clean_dataset.head().to_json()),
                "columns": list(clean_dataset.columns),
            },
        )
    )
    return clean_dataset


@op(required_resource_keys={"db"})
def feature_selection(context, input_data) -> pd.DataFrame:
    parquet_writer = context.resources.db
    importance_features = parquet_writer.read_from_parquet("feature_importance")
    top_10_features = importance_features.nlargest(10, "Importance")
    input_data = input_data[list(top_10_features["Feature"])]
    return input_data


@op
def predict_satisfaction(context, selected_features) -> pd.Series:
    return get_prediction(context, selected_features)


@op(required_resource_keys={"db"})
def merge_and_write(context, clean_data, prediction) -> pd.DataFrame:
    with open(
        f'{os.getenv("DAGSTER_MENTAL_PATH")}/config_files/mental_health.yaml'
    ) as f:
        data = yaml.load(f, Loader=SafeLoader)
        target = data["target"]
    parquet_writer = context.resources.db
    clean_data[target] = prediction
    cols = [col for col in clean_data.columns if col != target] + [target]
    clean_data = clean_data[cols]
    clean_data["created_date"] = clean_data["created_at"].dt.date
    parquet_writer.write_to_parquet(
        clean_data, "predicted_mental_satisfaction", ["company", "created_date"]
    )
    return clean_data



@op
def mark_skip(context, message) -> str:
    context.log.info(message)
    return message

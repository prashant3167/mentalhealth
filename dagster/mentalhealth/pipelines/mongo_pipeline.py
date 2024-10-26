from dagster import (
    graph,
    job,
    DailyPartitionsDefinition,
)
from resources.resources import (
    pull_data_from_mongo,
    process_ordinal_data,
    process_categorical_data,
    clean_dataset,
    process_categorical_data,
    process_ordinal_data,
    scale_dataset,
    merge_dataset,
    feature_selection,
    predict_satisfaction,
    merge_and_write,
    mark_skip
)

created_at_partitions = DailyPartitionsDefinition(start_date="2024-10-04")


@graph
def mongo_pipeline_with_parallel_ops():
    mongo_data, no_data = pull_data_from_mongo()
    clean_data_received, no_data = clean_dataset(mongo_data)
    ordinal_data = process_ordinal_data(clean_data_received)
    categorical_data = process_categorical_data(clean_data_received)
    scaled_data = scale_dataset(ordinal_data, clean_data_received)
    merged_data = merge_dataset(scaled_data, categorical_data, clean_data_received)
    selected_features = feature_selection(merged_data)
    predicted_data = predict_satisfaction(selected_features)
    merge_and_write(clean_data_received, predicted_data)
    # return predicted_data
    mark_skip(no_data)


@job(partitions_def=created_at_partitions)
def mongo_partitioned_job():
    mongo_pipeline_with_parallel_ops()

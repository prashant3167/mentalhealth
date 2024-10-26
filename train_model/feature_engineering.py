import pandas as pd
from sklearn.model_selection import train_test_split
from utils import (
    start_ray,
    shutdown_ray,
    read_dataset,
    clean_dataset,
    encode_categorical_dataset,
    encode_ordinal_dataset,
    scale_dataset,
)
from config import (
    numerical_features,
    one_hot_encoding_features,
    ordinal_encoding_features,
)
from sklearn.ensemble import RandomForestClassifier


model = RandomForestClassifier()


def start_process(
    numerical_features, one_hot_encoding_features, ordinal_encoding_features
):
    start_ray(dashboard=True)
    target = "Satisfaction_with_Remote_Work"
    dataset = read_dataset("data/Impact_of_Remote_Work_on_Mental_Health.csv")

    # Step 1: Clean Dataset
    dataset = clean_dataset(dataset=dataset)

    # Step 2: Encode Categorical data
    dataset = encode_categorical_dataset(
        dataset=dataset, features=one_hot_encoding_features
    )
    # Step 3: Encode Ordinal data
    dataset = encode_ordinal_dataset(
        dataset=dataset, features=ordinal_encoding_features
    )
    # Step 4: Scale features
    numerical_features = numerical_features + list(ordinal_encoding_features.keys())
    numerical_features.remove(target)

    dataset = scale_dataset(
        dataset=dataset, features=numerical_features + list(numerical_features)
    )
    dataset[target] = dataset[target].astype(int)

    dataset.to_csv("processed_data.csv")

    dataset.drop(columns=["Employee_ID"], inplace=True)
    features = dataset.drop(target, axis=1).columns
    Y = dataset[target].values
    X = dataset.drop(target, axis=1).values

    x_train, x_test, y_train, y_test = train_test_split(
        X, Y, random_state=42, test_size=0.2
    )

    model.fit(x_train, y_train)

    importances = model.feature_importances_
    feature_importance_df = pd.DataFrame(
        {"Feature": features, "Importance": importances}
    )
    feature_importance_df = feature_importance_df.sort_values(
        by="Importance", ascending=False
    )

    print(feature_importance_df)
    feature_importance_df.to_parquet(
        "persistent_db/feature_importance/importance.parquet"
    )


if __name__ == "__main__":
    start_process(
        numerical_features, one_hot_encoding_features, ordinal_encoding_features
    )

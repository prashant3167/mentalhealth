import wandb
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.svm import SVC
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib


import argparse


# Argument parser
parser = argparse.ArgumentParser(
    description="Check Model with sweep and get the best model"
)

parser.add_argument(
    "--check_model",
    action="store_true",
    help="Use Sweep configuration to check different model",
)
parser.add_argument(
    "--count", help="Configurations want to try", type=int, choices=range(5, 10)
)
parser.add_argument(
    "--train_best_model", action="store_true", help="Train and persist best model"
)

args = parser.parse_args()


sweep_config = {
    "method": "random",
    "metric": {"name": "accuracy", "goal": "maximize"},
    "parameters": {
        "model": {"values": ["RandomForestClassifier", "XGBoostClassifier", "SVC"]},
        "n_estimators": {"values": [50, 100, 200]},
        "max_depth": {"values": [5, 10, 20, None]},
        "min_samples_split": {"values": [2, 5, 10]},
    },
    "additional_metrics": [
        {"name": "r2_score", "goal": "maximize"},
        {"name": "mae", "goal": "minimize"},
        {"name": "mse", "goal": "minimize"},
        {"name": "accuracy", "goal": "maximize"},
    ],
}
project = "medical_health"

sweep_id = wandb.sweep(sweep_config, project=project)


class ModelTraining:
    def __init__(self, file_position, target, index_col=None):
        """Training class"""
        self.data = pd.read_csv(file_position)
        drop_cols = [target, index_col] if index_col is not None else [target]
        self.X = self.data.drop(drop_cols, axis=1)
        self.Y = self.data[target]
        self.features = self.X.columns

        important_features = pd.read_parquet("persistent_db/feature_importance")
        top_10_features = important_features.nlargest(10, "Importance")
        self.X = self.X[list(top_10_features["Feature"])]
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            self.X, self.Y, random_state=42, test_size=0.2
        )

    def train(self):
        wandb.init()

        config = wandb.config
        run_name = f"model-{config.model}"
        wandb.run.name = run_name

        if config.model == "RandomForestClassifier":
            model = RandomForestClassifier(
                n_estimators=config.n_estimators,
                max_depth=config.max_depth,
                min_samples_split=config.min_samples_split,
            )
        elif config.model == "XGBoostClassifier":
            model = XGBClassifier(
                n_estimators=config.n_estimators, max_depth=config.max_depth
            )
        elif config.model == "SVC":
            model = SVC()

        # Train the model
        model.fit(self.X_train, self.y_train)

        # Evaluate model
        acc = model.score(self.X_test, self.y_test)
        wandb.log({"accuracy": acc})

        y_pred = model.predict(self.X_test)

        mae = mean_absolute_error(self.y_test, y_pred)
        mse = mean_squared_error(self.y_test, y_pred)
        r2 = r2_score(self.y_test, y_pred)

        wandb.log({"mae": mae, "mse": mse, "r2_score": r2})

        # Log feature importance if applicable
        if hasattr(model, "feature_importances_"):
            importance = model.feature_importances_
            feature_importance = {
                self.features[i]: importance[i] for i in range(len(importance))
            }
            wandb.log({"feature_importance": feature_importance})

        wandb.finish()


def create_best_model(best_config, X, Y):
    best_model = best_config["model"]
    if best_model == "RandomForestClassifier":
        best_model = RandomForestClassifier(
            n_estimators=best_config["n_estimators"],
            max_depth=best_config["max_depth"],
            min_samples_split=best_config["min_samples_split"],
        )
    elif best_model == "XGBoostClassifier":
        best_model = XGBClassifier(
            n_estimators=best_config["n_estimators"], max_depth=best_config["max_depth"]
        )
    elif best_model == "SVC":
        best_model = SVC()

    best_model.fit(X, Y)

    joblib.dump(best_model, "resources/Satisfaction_with_Remote_Work_predict.pkl")
    print(f"Model created : {'resources/Satisfaction_with_Remote_Work_predict.pkl'}")


def get_best_config(project):
    api = wandb.Api()

    runs = api.runs(f"pacific31-xsor-capital/{project}")

    run_data = []
    for run in runs:
        if run.state == "finished":
            run_data.append(
                {
                    "id": run.id,
                    "name": run.name,
                    "accuracy": run.summary.get("accuracy"),
                    "mae": run.summary.get("mae"),
                    "mse": run.summary.get("mse"),
                    "r2_score": run.summary.get("r2_score"),
                    "config": run.config,
                }
            )

    sorted_run_data = sorted(run_data, key=lambda x: x["accuracy"], reverse=True)

    best_config = sorted_run_data[0]["config"]
    return best_config


config = get_best_config(project=project)
create_best_model(config, mt.X, mt.Y)


if __name__ == "__main__":

    mt = ModelTraining(
        file_position="data/processed_data.csv",
        target="Satisfaction_with_Remote_Work",
        index_col="Employee_ID",
    )
    if args.check_model:
        wandb.agent(sweep_id, function=mt.train, count=args.count)
    if args.train_best_model:
        config = get_best_config(project=project)
        create_best_model(config, mt.X, mt.Y)

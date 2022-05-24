import argparse
import pandas as pd
import time
import mlflow
from mlflow.models.signature import infer_signature
from sklearn.model_selection import train_test_split 
from sklearn.preprocessing import  StandardScaler, FunctionTransformer, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline


if __name__ == "__main__":

    ### MLFLOW Experiment setup
    experiment_name="car_rental_price"
    mlflow.set_experiment(experiment_name)
    experiment = mlflow.get_experiment_by_name(experiment_name)

    client = mlflow.tracking.MlflowClient()
    run = client.create_run(experiment.experiment_id)

    print("Start training model")
    
    # Time execution
    start_time = time.time()

    # Call mlflow autolog
    mlflow.sklearn.autolog(log_models=False) # We won't log models right away

    # Parse arguments given in shell script
    parser = argparse.ArgumentParser()
    parser.add_argument("--n_estimators")
    parser.add_argument("--min_samples_split")
    args = parser.parse_args()

    # Import dataset
    df = pd.read_csv("https://full-stack-assets.s3.eu-west-3.amazonaws.com/Deployment/get_around_pricing_project.csv", index_col=0)

    # X, y split 
    X = df.iloc[:, 0:-1]
    y = df.iloc[:, -1]

    # Train / test split 
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2)

    # Preprocessing
    categorical_features = [
        "model_key",
        "fuel",
        "paint_color",
        "car_type",
        "private_parking_available",
        "has_gps",
        "has_air_conditioning",
        "automatic_car",
        "has_getaround_connect",
        "has_speed_regulator",
        "winter_tires"
    ] # Columns containing strings or booleans
    categorical_transformer = OneHotEncoder(drop='first', handle_unknown='error', sparse=False)

    numerical_feature_mask = X_train.columns.isin(
        [
            "mileage",
            "engine_power"
        ]) # Columns containing ints
    numerical_features = X_train.columns[numerical_feature_mask]
    numerical_transformer = StandardScaler()

    feature_preprocessor = ColumnTransformer(
        transformers=[
            ("categorical_transformer", categorical_transformer, categorical_features),
            ("numerical_transformer", numerical_transformer, numerical_features)
        ]
    )

    # Pipeline 
    n_estimators = int(args.n_estimators)
    min_samples_split=int(args.min_samples_split)

    model = Pipeline(steps=[
        ('features_preprocessing', feature_preprocessor),
        ("Regressor",RandomForestClassifier(n_estimators=n_estimators, min_samples_split=min_samples_split))
    ])

    # Log experiment to MLFlow
    with mlflow.start_run(run_id = run.info.run_id) as run:
        model.fit(X_train, y_train)
        predictions = model.predict(X_train)

        # Log model seperately to have more flexibility on setup 
        mlflow.sklearn.log_model(
            sk_model=model,
            artifact_path=experiment_name,
            registered_model_name=f"Random_Forest_{experiment_name}",
            signature=infer_signature(X_train, predictions)
        )
        
    print(f"Training completed in {time.time()-start_time}")
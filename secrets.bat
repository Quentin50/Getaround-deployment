:: DO NOT PUSH to any repository
:: This is a sample file to store your secret keys

:: Set secrets available in other windows
SETX MLFLOW_EXPERIMENT_ID "secret_here"
SETX MLFLOW_TRACKING_URI "secret_here"
SETX AWS_ACCESS_KEY_ID "secret_here"
SETX AWS_SECRET_ACCESS_KEY "secret_here"
SETX BACKEND_STORE_URI "secret_here"
SETX ARTIFACT_ROOT "secret_here"

echo "Do not close this windows to keep secrets active. "
pause

:: Overrides secrets
SETX MLFLOW_EXPERIMENT_ID ""
SETX MLFLOW_TRACKING_URI ""
SETX AWS_ACCESS_KEY_ID ""
SETX AWS_SECRET_ACCESS_KEY """
SETX BACKEND_STORE_URI ""
SETX ARTIFACT_ROOT ""

echo "Secrets deleted. "
pause
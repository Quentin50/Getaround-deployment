import mlflow
from xmlrpc.client import Boolean
import uvicorn
import pandas as pd 
from pydantic import BaseModel
from typing import Literal, List
from fastapi import FastAPI
import json

description = """
GetAround API helps you learn more about GetAround rentals.

GetAround is a company that allows car owners to rent their cars to customers. Sometimes a customer might be late to checkout and the next customer might have to wait to checkin. It leads to cancellations, have a negative impact on the company revenues and image. The goal of this project is to be able to anticipate late checkouts, and evaluate the impact of some measures on car owners revenues.
## Preview

* `/preview` a few rows of your dataset

## Machine Learning

* `/predict` the rental price per day for the given car(s).


Check out documentation for more information on each endpoint.
"""

tags_metadata = [
    {
        "name": "Data",
        "description": "Functions related directly to the data",
    },

    {
        "name": "Machine Learning",
        "description": "Functions related to Machine Learning"
    },
]

app = FastAPI(
    title="GetAround API",
    description=description,
    version="1.0",
    contact={
        "name": "GetAround API - GitHub Quentin50",
        "url": "https://github.com/Quentin50",
    },
    openapi_tags=tags_metadata
)

# Define features used in machine learning
class PredictionFeatures(BaseModel):
    model_key: str
    mileage: int
    engine_power: int
    fuel: str
    paint_color: str
    car_type: str
    private_parking_available: Boolean
    has_gps: Boolean
    has_air_conditioning: Boolean
    automatic_car: Boolean
    has_getaround_connect: Boolean
    has_speed_regulator: Boolean
    winter_tires: Boolean

# Preview a few rows of the dataset
@app.get("/preview", tags=["Preview"])
async def random_car(rows: int=10):
    """
    Get a sample of the dataset.
    You can specify the number of rows returned with `rows`, default is `10`
    """
    print("/preview called")
    df = pd.read_csv("data/get_around_pricing_project.csv")
    sample = df.sample(rows)
    return sample.to_json()

# Predict the rental price for the given cars
@app.post("/predict", tags=["Machine-Learning"])
async def predict(predictionFeatures: PredictionFeatures):
    """
    Predict the rental price per day for one given car. Returns a dictionnary:

    ```
    {'prediction': PREDICTION_VALUE}
    ```

    All columns values are needed, as dictionnary or form data.
    """
    print("/predict called")
    # Read data 
    df = pd.DataFrame(dict(predictionFeatures), index=[0])

    # Log model from mlflow
    logged_model = 'runs:/96559a23cafb417c99d8047ec6a9f622/car_rental_price'

    # Load model as a PyFuncModel.
    loaded_model = mlflow.pyfunc.load_model(logged_model)
    prediction = loaded_model.predict(df)

    # Format response
    response = {"prediction": prediction.tolist()[0]}
    return response

if __name__=="__main__":
    uvicorn.run(app, host="0.0.0.0", port=4000, debug=True, reload=True)
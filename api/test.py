import requests 
import json
import pandas as pd 

# Test prediction endpoint
def test_prediction():
    car_0 = \
{
  "model_key": "BMW",
  "mileage": 86425,
  "engine_power": 190,
  "fuel": "diesel",
  "paint_color": "silver",
  "car_type": "suv",
  "private_parking_available": False,
  "has_gps": True,
  "has_air_conditioning": False,
  "automatic_car": False,
  "has_getaround_connect": False,
  "has_speed_regulator": False,
  "winter_tires": True
}

    response = requests.post(
        "http://localhost:4000/predict",
        data=json.dumps(car_0)
    )

    print(f"post: {car_0}")
    print(f"   response: {response}")

test_prediction()

def test_prediction2():

    df = pd.read_csv("https://full-stack-assets.s3.eu-west-3.amazonaws.com/Deployment/get_around_pricing_project.csv", index_col=0)
    df = df.sample(1)
    values = []
    for element in df.iloc[0,:].values.tolist():
        if type(element) != str:
            values.append(element.item())
        else:
            values.append(element)
    df_dict = {key:value for key, value in zip(df.columns, values)}

    response = requests.post(
        "http://localhost:4000/predict",
        data=json.dumps(df_dict)
    )

    print(f"post: {df_dict}")
    print(f"   response: {response}")

test_prediction2()
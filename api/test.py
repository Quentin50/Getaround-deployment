import requests 
import json
import pandas as pd 

# Test prediction endpoint localy with a random sample
def test_prediction_2():

    # import data
    df = pd.read_csv("https://full-stack-assets.s3.eu-west-3.amazonaws.com/Deployment/get_around_pricing_project.csv", index_col=0)
    df = df.sample(1)
    values = []

    # Create the sample dict
    for element in df.iloc[0,:].values.tolist():
        if type(element) != str:
            values.append(element.item())
        else:
            values.append(element)
    df_dict = {key:value for key, value in zip(df.columns, values)}

    # post localy
    response = requests.post(
        "http://localhost:4000/predict", # replace with any url to test online api
        data=json.dumps(df_dict)
    )

    print(f"post: {df_dict}")
    print(f"   response: {response}")

test_prediction_2()
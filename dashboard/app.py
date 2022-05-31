import streamlit as st
import pandas as pd
import plotly.express as px 
import plotly.graph_objects as go
import numpy as np
from datetime import datetime
import openpyxl

### Config
st.set_page_config(
    page_title="GetAround Dashboard",
    page_icon="🚗",
    layout="wide"
)

# Where to download data
DATA_URL = ('https://full-stack-assets.s3.eu-west-3.amazonaws.com/Deployment/get_around_delay_analysis.xlsx')

### App
# Everything will be printed lineraly on the dashboard
st.title("GetAround Dashboard")

st.markdown("""
    Data analysis concerning the late returns of cars and its impacts on users and business. This dashboard was created by Quentin Gottafray.
""")

st.markdown("---")

# Use `st.cache` to put data in cache
# Data will not be reloaded each time the app is refreshed
@st.cache
def load_data(nrows=''):
    data = pd.DataFrame()
    if(nrows == ''):
        data = pd.read_excel(DATA_URL)
    else:
        data = pd.read_excel(DATA_URL,nrows=nrows)

    # We consider that a negative delay_at_checkout_in_minutes means that the vehicule was returned in advance.
    # Therefore the vehicule was retuned in time, so we set negative values to 0
    data["delay_at_checkout_in_minutes"] = data["delay_at_checkout_in_minutes"].apply(lambda x: 0 if x < 0 else x)

    return data

data_load_state = st.text('Loading data...')
data = load_data()
data_load_state.text("") # change text from "Loading data..." to "" once the the load_data function has run

# Markdown explanations
st.subheader("About the data")
st.markdown(f"""
    The data is a sample of **{data["rental_id"].size}** rental records. Let's take a look at the proportion of late returns.
""")
# Graph showing the late checkouts proportions
fig = px.histogram(
    data["delay_at_checkout_in_minutes"].apply(lambda x: "Late" if x > 0 else "In time or in advance").rename("Late checkouts"),
    x="Late checkouts"
    )
st.plotly_chart(fig)

st.markdown("""
    Focusing only on late returns, here is the repartition of delay at checkout.
""")
# Graph showing the time passed in minutes before a late checkout
fig = px.histogram(
    data[
        (data["delay_at_checkout_in_minutes"] > 0) &
        (data["delay_at_checkout_in_minutes"] < 1000)
    ]["delay_at_checkout_in_minutes"].rename("Delay at checkout in minutes"),
    x="Delay at checkout in minutes")
st.plotly_chart(fig, use_container_width=True)

### Focus on chained rentals
st.subheader("Chained rentals")

# Join the table with itself to add info about the previous rental on each row
data_chain = pd.merge(data, data, how='inner', left_on = 'previous_ended_rental_id', right_on = 'rental_id')
data_chain = data_chain.drop(
    [
        "delay_at_checkout_in_minutes_x",
        "rental_id_y", 
        "car_id_y", 
        "time_delta_with_previous_rental_in_minutes_y",
        "previous_ended_rental_id_y"
    ], 
    axis=1
)
data_chain.columns = [
    'rental_id',
    'car_id',
    'checkin_type',
    'state',
    'previous_ended_rental_id',
    'time_delta_with_previous_rental_in_minutes',
    'prev_rent_checkin_type',
    "prev_rent_state",
    'prev_rent_delay_at_checkout_in_minutes',
]

# Remove rows where prev_rent_delay_at_checkout_in_minutes is NaN
data_chain = data_chain[~data_chain["prev_rent_delay_at_checkout_in_minutes"].isnull()]

## Delayed checkins count
chained_rentals_nb = data_chain["rental_id"].size
st.markdown(f"""
    Now let's focus on chained rentals. Two rentals are chained if the car is used by two different users in a short period of time.
    In this case the late checkout of a customer may or may not impact the next customer's checkin. 
    
    There are **{chained_rentals_nb}** usable cases of chained rentals in the data (rental neither canceled nor has a missing "delay_at_checkout" value).
""")
# Tag rows where the checkin was delayed because of a late return
data_chain["delay_at_checkin"] = (data_chain["time_delta_with_previous_rental_in_minutes"] - data_chain["prev_rent_delay_at_checkout_in_minutes"]).apply(lambda x: x if x > 0 else 0)
data_chain["delayed_checkin"] = data_chain["delay_at_checkin"].apply(lambda x: "Delayed" if x > 0 else "In time")

fig = px.histogram(
    data_chain["delayed_checkin"].rename("Delayed checkins"),
    x="Delayed checkins"
    )
st.plotly_chart(fig)

## Delayed checkins time
pb_in_data = data_chain["delayed_checkin"].value_counts()["Delayed"]
st.markdown(f"""
    There are **{pb_in_data}** problematic cases of chained rentals. Let's visualise how much the checkins were delayed.
""")
## 3 Graphs showing delay at checkin (total, and segmented less and more than 90min)
fig = px.histogram(
    data_chain[data_chain["delay_at_checkin"] > 0]["delay_at_checkin"].rename("Delay at checkin in minutes"),
    x="Delay at checkin in minutes")
st.plotly_chart(fig, use_container_width=True)
col1, col2 = st.columns(2)
with col1:
    fig = px.histogram(
        data_chain[(data_chain["delay_at_checkin"] > 0) & (data_chain["delay_at_checkin"] <= 100)]["delay_at_checkin"].rename("Delay at checkin in minutes (less than 100min)"),
        x="Delay at checkin in minutes (less than 100min)")
    st.plotly_chart(fig)
with col2:
    fig = px.histogram(
        data_chain[data_chain["delay_at_checkin"] > 100]["delay_at_checkin"].rename("Delay at checkin in minutes (more than 100min)"),
        x="Delay at checkin in minutes (more than 100min)")
    st.plotly_chart(fig)
st.markdown(f"""
    Note that the observed pics may come from the way the data was gathered, rather than a customer habits to be late of exactly multiples of 30min. Further investigations would be needed to conclude.
""")

### Threshold: minimum time between two rentals
st.subheader("Threshold testing")

## Reference
st.markdown(f"""
    Use the form below to apply different minimum delays between two rentals and visualise its effect on data.

    As a reference, without threshold there are:
    - **{pb_in_data}** problematic cases
    - **{chained_rentals_nb}** chained rentals in total
""")

## Threshold form
with st.form("threshold_testing"):
    threshold = st.number_input("Threshold in minutes", min_value = 0, step = 1)
    checkin_type = st.selectbox("Checkin types", ["Mobile and Connect", "Connect only", "Mobile only"])
    submit = st.form_submit_button("Apply")

    if submit:
        # Focus only on the selected checkin type
        data_chain_all = data_chain.iloc[:,:]
        if checkin_type == "Connect only":
            data_chain_all = data_chain_all[data_chain_all["checkin_type"] == "connect"]
        elif checkin_type == "Mobile only":
            data_chain_all = data_chain_all[data_chain_all["checkin_type"] == "mobile"]

        # Number of solved pb
        pb_solved = 0
        try:
            pb_solved = data_chain_all[data_chain_all["delayed_checkin"] == "Delayed"]["delay_at_checkin"].apply(lambda x: "Delayed" if x > threshold else "In time").value_counts()["In time"]
        except:
            pb_solved = 0 # there were no "In time" chekin

        # Number of affected cases
        affected_cases = 0
        try:
            affected_cases = data_chain_all["time_delta_with_previous_rental_in_minutes"].apply(lambda x: "Affected" if x < threshold else "Not affected").value_counts()["Affected"]
        except:
            affected_cases = 0 # there were no "Affected" rental
        st.markdown(f"""
            With a threshold of **{threshold}**min on **{checkin_type}** there are:
            - **{pb_solved}** problematic cases solved ({round(pb_solved/pb_in_data*100, 1)}% solved)
            - **{affected_cases}** affected rentals ({round(affected_cases/chained_rentals_nb*100, 1)}% of all rentals)
        """)
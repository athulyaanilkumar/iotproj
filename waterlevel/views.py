from django.shortcuts import render
import numpy as np
from datetime import datetime
from datetime import datetime
import requests 
import pandas as pd

from sklearn.linear_model import LinearRegression
import datetime

# from your_app_name.models import waterlevel  # Import your model if you had an app

def predict_exceed_time_view(request):
    read_api_key = 'I40GCLXRCZ7PIQP3'
    channel_id = '2568147'

    # Fetch data from ThingSpeak
    url = f'https://api.thingspeak.com/channels/{channel_id}/fields/1.json?api_key={read_api_key}&results=8000'
    response = requests.get(url)
    data = response.json()

    # Parse data
    feeds = data['feeds']
    df = pd.DataFrame(feeds)
    df['field1'] = pd.to_numeric(df['field1'])
    df['created_at'] = pd.to_datetime(df['created_at'])
    df.dropna(inplace=True)

    df['time_diff'] = (df['created_at'] - df['created_at'].min()).dt.total_seconds()
    X = df[['time_diff']].values
    y = df['field1'].values

    # Train the model
    model = LinearRegression()
    model.fit(X, y)

    # Predict the time when water level will exceed 7cm
    threshold = 7.0
    time_to_threshold = (threshold - model.intercept_) / model.coef_[0]
    exceed_time = df['created_at'].min() + datetime.timedelta(seconds=time_to_threshold)


    return render(request, 'exceed_time.html', {'exceed_time': exceed_time})
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import LinearRegression
from sklearn.svm import SVR
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split, GridSearchCV
import requests
import cloudscraper
import numpy as np
import warnings
from src import cprint
warnings.filterwarnings("ignore") 

def get_points():
    try:
        scraper = cloudscraper.CloudScraper()
        response = scraper.get("https://api.bloxflip.com/games/crash")
        response.raise_for_status()
        data = response.json()
        crash_points = [point["crashPoint"] for point in data["history"][:20]]
        return crash_points
    except requests.RequestException as e:
        cprint.error(f"Failed to get crash points: {e}")
        return None

def prepare_data(crash_points):
    df = pd.DataFrame({'Crash Point': crash_points})
    df['Time Step'] = range(len(df))
    df['Lagged_1'] = df['Crash Point'].shift(1).bfill()
    df['Lagged_2'] = df['Crash Point'].shift(2).bfill()
    df['Lagged_3'] = df['Crash Point'].shift(3).bfill()
    df['Rolling_Mean_3'] = df['Crash Point'].rolling(window=3, center=True).mean().bfill()
    df['Rolling_Mean_5'] = df['Crash Point'].rolling(window=5, center=True).mean().bfill()

    df.fillna(method='bfill', inplace=True)
    df.fillna(method='ffill', inplace=True)

    scaler = MinMaxScaler()
    features = ['Time Step', 'Lagged_1', 'Lagged_2', 'Lagged_3', 'Rolling_Mean_3', 'Rolling_Mean_5']
    df[features] = scaler.fit_transform(df[features])

    return df, scaler, features

def train_and_predict(df, model_type='linear', scaler=None, features=None):
    X_train, X_test, y_train, y_test = train_test_split(
        df[features],
        df['Crash Point'],
        test_size=0.3, random_state=42
    )

    if model_type == 'linear':
        model = LinearRegression()
    elif model_type == 'svr':
        param_grid = {'C': [1, 10, 100], 'gamma': ['scale', 'auto'], 'kernel': ['rbf', 'linear']}
        model = GridSearchCV(SVR(), param_grid, cv=5)
    elif model_type == 'random_forest':
        param_grid = {'n_estimators': [50, 100, 200], 'max_depth': [None, 10, 20]}
        model = GridSearchCV(RandomForestRegressor(random_state=42), param_grid, cv=5)
    else:
        raise ValueError("Invalid model_type. Choose 'linear', 'svr', or 'random_forest'.")

    model.fit(X_train, y_train)

    if hasattr(model, 'best_estimator_'):
        model = model.best_estimator_

    next_time_step = len(df)
    prediction_df = pd.DataFrame({
        'Time Step': [next_time_step],
        'Lagged_1': df['Crash Point'].iloc[-1],
        'Lagged_2': df['Crash Point'].iloc[-2],
        'Lagged_3': df['Crash Point'].iloc[-3],
        'Rolling_Mean_3': df['Rolling_Mean_3'].iloc[-1],
        'Rolling_Mean_5': df['Rolling_Mean_5'].iloc[-1]
    })

    prediction_df = scaler.transform(prediction_df)
    predicted_crash_point = model.predict(prediction_df)
    predicted_crash_point = predicted_crash_point[0]
    predicted_crash_point = max(predicted_crash_point, 1.0)
    
    return predicted_crash_point

def crash(model_type):
    crash_points = get_points()
    if crash_points:
        df, scaler, features = prepare_data(crash_points)
        prediction = train_and_predict(df, model_type, scaler, features)
        return prediction
    return 1.01

def slides():
    with requests.Session() as session:
        with session.post("https://aspectiser.vercel.app/slides") as response:
            if response.status_code == 200:
                data = response.json()
                return data.get("a")
            else:
                return None

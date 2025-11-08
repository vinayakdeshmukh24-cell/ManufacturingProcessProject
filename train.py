import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib

def load_and_preprocess_data():
    # Load the data
    df = pd.read_csv('machining_time_dataset.csv')
    
    # Separate features and target
    X = df.drop('Machining_Time_sec', axis=1)
    y = df['Machining_Time_sec']
    
    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Scale numeric features
    numeric_cols = ['Spindle_Speed_rpm', 'Feed_mm_per_rev', 'Depth_of_Cut_mm', 'Machining_Length_mm']
    scaler = StandardScaler()
    X_train[numeric_cols] = scaler.fit_transform(X_train[numeric_cols])
    X_test[numeric_cols] = scaler.transform(X_test[numeric_cols])
    
    return X_train, X_test, y_train, y_test, scaler

def train_model(X_train, y_train):
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    return model

def evaluate_model(model, X_test, y_test):
    predictions = model.predict(X_test)
    
    mae = mean_absolute_error(y_test, predictions)
    mse = mean_squared_error(y_test, predictions)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test, predictions)
    
    print("\nModel Performance Metrics:")
    print(f"Mean Absolute Error: {mae:.2f} seconds")
    print(f"Root Mean Squared Error: {rmse:.2f} seconds")
    print(f"R² Score: {r2:.3f}")

def save_model(model, scaler):
    joblib.dump(model, 'machining_model.joblib')
    joblib.dump(scaler, 'scaler.joblib')
    print("\nModel and scaler saved successfully!")

def main():
    print("Loading and preprocessing data...")
    X_train, X_test, y_train, y_test, scaler = load_and_preprocess_data()
    
    print("Training model...")
    model = train_model(X_train, y_train)
    
    print("Evaluating model...")
    evaluate_model(model, X_test, y_test)
    
    print("Saving model...")
    save_model(model, scaler)

if __name__ == "__main__":
    main()
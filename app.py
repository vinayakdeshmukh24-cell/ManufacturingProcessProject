import streamlit as st
import pandas as pd
import numpy as np
import joblib
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor

# Constants
N_RANGE = (500, 3000)
F_RANGE = (0.05, 0.5)
D_RANGE = (0.2, 3.0)
L_RANGE = (10, 300)

MATERIALS = ["Mild Steel", "Cast Iron", "Brass"]
TOOLS = ["HSS", "Carbide", "Coated Carbide"]
OPERATIONS = ["Turning", "Milling"]

def load_model():
    try:
        model = joblib.load('machining_model.joblib')
        scaler = joblib.load('scaler.joblib')
        return model, scaler
    except:
        return None, None

def main():
    st.title("⚙️ Machining Time Predictor")
    st.write("Enter machining parameters to predict the machining time")

    col1, col2 = st.columns(2)

    with col1:
        spindle_speed = st.number_input("Spindle Speed (rpm)", 
                                      min_value=N_RANGE[0], 
                                      max_value=N_RANGE[1],
                                      value=1000)
        
        feed_rate = st.number_input("Feed Rate (mm/rev)",
                                  min_value=F_RANGE[0],
                                  max_value=F_RANGE[1],
                                  value=0.2,
                                  step=0.01)
        
        depth_of_cut = st.number_input("Depth of Cut (mm)",
                                     min_value=D_RANGE[0],
                                     max_value=D_RANGE[1],
                                     value=1.0,
                                     step=0.1)

    with col2:
        length = st.number_input("Machining Length (mm)",
                               min_value=L_RANGE[0],
                               max_value=L_RANGE[1],
                               value=100)
        
        material = st.selectbox("Material", MATERIALS)
        tool_type = st.selectbox("Tool Type", TOOLS)
        operation = st.selectbox("Operation", OPERATIONS)

    if st.button("Predict Machining Time"):
        model, scaler = load_model()
        
        if model is None:
            st.error("Model not found. Please train the model first using train.py")
            return

        # Create DataFrame with all features in correct order
        feature_data = {
            'Spindle_Speed_rpm': [spindle_speed],
            'Feed_mm_per_rev': [feed_rate],
            'Depth_of_Cut_mm': [depth_of_cut],
            'Machining_Length_mm': [length],
            'Operation_Milling': [1 if operation == "Milling" else 0],
            'Operation_Turning': [1 if operation == "Turning" else 0],
            'Material_Brass': [1 if material == "Brass" else 0],
            'Material_Cast Iron': [1 if material == "Cast Iron" else 0],
            'Material_Mild Steel': [1 if material == "Mild Steel" else 0],
            'Tool_Type_Carbide': [1 if tool_type == "Carbide" else 0],
            'Tool_Type_Coated Carbide': [1 if tool_type == "Coated Carbide" else 0],
            'Tool_Type_HSS': [1 if tool_type == "HSS" else 0]
        }
        
        input_data = pd.DataFrame(feature_data)
        
        # Scale the numeric features
        numeric_cols = ['Spindle_Speed_rpm', 'Feed_mm_per_rev', 'Depth_of_Cut_mm', 'Machining_Length_mm']
        input_data[numeric_cols] = scaler.transform(input_data[numeric_cols])

        # Make prediction
        prediction = model.predict(input_data)[0]

        st.success(f"Estimated Machining Time: {prediction:.2f} seconds")

if __name__ == "__main__":
    main()
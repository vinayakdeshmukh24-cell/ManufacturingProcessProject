# Machining Time Predictor

This is a web application that predicts machining time based on various parameters using machine learning.

## Setup

1. Install the required packages:
```bash
pip install -r requirements.txt
```

2. Download the pre-trained model files:
   - Download `machining_model.joblib` and `scaler.joblib` from the [latest release](https://github.com/vinayakdeshmukh24-cell/ManufacturingProcessProject/releases/latest)
   - Place these files in the project root directory

3. Run the web application:
```bash
streamlit run app.py
```

## Training Your Own Model (Optional)

If you want to train your own model:
1. Generate the dataset:
```bash
python generate_data.py
```

2. Train the model:
```bash
python train.py
```

## Features

- Input machining parameters:
  - Spindle Speed (rpm)
  - Feed Rate (mm/rev)
  - Depth of Cut (mm)
  - Machining Length (mm)
  - Material Selection
  - Tool Type Selection
  - Operation Type Selection
- Real-time prediction of machining time
- User-friendly interface
- Input validation and constraints

## Model Details

The application uses a Random Forest Regressor to predict machining time based on the input parameters. The model is trained on a synthetic dataset that simulates realistic machining conditions.

## Large Files
The model files (`machining_model.joblib` and `scaler.joblib`) are not included in the repository due to size constraints. Please download them from the releases section.

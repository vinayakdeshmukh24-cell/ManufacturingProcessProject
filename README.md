# Machining Time Predictor

This is a web application that predicts machining time based on various parameters using machine learning.

## Setup

1. Install the required packages:
```bash
pip install -r requirements.txt
```

2. Generate the dataset and train the model:
```bash
python generate_data.py  # Generate the training dataset
python train.py         # Train and save the model
```

3. Run the web application:
```bash
streamlit run app.py
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

## Important Notes

The trained model files (`machining_model.joblib` and `scaler.joblib`) are not included in the repository due to size limitations. You need to generate them locally:

1. First generate the dataset:
```bash
python generate_data.py
```

2. Then train the model:
```bash
python train.py
```

This will create all necessary files:
- `machining_time_dataset.csv`: Training data
- `machining_model.joblib`: Trained model
- `scaler.joblib`: Feature scaler

These files are automatically ignored by git as they are either too large or can be regenerated.

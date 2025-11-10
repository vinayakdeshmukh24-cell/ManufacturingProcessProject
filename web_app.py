from flask import Flask, render_template, request, jsonify
import joblib
import pandas as pd
import numpy as np
import os

app = Flask(__name__)

# Constants
N_RANGE = (500, 3000)
F_RANGE = (0.05, 0.5)
D_RANGE = (0.2, 3.0)
L_RANGE = (10, 300)

MATERIALS = ["Mild Steel", "Cast Iron", "Brass"]
TOOLS = ["HSS", "Carbide", "Coated Carbide"]
OPERATIONS = ["Turning", "Milling"]

def generate_and_train_model():
    print("Generating dataset and training model...")
    import generate_data
    import train
    generate_data.generate_dataset()
    train.main()
    return load_model()

def load_model():
    try:
        model = joblib.load('machining_model.joblib')
        scaler = joblib.load('scaler.joblib')
        return model, scaler
    except:
        print("Model files not found. Generating new model...")
        return generate_and_train_model()

@app.route('/')
def home():
    return render_template('index.html',
                         n_range=N_RANGE,
                         f_range=F_RANGE,
                         d_range=D_RANGE,
                         l_range=L_RANGE,
                         materials=MATERIALS,
                         tools=TOOLS,
                         operations=OPERATIONS)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        model, scaler = load_model()
        if model is None:
            return jsonify({
                'error': 'Model not found. Please train the model first using train.py'
            }), 500

        # Get values from form
        data = request.get_json()
        spindle_speed = float(data['spindle_speed'])
        feed_rate = float(data['feed_rate'])
        depth_of_cut = float(data['depth_of_cut'])
        length = float(data['length'])
        material = data['material']
        tool_type = data['tool_type']
        operation = data['operation']

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

        # Calculate theoretical time without corrections
        theoretical_time = (60 * length) / (feed_rate * spindle_speed)

        # Calculate additional metrics
        material_factor = {"Mild Steel": 1.0, "Cast Iron": 1.1, "Brass": 0.8}
        tool_factor = {"HSS": 1.2, "Carbide": 1.0, "Coated Carbide": 0.9}
        operation_factor = {"Turning": 1.0, "Milling": 1.3}

        # Apply correction factors to theoretical time
        corrected_time = theoretical_time * material_factor[material] * tool_factor[tool_type] * operation_factor[operation]

        return jsonify({
            'predicted_time': round(prediction, 2),
            'theoretical_time': round(theoretical_time, 2),
            'material_factor': material_factor[material],
            'tool_factor': tool_factor[tool_type],
            'operation_factor': operation_factor[operation],
            'corrected_time': round(corrected_time, 2)
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port, debug=False)
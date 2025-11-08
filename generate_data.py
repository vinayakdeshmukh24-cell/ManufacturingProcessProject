import pandas as pd
import numpy as np
import random

# Ranges for numeric parameters
N_range = (500, 3000)          # rpm
f_range = (0.05, 0.5)          # mm/rev
d_range = (0.2, 3.0)           # mm
L_range = (10, 300)            # mm

materials = ["Mild Steel", "Cast Iron", "Brass"]
tools = ["HSS", "Carbide", "Coated Carbide"]
operations = ["Turning", "Milling"]

# Material correction factors (higher = slower)
material_factor = {"Mild Steel": 1.0, "Cast Iron": 1.1, "Brass": 0.8}
# Tool correction factors (lower = faster)
tool_factor = {"HSS": 1.2, "Carbide": 1.0, "Coated Carbide": 0.9}
# Operation correction factors
operation_factor = {"Turning": 1.0, "Milling": 1.3}

def generate_dataset():
    # Generate dataset
    data = []
    for _ in range(50000):  # large dataset
        N = random.randint(*N_range)
        f = round(random.uniform(*f_range), 3)
        d = round(random.uniform(*d_range), 3)
        L = random.randint(*L_range)
        mat = random.choice(materials)
        tool = random.choice(tools)
        op = random.choice(operations)

        # base machining time in seconds
        T_sec = (60 * L) / (f * N)

        # Apply realistic corrections
        T_sec *= material_factor[mat]
        T_sec *= tool_factor[tool]
        T_sec *= operation_factor[op]

        # Add noise for realism
        T_sec *= np.random.uniform(0.95, 1.05)

        data.append([N, f, d, L, T_sec, op, mat, tool])

    # Convert to DataFrame
    df = pd.DataFrame(data, columns=[
        "Spindle_Speed_rpm", "Feed_mm_per_rev", "Depth_of_Cut_mm",
        "Machining_Length_mm", "Machining_Time_sec",
        "Operation", "Material", "Tool_Type"
    ])

    # Save original dataset (before encoding)
    df.to_csv("machining_time_dataset_original.csv", index=False)

    # One-hot encode categorical columns
    df_encoded = pd.get_dummies(df, columns=["Operation", "Material", "Tool_Type"])

    print("Dataset shape:", df_encoded.shape)
    print(df_encoded.head())

    # Save encoded dataset
    df_encoded.to_csv("machining_time_dataset.csv", index=False)
    print("\n✅ Dataset saved as 'machining_time_dataset.csv'")

if __name__ == "__main__":
    generate_dataset()
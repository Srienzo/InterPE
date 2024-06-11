import tkinter as tk
from tkinter import ttk
import numpy as np

# Define feature names
feature_names = ['Pregnancies', 'Glucose', 'Blood Pressure', 'Skin Thickness', 'Insulin', 'BMI', 'Diabetes Pedigree Function', 'Age']

# Function to make predictions
def predict_diabetes():
    try:
        # Get user input values
        input_data = [float(entry.get()) for entry in entries]
        
        # Convert input data to numpy array and reshape
        input_data_array = np.asarray(input_data).reshape(1, -1)
        
        # Make prediction
        prediction = model.predict(input_data_array)
        
        # Display prediction result
        result_label.config(text="Result: " + ("Has Diabetes" if prediction[0] == 1 else "Does Not Have Diabetes"))
    
    except ValueError:
        result_label.config(text="Error: Please enter numeric values")

# Create tkinter window
root = tk.Tk()
root.title("Diabetes Prediction System")

# Create input fields
entries = []
for i, feature in enumerate(feature_names):
    label = ttk.Label(root, text=feature + ":")
    label.grid(row=i, column=0, padx=5, pady=5, sticky="e")
    
    entry = ttk.Entry(root)
    entry.grid(row=i, column=1, padx=5, pady=5)
    
    entries.append(entry)

# Create predict button
predict_button = ttk.Button(root, text="Predict", command=predict_diabetes)
predict_button.grid(row=len(feature_names), columnspan=2, padx=5, pady=10)

# Create result label
result_label = ttk.Label(root, text="")
result_label.grid(row=len(feature_names) + 1, columnspan=2, padx=5, pady=5)

# Run the tkinter event loop
root.mainloop()

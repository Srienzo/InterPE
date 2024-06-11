import numpy as np
import warnings
import pickle
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

warnings.filterwarnings("ignore", message="X does not have valid feature names")

# Define feature names
feature_names = ['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age']

# Load the pre-trained model
try:
    with open('model.pkl', 'rb') as file:
        model = pickle.load(file)
except FileNotFoundError:
    raise Exception("Model file not found. Please check the path and try again.")

# Function to make predictions
def predict_diabetes():
    input_data = []
    for entry in entries:
        try:
            value = float(entry.get())
            if value < 0:
                raise ValueError
            input_data.append(value)
        except ValueError:
            messagebox.showerror("Invalid input", "Please enter valid non-negative numeric values for all fields.")
            return
    
    input_data_as_numpy_array = np.asarray(input_data).reshape(1, -1)
    
    try:
        prediction = model.predict(input_data_as_numpy_array)
    except Exception as e:
        messagebox.showerror("Prediction error", f"An error occurred during prediction: {e}")
        return
    
    result = 'The person does not have diabetes.' if prediction[0] == 0 else 'The person has diabetes.'
    messagebox.showinfo("Diabetes Prediction", result)

# Function to clear all inputs
def clear_inputs():
    for entry in entries:
        entry.delete(0, tk.END)

# Set up the GUI
root = tk.Tk()
root.title("Diabetes Prediction System by Sherwin@interpe")
root.geometry("500x600")
root.resizable(False, False)  # Make the window non-resizable

# Load the background image
background_image = Image.open("background.jpg")
background_photo = ImageTk.PhotoImage(background_image)

# Create a canvas to display the background image
canvas = tk.Canvas(root, width=500, height=600)
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, image=background_photo, anchor="nw")

# Create a frame to hold the content
frame = tk.Frame(root, bg="#2e2e2e", bd=5)
frame.place(relwidth=0.9, relheight=0.9, relx=0.05, rely=0.05)

header = tk.Label(frame, text="Diabetes Prediction System", font=("Helvetica", 24, "bold"), bg="#2e2e2e", fg="#ffffff")
header.pack(pady=20)

entries = []
for feature_name in feature_names:
    entry_frame = tk.Frame(frame, bg="#2e2e2e")
    entry_frame.pack(padx=10, pady=5, fill=tk.X)

    label = tk.Label(entry_frame, text=f"{feature_name}:", font=("Helvetica", 14), bg="#2e2e2e", fg="#ffffff", width=20, anchor='w')
    label.pack(side=tk.LEFT, padx=5)
    
    entry = tk.Entry(entry_frame, font=("Helvetica", 14), width=15, bg="#ffffff", fg="#000000")
    entry.pack(side=tk.LEFT, padx=5)
    entries.append(entry)

button_frame = tk.Frame(frame, bg="#2e2e2e")
button_frame.pack(pady=20)

submit_button = tk.Button(button_frame, text="Predict", command=predict_diabetes, font=("Helvetica", 14), bg="#4CAF50", fg="white", padx=20, pady=10, bd=0, relief=tk.RIDGE, highlightthickness=0)
submit_button.pack(side=tk.LEFT, padx=10)

clear_button = tk.Button(button_frame, text="Clear", command=clear_inputs, font=("Helvetica", 14), bg="#f44336", fg="white", padx=20, pady=10, bd=0, relief=tk.RIDGE, highlightthickness=0)
clear_button.pack(side=tk.LEFT, padx=10)

footer = tk.Label(frame, text="Powered by Sherwin @InternPe", font=("Helvetica", 12), bg="#2e2e2e", fg="#888888")
footer.pack(side=tk.BOTTOM, pady=10)

root.mainloop()

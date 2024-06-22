import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import numpy as np
import pickle
import locale
from PIL import ImageTk, Image

# Set locale to Indian English
locale.setlocale(locale.LC_ALL, 'en_IN')

# Unique car company names from the provided list
car_companies = [
    "Hyundai", "Mahindra", "Maruti", "Ford", "Skoda", "Audi", "Toyota", "Renault", "Honda", "Datsun",
    "Mitsubishi", "Tata", "Volkswagen", "BMW", "Chevrolet", "Mini", "Nissan", "Hindustan", "Fiat", "Force",
    "Mercedes", "Land", "Yamaha"
]

# Dictionary to store car models for each company
car_models = {
    "Hyundai": ["Santro Xing XO eRLX Euro III", "Grand i10 Magna 1.2 Kappa VTVT", "Grand i10", "Elite i20", "Verna",
                "Creta", "i20 Active", "i20 Active 1.2 SX", "Elantra 2.0 SX Option AT", "Tucson", "i20",
                "Verna VTVT 1.6 SX Option", "Creta 1.6 CRDi SX Plus", "i10"],
    "Mahindra": ["Jeep CL550 MDI", "Scorpio S10", "Scorpio", "XUV500", "Bolero", "Thar", "KUV100", "Xylo H4",
                 "TUV300", "TUV300 T6 Plus", "NuvoSport", "Verito", "KUV100 NXT", "Bolero Power Plus", "XUV300",
                 "Bolero Power Plus ZLX"],
    "Maruti": ["Suzuki Alto 800 Vxi", "Suzuki Baleno Delta 1.2", "Suzuki Alto K10", "Suzuki Celerio", "Suzuki Swift",
               "Suzuki Swift Dzire", "Suzuki Wagon R", "Suzuki Ertiga", "Suzuki Ciaz", "Suzuki Ignis", "Suzuki Eeco",
               "Suzuki Baleno", "Suzuki Vitara Brezza", "Suzuki S-Cross", "Suzuki Dzire", "Suzuki XL6",
               "Suzuki Ignis 1.2 Delta", "Suzuki Ciaz Alpha"],
    "Ford": ["EcoSport Titanium 1.5L TDCi", "Aspire", "Figo", "Figo Aspire", "Endeavour", "Freestyle"],
    "Skoda": ["Yeti Ambition 2.0 TDI CR 4x2", "Octavia RS"],
    "Audi": ["A8", "TT Coupe"],
    "Toyota": ["Innova 2.0 G 8 STR BS IV", "Corolla Altis"],
    "Renault": ["Lodgy 85 PS RXL", "Kwid", "Captur"],
    "Honda": ["Amaze", "Brio", "City", "WR-V", "Jazz"],
    "Datsun": ["Redi GO S"],
    "Mitsubishi": ["Pajero Sport Limited Edition"],
    "Tata": ["Zest", "Nano Cx BSIV", "Safari Storme", "Tiago", "Nexon", "Harrier"],
    "Volkswagen": ["Vento Highline Plus 1.5 Diesel AT", "Beetle"],
    "BMW": ["3 Series 320i"],
    "Chevrolet": ["Spark LS 1.0", "Tavera Neo"],
    "Mini": ["Cooper Convertible", "Countryman"],
    "Nissan": ["Sunny", "GT-R"],
    "Hindustan": [],  # No specific models provided in the list
    "Fiat": ["Linea", "Abarth 595 Competizione"],
    "Force": ["Force One LX 4x4"],
    "Mercedes": ["GLA Class 200 CDI Sport"],
    "Land": ["Freelander 2 SE"],
    "Yamaha": []  # No specific models provided in the list
}

# Load the saved model
with open('car_price_model.pkl', 'rb') as file:
    model = pickle.load(file)

# Function to predict the car price
def predict():
    company = company_entry.get()
    car_model = model_entry.get()
    year = year_entry.get()
    fuel_type = fuel_type_entry.get()
    driven = kms_driven_entry.get()

    try:
        # Clean and convert inputs
        year = int(year)
        driven = int(driven.replace(',', ''))

        # Prepare the data for prediction
        data = pd.DataFrame(columns=['name', 'company', 'year', 'kms_driven', 'fuel_type'],
                            data=np.array([car_model, company, year, driven, fuel_type]).reshape(1, 5))

        # Predict the price
        prediction = model.predict(data)
        predicted_price = locale.currency(prediction[0], grouping=True)
        result_label.config(text=f"Predicted Price: {predicted_price}")

    except ValueError as e:
        messagebox.showerror("Input Error", f"Invalid input: {e}")

# Function to clear the input fields and result
def clear():
    company_entry.set('')
    model_entry.set('')
    year_entry.set('')
    fuel_type_entry.set('')
    kms_driven_entry.delete(0, tk.END)
    result_label.config(text="")

# Function to update car models based on selected company
def update_car_models(event):
    selected_company = company_entry.get()
    models = car_models.get(selected_company, [])
    model_entry['values'] = models

# Create the main window
root = tk.Tk()
root.title("Sherwin @INTERPE CAR PREDICT ML ")

# Set window size and center the window
window_width = 1920
window_height = 1080
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_cordinate = int((screen_width/2) - (window_width/2))
y_cordinate = int((screen_height/2) - (window_height/2))
root.geometry(f"{window_width}x{window_height}+{x_cordinate}+{y_cordinate}")

# Create a canvas for the background image
canvas = tk.Canvas(root, width=window_width, height=window_height)
canvas.pack(fill="both", expand=True)

# Load the background image
bg_image = Image.open("background.jpg")  # Replace with your background image path
bg_image = bg_image.resize((window_width, window_height), Image.Resampling.LANCZOS)
bg_image = ImageTk.PhotoImage(bg_image)
canvas.create_image(0, 0, image=bg_image, anchor="nw")


# Company
tk.Label(canvas, text="Select Company:", font=("Helvetica", 18), bg='white').place(x=650, y=150)
company_entry = ttk.Combobox(canvas, values=car_companies, font=("Helvetica", 18))  # Use unique car company names
company_entry.place(x=1050, y=150)
company_entry.bind("<<ComboboxSelected>>", update_car_models)  # Bind event to update car models

# Car Model
tk.Label(canvas, text="Select Model:", font=("Helvetica", 18), bg='white').place(x=650, y=250)
model_entry = ttk.Combobox(canvas, values=[], font=("Helvetica", 18))  # Initially empty
model_entry.place(x=1050, y=250)

# Year
tk.Label(canvas, text="Select Year of Purchase:", font=("Helvetica", 18), bg='white').place(x=650, y=350)
year_entry = ttk.Combobox(canvas, values=[str(year) for year in range(2000, 2024)], font=("Helvetica", 18))  # Add actual years
year_entry.place(x=1050, y=350)

# Fuel Type
tk.Label(canvas, text="Select Fuel Type:", font=("Helvetica", 18), bg='white').place(x=650, y=450)
fuel_type_entry = ttk.Combobox(canvas, values=["Petrol", "Diesel"], font=("Helvetica", 18))  # Add actual fuel types
fuel_type_entry.place(x=1050, y=450)

# Kilometers Driven
tk.Label(canvas, text="Kilometers travelled:", font=("Helvetica", 18),fg='black').place(x=650, y=550)
kms_driven_entry = tk.Entry(canvas, font=("Helvetica", 18))
kms_driven_entry.place(x=1050, y=550)

# Predict button
predict_button = tk.Button(root, text="Predict", command=predict, font=("Roboto Slab", 18, "bold"), fg="white", bg="green")
predict_button.place(x=800, y=650)


# Clear button
clear_button = tk.Button(root, text="Clear", command=clear, font=("Roboto Slab", 18, "bold"), fg="white", bg="red")
clear_button.place(x=1050, y=650)


# Result label
result_label = tk.Label(canvas, text="", font=("Helvetica", 18), bg='white')
canvas.create_window(window_width//2, 750, window=result_label)

# Footer label
canvas.create_text(window_width//2, 980, text="ALL RIGHTS RESERVED BY SHERWIN @INTERNPE", font=("Roboto Slab", 30,"bold"), fill="red")
canvas.create_text(940, 29, text="CAR PRICE PREDICTION ML", font=("Roboto Slab", 39, "bold"), fill="red")


# Style for buttons to blend with background
style = ttk.Style()
style.configure("Custom.TButton", font=("Helvetica", 18), background='white', borderwidth=0)

# Run the application
root.mainloop()

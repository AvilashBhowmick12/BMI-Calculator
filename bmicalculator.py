import tkinter as tk
from tkinter import messagebox
import psycopg2
from datetime import datetime

class BMI_Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("BMI Calculator")

        # Connect to PostgreSQL database
        self.connection = psycopg2.connect(
            host="localhost",
            database="BMI",
            user="postgres",
            password="0000"
        )
        self.cursor = self.connection.cursor()

        
        self.weight_label = tk.Label(root, text="Weight (kg):")
        self.weight_label.grid(row=0, column=0, padx=10, pady=10)
        self.weight_entry = tk.Entry(root)
        self.weight_entry.grid(row=0, column=1, padx=10, pady=10)

        self.height_label = tk.Label(root, text="Height (m):")
        self.height_label.grid(row=1, column=0, padx=10, pady=10)
        self.height_entry = tk.Entry(root)
        self.height_entry.grid(row=1, column=1, padx=10, pady=10)

        
        #self.cursor = self.connection
        #self.connection = 

        self.calculate_button = tk.Button(root, text="Calculate BMI", command=self.calculate_bmi)
        self.calculate_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        # BMI Result Label
        self.result_label = tk.Label(root, text="")
        self.result_label.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

    def calculate_bmi(self):
        weight = float(self.weight_entry.get())
        height = float(self.height_entry.get())

        if weight <= 0 or height <= 0:
            messagebox.showerror("Error", "Weight and height must be positive numbers.")
            return

        bmi = weight / (height ** 2)
        bmi_category = self.get_bmi_category(bmi)
        result_text = "BMi: " + str(bmi) +" Category: "+bmi_category
        self.result_label.config(text=result_text)

        
        self.store_data(weight, height, bmi)

    def get_bmi_category(self, bmi):
        if bmi < 18.5:
            return "Underweight"
        elif bmi < 25:
            return "Normal weight"
        elif bmi < 30:
            return "Overweight"
        else:
            return "Obese"

    def store_data(self, weight, height, bmi):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        query = "INSERT INTO bmi_data (timestamp, weight, height, bmi) VALUES (%s, %s, %s, %s)"
        data = (timestamp, weight, height, bmi)
        self.cursor.execute(query, data)
        self.connection.commit()

def main():
    root = tk.Tk()
    app = BMI_Calculator(root)
    root.mainloop()

if __name__ == "__main__":
    main()
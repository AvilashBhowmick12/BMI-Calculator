from tkinter import *
import customtkinter as ct
import psycopg2
from datetime import date
import matplotlib.pyplot as plt
#from matplotlib.figure import Figure 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg 


ct.set_appearance_mode("light")
ct.set_default_color_theme("green")

root = ct.CTk()
root.geometry('700x600')
root.title("BMI Calculator")

def calculate_BMI():
    name = e1.get()
    wt = float(e2.get())
    ht = float(e3.get())
    age = e4.get()
    category = ''
    Bmi = 0.0
    timestamp =''


    timestamp = date.today()
    Bmi = wt/(ht)**2

    if Bmi < 18.5:
        category = 'Underweight'
    elif Bmi>=18.5 and Bmi<24.9:
        category = 'Healthy'
    elif Bmi>=24.9 and Bmi<30:
        category = 'OverWeight'
    else : category='Obese'

    output1.delete(0,'end')
    output1.insert(0,Bmi)

    output2.delete(0,'end')
    output2.insert(0,category)

    StoreData(timestamp, name, age, wt, ht, Bmi, category)


def StoreData(timestamp, name, age, weight, height, Bmi, category):
    database = psycopg2.connect(
        host = 'localhost',
        user = 'postgres',
        password = '0000',
        database = 'BMI_Data'
    )

    mycursor = database.cursor()

    sql = "Insert Into bmi_data(timestamp, name, age, weight, height, bmi, category) Values(%s,%s,%s,%s,%s,%s,%s)"
    val = timestamp, name, str(age), str(weight), str(height), str(Bmi), category

    mycursor.execute(sql,val)
    database.commit()
    database.close()

def ShowAnalytics():
    result = []
    x=0
    database = psycopg2.connect(
        host = 'localhost',
        user = 'postgres',
        password = '0000',
        database = 'BMI_Data'
    )

    mycursor = database.cursor()

    n = e5.get()

    sql = "Select bmi from bmi_data Where name='" + n + "'"
    mycursor.execute(sql)
    temp = mycursor.fetchall()
    result = list(temp)

    sql = "Select timestamp from bmi_data Where name='" + n + "'"
    mycursor.execute(sql)
    temp1 = mycursor.fetchall()
    time = list(temp1)

    
          
    #for i in result:
    #    print(i)

    #Plotting in canvas
    ax.clear()
    plt.xlabel("Date")
    plt.ylabel("BMI")
    ax.scatter(time,result)
    ax.plot(time,result)
    canvas.draw()


mytab = ct.CTkTabview(
    root,
    height = 570,
    width = 750
)
mytab.pack(pady = 10)

tab1 = mytab.add("Calculator")
tab2 = mytab.add("Analytics")

#Name Entry
l1 = ct.CTkLabel(tab1, text="Enter Name")
l1.pack()
e1 = ct.CTkEntry(tab1)
e1.pack()

#Weight Entry
l2 = ct.CTkLabel(tab1, text="Enter Weight in kg")
l2.pack()
e2 = ct.CTkEntry(tab1)
e2.pack()


#Height Entry
l3 = ct.CTkLabel(tab1, text="Enter Height in m")
l3.pack()
e3 = ct.CTkEntry(tab1)
e3.pack()

#Age Entry
l4 = ct.CTkLabel(tab1, text="Enter Age")
l4.pack()
e4 = ct.CTkEntry(tab1)
e4.pack()

b1 = ct.CTkButton(tab1, text="Calculate",command=calculate_BMI)
b1.pack(pady = 5)

l5 = ct.CTkLabel(tab1, text = "BMI:")
l5.pack()

output1 = ct.CTkEntry(tab1)
output1.pack()

output2 = ct.CTkEntry(tab1)
output2.pack()


# Analytics
l6 = ct.CTkLabel(tab2, text="Enter Person Name")
l6.pack() 
e5 = ct.CTkEntry(tab2)
e5.pack()


fig,ax = plt.subplots(1, 1, figsize=(9,5))
plt.xlabel("Date")
plt.ylabel("BMI")
canvas = FigureCanvasTkAgg(fig, tab2)
canvas.get_tk_widget().pack()



b2 = ct.CTkButton(tab2, text = "Show BMI Data", command=ShowAnalytics)
b2.pack(pady=5)

root.mainloop()
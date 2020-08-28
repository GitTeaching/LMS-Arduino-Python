
import tkinter as tk
import serial
import time


# get and connect to arduino device
arduino_serial = serial.Serial(port='COM6', baudrate=9600, timeout=0.5) 

############################################################
# GUI Tkinter version
def read_data():
    # assume the data format: humidity / temperature
    data.set(arduino_serial.readline().decode('ascii').strip()) 
    print('{}'.format(data.get()))
    root.after(2000, read_data)

root = tk.Tk()

data = tk.StringVar()

tk.Label(root, text='Humidity / Temperature:').grid(row=0, column=0, padx=5, pady=5)
tk.Label(root, textvariable=data, bd=2, relief='solid', width=20, fg='black', bg='white').grid(row=0, column=1, padx=5)

read_data()
root.mainloop()

############################################################
# shell simple version
# while True:
#     time.sleep(2)
#     sensor = arduino_serial.readline().decode('ascii').strip() 
#     print(sensor)

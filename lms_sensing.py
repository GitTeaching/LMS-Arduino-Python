
from tkinter import *
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import serial
import datetime
import mysql.connector
from mysql.connector import Error


###################################################################################################

def read_temp_humdity():
    vals = arduino_serial.readline().decode('ascii').strip()
    temp.set('Temperature = ' + vals[0:5]) 
    #print('{}'.format(temp.get()))
    humidity.set('Humidity = ' + vals[5:11]) 
    #print('{}'.format(humidity.get()))
    if vals :
    	save_data_to_db(vals[0:5], vals[5:11], 'NO')
    	update_pie_vals(float(vals[0:5]), 'b', ax1, fig, pie1)
    	update_pie_vals(float(vals[5:11]), 'r', ax3, fig_2, pie2)
    root.after(2000, read_temp_humdity) 


def update_pie_vals(val, c, ax_f, fig_f, pie):
	sizes = [100-val, val]
	colors = ['w', c]
	ax_f.clear()
	ax_f.pie(sizes, colors=colors, autopct='%1.f', startangle=250, pctdistance=0.85)
	ax_f.axis('equal')
	centre_circle = plt.Circle((0,0), 0.70, color='black')
	fig_f.gca().add_artist(centre_circle)
	fig_f.set_size_inches(2,2)
	plt.tight_layout()
	pie.draw()


def save_data_to_db(temp_str, humidity_str, is_fire):
	try:
		query = """insert into sensing (temperature, humidity, is_fire, sensed_datetime) values (%s, %s, %s, %s)"""
		cursor = connection.cursor()
		sensed_datetime = datetime.datetime.now()
		cursor.execute(query, (float(temp_str), float(humidity_str), is_fire, sensed_datetime))
		connection.commit()
		print("Record inserted successfully into Sensing table")
		cursor.close()

	except Error as e:
		print("Error inserting data into MySQL sensing table", e)


def save_df_to_csv(df):
	df.to_csv(r'dataset.csv', index=False)

#############################################################################################################

# establish connection to MySQL. 
connection = mysql.connector.connect(host="localhost", user="root", password="", database="lms_arduino_python")

##############################################################################################################

# get and connect to arduino device
arduino_serial = serial.Serial(port='COM6', baudrate=9600, timeout=0.5)

##############################################################################################################

# read dataset from database
df = pd.read_sql('SELECT * FROM sensing', con=connection)
df = pd.DataFrame(df, columns=['sensed_datetime','temperature', 'humidity'])

###############################################################################################################

# create window
root = Tk()
root.title("Library MS")
root.minsize(width=1100, height=650)
root.geometry("1100x650")
root.iconbitmap('images/book.ico')
root.config(background='black')

# main frame
frame = Frame(root, bg='black')

# pie frame
pie_frame = Frame(frame, bg='black')
pie_frame.grid(row=0, column=0, padx=20)

# Temperature Label
temp = StringVar()
temp_label = Label(pie_frame, textvariable=temp, bg='black', fg='white', font=('Courier', 20, 'bold'))
temp_label.grid(row=0, column=0, pady=10)

# plt dark style
plt.style.use('dark_background')

# Temperature Pie chart autopct='%1.1f%%'
fig1, ax1 = plt.subplots()
#fig1.patch.set_facecolor('black')
sizes = [70, 30]
colors = ['w','b']
ax1.pie(sizes, colors=colors, autopct='%1.f', startangle=250, pctdistance=0.85)
ax1.axis('equal')
centre_circle = plt.Circle((0,0), 0.70, color='black')
fig = plt.gcf()
fig.gca().add_artist(centre_circle)
fig.set_size_inches(2,2)
plt.tight_layout()
pie1 = FigureCanvasTkAgg(fig, pie_frame)
pie1.get_tk_widget().grid(row=1, column=0, pady=10)

# Humidity label
humidity = StringVar()
humidity_label = Label(pie_frame, textvariable=humidity, bg='black', fg='white', font=('Courier', 20, 'bold'))
humidity_label.grid(row=2, column=0, pady=10)

# Humidity Pie chart autopct='%1.1f%%'
fig3, ax3 = plt.subplots()
sizes = [60, 40]
colors = ['w','r']
ax3.pie(sizes, colors=colors, autopct='%1.f', startangle=250, pctdistance=0.85)
ax3.axis('equal')
centre_circle = plt.Circle((0,0), 0.70, color='black')
fig_2 = plt.gcf()
fig_2.gca().add_artist(centre_circle)
fig_2.set_size_inches(2,2)
plt.tight_layout()
pie2 = FigureCanvasTkAgg(fig_2, pie_frame)
pie2.get_tk_widget().grid(row=3, column=0, pady=10)

# Line plot temp and humidity
fig2 = plt.Figure(figsize=(6,5), dpi=90)
ax2 = fig2.add_subplot(111)
df['Time'] = [datetime.datetime.time(d) for d in df['sensed_datetime']] 
df1 = df[['Time','temperature']].groupby('Time').sum()
print(df1)
df1.plot(kind='line', legend=True, ax=ax2, color='r',marker='o', fontsize=10, rot=45, figsize=(9,6))
df2 = df[['Time','humidity']].groupby('Time').sum()
df2.plot(kind='line', legend=True, ax=ax2, color='b',marker='x', fontsize=10, rot=45, figsize=(9,6))
ax2.set_title('Time Vs. Temperature/Humidity Rate')
line = FigureCanvasTkAgg(fig2, frame)
line.get_tk_widget().grid(row=0, column=1, padx=20)

# display main frame
frame.pack(expand=YES)

# sense and update tempertaure and humidity every 2 seconds
read_temp_humdity()

root.mainloop()


##################################################################################################################

df = pd.read_sql('SELECT * FROM sensing', con=connection)
save_df_to_csv(df)

if (connection.is_connected()):
    connection.close()
    print("MySQL connection is closed")

##################################################################################################################
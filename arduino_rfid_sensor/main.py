import serial
import time
import mysql.connector
from mysql.connector import Error


#establish connection to MySQL. You'll have to change this for your database.
connection = mysql.connector.connect(host="localhost", user="XXXXXXX", password="", database="YYYYYYYYY")

#open a cursor to the database
cursor = connection.cursor()

# get an connect to arduino
arduino_serial = serial.Serial('COM6', 9600)

while True:
	time.sleep(1)

    # Get arduino data = rfid id of the book, ex : b'41617690\r\n'
	rfid_id = arduino_serial.readline()
	print(rfid_id)

	pieces = [int(s) for s in rfid_id.split() if s.isdigit()]
	print(pieces[0])

	try:
		cursor=connection.cursor()
		query = """select * from Book where rfid_id = %s"""
		cursor.execute(query, (pieces[0],))
		record = cursor.fetchall()

		if record :
			for row in record:
				print("Rfid_Id = ", row[1], )
				print("Title = ", row[2])
				print("Authors = ", row[3])
				print("Description  = ", row[4], "\n")
		else:
			print('Not found in DB\n')
			query = """insert into Book (rfid_id, title, authors, description, status, issued_by)
			            values (%s, 'test title', 'test author', 'test descr', 'availabe', 'None')"""
			cursor = connection.cursor()
			cursor.execute(query, (rfid_id,))
			connection.commit()
			print("Record inserted successfully into Laptop table")

		cursor.close()

	except Error as e:
		print("Error reading data from MySQL table", e)

if (connection.is_connected()):
    connection.close()
    print("MySQL connection is closed")

# ArduinoUnoSerial.write(val.encode())
	
		
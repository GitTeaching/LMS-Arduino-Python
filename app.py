
from tkinter import *
from tkinter import scrolledtext, messagebox 
from PIL import ImageTk, Image
import mysql.connector
from mysql.connector import Error
import serial
import time
from add_book import add_book
from update_book import update_book


#####################################################################################

def display_scanned_book():

	global status

	try:
		# Get arduino data = rfid id of the book, ex : b'41617690\r\n'
		arduino_serial.flushInput()
		rfid_id = arduino_serial.readline()

		pieces = [int(s) for s in rfid_id.split() if s.isdigit()]
		print(pieces[0])

		canvas.destroy()
		scan_label.destroy()

		cursor=connection.cursor()
		query = """select * from Book where rfid_id = %s"""
		cursor.execute(query, (pieces[0],))
		record = cursor.fetchall()

		if record :
			for row in record:
				update_btn['command'] = lambda: update_book(connection, row[0])

				content_frame.grid(row=3, column=0, pady=20)

				image = ImageTk.PhotoImage(Image.open('images/book_' + str(row[1]) +'.jpg'))
				root.one = image
				book_canvas = Canvas(content_frame, width=180, height=250, bg='#DADAE6', bd=0, highlightthickness=0)
				book_canvas.create_image(0, 0, image=image, anchor=NW)
				book_canvas.grid(row=3, column=0, padx=20)

				book_frame = Frame(content_frame, bg="#DADAE6")
				id_book = Button(book_frame, text=row[1], bg='#4065A4', fg='white', font=('Courier', 15), borderwidth=0)
				id_book.pack(expand=YES, fill=BOTH, pady=5)
				title = Button(book_frame, text=row[2], bg='#DADAE6', fg='black', font=('Times New Roman', 17), borderwidth=0)
				title.pack(expand=YES, fill=BOTH, pady=5)
				authors = Button(book_frame, text=row[3], bg='#FF4140', fg='white', font=('Courier', 15), borderwidth=0)
				authors.pack(expand=YES, fill=BOTH, pady=5)
				descr = scrolledtext.ScrolledText(book_frame, wrap=WORD, width=40, height=8, bg='#DADAE6', fg='black', font=('Times New Roman', 15), borderwidth=0) 
				descr.pack(expand=YES, fill=BOTH, pady=5)
				descr.insert(INSERT, row[4])
				descr.focus() 
				status = Button(book_frame, text=row[5], bg='#FFA500', fg='white', font=('Courier', 15, 'bold'), borderwidth=0)
				status.pack(expand=YES, fill=BOTH, pady=5)
				book_frame.grid(row=3, column=1)

				bookbtn_frame = Frame(book_frame, bg="#DADAE6")
				return_btn = Button(bookbtn_frame, text="Return Book", bg='#4065A4', fg='white', font=('Courier', 15), borderwidth=0, command=lambda: return_book(row[1]))
				return_btn.grid(row=3, column=0, padx=30)
				issueto_entry = Entry(bookbtn_frame, fg='black', font=('Courier', 15))
				issueto_entry.grid(row=3, column=1, padx=10)
				issueto_entry.insert(0, "Enter name..")
				issue_btn = Button(bookbtn_frame, text="Issue Book", bg='#4065A4', fg='white', font=('Courier', 15), borderwidth=0, 
									command=lambda: issue_book(row[1], issueto_entry.get()))
				issue_btn.grid(row=3, column=2, padx=10)
				
				bookbtn_frame.pack(expand=YES, fill=BOTH, pady=5)
		else:
			label = Label(content_frame, text='Book not in our DataBase. Please click on Add Book.', bg='#DADAE6', fg='black', font=('Courier', 20))
			label.grid(row=3, column=0)

		cursor.close()

	except Error as e:
		print("Error reading data from MySQL table", e)

#####################################################################################

def return_book(rfid_id):
	try:
		cursor=connection.cursor()
		query = """update Book set status = 'Available' where rfid_id = %s"""
		cursor.execute(query, (rfid_id,))
		query = """update Book set issued_by = 'None' where rfid_id = %s"""
		cursor.execute(query, (rfid_id,))
		connection.commit()
		messagebox.showinfo("Return Book","Book returned successfully.")
		status['text'] = 'Available'
		cursor.close()

	except mysql.connector.Error as error:
		print("Failed to update table record.")


def issue_book(rfid_id, issuedby):
	try:
		cursor=connection.cursor()
		query = """select status from Book where rfid_id = %s"""
		cursor.execute(query, (rfid_id,))
		record = cursor.fetchone()
		
		if record[0] == 'Available':
			if issuedby == 'Enter name..' or issuedby == '':
				messagebox.showwarning("Warning","Please provide a name.")
				cursor.close()
				return 
			query = """update Book set status = 'Issued' where rfid_id = %s"""
			cursor.execute(query, (rfid_id,))
			query = """update Book set issued_by = %s where rfid_id = %s"""
			cursor.execute(query, (issuedby, rfid_id))
			connection.commit()
			messagebox.showinfo("Issue Book","Book issued successfully.")
			status['text'] = 'Issued' 
		else:
			messagebox.showwarning("Warning","Sorry! The book is not available yet.") 
		cursor.close()

	except mysql.connector.Error as error:
		print("Failed to update table record.")

#####################################################################################

# establish connection to MySQL. 
connection = mysql.connector.connect(host="localhost", user="XXXXXXXXXXXX", password="", database="YYYYYYYYYYYYYYY")


######################################################################################

# get and connect to arduino
arduino_serial = serial.Serial('COM6', 9600)

######################################################################################

# create window
root = Tk()
root.title("Library Management System")
root.minsize(width=820, height=500)
root.geometry("900x650")
root.iconbitmap('images/book.ico')
root.config(background='#DADAE6')

# main frame
frame = Frame(root, bg='#DADAE6')

# heading frame
heading_frame = Frame(frame, bg="#4065A4", bd=5)
heading_label = Label(heading_frame, text="Welcome to Our \n Arduino Based Library", bg='#DADAE6', fg='black', 
						font=('Courier', 20, 'bold'))
heading_label.pack(ipadx=40, ipady=10)
heading_frame.grid(row=0, column=0, pady=10)

# buttons frame
buttons_frame = Frame(frame, bg="#DADAE6")
add_btn = Button(buttons_frame, text="Add Book", bg='#FF4140', fg='white', font=('Helvetica', 15), borderwidth=0, command=lambda: add_book(connection))
add_btn.grid(row=1, column=0, padx=20)
update_btn = Button(buttons_frame, text="Update Book", bg='#1AA6B7', fg='white', font=('Helvetica', 15), borderwidth=0)
update_btn.grid(row=1, column=1, padx=20)
scan_btn = Button(buttons_frame, text="Scan Book", bg='#39998E', fg='white', font=('Helvetica', 15), command=display_scanned_book)
scan_btn.grid(row=1, column=2, padx=20)
buttons_frame.grid(row=1, column=0, pady=10)

# label frame
scan_label = Label(frame, text="Scan your Book to show its details", bg='#DADAE6', fg='black', font=('Courier', 20))
scan_label.grid(row=2, column=0, pady=5)

# content frame
content_frame = Frame(frame, bg='#DADAE6')
# image = PhotoImage(file="library.png")
image = ImageTk.PhotoImage(Image.open('images/library3.png'))
root.one = image
canvas = Canvas(content_frame, width=500, height=400, bg='#DADAE6', bd=0, highlightthickness=0)
canvas.create_image(0, 0, image=image, anchor=NW)
canvas.pack(expand=YES, fill=BOTH)
content_frame.grid(row=3, column=0)

# display main frame
frame.pack(expand=YES)


root.mainloop()

##################################################################################################################

if (connection.is_connected()):
    connection.close()
    print("MySQL connection is closed")

##################################################################################################################


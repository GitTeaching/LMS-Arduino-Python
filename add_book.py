
from tkinter import *
from tkinter import scrolledtext, messagebox 
import mysql.connector
from mysql.connector import Error



def add_book(connection):

	def add_book_in_db():
		rfid_id = id_entry.get()
		title = title_entry.get()
		authors = authors_entry.get()
		descr = descr_entry.get('1.0', END)

		if not rfid_id.isdigit():
			messagebox.showwarning("Warning","The RFID Numer should be a digit.")
		else:
			try:
				query = """insert into Book (rfid_id, title, authors, description, status, issued_by)
				            values (%s, %s, %s, %s, 'Availabe', 'None')"""
				cursor = connection.cursor()
				cursor.execute(query, (rfid_id, title, authors, descr))
				connection.commit()
				messagebox.showinfo("Add Book","Book added successfully.")
				cursor.close()

			except Error as e:
				print("Error inserting data into MySQL table", e)
				

	######################################################################################################


	# create window 
	root = Tk()
	root.title("Library Management System")
	root.minsize(width=820, height=500)
	root.geometry("900x650")
	root.iconbitmap('images/book.ico')
	root.config(background='#151713')

	# main frame
	frame = Frame(root, bg='#151713')

	# heading frame
	heading_frame = Frame(frame, bg="#e39910", bd=5)
	heading_label = Label(heading_frame, text="Welcome to Our \n Arduino Based Library", bg='#151713', fg='white', font=('Courier', 20, 'bold'))
	heading_label.pack(ipadx=40, ipady=10)
	heading_frame.grid(row=0, column=0, pady=30)


	# book fields : label + entry
	content_frame = Frame(frame, bg='#e39910')

	id_label = Label(content_frame, text='RFID-Number: ', bg='#e39910', fg='#151713', font=('Courier', 15, 'bold'))
	id_label.grid(row=0, column=0, padx=5, pady=10)
	id_entry = Entry(content_frame, fg='black', font=('Courier', 15), width=32)
	id_entry.grid(row=0, column=1, padx=10)

	title_label = Label(content_frame, text='Title: ', bg='#e39910', fg='#151713', font=('Courier', 15, 'bold'))
	title_label.grid(row=1, column=0, padx=5, pady=10)
	title_entry = Entry(content_frame, fg='black', font=('Courier', 15), width=32)
	title_entry.grid(row=1, column=1, padx=10)

	authors_label = Label(content_frame, text='Authors: ', bg='#e39910', fg='#151713', font=('Courier', 15, 'bold'))
	authors_label.grid(row=2, column=0, padx=5, pady=10)
	authors_entry = Entry(content_frame, fg='black', font=('Courier', 15), width=32)
	authors_entry.grid(row=2, column=1, padx=10)

	descr_label = Label(content_frame, text='Book Description: ', bg='#e39910', fg='#151713', font=('Courier', 15, 'bold'))
	descr_label.grid(row=3, column=0, padx=5, pady=10)
	descr_entry = scrolledtext.ScrolledText(content_frame,  wrap=WORD, width=30, height=6, fg='black', font=('Courier', 15))
	descr_entry.focus() 
	descr_entry.grid(row=3, column=1, padx=10, pady=20)

	add_btn = Button(content_frame, text='Quit', bg='#151713', fg='white', font=('Courier', 15, 'bold'), command=root.destroy)
	add_btn.grid(row=4, column=0, padx=5, pady=10)
	quit_btn = Button(content_frame, text='Add Book', bg='#151713', fg='white', font=('Courier', 15, 'bold'), command=add_book_in_db)
	quit_btn.grid(row=4, column=1, padx=5, pady=10)

	content_frame.grid(row=1, column=0, pady=30)


	# display main frame
	frame.pack(expand=YES)


	root.mainloop()

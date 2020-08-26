
from tkinter import *
from tkinter import scrolledtext, messagebox 
import mysql.connector
from mysql.connector import Error


def update_book(connection, bid):

	def update_book_in_db():

		new_rfid_id = id_entry.get()
		new_title = title_entry.get()
		new_authors = authors_entry.get()
		new_descr = descr_entry.get('1.0', END)

		if not new_rfid_id.isdigit():
			messagebox.showwarning("Warning","The RFID Numer should be a digit.")
		else:
			try:
				cursor = connection.cursor()
				query = """update Book set rfid_id = %s, title = %s, authors = %s, description = %s where rfid_id = %s"""
				cursor.execute(query, (new_rfid_id, new_title, new_authors, new_descr, rfid_id))
				connection.commit()
				messagebox.showinfo("Update Book","Book updated successfully.")
				cursor.close()

				root.destroy()

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

	# get book details to be updated
	cursor=connection.cursor()
	query = """select * from Book where bid = %s"""
	cursor.execute(query, (bid,))
	record = cursor.fetchall()
	if record :
		for row in record:
			rfid_id = row[1]
			title = row[2]
			authors = row[3]
			descr = row[4]
		cursor.close()

	# book fields : label + entry
	content_frame = Frame(frame, bg='#e39910')

	id_label = Label(content_frame, text='RFID-Number: ', bg='#e39910', fg='#151713', font=('Courier', 15, 'bold'))
	id_label.grid(row=0, column=0, padx=5, pady=10)
	id_entry = Entry(content_frame, fg='black', font=('Courier', 15), width=32)
	id_entry.insert(0, rfid_id)
	id_entry.grid(row=0, column=1, padx=10)

	title_label = Label(content_frame, text='Title: ', bg='#e39910', fg='#151713', font=('Courier', 15, 'bold'))
	title_label.grid(row=1, column=0, padx=5, pady=10)
	title_entry = Entry(content_frame, fg='black', font=('Courier', 15), width=32)
	title_entry.insert(0, title)
	title_entry.grid(row=1, column=1, padx=10)

	authors_label = Label(content_frame, text='Authors: ', bg='#e39910', fg='#151713', font=('Courier', 15, 'bold'))
	authors_label.grid(row=2, column=0, padx=5, pady=10)
	authors_entry = Entry(content_frame, fg='black', font=('Courier', 15), width=32)
	authors_entry.insert(0, authors)
	authors_entry.grid(row=2, column=1, padx=10)

	descr_label = Label(content_frame, text='Book Description: ', bg='#e39910', fg='#151713', font=('Courier', 15, 'bold'))
	descr_label.grid(row=3, column=0, padx=5, pady=10)
	descr_entry = scrolledtext.ScrolledText(content_frame,  wrap=WORD, width=30, height=6, fg='black', font=('Courier', 15))
	descr_entry.insert(INSERT, descr)
	descr_entry.focus() 
	descr_entry.grid(row=3, column=1, padx=10, pady=20)

	add_btn = Button(content_frame, text='Quit', bg='#151713', fg='white', font=('Courier', 15, 'bold'), command=root.destroy)
	add_btn.grid(row=4, column=0, padx=5, pady=10)
	quit_btn = Button(content_frame, text='Update Book', bg='#151713', fg='white', font=('Courier', 15, 'bold'), command=update_book_in_db)
	quit_btn.grid(row=4, column=1, padx=5, pady=10)

	content_frame.grid(row=1, column=0, pady=30)


	# display main frame
	frame.pack(expand=YES)


	root.mainloop()

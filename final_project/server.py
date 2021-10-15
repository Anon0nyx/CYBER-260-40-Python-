import sqlite3
import socket
import os
import time
from lib import server as serv

# Function to configure the database
def configure_database():
	# Try to connect to the database and check of client_info table, if not there, create it
	try:
		sqlConn = sqlite3.connect("./server/database.db")
	except:
		print("Database unavailable")
		return 0
	conn = sqlConn.cursor()
	search = conn.execute("SELECT count(name) FROM sqlite_master WHERE type='table' AND name='client_info'")
	if search.fetchone()[0]:
		print("Database configured.")
		return sqlConn
	search = sqlConn.execute(""" CREATE TABLE client_info (
									Username VARCHAR(255) NOT NULL,
									Password VARCHAR(255) NOT NULL,
									PubKey VARCHAR(4096) NOT NULL
									); """)
	sqlConn.commit()
	print("Database configured.")
	return sqlConn

def main():
	print("Starting server.")
	
	db = configure_database()
	
	if not db:
		print("Database error")
		return 0

	# Create our server object for handling client interactions
	server = serv.Server(db)

	# Determine the servers keys for the session
	server.configure_keys()

	# While client is logged in
	while True:
		data = server.client_sock.recv(5)
		data = data.decode('utf-8')
		data = str(data)
		
		print(data)
	
		# Make decisions based on user inupt
		if data == "DONE":
			server.client_sock.send(b"Thank you for connecting.")
			print("Done Receiving from client.")
		elif data == "CODE2":
			user_created = server.create_user()
			if user_created:
				server.client_sock.send(b"CODE2")
		elif data == "CODE1":
			logged_in = server.login()
			if logged_in:
				server.client_sock.send(b"CODE1")
			else:
				server.client_sock.send(b"CODE0")
		elif data == "CODE3":
			print(server.login_info["logged_in"])
			server.list_files()
		elif data == "CODE4":
			server.upload_file()
		elif data == "CODE5":
			server.download_file()
		elif data == "PORTS":
			server.check_ports()
		else:
			break

	# Close everything up
	server.client_sock.close()	
	server.sock.close()
	server.db.close()

if __name__ == "__main__":
	main()

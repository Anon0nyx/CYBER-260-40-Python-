import sqlite3
import socket
import encryption_functions as ef
import os
import time
from cryptography.fernet import Fernet

def configure_database():
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

def check_db_user(conn, username):
	search = f"SELECT Username FROM client_info WHERE Username='{username}'"
	search = conn.execute(search)
	result = search.fetchone()
	if result:
		return True
	else:
		return False

class Server:
	def __init__(self, db):
		self.db = db

		self.client_pub_key = ""
		self.client_sym_key = ""
		
		self.priv_key = ""
		self.pub_key = ""
		self.sym_key = ""

		self.login_info = {"logged_in": False,
							"username": None}
		self.sock = socket.socket()
		self.sock.bind(("localhost", 8080))
		self.sock.listen(5)
		self.client_sock, self.address = self.sock.accept()

	def configure_keys(self):
		print("Configuring server keys.")
		self.pub_key = str(open("./server/keys/server_keys.pub", "r").read())
		self.priv_key = str(open("./server/keys/server_keys", "r").read())
		self.sym_key = open("./server/keys/server_keys.sym", "rb").read() 

	def key_exchange(self):
		self.client_sock.send(self.pub_key.encode("utf-8"))	
		sym_key = self.client_sock.recv(4096)	
		self.client_sym = ef.decrypt_key(sym_key, self.priv_key)
		print(f"Client SYM: {self.client_sym}")
		self.client_sock.send(ef.encrypt_key(self.sym_key, self.client_pub_key))

	def create_user(self):
		print("Creating user (server)")
		conn = self.db.cursor()
		
		data = self.client_sock.recv(4096)
		data = data.decode("utf-8")
		data = str(data)
		data = data.split(":")
		print(data)

		username = data[0]
		password = data[1]
		
		key = data[2]
		key = key.replace("b'", "")
		key = key.replace("'", "")
		self.client_pub_key = key

		user_exist = check_db_user(conn, username)
		if user_exist:
			self.client_sock.send(b"EXIST")
			return False
		else:
			self.key_exchange()
			query = f"INSERT INTO client_info VALUES ('{username}', '{password}', '{username}_pub.pem');"

			search = conn.execute(query)
			
			os.system(f"mkdir ./server/folder_clients/{username}")
			
			self.db.commit()
			
			self.login_info["username"] = username
			self.login_info["logged_in"] = True

			return True
		
		if self.login_info["logged_in"]:
			key_file = open(f"./folder_clients/{self.login_info['username']}_pub.pem", "w")
		
			key_file.write(key)
			key_file.close()
		else:
			return False

	def list_files(self):
		files = os.listdir(f"./server/folder_clients/{self.login_info['username']}/")
		self.client_sock.send(str(files).encode("utf-8"))

	def login(self):
		data = self.client_sock.recv(4096)
		data = data.decode("utf-8")
		data = str(data).split(":")
		
		username = data[0]
		password = data[1]
		self.client_pub_key = data[2]
		conn = self.db.cursor()

		query = f"SELECT * FROM client_info WHERE Username='{username}' AND Password='{password}'"
		search = conn.execute(query)

		result = search.fetchone()

		if result:
			self.login_info["username"] = username
			self.login_info["logged_in"] = True
			self.key_exchange()
			return True
		else:
			return False

	def upload_file(self):
		self.client_sock.send(b"CODE4")
		filename = self.client_sock.recv(52).decode("utf-8")
		self.client_sock.send(b"CODE4")
		data = self.client_sock.recv(4096)
		data = ef.decrypt_data(data, self.sym_key)
		data = ef.encrypt_data(data, self.client_sym)
		self.client_sock.send(b"CODE4")
		with open(f"./server/folder_clients/{self.login_info['username']}/{filename}", "wb") as data_file:
			data_file.write(data)
		
		return 0

	def download_file(self):
		self.client_sock.send(b"CODE5")
		filename = self.client_sock.recv(52).decode("utf-8")
		data = ""
		with open(f"./server/folder_clients/{self.login_info['username']}/{filename}", "rb") as data_file:
			data = data_file.read()
		self.client_sock.send(data)

		return 0

def main():
	print("Starting server.")
	
	db = configure_database()
	
	if not db:
		print("Database error")
		return 0
	
	server = Server(db)
	
	server.configure_keys()

	while True:
		data = server.client_sock.recv(5)
		data = data.decode('utf-8')
		data = str(data)
		
		print(data)
		
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
		else:
			break

	server.client_sock.close()	
	server.sock.close()
	server.db.close()

if __name__ == "__main__":
	main()

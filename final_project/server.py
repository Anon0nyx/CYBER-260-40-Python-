import sqlite3
import socket
import extra_functions as ef
import time

def configure_database():
	try:
		sqlConn = sqlite3.connect("./project_database.db")
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

class Server:
	def __init__(self, db):
		self.db = db
		self.sock = socket.socket()
		self.sock.bind(("localhost", 8080))
		self.sock.listen(5)
		self.client_sock, self.address = self.sock.accept()

	def create_user(self):
		print("Creating user (server)")
		data = self.client_sock.recv(4096)
		data = data.decode("utf-8")
		data = str(data)
		data = data.split(":")
		username = data[0]
		password = data[1]
		key = data[2]
		query = f"INSERT INTO client_info VALUES ('{username}', '{password}', '{key}');"
		print(query)
		search = self.db.execute(query)
		time.sleep(10)

	def login_user():
		data = self.client_sock.recv(4096)
		print(data)

	def upload_file():
		return 0

	def download_file():
		return 0

def main():
	print("Starting server.")
	db = configure_database()
	if not db:
		return 0
	server = Server(db)
	while True:
		data = server.client_sock.recv(5)
		data = data.decode('utf-8')
		data = str(data)
		print(data)
		print("CODE2")
		print(data == "CODE2")
		if data == "DONE":
			print("Done Receiving.")
			break
		elif data == "CODE2":
			server.create_user()
			server.client_sock.send(b"CODE2")
		elif data == "CODE1":
			server.login_user()
			server.client_sock.send(b"CODE1")
		elif data == "CODE3":
			server.upload_file()
		elif data == "CODE4":
			server.download_file()
		else:
			server.client_sock.send(b"CODE0")
	server.client_sock.send(b"Thank you for connecting.")
	server.client_sock.close()
	server.sock.close()

if __name__ == "__main__":
	main()

import sqlite3
import socket
import extra_functions as ef

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
	def __init__(self):
		self.sock = socket.socket()
		self.sock.bind(("localhost", 8080))
		self.sock.listen(5)
		self.client_sock, self.address = self.sock.accept()

	def create_user(self):
		print("Creating user (server)")
		data = self.client_sock.recv(4096)
		data = data.decode("utf-8")
		print(data)

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
	server = Server()
	while True:
		data = server.client_sock.recv(4096)
		data = data.decode('utf-8')
		data = str(data)
		if data == "DONE":
			print("Done Receiving.")
			break
		elif data == "CREATE":
			server.create_user()
			server.client_sock.send(b"CREATED")
		elif data == "LOGIN":
			server.login_user()
			server.client_sock.send(b"LOGGEDIN")
		elif data == "UPLOAD":
			server.upload_file()
		elif data == "DOWNLOAD":
			server.download_file()
	server.client_sock.send(b"Thank you for connecting.")
	server.client_sock.close()
	server.sock.close()

if __name__ == "__main__":
	while True:
		main()

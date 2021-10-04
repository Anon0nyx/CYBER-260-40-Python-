import socket
import extra_functions as ef

class socket_instance:
	def __init__(self, username, password):
		self.username = username
		self.password = password
		self.sock = socket.socket()
		self.sock.connect(("localhost", 8080))
		print("Connected to file server.")
		return 0

	def login(self):
		data = f"{self.sock.username}:{self.sock.password}"
		self.sock.send(data)
		return 0

def login():
	return 0

def main():
	user = login()
	conn = socket_instance("dforkey", "Testing!123")
	filetosend = open("test.txt", "rb")
	data = filetosend.read(4096)
	data = ef.encrypt(data)
	while data:
		print(data)
		print("Sending...")
		conn.sock.send(data)
		data = filetosend.read(4096)
	filetosend.close()
	sock.send(b"DONE")
	print("Done Sending.")
	print(sock.recv(1024))
	sock.close()

if __name__ == "__main__":
	main()

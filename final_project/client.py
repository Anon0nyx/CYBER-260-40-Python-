import socket
import extra_functions as ef

class socket_instance:
	def __init__(self, username, password):
		self.username = username
		self.password = password
		self.sock = socket.socket()
		try:
			self.sock.connect(("localhost", 8080))
			print("Connected to file server")
		except:
			print("Failed to connect to file server")

	def login(self):
		username = input("Enter username: ")
		password = input("Enter password: ")
		self.username = username
		self.password = password
		data = f"{self.username}:{self.password}"
		self.sock.send(data.encode('utf-8'))
		return 0

	def create_user(self):
		username = input("Enter username: ")
		password = input("Enter password: ")
		self.username = username
		self.password = password
		#keys = generate_keys()
		#pub_key = keys[1]
		pub_key = "testingkey"
		data = f"{self.username}:{self.password}:{pub_key}"
		self.sock.send(data.encode("utf-8"))
		return 0

	def upload_file(self):
		filename = input("Enter the filename to upload: ")
		filetosend = open(filename, "rb")
		self.sock.send(b"CODE3")

	def download_file(self):
		filename = input("Enter the filename to download: ")
		self.sock.send(b"CODE4")

	def check_ports():
		return 0

def main():
	conn = ""
	choice = input("""
	Login or Create Account
		1 - Login
		2 - Create account
: """)
	if choice == "1":
		conn = socket_instance("DEFAULT", "DEFAULT")
		conn.sock.send(b"CODE1")
		conn.login()
	elif choice == "2":
		conn = socket_instance("DEFAULT", "DEFAULT")
		conn.sock.send(b"CODE2")
		conn.create_user()

	print("Sent data")
	data = conn.sock.recv(4096)
	print(data)
	if data == b"CODE1" or data == b"CODE2":
		print("Logged in")
		logged_in = True
		while logged_in:
			option = input("""
		Please choose an option below
			1 - Upload a file
			2 - Download a file
			3 - Show files
			4 - Check ports
			5 - Log out
: """)
			if option == "1":
				conn.upload_file()
			elif option == "2":
				conn.download_file()
			elif option == "3":
				conn.show_files()
			elif option == "4":
				conn.check_ports()
			elif option == "5":
				logged_in = False
				conn.sock.send(b"DONE")
	elif data == b"CODE0":
		print("Incorrect username or password.")
		return 0
	else:
		print("Server error.")
		return 0
	
	logout = conn.sock.recv(4096)
	print(logout)

	conn.sock.close()

if __name__ == "__main__":
	main()

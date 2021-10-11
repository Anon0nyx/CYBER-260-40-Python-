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
		self.sock.send(b"LOGIN")
		data = f"{self.username}:{self.password}"
		self.sock.send(data.encode('utf-8'))
		return 0

	def create_user(self):
		self.sock.send(b"CREATE")
		data = f"{self.username}:{self.password}"
		self.sock.send(data.encode("utf-8"))
		return 0

	def upload_file(self):
		filename = input("Enter the filename to upload: ")
		filetosend = open(filename, "rb")
		self.sock.send(b"UPLOAD")

	def download_file(self):
		filename = input("Enter the filename to download: ")
		self.sock.send(b"DOWNLOAD")

	def check_ports():
		return 0

	def display_options():
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
				self.upload_file()
			elif option == "2":
				self.download_file()
			elif option == "3":
				self.show_files()
			elif option == "4":
				self.check_ports()
			elif option == "5":
				logged_in = False
				self.sock.send(b"DONE")

def login_or_create_user():
	choice = input("""
		Login or Create Account
			1 - Login
			2 - Create account
: """)
	if choice == "1":
		username = input("Enter username: ")
		password = input("Enter password: ")
		conn = socket_instance(username, password)
		conn.login()
		return conn
	elif choice == "2":
		username = input("Enter new username: ")
		password = input("Enter new password: ")
		conn = socket_instance(username, password)
		conn.create_user()
		return conn

def main():
	conn = ""
	choice = input("""
	Login or Create Account
		1 - Login
		2 - Create account
: """)
	if choice == "1":
		username = input("Enter username: ")
		password = input("Enter password: ")
		conn = socket_instance(username, password)
		conn.login()
	elif choice == "2":
		username = input("Enter new username: ")
		password = input("Enter new password: ")
		conn = socket_instance(username, password)
		conn.create_user()

	data = conn.sock.recv(4096)
	print(data)
	if data == b"LOGGEDIN":
		print("Logged in")
	elif data == b"CREATED":
		print("User created")
	elif data == b"LOGINFAILED":
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

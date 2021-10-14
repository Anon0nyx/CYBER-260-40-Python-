import socket
import time
import os
import encryption_functions as ef

DEBUG = True

class socket_instance:
	def __init__(self, username, password):
		self.username = username
		self.password = password
		
		self.priv_key = ""
		self.pub_key = ""
		self.sym_key = ""
		
		self.server_pub_key = ""
		self.server_sym_key = ""
		
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
		
		self.pub_key = open(f"./client/keys/{username}/{username}_pub.pem", "r").read()
		self.priv_key = open(f"./client/keys/{username}/{username}_priv.pem", "r").read()
		self.sym_key = open(f"./client/keys/{username}/{username}_sym.key", "rb").read()
		data = f"{self.username}:{self.password}:{self.pub_key}"
		self.sock.send(data.encode('utf-8'))
		
		return 0
	
	def set_personal_keys(self, key_list):
		self.pub_key = key_list[0]
		self.priv_key = key_list[1]
		self.sym_key = key_list[2]

	def create_user(self):
		username = input("Enter username: ")
		password = input("Enter password: ")
		self.username = username
		self.password = password
	
		os.system(f"mkdir ./client/keys/{username}")
		time.sleep(3)
		secret_keys = ef.generate_secret_keys(username)
		with open(f"./client/keys/{username}/{username}_sym.key", "wb") as sym_file:
			sym_file.write(secret_keys[2])

		self.set_personal_keys(secret_keys)

		data = f"{self.username}:{self.password}:{self.pub_key}"
		self.sock.send(data.encode("utf-8"))
			
		return 0

	def upload_file(self):
		filename = input("Enter the filename to upload: ")
		filetosend = open(f"./client/home/{filename}", "rb").read()
		data = ef.encrypt_data(filetosend, self.server_sym_key)
		self.sock.send(b"CODE4")
		result = self.sock.recv(5)
		if result == b"CODE4":
			self.sock.send(filename.encode("utf-8"))
		else:
			print("Upload failed")
			return 0
		result = self.sock.recv(5)
		if result == b"CODE4":
			self.sock.send(data)
		result = self.sock.recv(5)
		if result == b"CODE4":
			print("Upload successful")

	def download_file(self):
		filename = input("Enter the filename to download: ")
		self.sock.send(b"CODE5")
		result = self.sock.recv(5)
		if result == b"CODE5":
			self.sock.send(filename.encode("utf-8"))
			data = self.sock.recv(4096)
			data = ef.decrypt_data(data, self.sym_key)
			data = data.decode("utf-8")
			write_file = open(f"./client/home/{filename}.downloaded", "w")
			write_file.write(data)
			write_file.close()

	def check_ports(self):
		self.sock.send(b"CODE3")
		data = self.sock.recv(4096)
		print(data.decode("utf-8"))
		return 0

	def show_files(self):
		self.sock.send(b"CODE3")
		data = self.sock.recv(4096)
		print(data.decode("utf-8"))
		return 0

	def key_exchange(self):
		server_key = self.sock.recv(4096)
		#if DEBUG: print(f"Server pub key: {server_key}")
		if server_key == "CODE0":
			print("Login Failed")
			self.sock.send(b"DONE")
		self.server_pub_key = server_key
		
		encrypted_sym_key = ef.encrypt_key(self.sym_key, self.server_pub_key)
		self.sock.send(encrypted_sym_key)
		
		server_sym = self.sock.recv(4096)
		self.server_sym_key = ef.decrypt_key(server_sym, self.priv_key)
		if DEBUG: print(f"Server sym: {self.server_sym_key}")

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

	try:
		conn.key_exchange()
	except:
		print("Failed to login")
		conn.sock.send(b"DONE")
	data = conn.sock.recv(5)
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
	print(logout.decode())

	conn.sock.close()

if __name__ == "__main__":
	main()

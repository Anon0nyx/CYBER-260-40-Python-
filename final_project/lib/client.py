from lib import encryption_functions as ef
import os
import socket
import time

DEBUG = True

# Class that is our connection to the server
class socket_instance:
	# Init method to set and declare instance variables
	def __init__(self, username, password):
		# The client will have a username and password
		self.username = username
		self.password = password
		
		# As well as the three keys 
		self.priv_key = ""
		self.pub_key = ""
		self.sym_key = ""
		
		# The instance will also have a public and symmetric key for the server
		self.server_pub_key = ""
		self.server_sym_key = ""
		
		# The socket variable
		self.sock = socket.socket()
		
		# Creating a connecting to the server itself
		try:
			self.sock.connect(("localhost", 8080))
			print("Connected to file server")
		except:
			print("Failed to connect to file server")

	# Method to log the user into the server 
	def login(self):
		# Collect the username and password
		username = input("Enter username: ")
		password = input("Enter password: ")
		self.username = username
		self.password = password
		
		# Attempt to open the keys, if they dont exist, the user probably doesnt exist
		try:
			self.pub_key = open(f"./client/keys/{username}/{username}_pub.pem", "r").read()
			self.priv_key = open(f"./client/keys/{username}/{username}_priv.pem", "r").read()
			self.sym_key = open(f"./client/keys/{username}/{username}_sym.key", "rb").read()
			data = f"{self.username}:{self.password}:{self.pub_key}"
			self.sock.send(data.encode('utf-8'))
		except:
			self.sock.send(b"FAIL")
			print("Login failed due to non-existant key files")
		return 0

	# Method to create a new user
	def create_user(self):
		# Imbedded method to set the clients keys
		def set_personal_keys(key_list):
			self.pub_key = key_list[0]
			self.priv_key = key_list[1]
			self.sym_key = key_list[2]
		
		# Collect the username and password
		username = input("Enter username: ")
		password = input("Enter password: ")
		self.username = username
		self.password = password
	
		# Create a new directory for the client to hold their keys 
		os.system(f"mkdir ./client/keys/{username}")
		time.sleep(3)
		# Generate the clients keys (RSA and symmetric)
		secret_keys = ef.generate_secret_keys(username)
		with open(f"./client/keys/{username}/{username}_sym.key", "wb") as sym_file:
			sym_file.write(secret_keys[2])
		set_personal_keys(secret_keys)
	
		# Send data to the server
		data = f"{self.username}:{self.password}:{self.pub_key}"
		self.sock.send(data.encode("utf-8"))
			
		return 0

	# Method to upload files to the server
	def upload_file(self):
		# Collect and open file
		filename = input("Enter the filename to upload: ")
		filetosend = open(f"./client/home/{filename}", "rb").read()
		# Encrypt the file data with the symmetric key
		data = ef.encrypt_data(filetosend, self.server_sym_key) 
		self.sock.send(b"CODE4") # Tell the server to get ready for file
		result = self.sock.recv(5) # Get response
		if result == b"CODE4":
			self.sock.send(filename.encode("utf-8")) # If the server is good, send the filename so the server can create the write file
		else:
			print("Upload failed")
			return 0
		result = self.sock.recv(5)
		if result == b"CODE4":
			self.sock.send(data) # Once the server has the filename, send it the file contents
		result = self.sock.recv(5)
		if result == b"CODE4":
			print("Upload successful")

	# Method to download a file from the server
	def download_file(self):
		# Collect filename and let server know we want to download a file
		filename = input("Enter the filename to download: ")
		self.sock.send(b"CODE5")
		result = self.sock.recv(5)
		if result == b"CODE5":
			self.sock.send(filename.encode("utf-8")) # If the server is ready, send the name of the file
			data = self.sock.recv(4096) # Receive the file contents, currently limited in size
			data = ef.decrypt_data(data, self.sym_key) # Decrypt the file data and write it to a .downloaded file in the downloads directory
			data = data.decode("utf-8")
			write_file = open(f"./client/home/downloads/{filename}.downloaded", "w")
			write_file.write(data)
			write_file.close()
			print("File download successful.")

	# Method to show the files the user has on the server
	def show_files(self):
		self.sock.send(b"CODE3")
		data = self.sock.recv(4096)
		print(f"Server files: {data.decode('utf-8')}")
		local = os.listdir("./client/home")
		print(f"Local files: {local}")
		return 0

	# Key exchange to get the symmetric keys passed in a secure manor
	"""
		Essentially, the logic here is that the client has already send their pub key to the server
		 the server will then send its pub key to the client and the client will use this to encrypt
		 their symmetric key, they will then send their symmetric key and the server will use its private
		 key to decrypt the symmetric key; then the server will encrypt its symmetric key with the 
		 client pub key (Received first) and send this to the client where it will be decrypted with the
		 clients private key. This process ensures the symmetric key, which is used for file encryption, 
		 is encrypted end-to-end
	"""
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



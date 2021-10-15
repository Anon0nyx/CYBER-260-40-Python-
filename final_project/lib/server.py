import socket
import os
from lib import encryption_functions as ef

# Function to check the database for a given user
def check_db_user(conn, username):
	search = f"SELECT Username FROM client_info WHERE Username='{username}'"
	search = conn.execute(search)
	result = search.fetchone()
	print(result)
	if result:
		return True
	else:
		return False

# Server class used to instantiate a client connection
class Server:
	# init method 
	def __init__(self, db):
		self.db = db # Set servers db

		# Declare client keys
		self.client_pub_key = ""
		self.client_sym_key = ""
		
		# Declare self keys
		self.priv_key = ""
		self.pub_key = ""
		self.sym_key = ""

		# Declare login info dictionary
		self.login_info = {"logged_in": False,
							"username": None}
		# Initialize socket connections
		self.sock = socket.socket()
		self.sock.bind(("localhost", 8080))
		self.sock.listen(5)
		self.client_sock, self.address = self.sock.accept()

	# Method to configure the servers keys by opening the respected files
	def configure_keys(self):
		print("Configuring server keys.")
		self.pub_key = str(open("./server/keys/server_keys.pub", "r").read())
		self.priv_key = str(open("./server/keys/server_keys", "r").read())
		self.sym_key = open("./server/keys/server_keys.sym", "rb").read() 

	# Key exchange function (Server side), serves same purpose as the client side
	def key_exchange(self):
		self.client_sock.send(self.pub_key.encode("utf-8"))	
		sym_key = self.client_sock.recv(4096)	
		self.client_sym = ef.decrypt_key(sym_key, self.priv_key)
		print(f"Client SYM: {self.client_sym}")
		self.client_sock.send(ef.encrypt_key(self.sym_key, self.client_pub_key))
	
	# Create user method
	def create_user(self):
		print("Creating user (server)")
		conn = self.db.cursor()
	
		# Receive new user data
		data = self.client_sock.recv(4096)
		data = data.decode("utf-8")
		data = str(data)
		data = data.split(":")
		print(data)

		# Parse this data properly
		username = data[0]
		password = data[1]
		
		key = data[2]
		# Clean the key
		key = key.replace("b'", "")
		key = key.replace("'", "")
		self.client_pub_key = key

		# Check if the user exists
		user_exist = check_db_user(conn, username)
		
		if user_exist:
			print("User exists")
			self.client_sock.send(b"EXIST")
			return False
		else:
			self.key_exchange() # Key exchange and then create the new user
			query = f"INSERT INTO client_info VALUES ('{username}', '{password}', '{username}_pub.pem');"

			search = conn.execute(query)
			
			os.system(f"mkdir ./server/folder_clients/{username}")
			
			self.db.commit()
			
			self.login_info["username"] = username
			self.login_info["logged_in"] = True

			return True
		# if the login was successful	
		if self.login_info["logged_in"]:
			key_file = open(f"./folder_clients/{self.login_info['username']}_pub.pem", "w")
		
			key_file.write(key)
			key_file.close()
		else:
			return False

	# Method to find files for user and send a list of these files
	def list_files(self):
		files = os.listdir(f"./server/folder_clients/{self.login_info['username']}/")
		self.client_sock.send(str(files).encode("utf-8"))

	# Method to log a user into the server
	def login(self):
		# Collect the user data
		data = self.client_sock.recv(4096)
		data = data.decode("utf-8")
		data = str(data).split(":")
		
		# Parse the users data
		username = data[0]
		password = data[1]
		self.client_pub_key = data[2]
		conn = self.db.cursor() # Create a cursor db object 

		# Create and execute our database query
		query = f"SELECT * FROM client_info WHERE Username='{username}' AND Password='{password}'"
		search = conn.execute(query)

		result = search.fetchone()
		# Test if there are any results
		if result:
			self.login_info["username"] = username
			self.login_info["logged_in"] = True
			self.key_exchange()
			return True
		else:
			return False

	# Method to upload a file to the server
	def upload_file(self):
		self.client_sock.send(b"CODE4")
		filename = self.client_sock.recv(52).decode("utf-8") # Receive filename
		self.client_sock.send(b"CODE4")
		data = self.client_sock.recv(4096) # Receive file data
		data = ef.decrypt_data(data, self.sym_key) # Decrypt the data with server key
		data = ef.encrypt_data(data, self.client_sym) # Re-encrypt the data client key
		self.client_sock.send(b"CODE4")
		with open(f"./server/folder_clients/{self.login_info['username']}/{filename}", "wb") as data_file:
			data_file.write(data) # Create file with filename and write encrypted data
		
		return 0

	# Method to download a file from the server
	def download_file(self):
		self.client_sock.send(b"CODE5")
		filename = self.client_sock.recv(52).decode("utf-8") # Receive the filename
		data = ""
		with open(f"./server/folder_clients/{self.login_info['username']}/{filename}", "rb") as data_file:
			data = data_file.read() # Put the file data into a variable
		self.client_sock.send(data) # Send this data to the client

		return 0


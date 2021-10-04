import socket # We need our socket functions
# This is the client function, used for sending the mbr info to the server
class Client:
	# Declaring the host and port variables
	host = '127.0.0.1'
	port = 5000
	def __init__(self):
		try:
			self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Creating our socket
		except socket.error as err:
			print('Socket failed with error: ' + str(err))
			return 1

	# Method for sending chunk of data to host
	def send_data(self, data):
		try:
			self.sock.connect((Client.host, Client.port)) # Create locatlhost:8080 connection
			self.sock.send(data) # Send our data
		except socket.error as err:
			print('Error sending sector data with error: ' + str(err))
			return 1

# The main function
def main():
	mbr = bytearray() # Declare the MBR variable, open and read the MBR into the variable
	try:
		binary = open('./block.dd', 'rb')
	except IOError as err:
		print('File not found: ' + str(err))
		return 1
	mbr = binary.read(512)
	
	# Collect our 15 byte sector from the MBR
	sector = bytearray(mbr[0x1BE:0x1CD])

	# Initialize the Client object and send the sector collected
	client = Client()
	print("[+] Sending sector data")
	client.send_data(sector)
	print("[+] Data sent successfully")
	# Once the data is sent, close the socket connection
	client.sock.close()

if __name__ == '__main__':
	main()

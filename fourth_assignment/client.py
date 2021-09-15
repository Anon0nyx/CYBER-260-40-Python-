import socket
# This is the client function, used for sending the mbr info to the server
class Client:
	host = '127.0.0.1'
	port = 8080
	def __init__(self):
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	def send_data(self, data):
		self.sock.connect((Client.host, Client.port))
		self.sock.send(data)

def main():
	mbr = bytearray()
	binary = open('./block.dd', 'rb')
	mbr = binary.read(512)
	
	sector = bytearray(mbr[0x1BE:0x1CD])

	# Initialize the Client object and send the sector collected
	client = Client()
	client.send_data(sector)
	# Once the data is sent, close the socket connection
	client.sock.close()

if __name__ == '__main__':
	main()

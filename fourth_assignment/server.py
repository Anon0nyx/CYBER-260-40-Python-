# Name:    Dylan
# To:      Instructor, CYBER-260-40
# Program: Create server and client where client sends first entry of mbr to server and server prints info
# Date:	   Sept 15th, 2021
import socket
import struct
class Server:
	# Initialize the host and port variables which are always localhost and 8080
	host = '127.0.0.1'
	port = 8080

	# Init function for instance variables
	def __init__(self):
		self.sector = bytearray() # Initialize the sector we are going to receive
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create our socket

	def parse_mbr(self, sector):
		print('Status flag: ' + str(hex(sector[0x00])))
		print('Partition type: ' + str(hex(sector[0x04])))
		partition_addr = struct.unpack('I', sector[0x08:0x0C])
		partition_addr = partition_addr[0]
		partition_addr = str(partition_addr)
		print('Partition address: ' + partition_addr)

	def receive_data(self):
		self.sock.bind((Server.host, Server.port))
		self.sock.listen(1)
		con, addr = self.sock.accept()
		data = bytearray(con.recv(15))
		self.parse_mbr(data)

def main():
	server = Server()
	server.receive_data()

if __name__ == '__main__':
	main()

import socket
import extra_functions as ef

def main():
	sock = socket.socket()
	sock.bind(("localhost", 5000))
	sock.listen(5)
	client_sock, address = sock.accept()
	filetodown = open("newtest.txt", "wb")

	while True:
		print("Receiving....")
		data = client_sock.recv(4096)
		if data == b"DONE":
			print("Done Receiving.")
			break
	filetodown.write(data)
	filetodown.close()
	client_sock.send(b"Thank you for connecting.")
	client_sock.close()
	sock.close()

if __name__ == "__main__":
	main()

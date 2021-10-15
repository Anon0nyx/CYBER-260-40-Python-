import socket
import subprocess
import time
import pyfiglet
from lib import client as cl

# Function to check open ports of provided IPv4 address
def check_ports():
	# Gather target information and print banner
	target = input("Enter IPv4 address to scan: ")
	banner = pyfiglet.figlet_format("SCANNING PORTS")
	print(banner)
	print("-" * 75)
	print(f"Scanning IPv4: {target}")
	print("-" * 75)
	# For each port in our range, check if it is open by attempting a socket connection
	try:
		socket.setdefaulttimeout(.5)
		count = 0
		for port in range(1,65535):
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # create the connection
			result = s.connect_ex((target, port)) # attempt port connection
			if result == 0:
				print(f"Port {port} is open") # Print result to screen if port is open
			s.close()
			if port % 1000 == 0:
				print(f"Progress: %{port/65535}")
	except socket.error:
		print("Socket error")
	except KeyboardInterrupt:
		print(f"Scan halted on port {port}")

def main():
	conn = ""
	# Not the cleanest main file, pretty redundant but below handles the users first choice
	choice = input("""
	Login or Create Account
		1 - Login
		2 - Create account
: """)
	if choice == "1":
		conn = cl.socket_instance("DEFAULT", "DEFAULT")
		conn.sock.send(b"CODE1")
		conn.login()
	elif choice == "2":
		conn = cl.socket_instance("DEFAULT", "DEFAULT")
		conn.sock.send(b"CODE2")
		conn.create_user()

	# Once the user has either logged in or created a user, the key exchange begins
	try:
		conn.key_exchange()
	except:
		print("Key exchange failed")
		conn.sock.send(b"DONE") # If the exchange fails print that and send logoff signal
	
	try:
		# Recieve data after key exchange
		data = conn.sock.recv(5)
	except:
		print("Failed to receive data")
	if data == b"CODE1" or data == b"CODE2":
		print("Logged in")
		logged_in = True
		# For some reason, modulating the section below breaks the code, so it cannot be in a function
		while logged_in: # While the user is logged in, present them with their options
			option = input("""
		Please choose an option below
			1 - Upload a file
			2 - Download a file
			3 - Show files
			4 - Check ports
			5 - Log out
: """)
			subprocess.run(["clear"])
			if option == "1":
				conn.upload_file()
			elif option == "2":
				conn.download_file()
			elif option == "3":
				conn.show_files()
			elif option == "4":
				check_ports()
			elif option == "5":
				logged_in = False
				try:
					conn.sock.send(b"DONE")
				except:
					print("Failed to send logoff code")
	elif data == b"CODE0":
		print("Incorrect username or password.")
		return 0
	else:
		print("Server error.")
		return 0
	
	# If the server sends the logoff signal print it
	try:
		logout = conn.sock.recv(4096)
		print(logout.decode())
	except:
		print("Failed to receive logoff message")

	# Close the connection to the server
	conn.sock.close()

if __name__ == "__main__":
	main()

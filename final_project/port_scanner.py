import socket
import time
import pyfiglet

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
		socket.setdefaulttimeout(.25)
		for port in range(1,65535):
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # create the connection
			result = s.connect_ex((target, port)) # attempt port connection
			if result == 0:
				print(f"Port {port} is open") # Print result to screen if port is open
			s.close()
			#if port % 100 == 0:
				#print(f"Progress: %{100*(port/65535)}")
	except socket.error:
		print("Socket error")
	except KeyboardInterrupt:
		print(f"Scan halted on port {port}")

check_ports()

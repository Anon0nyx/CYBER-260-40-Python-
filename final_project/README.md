# Final Project: 
# Encrypted file-server
The primary function of this project is to create a baseline client-server interaction which allows a client to upload and download files 
from the server in a fully end-to-end encrypted way where the files maintain their encryption during the time they are stored on the server
# Use
To start, you must ensure you run the command:
	```
		source venv/bin/activate
	```
to enter the projects environment which has all of the dependencies. That is the only major requirement before running either program.
# Server
Essentially, ensure port 8080 is open on your machine and then: python3 server.py
The server will handle the rest, although currently the server is only good for one interaction at a time and when this interaction ends
the server itself also shuts down. I have been unable to find a way to keep the server open to reconnection from the client after the
client disconnects.
# Client
Once the server is running successfully you are able to simply do: 
	```
	python3 client.py
	```
Once the client is running you can either create a new user or login as the only existing user:
	```
	username: tester
	password: Testing123
	```
Once the user is logged in a menu will be displayed on the terminal awaiting numerical input depending on the users choice

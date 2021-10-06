# Name:		Dylan
# To:		Instructor, CYBER-260-40
# Program:	Open the History.db database and pull the urls visited as well as the number of times visited and the date of the last vistir
# Date:		Oct 6rd, 2021
import os
import sqlite3

def print_data(data):
	# For each collected row
	for row in data:
		# Print the data in a formatted way
		print("Url: %s\nVisit Count: %s\nLast Time Visited: %s\n\n" % (row[0], row[1], row[2]))

def create_array(data):
	# Create an array containing each row from the data
	return [row for row in data]

def open_db(filepath):
	try:
		# Try to open the sqlite database based on the filepath provided
		sqlConn = sqlite3.connect(filepath)
	except:
		# If the database is unavailable, handle this
		print("Database unavailable")
		return 0
	print("Database opened successfully")
	# If the database opens successfully, return this value
	return sqlConn

def main():
	# Create the databae object
	db = open_db("History.db")

	# Search the database for our data and store this data
	search = db.execute("SELECT url, visit_count, last_visit_time FROM urls")
	# Create an array out of the data collected
	data = create_array(search)

	# Print the data
	print_data(data)

if __name__ == "__main__":
	main()

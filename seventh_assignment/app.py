# Name:		Dylan Forkey
# To:		Instructor, CYBER-260-40
# Subject:	This progam is meant to navigate to the domain catalog.champlain.edu
#			and pull all of the <a tags and parse out the href={url} section
#			to collect and upload the urls to the database
# Date:		Oct. 15th, 2021
import requests
import re
import sqlite3
import datetime

# Function to refine the line down to the url itself
def refine_line(db_row):
	db_row = db_row.rstrip()
	db_row = db_row.split('href="')
	db_row = db_row[1].split('"')
	return db_row[0]

# Function to collect the urls from the domain
def collect_urls(data):
	new_data = []
	try:
		for line in data.text.split("\n"):
			if re.search("<a", line):
				line = refine_line(line)
				new_data.append(line)

	except UnicodeDecodeError:
		return new_data

	return new_data

# Using requests lib to get url contents
def gather_webpage(url):
	return requests.get(url)

# Determine if the sqlite3 table exists, if not create it
def create_table(db):
	result = db.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='storage';")
	if not len(str(result)):
		print("Table not found, creating")	
		result = sqlConn.execute("CREATE TABLE storage(curtime TEXT, url TEXT)")
	else:
		print("Table found")
	return db

# Initialize the database at the given path
def initialize_db(filepath):
	try:
		sqlConn = sqlite3.connect(filepath)
	except:
		print("Db unavailable")
		return 0
	# Create the necessary table
	create_table(sqlConn)
	# Clear the storage as the domain is always the same
	sqlConn.execute("DELETE FROM storage;")
	return sqlConn

# Put the domain and cur time into the database
def put_in_db(db, current_time, url):
	conn = db.cursor()
	print(f"INSERTING: %s || %s" % (current_time, url))
	conn.execute("INSERT INTO storage(curtime, url) VALUES ('%s', '%s');" % (current_time, url))
	db.commit()

# Main funcation
def main():
	# Initialize the database
	db = initialize_db("./week7.db")
	# Collect web page
	response = gather_webpage("https://catalog.champlain.edu/")

	# Collect the urls from the page provided
	url_list = collect_urls(response)
	for url in url_list: # For each of these urls
		current_time = datetime.datetime.now().time()
		put_in_db(db, current_time, url)

if __name__ == "__main__":
	main()

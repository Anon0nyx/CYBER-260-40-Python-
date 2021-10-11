import requests
import re
import sqlite3
import datetime

def refine_line(db_row):
	db_row = db_row.rstrip()
	db_row = db_row.split('href="')
	db_row = db_row[1].split('"')
	return db_row[0]

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

def gather_webpage(url):
	return requests.get(url)

def create_table(db):
	result = db.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='storage';")
	if not len(str(result)):
		print("Table not found, creating")	
		result = sqlConn.execute("CREATE TABLE storage(curtime TEXT, url TEXT)")
	else:
		print("Table found")
		return db
	return db

def initialize_db(filepath):
	try:
		sqlConn = sqlite3.connect(filepath)
	except:
		print("Db unavailable")
		return 0
	create_table(sqlConn)
	sqlConn.execute("DELETE FROM storage;")
	return sqlConn

def put_in_db(db, current_time, url):
	print(f"%s\n%s\n" % (current_time, url))
	db.execute("INSERT INTO storage(curtime, url) VALUES (%s, %s);" % (current_time, url))

def main():
	db = initialize_db("./week7.db")	
	response = gather_webpage("https://catalog.champlain.edu/")

	url_list = collect_urls(response)
	for url in url_list:
		current_time = datetime.datetime.now().time()
		put_in_db(db, current_time, url)

if __name__ == "__main__":
	main()

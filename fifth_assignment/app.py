# Name:		Dylan
# To:		Instructor, CYBER-260-40
# Program:	Create two registry keys, store user input and current time in the first and cwd in the second
# Date:		Oct 3rd, 2021
import winreg
import sys
import os
from datetime import datetime

def main():
	# Variable assignment
	userValue = str(input("Enter a value for the registry: "))
	now = datetime.now()
	time = now.strftime("%H:%M:%S")
	cwd = os.getcwd()


	# Create user value key and input user value 
	try:
		firstKey = winreg.CreateKey(winreg.HKEY_CURRENT_USER, "Software\\" + "userInput")
	except WindowsError as err:
		print("Failed to create input key: " + err)
	try:
		winreg.SetValue(firstKey, "input", winreg.REG_SZ, userValue)
		# Using the same key as the user input, create the value time and set it to the time
		winreg.SetValue(firstKey, "time", winreg.REG_SZ, time)
	except WindowsError as err:
		print("Failed to set registry values: " + err)
	# Create cwd key and input the cwd into this key
	try:
		secondKey = winreg.CreateKey(winreg.HKEY_CURRENT_USER, "Software\\" + "cwd")
	except WindowsError as err:
		print("Failed to create wd key: " + err)
	try:
		winreg.SetValue(secondKey, "cwd", winreg.REG_SZ, cwd)
	except WindowsError as err:
		print("Failed to set registry value: " + err)

	# Collect each of the values from the registry
	userInput = winreg.QueryValue(firstKey, "input")
	time = winreg.QueryValue(firstKey, "time")
	cwd = winreg.QueryValue(secondKey, "cwd")
	# Print these values to the screen
	print(userInput)
	print(time)
	print(cwd)

if __name__ == "__main__":
	main()

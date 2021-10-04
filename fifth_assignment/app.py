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
		foo = winreg.CreateKey(winreg.HKEY_CURRENT_USER, "Software\\" + "userInput")
	except WindowsError as err:
		print("Failed to create input key: " + err)
	try:
		winreg.SetValue(foo, "input", winreg.REG_SZ, userValue)
		# Using the same key as the user input, create the value time and set it to the time
		winreg.SetValue(foo, "time", winreg.REG_SZ, time)
	except WindowsError as err:
		print("Failed to set registry values: " + err)
	# Create cwd key and input the cwd into this key
	try:
		bar = winreg.CreateKey(winreg.HKEY_CURRENT_USER, "Software\\" + "cwd")
	except WindowsError as err:
		print("Failed to create wd key: " + err)
	try:
		winreg.SetValue(bar, "cwd", winreg.REG_SZ, cwd)
	except WindowsError as err:
		print("Failed to set registry value: " + err)
	userInput = winreg.QueryValue(foo, "input")
	time = winreg.QueryValue(foo, "time")
	cwd = winreg.QueryValue(bar, "cwd")
	print(userInput)
	print(time)
	print(cwd)

if __name__ == "__main__":
	main()

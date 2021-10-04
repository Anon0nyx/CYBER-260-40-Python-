import winreg
import sys
import os
import datetime

def main():
	# Variable assignment
	userValue = str(input("Enter a value for the registry: "))
	now = datetime.now()
	time = now.strftime("%H:%M:%S")
	cwd = os.getcwd()


	# Create user value key and input user value 
	try:
		key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, "Software\\" + "userInput")
	except WindowsError as err:
		print("Failed to create input key: " + err)
	try:
		winreg.SetValue(key, "input", winreg.REG_SZ, userValue)
		# Using the same key as the user input, create the value time and set it to the time
		winreg.SetValue(key, "time", winreg.REG_SZ, time)
	except WindowsError as err:
		print("Failed to set registry values: " + err)
	# Create cwd key and input the cwd into this key
	try:
		key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, "Software\\" + "cwd")
	except WindowsError as err:
		print("Failed to create wd key: " + err)
	try:
		winreg.SetValue(key, "AValue", winreg.REG_SZ, cwd)
	except WindowsError as err:
		print("Failed to set registry value: " + err)

if __name__ == "__main__":
	main()

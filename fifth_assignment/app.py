import winreg
import sys
import os

def main():
	keyName = "userInput"
	userValue = str(input("Enter a value for the registry: "))

	key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, "Software\\" + keyName)
	winreg.SetValue(key, "AValue", winreg.REG_SZ, userValue)
	response = winreg.QueryValue(key, "AValue")

	print(response)

if __name__ == "__main__":
	main()

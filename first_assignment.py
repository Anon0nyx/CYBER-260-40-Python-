import sys

# Function: main
# Purpose: primary functions for program
# Inputs: None
# Returns: 1 or 0 depending on errors
def main():
	if len(sys.argv) <= 1:
		get_help()
		return 1
	data = sys.argv
	
	name, num1, num2, num3 = str(data[1]), int(data[2]), int(data[3]), int(data[4])

	add = num1 + num2 + num3
	mult = num1 * num2 * num3
	div = (num1 / num2) * num3

	print("Hello " + name + ", the results are:")
	print("Addition: " + str(add))
	print("Multiplication: " + str(mult))
	print("Divide first 2 multiple by third: " + str(div))
	return 0

# Function: get_help
# Purpose: Provide user with guide to use program
# Inputs: None
# Returns: 1 because only called if error occurs
def get_help():
	print("\n\tProper use: python3 first_assignment.py [NAME] [NUM ONE] [NUM TWO] [NUM THREE]\n")
	return 1

# Call main function
if __name__ == '__main__':
	main()

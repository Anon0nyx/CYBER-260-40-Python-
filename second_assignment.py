def main():
	grades = input('Enter grades: ')

	# Check data
	grades = check_data(grades, 6)
	if grades == 1: return 1

	# Collect initial average
	avg = average(grades)
	print('Average: ' + str(avg))

	try:
		count = int(input('How many grades do you have total: '))
	except ValueError:
		print('\n\tEnter a number of grades\n')
		return 
	if count < 6: 
		print('\n\tMust have at least 6 grades\n')
		return 1
	grades = input('Enter grades: ')
	
	# Check data
	grades = check_data(grades, count)
	if grades == 1: return 1
	
	avg = average(grades)
	print("All Grade Average: " + str(avg))
	return 0


# Function: average
# Purpose: provide the average of the number list given
# Input: grades, a list containing the grades
# Output: avg, integer that is the average of the grades list
def average(grades):
	avg = 0
	for grade in grades:
		avg += grade
	avg = avg/len(grades)
	return avg

# Function: check_data
# Purpose: Sanatize the input data
# Inputs: grades, count		the grade list and the length of the list
# Returns: 1 or 0 depending upon the data
def check_data(grades, count):
	if ',' not in grades:
		print('\n\tEnsure to use a comma delimiter\n\ti.e. 89,78,97,88,98, etc..\n')
		return 1
	elif len(grades.split(',')) != count:
		print('\n\tEnsure you enter the correct number of grades\n')
		return 1

	# Alter data and re-check before returning
	grades = grades.split(',')
	try:
		grades = [int(grade) for grade in grades]
	except ValueError:
		print('\n\tEnter numerical grades\n')
		return 1
	for grade in grades:
		if (grade > 100 or grade < 0): 
			print('\n\tEnsure grades are < 100 and > 0\n')
			return 1
	return grades

if __name__ == '__main__':
	main()

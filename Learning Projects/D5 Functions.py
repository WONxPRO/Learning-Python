# First Function Study
def HelloName(name):
	print(f"Hello {name}!")
	
print("This is Case 1 of the Function Study.")
name = input("What is your name?: ")
HelloName(name)

#------------------------------------------------

# Second Function Study
def WordNumber(word, number):
	print(f"The word is {word}.")
	print(f"The number is {number}.")
	
print("\nThis is Case 2 of the Function Study.")
print("Possibility 1")
WordNumber("Among", 67)

print("Possibility 2")
WordNumber(69, "AmongUs")

#------------------------------------------------

# Third Function Study
def Square(number):
	return number * number

print("\nThis is Case 3 of the Function Study.")
number = float(input("Enter a number to be squared: "))
result = Square(number)
print(f"The square of {number} is {result}.")


#------------------------------------------------

# Fourth Function Study
def CalculateArea(length, width):
	area = length * width
	return area

print("\nThis is Case 4 of the Function Study.")
length = float(input("Enter the length: "))
width = float(input("Enter the width: "))
result = CalculateArea(length, width)
print(f"The area of the rectangle is {result}.")

#------------------------------------------------

# Fifth Function Study
def IsEven(number):
	if number % 2 == 0:
		return True
	else:
		return False
	
print("\nThis is Case 5 of the Function Study.")
number = int(input("Enter a number to check if it's even: "))
if IsEven(number):
	print(f"{number} is even.")
else:
	print(f"{number} is not odd.")

#------------------------------------------------

# Sixth Function Study
def Addition(num1, num2):
	return num1 + num2
def Subtraction(num1, num2):
	return num1 - num2
def Multiplication(num1, num2):
	return num1 * num2
def Division(num1, num2):
	if num2 != 0:
		return num1 / num2
	else:
		return "Error: Division by zero is not allowed."
def Modulus(num1, num2):
	if num2 != 0:
		return num1 % num2
	else:
		return "Error: Modulus by zero is not allowed."
	
print("\nThis is Case 6 of the Function Study.")
num1 = float(input("Enter the first number: "))
num2 = float(input("Enter the second number: "))
print(f"Addition: {num1} + {num2} = {Addition(num1, num2)}")
print(f"Subtraction: {num1} - {num2} = {Subtraction(num1, num2)}")
print(f"Multiplication: {num1} * {num2} = {Multiplication(num1, num2)}")
print(f"Division: {num1} / {num2} = {Division(num1, num2)}")
print(f"Modulus: {num1} % {num2} = {Modulus(num1, num2)}")

#------------------------------------------------

# Seventh Function Study
def StudentGrade(grade):
	if grade > 100:
		return "Invalid grade. Grade must be between 0 and 100."
	elif 100 >= grade >= 90:
		return "A"
	elif 89 >= grade >= 80:
		return "B"
	elif 79 >= grade >= 70:
		return "C"
	elif 69 >= grade >= 60:
		return "D"
	else:
		return "F"
	
print("\nThis is Case 7 of the Function Study.")
grade = float(input("Enter the student's grade: "))
result = StudentGrade(grade)
print(f"The student's grade is: {result}")
# Comparison Operators
# This program demonstrates the use of comparison operators in Python.
# It prompts the user to enter a number and then compares that number to 20 using various comparison operators.

num1 = input("Enter first number: ")

print(f"First number is smaller than 20: {int(num1) < 20}")                 # Uses the operator '<' to check if num1 is less than 20
print(f"First number is greater than 20: {int(num1) > 20}")                 # Uses the operator '>' to check if num1 is greater than 20
print(f"First number is equal to 20: {int(num1) == 20}")                    # Uses the operator '==' to check if num1 is equal to 20
print(f"First number is not equal to 20: {int(num1) != 20}")                # Uses the operator '!=' to check if num1 is not equal to 20
print(f"First number is smaller than or equal to 20: {int(num1) <= 20}")    # Uses the operator '<=' to check if num1 is less than or equal to 20
print(f"First number is greater than or equal to 20: {int(num1) >= 20}")    # Uses the operator '>=' to check if num1 is greater than or equal to 20
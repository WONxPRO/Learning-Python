# This program checks the grade input by the user and prints out the corresponding letter grade.
grade = int(input("Input your grade: ")) # Asks the user to input their grade and converts it to an integer.

if 90 <= grade <= 100:          # Checks if the grade is between 90 and 100 (inclusive) and prints "Your grade is A" if true.
    print("Your grade is A")
elif 80 <= grade < 90:          # Checks if the grade is between 80 and 89 (inclusive) and prints "Your grade is B" if true.
    print("Your grade is B")
elif 70 <= grade < 80:          # Checks if the grade is between 70 and 79 (inclusive) and prints "Your grade is C" if true.
    print("Your grade is C")
else:                           # If the grade is below 70, it prints "Your grade is D".
    print("Your grade is D")
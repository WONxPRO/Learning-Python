#-------------------------------------------------------------------------------
# 1 Variables & Data Types
print("Variables & Data Types Review")
name = "Nathan" # string variable
age = 17        # integer variable
college = True  # boolean variable
braincell = 2.3 # float variable

print(type(name))      # <class 'str'>
print(type(age))       # <class 'int'>
print(type(college))   # <class 'bool'>
print(type(braincell)) # <class 'float'>
# Output will be the data type of each variable.

print("\nArithmetic Operations Review")
x = 10      # Declares a variable x and assigns it the value 10 (integer) 
x = x + 5   # Adds 5 to the current value of x and assigns the result back to x (x is now 15)
x *= 2      # Multiplies the current value of x by 2 and assigns the result back to x (x is now 30)
print(f"x = {x}")      # Prints the current value of x (30)
#-------------------------------------------------------------------------------
# 2 Input & Output
print("\nInput & Output Review")
name = input("Input username: ") # Prompts the user to input their username and assigns it to the variable name
age = input("Input age: ")       # Prompts the user to input their age and assigns it to the variable age
print(f"Hello {name}, you are {age} years old.") # Prints a greeting

#-------------------------------------------------------------------------------
# 3 Conditional Statements
print("\nConditional Statements Review")
score = 75          # Declares a variable score and assigns it the value 75 (integer)

if score >= 80:     # First parameter checks if score is greater than or equal to 80, if true it will print "A"
    print("A")      
elif score >= 70:   # Second parameter checks if score is greater than or equal to 70, if true it will print "B"
    print("B")
else:               # Last parameter is the default case, if score is less than 70 it will print "C"
    print("C")

print("\n Age Legality Checker")
age = int(input("Input your current age: "))  # Prompts the user to input their current age and converts it to an integer

if age >= 18:                                 # First parameter checks if age is greater than or equal to 18, if true it will print "You are an adult."
    print("You are an adult.")                # Announces that the user is an adult if the condition is met
else:                                         # Last parameter is the default case, if age is less than 18 it will print "You are a minor."
    print("You are a minor.")                 # Announces that the user is a minor if the condition is met

#-------------------------------------------------------------------------------
# 4 Loops
print("\nLoops Review")
for i in range(5):  # Loops for 5 iterations, starting from 0 to 4 (inclusive)
    print(i)        # Prints the current value of i in each iteration (0, 1, 2, 3, 4)


count = 3           # Declares a variable count and assigns it the value 3 (integer)

while count > 0:    # Loops while the value of count is greater than 0
    print(count)    # Prints the current value of count in each iteration
    count -= 1      # Decreases the value of count by 1 in each iteration (count is now 2, then 1, then 0)
# After every iteration, the value of count decreases by 1, where when it reaches 0 the loop will stop.

# Creating a loop that prints 1-5 
for j in range(5):
    print(j+1)

#-------------------------------------------------------------------------------
# 5 Functions
print("\n Function Review")

def greet(name):            
    return f"Hello {name}"

print(greet("Nathan"))
# Outputs "Hello Nathan"

def add(a, b):
    return a + b

print(add(2,3))

#-------------------------------------------------------------------------------
# 6 Lists
print("\n List Review")

#
fruits = ["apple", "banana", "orange"]
print(fruits[1])
fruits.append("grape")               # Inserts a new item named "grape" into the list
fruits.remove("apple")                  # Removes an item named "apple" from the list

# 
numbers = [1, 2, 3]     # A list consisting of the numbers 1, 2, and 3

for num in numbers:     # A loop that runs for each element inside the list "numbers"
    print(num * 2)      # For each element inside "numbers", the program will print the value of each element multiplied by 2

#-------------------------------------------------------------------------------
# 7 Tuples
my_list = [1, 2, 3]     # A list is a set of data that's modify-able
my_tuple = (1, 2, 3)    # While a tuple, once declared, cannot be modified. The data set is also ordered

#-------------------------------------------------------------------------------
# 8 Sets
items = {1, 1, 2, 2, 3} # The duplicates are removed immediately when the set is created.
print(items)            # While printing a list, it will only print all the different elements.
# A set cannot contain duplicate values.

#-------------------------------------------------------------------------------
# 9 Dictionaries
person = {                      # This is a dictionary, storing datas by key-value system
    "name": "Nathan",           # Key is name, value is Nathan
    "age": 17                   # Key is age, value is 17
}

print(person["name"])           # We can access/print the dictionary based off keys or values, this one is key-based
print(person.get("age"))        # Another way to access is using .get

person["age"] = 18              # Updating the value of "age" to 18
person["city"] = "Surakarta"    # Adding a new variable with key "city", with the value "Surakarta"

person1 = {                         # A new dictionary with similar data stored
    "name": "Nathan",
    "age": 17
}

for key, value in person1.items():  # Loops for each key and value inside the dictionary
    print(key, value)               # Prints all the key and values inside the dictionary

#-------------------------------------------------------------------------------
# 10 Combined
students = {                            # A dictionary containing 3 datasets, where the key is name and value is their grade
    "Alice": 85,
    "Bob": 72,
    "Charlie": 91
}

for name, score in students.items():    # A loop that runs through each name and score in dictionary "students"
    if score >= 80:                     # Checks if the individual has a grade equals/better than 80
        print(name)                     # If yes, it will print the student
# This short program will output / print ONLY the students that have grades equal to / higher than 80
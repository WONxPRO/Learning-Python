# =============================================================================
# 1. VARIABLES & DATA TYPES
# =============================================================================

print("Variables & Data Types Review")

# String variable
name = "Nathan"

# Integer variable
age = 17

# Boolean variable
college = True

# Float variable
braincell = 2.3

# Print data types
print(type(name))
print(type(age))
print(type(college))
print(type(braincell))

# -----------------------------------------------------------------------------
# Arithmetic Operations
# -----------------------------------------------------------------------------

print("\nArithmetic Operations Review")

# Declare x
x = 10

# Add 5
x = x + 5

# Multiply by 2
x *= 2

# Print result
print(f"x = {x}")


# =============================================================================
# 2. INPUT & OUTPUT
# =============================================================================

print("\nInput & Output Review")

# Ask for username
name = input("Input username: ")

# Ask for age
age = input("Input age: ")

# Print greeting
print(f"Hello {name}, you are {age} years old.")


# =============================================================================
# 3. CONDITIONAL STATEMENTS
# =============================================================================

print("\nConditional Statements Review")

# Example score
score = 75

# Check grade
if score >= 80:
    print("A")
elif score >= 70:
    print("B")
else:
    print("C")


# -----------------------------------------------------------------------------
# Age Legality Checker
# -----------------------------------------------------------------------------

print("\nAge Legality Checker")

# Ask user age
age = int(input("Input your current age: "))

# Check adulthood
if age >= 18:
    print("You are an adult.")
else:
    print("You are a minor.")


# =============================================================================
# 4. LOOPS
# =============================================================================

print("\nLoops Review")

# Print numbers 0–4
for i in range(5):
    print(i)


# Countdown using while loop
count = 3

while count > 0:
    print(count)
    count -= 1

# Loop that prints 1–5
for j in range(5):
    print(j + 1)


# =============================================================================
# 5. FUNCTIONS
# =============================================================================

print("\nFunction Review")

# Function that returns a greeting
def greet(name):
    return f"Hello {name}"

print(greet("Nathan"))


# Function that adds two numbers
def add(a, b):
    return a + b

print(add(2, 3))


# =============================================================================
# 6. LISTS
# =============================================================================

print("\nList Review")

# Create list
fruits = ["apple", "banana", "orange"]

# Access item
print(fruits[1])

# Add item
fruits.append("grape")

# Remove item
fruits.remove("apple")


# List of numbers
numbers = [1, 2, 3]

# Print each number multiplied by 2
for num in numbers:
    print(num * 2)


# =============================================================================
# 7. TUPLES
# =============================================================================

# Lists can be modified
my_list = [1, 2, 3]

# Tuples cannot be modified after creation
my_tuple = (1, 2, 3)


# =============================================================================
# 8. SETS
# =============================================================================

# Duplicate values are automatically removed
items = {1, 1, 2, 2, 3}

print(items)


# =============================================================================
# 9. DICTIONARIES
# =============================================================================

# Dictionary stores data using key-value pairs
person = {
    "name": "Nathan",
    "age": 17
}

# Access values
print(person["name"])
print(person.get("age"))

# Update value
person["age"] = 18

# Add new key-value pair
person["city"] = "Surakarta"


# Another dictionary
person1 = {
    "name": "Nathan",
    "age": 17
}

# Print all keys and values
for key, value in person1.items():
    print(key, value)


# =============================================================================
# 10. COMBINED EXERCISE
# =============================================================================

# Dictionary of students and grades
students = {
    "Alice": 85,
    "Bob": 72,
    "Charlie": 91
}

# Print students with grades >= 80
for name, score in students.items():
    if score >= 80:
        print(name)
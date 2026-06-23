# Challenge for Day 6:
# Create a dictionary with 5 keys.
# Loop through all keys and values.
# Create a set with duplicate values.
# Create a tuple with 3 numbers.
# Create a dictionary containing a list.

# Creating a dictionary with 5 keys
DictionaryChallenge = {
    "name" : "Nathan",
    "age" : 17,
    "hobby" : "Gaming",
    "favorite color" : "Light Blue",
    "id" : 1
}

# Looping through all keys and values
for key, value in DictionaryChallenge.items():
    print(key, value)

# Creating a set with duplicate values
DupeSet = {"Nathan", "Nathan", "Nathan", "Nathan", "Nathan"}
print(DupeSet)

# Creating a tuple with 3 numbers
NumTuple = (1, 2, 3)
print(NumTuple)

# Creating a dictionary containing a list
DictList = {
    "name" : "Nathan",
    "hobbies" : ["Gaming", "Coding", "Cooking"]
}
print(DictList)
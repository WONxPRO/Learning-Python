# A dictionary is a collection of key-value pairs. Each key is unique and maps to a value.

#-------------------------------------------------------------------------------------------------------------------
# Creating a dictionary.
dictionary1 = { # This is a dictionary with four key-value pairs.
    "name" : "Nathan", # The key is "name" and the value is "Nathan".
    "age" : 16, # The key is "age" and the value is 16.
    "city" : "Surakarta", # The key is "city" and the value is "Surakarta".
    "country" : "Indonesia" # The key is "country" and the value is "Indonesia".
}

#-------------------------------------------------------------------------------------------------------------------
# Accessing dictionary items.

# A dictionary can be outputted whole or by specific keys.
# Case 1, outputting the whole dictionary. 
# We can use the print function to output the entire dictionary, which will show all key-value pairs.
print("\nCase 1, outputting the whole dictionary.")
print(dictionary1)

# Case 2, outputting specific keys. 
# We can access specific values in the dictionary by using their corresponding keys. 
# This is done by using square brackets [] and the key name.
print("\nCase 2, outputting specific keys.")
print(dictionary1["name"])
print(dictionary1["age"])
print(dictionary1["city"])
print(dictionary1["country"])

# Case 3, outputting specific keys using the get() method.
# Using the get() method to access values in the dictionary.
# The get() method is another way to access values in a dictionary. 
# It takes the key as an argument and returns the corresponding value.
print("\nUsing the get() method to access values in the dictionary.")
get_name = dictionary1.get("name")
get_age = dictionary1.get("age")
get_city = dictionary1.get("city")
get_country = dictionary1.get("country")

#-------------------------------------------------------------------------------------------------------------------
# Modifying a dictionary.

# Adding new key-value pairs to the dictionary.
# We can add new key-value pairs to the dictionary by assigning a value to a new key.
print("\nAdding new key-value pairs to the dictionary.")
dictionary1["hobby"] = "Gaming" # Adding a new key-value pair to the dictionary.
print(dictionary1) 

# Updating values in the dictionary. 
# We can update the value of a specific key by assigning a new value to that key.
print("\nUpdating values in the dictionary.")
dictionary1["name"] = "Not Nathan"
dictionary1["age"] = 17
dictionary1["city"] = "Moscow"
dictionary1["country"] = "Russia"

#-------------------------------------------------------------------------------------------------------------------
# Removing dictionary items.
print("\nRemoving dictionary items.")
# We can remove items from the dictionary using the del statement or the pop() method.

# Using the del statement to remove an item by key.
print("\nUsing the del statement to remove an item by key.")
del dictionary1["age"] # This will remove the key-value pair with the key "age" from the dictionary.
print(dictionary1)

# Using the pop() method to remove an item by key.
print("\nUsing the pop() method to remove an item by key.")
dictionary1.pop("city") # This will remove the key-value pair with the key "city" from the dictionary.
print(dictionary1)

# Using the popitem() method to remove the last inserted item.
print("\nAdding back age.")
dictionary1["age"] = 16 # Adding back the key-value pair with the key "age".
print(dictionary1)
print("\nUsing the popitem() method to remove the last inserted item.")
dictionary1.popitem() # This will remove the last inserted key-value pair from the dictionary.
print(dictionary1)

# Clearing the dictionary.
# We can clear all items from the dictionary using the clear() method, which will leave us with an empty dictionary.
print("\nClearing the dictionary with clear().")
dictionary1.clear() # This will remove all key-value pairs from the dictionary, leaving it empty.
print(dictionary1)
print("^^ The dictionary is now empty.\n")

# Adding back the removed items to the dictionary.
dictionary1 = { 
    "name" : "Nathan", 
    "age" : 16, 
    "city" : "Surakarta",
    "country" : "Indonesia" 
}

#-------------------------------------------------------------------------------------------------------------------

# Iterating through a dictionary.
# We can iterate through a dictionary using a for loop.
print("\nIterating through a dictionary.")

# Using a for loop to iterate through the keys of the dictionary.
print("\nUsing a for loop to iterate through the keys of the dictionary.")
for key in dictionary1:
    print(key) # This will print each key in the dictionary.

# Using a for loop to iterate through the values of the dictionary.
print("\nUsing a for loop to iterate through the values of the dictionary.")
for value in dictionary1.values():
    print(value) # This will print each value in the dictionary.

# Using a for loop to iterate through the key-value pairs of the dictionary.
print("\nUsing a for loop to iterate through the key-value pairs of the dictionary.")
for key, value in dictionary1.items():
    print(f"{key}: {value}") # This will print each key and its corresponding value in the dictionary.

#-------------------------------------------------------------------------------------------------------------------
# Nested dictionaries.
# A nested dictionary is a dictionary that contains another dictionary as a value.
print("\nNested dictionaries.")
nested_dictionary = {
    "person1": {
        "name": "Alice",
        "age": 30,
        "city": "New York"
    },
    "person2": {
        "name": "Bob",
        "age": 25,
        "city": "Los Angeles"
    }
}

print(nested_dictionary) # This will print the entire nested dictionary.
print(nested_dictionary["person1"]) # This will print the dictionary for person1.
print(nested_dictionary["person1"]["name"]) # This will print the name of person1, which is "Alice".
print(nested_dictionary["person2"]["age"]) # This will print the age of person2, which is 25.

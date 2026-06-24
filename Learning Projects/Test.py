# 9 Dictionaries
person = {                      # This is a dictionary, storing datas by key-value system
    "name": "Nathan",           # Key is name, value is Nathan
    "age": 17                   # Key is age, value is 17
}

print(person["name"])           # We can access/print the dictionary based off keys or values, this one is key-based
print(person.get("age"))        # Another way to access is using .get

person["age"] = 18              # Updating the value of "age" to 18
person["city"] = "Surakarta"    # Adding a new variable with key "city", with the value "Surakarta"
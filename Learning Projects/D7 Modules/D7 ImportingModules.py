def newline():
    print("--------------------------")

# Importing a custom-made module from another file in the same folder
import D7_Module1 as M1
    
a = M1.Amonging("Galaxy Knight")
print(a)

# Importing a pre-made module from Python
newline()
import math
print(math.sqrt(4))

# Challenge 1
newline()
print(math.sqrt(81))   # Prediction 9.0
print(math.ceil(7.1))  # Prediction 8.0
print(math.floor(7.9)) # Prediction 7.0

# Challenge 2
newline()
import random as rand

number = rand.randint(1, 10)
print(number)
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
	
print("This is Case 2 of the Function Study.")
print("Possibility 1")
WordNumber("Among", 67)

print("Possibility 2")
WordNumber(69, "AmongUs")
# Learns about and, or, and not (logical operators in Python)

age = int(input("Input age: "))
has_id = bool(input("Input ID: "))

if age >= 18:
    if has_id:
        print("You are allowed to enter.")
    else:
        print("You are not allowed to enter. You need an ID.")
else:
    print("You are not allowed to enter. You are underage.")
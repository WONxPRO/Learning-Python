print("A Simple Diary Entry Program")

diary = input("Enter diary entry: ")

with open("diary.txt", "a") as file:
    file.write(f"\n{diary}")
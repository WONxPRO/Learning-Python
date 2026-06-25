import sys
import time

def MenuScreen():
    print("====================")
    print("Sussy Notes App")
    print("1. Add Note")
    print("2. View Notes")
    print("3. Exit")
    print("====================")
    
    
def AddNote():
    print("====================")
    diary = input("Enter diary entry: ")
    
    with open("diary.txt", "a") as file:
       file.write(diary)
    print("====================")

def ViewNotes():
    print("====================")
    print("Displaying All Notes...\n")
    time.sleep(1)
    
    with open("diary.txt", "r") as file:
        lines = file.readlines()

    for line in lines:
        print(f"Diary Entry: {line}", end="")

    print(f"\n\nTotal Entries: {len(lines)}")
    print("")

while True:
    action = ""
    MenuScreen()
    action = input("Enter Action (1, 2, or 3): ")

    if action == "1":
        AddNote()
        time.sleep(1)
        print("Note Saved!\n\n")
        time.sleep(1)

    elif action == "2":
        ViewNotes()
        time.sleep(2)
        home = input("Go Home? (y/n): ")
        if home == "y":
            print("Ok Boss\n\n")
            time.sleep(1)
        else:
            print("Where else u wanna go")
            time.sleep(1)
            print("This is a program made by a kid\n\n")
            time.sleep(1)

    elif action == "3":
        print("Okay, bye bye.\n\n")
        time.sleep(1)
        sys.exit()
        
    else:
        print(f"Picking 1-3 so hard you entered {action}?\n\n")
        time.sleep(2)

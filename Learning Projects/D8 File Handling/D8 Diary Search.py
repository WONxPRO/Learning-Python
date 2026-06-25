import os

print("===========================" \
        "\nA Simple Diary Search System" \
        "\n* A Part of D8 Diary Entry"
        "\n===========================")

if os.path.exists("diary.txt"):
    keyword = input("Enter keyword: ")
    file = open("diary.txt", "r")
    content = file.read()

    if keyword in content:
        print("Found!")
    else:
        print("Get Amongussed")

else: 
    print("Diary File Is Not Found (404)\n")
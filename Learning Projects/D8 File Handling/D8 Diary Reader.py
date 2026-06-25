import os

print("===========================" \
        "\nA Simple Diary Reader" \
        "\n* A Part of D8 Diary Entry"
        "\n===========================")

if os.path.exists("diary.txt"):
    with open("diary.txt", "r") as file:
        lines = file.readlines()

    print("Diary Entry:".join(lines))
    print(f"\nTotal Entries: {len(lines)}")
    print("")
else: 
    print("Diary File Is Not Found (404)\n")


inventory = {
    "Potion": 10,
    "Amongus Ball": 25,
    "Revive": 5
}

for item, amount in inventory.items():
    print(f"{item}: {amount}")

print("\nYou got a Potion!")
inventory["Potion"] += 1
print(f"You now have {inventory['Potion']} Potions.")
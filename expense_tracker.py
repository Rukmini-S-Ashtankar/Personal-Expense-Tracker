print("==============================")
print("  PERSONAL EXPENSE TRACKER   ")
print("==============================")

print("1. Add Expense")
print("2. View Expenses")
print("3. Calculate Total")
print("4. Exit")

choice = input("Enter your choice: ")

if choice == "1":
    print("Add Expense selected")
elif choice == "2":
    print("View Expenses selected")
elif choice == "3":
    print("Calculate Total selected")
elif choice == "4":
    print("Goodbye!")
else:
    print("Invalid choice")
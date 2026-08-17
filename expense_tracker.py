expenses = []

while True:
    print("==============================")
    print("   PERSONAL EXPENSE TRACKER   ")
    print("==============================")

    print("1. Add Expense")
    print("2. View Expenses")
    print("3. Calculate Total")
    print("4. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        category = input("Enter expense category: ")
        amount = float(input("Enter expense amount: "))
        description = input("Enter description: ")

        expense = {
            "category": category,
            "amount": amount,
            "description": description
        }

        expenses.append(expense)

        print("Expense added successfully!")
        print("Expense:", expense)

    elif choice == "2":
        if expenses:
            print("\nYour Expenses:")

            for expense in expenses:
                print(
                    f"Category: {expense['category']}, "
                    f"Amount: ₹{expense['amount']}, "
                    f"Description: {expense['description']}"
                )
        else:
            print("No expenses recorded.")

    elif choice == "3":
        print("Calculate Total selected")

    elif choice == "4":
        print("Goodbye!")
        break

    else:
        print("Invalid choice")

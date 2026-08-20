expenses = []

while True:
    print("==============================")
    print("   PERSONAL EXPENSE TRACKER   ")
    print("==============================")

    print("1. Add Expense")
    print("2. View Expenses")
    print("3. Calculate Total")
    print("4. Exit")
    print("5. Delete Expense")
    print("6. Edit Expense")

    choice = input("Enter your choice: ")

    if choice == "1":
        category = input("Enter expense category: ")
        while True:
    try:
        amount = float(input("Enter expense amount: ₹"))

        if amount <= 0:
            print("Amount must be greater than 0.")
        else:
            break

    except ValueError:
        print("Please enter a valid amount.")
        description = input("Enter description: ")

        date = input("Enter date (DD-MM-YYYY): ")

        expense = {
            "category": category,
            "amount": amount,
            "description": description,
            "date": date
        }

        expenses.append(expense)

        print("Expense added successfully!")

    elif choice == "2":
        if expenses:
            print("\nYour Expenses:")

            for i, expense in enumerate(expenses, start=1):
                print(
                    f"{i}. Date: {expense['date']}, "
                    f"Category: {expense['category']}, " 
                    f"Amount: ₹{expense['amount']}, " 
                    f"Description: {expense['description']}"
                )
        else:
            print("No expenses recorded.")

    elif choice == "3":
        total = 0

        for expense in expenses:
            total += expense["amount"]

        print(f"Total Expenses: ₹{total}")

    elif choice == "4":
        print("Goodbye!")
        break

    elif choice == "5":
        if expenses:
            for i, expense in enumerate(expenses, start=1):
                print(
                    f"{i}. {expense['category']} - "
                    f"₹{expense['amount']} - "
                    f"{expense['description']}"
                )

            index = int(input("Enter expense number to delete: "))

            if 1 <= index <= len(expenses):
                deleted = expenses.pop(index - 1)
                print(f"Deleted: {deleted['description']}")
            else:
                print("Invalid expense number.")
        else:
            print("No expenses to delete.")

    elif choice == "6":
        if expenses:
            for i, expense in enumerate(expenses, start=1):
                print(
                    f"{i}. {expense['category']} - "
                    f"₹{expense['amount']} - "
                    f"{expense['description']}"
                )

            index = int(input("Enter expense number to edit: "))

            if 1 <= index <= len(expenses):
                expenses[index - 1]["category"] = input(
                    "Enter new category: "
                )

                while True:
    try:
        amount = float(input("Enter new amount: ₹"))

        if amount <= 0:
            print("Amount must be greater than 0.")
        else:
            expenses[index - 1]["amount"] = amount
            break

    except ValueError:
        print("Please enter a valid amount.")
                )

                expenses[index - 1]["description"] = input(
                    "Enter new description: "
                )

                expenses[index - 1]["date"] = input(
                    "Enter new date (DD-MM-YYYY): "
                )


                print("Expense updated successfully!")

            else:
                print("Invalid expense number.")
        else:
            print("No expenses to edit.")

    else:
        print("Invalid choice")

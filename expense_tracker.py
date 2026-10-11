
import json
import csv
from datetime import datetime

FILE_NAME = "expenses.json"


# ---------- DATA MANAGEMENT ----------

def load_expenses():
    try:
        with open(FILE_NAME, "r") as file:
            data = json.load(file)

            if isinstance(data, list):
                return data

            print("Invalid data format. Starting with empty expenses.")
            return []

    except FileNotFoundError:
        return []

    except json.JSONDecodeError:
        print("Warning: expenses.json contains invalid JSON.")
        return []


expenses = load_expenses()


def save_expenses():
    try:
        with open(FILE_NAME, "w") as file:
            json.dump(expenses, file, indent=4)
        return True
    except OSError as error:
        print("Could not save expenses:", error)
        return False


# ---------- INPUT VALIDATION ----------

def get_amount(prompt):
    while True:
        try:
            amount = float(input(prompt))

            if amount <= 0:
                print("Amount must be greater than zero.")
            else:
                return round(amount, 2)

        except ValueError:
            print("Enter a valid amount.")


def get_date(prompt, default=None):
    while True:
        value = input(prompt).strip()

        if not value and default is not None:
            return default

        try:
            return datetime.strptime(value, "%d-%m-%Y").strftime(
                "%d-%m-%Y"
            )
        except ValueError:
            print("Enter a valid date in DD-MM-YYYY format.")


def get_payment_method():
    methods = ["Cash", "UPI", "Card", "Bank Transfer"]

    print("Payment Methods:")
    for i, method in enumerate(methods, start=1):
        print(f"{i}. {method}")

    while True:
        choice = input("Choose payment method (1-4): ").strip()

        if choice in ["1", "2", "3", "4"]:
            return methods[int(choice) - 1]

        print("Invalid payment method.")


def display_expense(index, expense):
    print(
        f"{index}. Date: {expense.get('date', 'N/A')} | "
        f"Category: {expense.get('category', 'N/A')} | "
        f"Amount: Rs. {expense.get('amount', 0):.2f} | "
        f"Payment: {expense.get('payment_method', 'Not recorded')} | "
        f"Description: {expense.get('description', '')}"
    )


def show_all_expenses():
    if not expenses:
        print("No expenses recorded.")
        return

    print("\n---------- YOUR EXPENSES ----------")

    for i, expense in enumerate(expenses, start=1):
        display_expense(i, expense)


def select_expense():
    if not expenses:
        print("No expenses available.")
        return None

    show_all_expenses()

    while True:
        try:
            index = int(input("Enter expense number: "))

            if 1 <= index <= len(expenses):
                return index - 1

            print("Please select a valid expense number.")

        except ValueError:
            print("Enter a whole number.")


# ---------- 1. ADD EXPENSE ----------

def add_expense():
    category = input("Enter category: ").strip()

    if not category:
        print("Category cannot be empty.")
        return

    amount = get_amount("Enter amount: Rs. ")

    description = input("Enter description: ").strip()

    date = get_date(
        "Enter date (DD-MM-YYYY), or press Enter for today: ",
        datetime.today().strftime("%d-%m-%Y")
    )

    payment_method = get_payment_method()

    expense = {
        "category": category.title(),
        "amount": amount,
        "description": description,
        "date": date,
        "payment_method": payment_method
    }

    expenses.append(expense)

    if save_expenses():
        print("Expense added and saved successfully!")


# ---------- 2. VIEW EXPENSES ----------

def view_expenses():
    show_all_expenses()


# ---------- 3. CALCULATE TOTAL ----------

def calculate_total():
    total = sum(expense.get("amount", 0) for expense in expenses)

    print(f"Total Expenses: Rs. {total:.2f}")


# ---------- 4. DELETE EXPENSE ----------

def delete_expense():
    index = select_expense()

    if index is None:
        return

    confirm = input("Delete this expense? (y/n): ").strip().lower()

    if confirm == "y":
        deleted = expenses.pop(index)

        if save_expenses():
            print(f"Deleted: {deleted.get('description', 'Expense')}")
    else:
        print("Deletion cancelled.")


# ---------- 5. EDIT EXPENSE ----------

def edit_expense():
    index = select_expense()

    if index is None:
        return

    expense = expenses[index]

    print("Press Enter to keep the current value.")

    category = input(
        f"Category [{expense.get('category', '')}]: "
    ).strip()

    description = input(
        f"Description [{expense.get('description', '')}]: "
    ).strip()

    if category:
        expense["category"] = category.title()

    if description:
        expense["description"] = description

    while True:
        value = input(
            f"Amount [{expense.get('amount', 0)}]: "
        ).strip()

        if not value:
            break

        try:
            amount = float(value)

            if amount > 0:
                expense["amount"] = round(amount, 2)
                break

            print("Amount must be greater than zero.")

        except ValueError:
            print("Enter a valid amount.")

    while True:
        value = input(
            f"Date [{expense.get('date', '')}] (DD-MM-YYYY): "
        ).strip()

        if not value:
            break

        try:
            expense["date"] = datetime.strptime(
                value, "%d-%m-%Y"
            ).strftime("%d-%m-%Y")
            break

        except ValueError:
            print("Enter a valid date in DD-MM-YYYY format.")

    if input("Change payment method? (y/n): ").strip().lower() == "y":
        expense["payment_method"] = get_payment_method()

    if save_expenses():
        print("Expense updated successfully!")


# ---------- 6. CATEGORY SUMMARY ----------

def category_summary():
    if not expenses:
        print("No expenses recorded.")
        return

    summary = {}

    for expense in expenses:
        category = expense.get("category", "Other").title()
        summary[category] = (
            summary.get(category, 0) + expense.get("amount", 0)
        )

    print("\n---------- CATEGORY SUMMARY ----------")

    for category, total in sorted(summary.items()):
        print(f"{category}: Rs. {total:.2f}")


# ---------- 7. SEARCH EXPENSES ----------

def search_expenses():
    search = input(
        "Search by category or description: "
    ).strip().lower()

    if not search:
        print("Search cannot be empty.")
        return

    found = False

    for i, expense in enumerate(expenses, start=1):
        category = expense.get("category", "").lower()
        description = expense.get("description", "").lower()

        if search in category or search in description:
            display_expense(i, expense)
            found = True

    if not found:
        print("No matching expenses found.")


# ---------- 8. MONTHLY SUMMARY ----------

def monthly_summary():
    month_year = input(
        "Enter month and year (MM-YYYY): "
    ).strip()

    try:
        datetime.strptime(month_year, "%m-%Y")
    except ValueError:
        print("Invalid format. Example: 10-2026")
        return

    total = 0
    count = 0
    category_totals = {}

    for expense in expenses:
        try:
            expense_date = datetime.strptime(
                expense["date"], "%d-%m-%Y"
            )
        except (ValueError, KeyError, TypeError):
            continue

        if expense_date.strftime("%m-%Y") == month_year:
            amount = expense.get("amount", 0)
            category = expense.get("category", "Other")

            total += amount
            count += 1
            category_totals[category] = (
                category_totals.get(category, 0) + amount
            )

    print(f"\nMonthly Report: {month_year}")
    print(f"Number of expenses: {count}")
    print(f"Total spent: Rs. {total:.2f}")

    if count:
        print(f"Average expense: Rs. {total / count:.2f}")

        print("Category breakdown:")
        for category, amount in sorted(category_totals.items()):
            print(f"{category}: Rs. {amount:.2f}")
    else:
        print("No expenses found for this month.")


# ---------- 9. PAYMENT SUMMARY ----------

def payment_summary():
    if not expenses:
        print("No expenses recorded.")
        return

    summary = {}

    for expense in expenses:
        method = expense.get("payment_method", "Not recorded")
        summary[method] = (
            summary.get(method, 0) + expense.get("amount", 0)
        )

    print("\n---------- PAYMENT SUMMARY ----------")

    for method, total in sorted(summary.items()):
        print(f"{method}: Rs. {total:.2f}")


# ---------- 10. EXPORT TO CSV ----------

def export_csv():
    if not expenses:
        print("No expenses available to export.")
        return

    fields = [
        "date", "category", "amount",
        "description", "payment_method"
    ]

    try:
        with open("expenses_report.csv", "w", newline="",
                  encoding="utf-8-sig") as file:
            writer = csv.DictWriter(file, fieldnames=fields)
            writer.writeheader()

            for expense in expenses:
                writer.writerow({
                    field: expense.get(field, "")
                    for field in fields
                })

        print("Report exported to expenses_report.csv")

    except OSError as error:
        print("Could not export report:", error)


# ---------- MAIN MENU ----------

while True:
    print("\n================================")
    print("     PERSONAL EXPENSE TRACKER")
    print("================================")
    print("1. Add Expense")
    print("2. View Expenses")
    print("3. Calculate Total")
    print("4. Delete Expense")
    print("5. Edit Expense")
    print("6. Category Summary")
    print("7. Search Expenses")
    print("8. Monthly Summary")
    print("9. Payment Method Summary")
    print("10. Export to CSV")
    print("11. Exit")

    choice = input("Enter your choice: ").strip()

    if choice == "1":
        add_expense()
    elif choice == "2":
        view_expenses()
    elif choice == "3":
        calculate_total()
    elif choice == "4":
        delete_expense()
    elif choice == "5":
        edit_expense()
    elif choice == "6":
        category_summary()
    elif choice == "7":
        search_expenses()
    elif choice == "8":
        monthly_summary()
    elif choice == "9":
        payment_summary()
    elif choice == "10":
        export_csv()
    elif choice == "11":
        print("Goodbye!")
        break
    else:
        print("Invalid choice. Please select 1-11.")

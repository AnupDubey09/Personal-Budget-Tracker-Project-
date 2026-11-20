
import numpy as np
import pandas as pd
import csv
import pickle
import os

# ==========================================
# PERSONAL BUDGET TRACKER
# Python Data Analysis Project
# ==========================================

CSV_FILE = "transactions.csv"
PICKLE_FILE = "transactions.pkl"

columns = [
    "Date",
    "Type",
    "Category",
    "Description",
    "Amount"
]

# ==========================================
# 1. INITIALIZE DATA
# ==========================================

def initialize_data():

    if os.path.exists(CSV_FILE):
        df = pd.read_csv(CSV_FILE)

    else:
        df = pd.DataFrame(columns=columns)
        df.to_csv(CSV_FILE, index=False)

    return df


# ==========================================
# 2. SAVE DATA
# ==========================================

def save_data(df):

    df.to_csv(CSV_FILE, index=False)

    with open(PICKLE_FILE, "wb") as file:
        pickle.dump(df, file)

    print("\nData saved successfully!")


# ==========================================
# 3. LOAD PICKLE DATA
# ==========================================

def load_pickle_data():

    if os.path.exists(PICKLE_FILE):

        with open(PICKLE_FILE, "rb") as file:
            df = pickle.load(file)

        print("\nData loaded from Pickle successfully!")

        return df

    else:
        print("\nPickle file not found!")
        return initialize_data()


# ==========================================
# 4. ADD TRANSACTION
# ==========================================

def add_transaction(df):

    print("\n----- ADD TRANSACTION -----")

    print("1. Income")
    print("2. Expense")

    choice = input("Enter your choice: ")

    if choice == "1":
        transaction_type = "Income"

    elif choice == "2":
        transaction_type = "Expense"

    else:
        print("Invalid choice!")
        return df

    date = input("Enter date (YYYY-MM-DD): ")

    try:
        pd.to_datetime(date, format="%Y-%m-%d")
    except ValueError:
        print("Invalid date!")
        return df

    category = input("Enter category: ")
    description = input("Enter description: ")

    try:
        amount = float(input("Enter amount: "))

        if amount <= 0:
            print("Amount must be positive!")
            return df

    except ValueError:
        print("Invalid amount!")
        return df

    new_transaction = pd.DataFrame([{
        "Date": date,
        "Type": transaction_type,
        "Category": category,
        "Description": description,
        "Amount": amount
    }])

    df = pd.concat(
        [df, new_transaction],
        ignore_index=True
    )

    save_data(df)

    print("Transaction added successfully!")

    return df


# ==========================================
# 5. DISPLAY ALL TRANSACTIONS
# ==========================================

def view_transactions(df):

    print("\n----- TRANSACTION HISTORY -----")

    if df.empty:
        print("No transactions found.")

    else:
        print(df.to_string(index=False))


# ==========================================
# 6. FINANCIAL SUMMARY
# ==========================================

def financial_summary(df):

    print("\n----- FINANCIAL SUMMARY -----")

    if df.empty:
        print("No data available.")
        return

    income = df.loc[
        df["Type"] == "Income", "Amount"
    ].sum()

    expenses = df.loc[
        df["Type"] == "Expense", "Amount"
    ].sum()

    savings = income - expenses

    if income > 0:
        saving_percentage = (
            savings / income
        ) * 100
    else:
        saving_percentage = 0

    print("Total Income: Rs.", round(income, 2))
    print("Total Expenses: Rs.", round(expenses, 2))
    print("Total Savings: Rs.", round(savings, 2))
    print("Saving Percentage:", round(saving_percentage, 2), "%")


# ==========================================
# 7. CATEGORY-WISE EXPENSE ANALYSIS
# ==========================================

def category_analysis(df):

    print("\n----- CATEGORY ANALYSIS -----")

    expense_data = df[
        df["Type"] == "Expense"
    ]

    if expense_data.empty:
        print("No expenses available.")
        return

    result = expense_data.groupby(
        "Category"
    )["Amount"].sum()

    print(result.to_string())

    print("\nHighest Spending Category:")

    print(result.idxmax())

    print("Highest Amount: Rs.", result.max())


# ==========================================
# 8. HIGHEST AND AVERAGE EXPENSE
# ==========================================

def expense_statistics(df):

    print("\n----- EXPENSE STATISTICS -----")

    expenses = df.loc[
        df["Type"] == "Expense", "Amount"
    ]

    if expenses.empty:
        print("No expenses available.")
        return

    values = expenses.to_numpy()

    highest = np.max(values)
    lowest = np.min(values)
    average = np.mean(values)
    total = np.sum(values)

    print("Highest Expense: Rs.", highest)
    print("Lowest Expense: Rs.", lowest)
    print("Average Expense: Rs.", round(average, 2))
    print("Total Expense: Rs.", total)


# ==========================================
# 9. SEARCH TRANSACTIONS BY DATE
# ==========================================

def search_by_date(df):

    print("\n----- SEARCH TRANSACTION -----")

    search_date = input(
        "Enter date (YYYY-MM-DD): "
    )

    try:
        pd.to_datetime(search_date, format="%Y-%m-%d")
    except ValueError:
        print("Invalid date!")
        return

    result = df[
        df["Date"] == search_date
    ]

    if result.empty:
        print("No transactions found for this date.")

    else:
        print(result.to_string(index=False))


# ==========================================
# 10. MONTHLY ANALYSIS
# ==========================================

def monthly_analysis(df):

    print("\n----- MONTHLY ANALYSIS -----")

    if df.empty:
        print("No data available.")
        return

    data = df.copy()

    data["Date"] = pd.to_datetime(
        data["Date"], errors="coerce"
    )

    data = data.dropna(subset=["Date"])

    data["Month"] = data["Date"].dt.to_period("M")

    result = data.pivot_table(
        index="Month",
        columns="Type",
        values="Amount",
        aggfunc="sum",
        fill_value=0
    )

    print(result.to_string())


# ==========================================
# 11. MAIN MENU
# ==========================================

def main():

    df = initialize_data()

    while True:

        print("\n====================================")
        print("       PERSONAL BUDGET TRACKER")
        print("====================================")

        print("1. Add Income / Expense")
        print("2. View All Transactions")
        print("3. Financial Summary")
        print("4. Category-wise Analysis")
        print("5. Expense Statistics")
        print("6. Search Transaction by Date")
        print("7. Monthly Analysis")
        print("8. Load Data from Pickle")
        print("9. Exit")

        choice = input("\nEnter your choice: ")

        if choice == "1":
            df = add_transaction(df)

        elif choice == "2":
            view_transactions(df)

        elif choice == "3":
            financial_summary(df)

        elif choice == "4":
            category_analysis(df)

        elif choice == "5":
            expense_statistics(df)

        elif choice == "6":
            search_by_date(df)

        elif choice == "7":
            monthly_analysis(df)

        elif choice == "8":
            df = load_pickle_data()

        elif choice == "9":
            save_data(df)
            print("\nThank you for using Budget Tracker!")
            break

        else:
            print("Invalid choice! Try again.")


# ==========================================
# START PROGRAM
# ==========================================

if __name__ == "__main__":
    main()

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

MONTH_ORDER = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
               "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def show(value):
    # Print 2000.0 as 2000, but keep 2000.5 as it is
    if value == int(value):
        return str(int(value))
    return str(value)


def load_data(filename):
    try:
        df = pd.read_csv(filename, dtype=str, keep_default_na=False)
    except FileNotFoundError:
        print("Error: File", filename, "not found.")
        return None

    # Clean spaces and turn Amount into numbers
    df.columns = df.columns.str.strip()
    df["Month"] = df["Month"].str.strip()
    df["Category"] = df["Category"].str.strip()
    df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce")

    # Warn about bad rows
    for i in range(len(df)):
        if pd.isna(df["Amount"][i]):
            print("Warning: Row", i + 1, "skipped - Amount must be a number.")
        elif df["Amount"][i] < 0:
            print("Warning: Row", i + 1, "skipped - Amount cannot be negative.")

    # Keep valid rows only
    valid = df[df["Amount"] >= 0]
    if len(valid) < len(df):
        print("Valid orders analysed:", len(valid))
    return valid


def get_monthly_totals(df):
    totals = df.groupby("Month")["Amount"].sum()
    names = []
    values = []
    for month in MONTH_ORDER:
        if month in totals.index:
            names.append(month)
            values.append(totals[month])
    return names, values


def print_best_month(names, values):
    best = max(values)
    print("Best month:", names[values.index(best)], "(Rs. " + show(best) + ")")


def print_mean_and_median(df):
    print("Mean order value: Rs. {:.2f}".format(np.mean(df["Amount"])))
    print("Median order value: Rs. {:.2f}".format(np.median(df["Amount"])))


def monthly_spending(df):
    names, values = get_monthly_totals(df)
    for i in range(len(names)):
        print(names[i], ": Rs.", show(values[i]))
    print("Total: Rs.", show(sum(values)))
    print_best_month(names, values)

    plt.bar(names, values, color="grey")
    plt.title("Monthly Spending")
    plt.xlabel("Month")
    plt.ylabel("Amount (Rs.)")
    plt.show()


def order_statistics(df):
    names, values = get_monthly_totals(df)
    print("Orders analysed:", len(df))
    print_mean_and_median(df)
    print_best_month(names, values)


def category_share(df):
    totals = df.groupby("Category")["Amount"].sum()
    totals = totals.sort_values(ascending=False)

    for category in totals.index:
        percent = totals[category] / totals.sum() * 100
        print(category, ": Rs.", show(totals[category]), "({:.2f}%)".format(percent))
    print_mean_and_median(df)

    plt.pie(totals.values, labels=totals.index, autopct="%1.2f%%")
    plt.title("Category Share of Spending")
    plt.show()


def main():
    df = load_data("orders.csv")
    if df is None:
        print("Program stopped.")
        return
    if len(df) == 0:
        print("No valid orders found in the file.")
        return

    choice = ""
    while choice != "4":
        print("\n===== MENU =====")
        print("1. Monthly spending")
        print("2. Order statistics")
        print("3. Category share and statistics")
        print("4. Exit")
        choice = input("Enter your choice (1-4): ")
        print()

        if choice == "1":
            monthly_spending(df)
        elif choice == "2":
            order_statistics(df)
        elif choice == "3":
            category_share(df)
        elif choice == "4":
            print("Thank you. Goodbye!")
        else:
            print("Invalid choice. Please enter a number from 1 to 4.")


if __name__ == "__main__":
    main()
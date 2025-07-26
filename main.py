import pandas as pd 
import csv
from datetime import datetime 
from data_entry import get_amount, get_category,get_date,get_description
import matplotlib.pyplot as plt

class CSV:
    csv_file = "finance_data.csv"
    columns = ["date", "amount", "category", "description"]
    FORMAT="%d-%m-%Y"
    
    @classmethod
    def initialize_csv(cls):
        try:
            pd.read_csv(cls.csv_file)
        except FileNotFoundError:
            df = pd.DataFrame(columns=cls.columns) #df=dataframes variable1    creating dataframe
            df.to_csv(cls.csv_file, index=False) #converting dataframe into csv

    @classmethod
    def add_entry(cls, date, amount, category, description):
        new_entry={
            "date":date,
            "amount":amount,
            "category": category,
            "description": description,
        }
        with open(cls.csv_file, "a", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=cls.columns)
            writer.writerow(new_entry)
        print("Entry added successfully")


    @classmethod
    def get_transaction(cls,start_date,end_date):
        df = pd.read_csv(cls.csv_file)
        df["date"] = pd.to_datetime(df["date"], format=CSV.FORMAT)
        df['amount'] = pd.to_numeric(df['amount'], errors='coerce')  
        start_date=datetime.strptime(start_date, CSV.FORMAT)
        end_date=datetime.strptime(end_date, CSV.FORMAT)

        mask=(df["date"]>=start_date)& (df["date"]<=end_date)
        filtered_df=df.loc[mask]

        if filtered_df.empty:
            print("No transaction found in the given data.")   
        else:
            print(f"Transaction from {start_date.strftime(CSV.FORMAT)} to {end_date.strftime(CSV.FORMAT)}")  
            print(filtered_df.to_string(index=False, formatters={"date": lambda x: x.strftime(CSV.FORMAT)}) ) 

            total_income=filtered_df[filtered_df["category"]=='Income']["amount"].sum()
            total_expense = filtered_df[filtered_df["category"]=='Expense']['amount'].sum()

            print("\n Summary")
            print(f"Total Income: ${total_income:.2f}")
            print(f"Total Expense: ${total_expense:.2f}")
            print(f"Net savings: ${(total_income-total_expense):.2f}")
        return filtered_df

def add():
    CSV.initialize_csv()
    date= get_date("Enter the date of the transcation (dd-mm-yy) or enter for today's date:", allow_default=True)
    amount=get_amount()
    category=get_category()
    description=get_description()
    CSV.add_entry(date,amount,category,description)

#CSV.get_transaction("01-01-2023", "30-07-2024")

def plot_transactions(df):
    df.set_index("date", inplace=True)

    income_df = (
        df[df["category"] == "Income"]
        .resample("D")
        .sum()
        .reindex(df.index, fill_value=0)
    )
    expense_df = (
        df[df["category"] == "Expense"]
        .resample("D")
        .sum()
        .reindex(df.index, fill_value=0)
    )

    plt.figure(figsize=(10, 5))
    plt.plot(income_df.index, income_df["amount"], label="Income", color="g")
    plt.plot(expense_df.index, expense_df["amount"], label="Expense", color="r")
    plt.xlabel("Date")
    plt.ylabel("Amount")
    plt.title("Income and Expenses Over Time")
    plt.legend()
    plt.grid(True)
    plt.show()


def main():
    while True:
        print("\n1.Add a new Transaction.")
        print("\n2.View transaction and summary within a date range.")
        print("\n3.Exit")
        choice=input("\n Enter your choice (1-3): ")
        if choice=='1':
            add()
        elif choice=='2':
            start_date = get_date("Enter the start date (dd-mm-yy): ")
            end_date= get_date("Enter the end date (dd-mm-yy): ")
            df=CSV.get_transaction(start_date,end_date)
            if input("Do you wnat to see a plot? (y/n) ").lower()=='y':
                plot_transactions(df)
        elif choice=='3':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Enter 1, 2, or 3")

if __name__=="__main__":
    main()
            
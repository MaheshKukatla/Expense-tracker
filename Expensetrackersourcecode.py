'''
 Hi, This is Mahesh Kukatla. i have done this project using Python Tkinter. Here user can add his different expenses by selecting his currency.user can add ,delete and save the expenses.
''''

import tkinter as tk
from tkinter import messagebox, ttk
import csv
from tkinter import filedialog
from datetime import datetime

class ExpenseTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker")

        self.expense_dict = {}

        # Configure style for ttk widgets
        style = ttk.Style()
        style.configure('TLabel', font=('Arial', 12))
        style.configure('TButton', font=('Arial', 12))
        style.configure('TCombobox', font=('Arial', 12))
        style.configure('TEntry', font=('Arial', 12))

        # Frame to hold the content
        content_frame = ttk.Frame(root, padding=(20, 10))
        content_frame.grid(row=0, column=0, sticky=tk.W+tk.E)

        # Expense Category Combobox
        ttk.Label(content_frame, text="Expense Category:").grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
        self.category_var = tk.StringVar()
        self.category_combobox = ttk.Combobox(content_frame, textvariable=self.category_var, values=[
            "Food & Groceries", "Transport", "Cable", "Subscriptions", "Insurance",
            "House Rent", "Taxes", "Savings", "Maintenance", "Childcare", 
            "Entertainment", "Debt Payments"
        ], state='readonly', width=30)
        self.category_combobox.grid(row=0, column=1, padx=10, pady=5, sticky=tk.W)

        # Amount Entry
        ttk.Label(content_frame, text="Amount:").grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
        self.amount_entry = ttk.Entry(content_frame, font=('Arial', 12), width=32)
        self.amount_entry.grid(row=1, column=1, padx=10, pady=5, sticky=tk.W)

        # Date Selection
        ttk.Label(content_frame, text="Date:").grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)
        self.day_var = tk.StringVar()
        self.month_var = tk.StringVar()
        self.year_var = tk.StringVar()
        
        self.day_combobox = ttk.Combobox(content_frame, textvariable=self.day_var, values=[str(i) for i in range(1, 32)], width=5)
        self.day_combobox.grid(row=2, column=1, padx=2, pady=5, sticky=tk.W)
        self.day_combobox.set(datetime.now().day)

        self.month_combobox = ttk.Combobox(content_frame, textvariable=self.month_var, values=[
            "January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December"
        ], width=10)
        self.month_combobox.grid(row=2, column=1, padx=2, pady=5)
        self.month_combobox.set(datetime.now().strftime("%B"))

        self.year_combobox = ttk.Combobox(content_frame, textvariable=self.year_var, values=[str(i) for i in range(2000, datetime.now().year + 1)], width=7)
        self.year_combobox.grid(row=2, column=1, padx=2, pady=5, sticky=tk.E)
        self.year_combobox.set(datetime.now().year)

        # Currency Combobox
        ttk.Label(content_frame, text="Currency:").grid(row=3, column=0, padx=10, pady=5, sticky=tk.W)
        self.currency_var = tk.StringVar()
        self.currency_combobox = ttk.Combobox(content_frame, textvariable=self.currency_var, values=[
            "INR - Indian Rupee", "USD - US Dollar", "EUR - Euro", "GBP - British Pound"
        ], state='readonly', width=30)
        self.currency_combobox.grid(row=3, column=1, padx=10, pady=5, sticky=tk.W)

        # Add Expense Button
        self.add_button = ttk.Button(content_frame, text="Add Expense", command=self.add_expense)
        self.add_button.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky=tk.W+tk.E)

        # Total Expenses Label
        self.total_expenses_label = ttk.Label(content_frame, text="Total Expenses: ₹ 0.00", font=('Arial', 14, 'bold'))
        self.total_expenses_label.grid(row=5, column=0, columnspan=2, padx=10, pady=5, sticky=tk.W)

        # Listbox to display added expenses
        ttk.Label(content_frame, text="Added Expenses:", font=('Arial', 12, 'bold')).grid(row=6, column=0, padx=10, pady=5, sticky=tk.W)
        self.expense_listbox = tk.Listbox(content_frame, height=10, width=50, font=('Arial', 12))
        self.expense_listbox.grid(row=7, column=0, columnspan=2, padx=10, pady=5, sticky=tk.W)

        # Delete Expense Button
        self.delete_button = ttk.Button(content_frame, text="Delete Expense", command=self.delete_expense)
        self.delete_button.grid(row=8, column=0, columnspan=2, padx=10, pady=10, sticky=tk.W+tk.E)

        # Export to CSV Button
        self.export_button = ttk.Button(content_frame, text="Export to CSV", command=self.export_to_csv)
        self.export_button.grid(row=9, column=0, columnspan=2, padx=10, pady=10, sticky=tk.W+tk.E)

        # Currency Symbols Dictionary
        self.currency_symbols = {
            "INR - Indian Rupee": "₹",  # Indian Rupee
            "USD - US Dollar": "$",    # US Dollar
            "EUR - Euro": "€",         # Euro
            "GBP - British Pound": "£"  # British Pound
        }

    def add_expense(self):
        category = self.category_var.get()
        amount_str = self.amount_entry.get()
        day = self.day_var.get()
        month = self.month_var.get()
        year = self.year_var.get()
        currency_selection = self.currency_var.get()

        if not category:
            messagebox.showerror("Error", "Please select an expense category")
            return

        if not amount_str:
            messagebox.showerror("Error", "Please enter an amount")
            return

        if not day or not month or not year:
            messagebox.showerror("Error", "Please select a valid date")
            return

        try:
            amount = float(amount_str)
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid amount")
            return

        month_number = datetime.strptime(month, "%B").month

        try:
            date = datetime(year=int(year), month=month_number, day=int(day)).date()
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid date")
            return

        currency_code = currency_selection.split(" - ")[0].strip()

        if category not in self.expense_dict:
            self.expense_dict[category] = []

        self.expense_dict[category].append((amount, currency_code, date))
        self.update_total_expenses()
        self.update_added_expenses_list()

        self.category_combobox.set('')
        self.amount_entry.delete(0, tk.END)

    def update_total_expenses(self):
        total_expenses = sum(sum(expense[0] for expense in expenses) for expenses in self.expense_dict.values())
        currency_selection = self.currency_var.get()
        currency_symbol = self.currency_symbols.get(currency_selection, "")
        self.total_expenses_label.config(text=f"Total Expenses: {currency_symbol} {total_expenses:.2f}")

    def update_added_expenses_list(self):
        self.expense_listbox.delete(0, tk.END)
        for category, expenses in self.expense_dict.items():
            for amount, currency_code, date in expenses:
                currency_selection = [key for key, value in self.currency_symbols.items() if key.startswith(currency_code)][0]
                currency_symbol = self.currency_symbols.get(currency_selection, "")
                self.expense_listbox.insert(tk.END, f"{category}: {currency_symbol} {amount:.2f} on {date.strftime('%d %B %Y')}")

    def delete_expense(self):
        selected_index = self.expense_listbox.curselection()
        if not selected_index:
            messagebox.showerror("Error", "Please select an expense to delete")
            return

        selected_expense = self.expense_listbox.get(selected_index)
        category = selected_expense.split(":")[0].strip()

        for key in list(self.expense_dict.keys()):
            if key == category:
                del self.expense_dict[key]

        self.update_total_expenses()
        self.update_added_expenses_list()

    def export_to_csv(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if not file_path:
            return

        with open(file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Category", "Amount", "Currency", "Date"])
            for category, expenses in self.expense_dict.items():
                for amount, currency_code, date in expenses:
                    writer.writerow([category, amount, currency_code, date.strftime('%Y-%m-%d')])

        messagebox.showinfo("Export Successful", "Expenses exported successfully!")

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTracker(root)
    root.mainloop()


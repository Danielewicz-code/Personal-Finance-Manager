import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import calendar
from finance import Income, Management  # Backend


class FinancialApp:
    def __init__(self, root) -> None:
        self.root = root
        self.root.title("Personal Finance Manager")
        self.root.geometry("380x400")
        self.root.configure(bg="black")

        # Aesthetics
        self.header_font = ("Helvetica", 14, "bold")
        self.label_font = ("Helvetica", 12)
        self.button_font = ("Helvetica", 12)
        self.bg_color = 'black'
        self.fg_color = 'white'
        self.button_bg = 'gray'
        self.entry_bg = 'white'
        self.entry_fg = 'black'

        # Initial values for classes
        self.income = Income(0)
        self.management = Management(575, 600, 825)

        self.create_main_window()

    def create_main_window(self):
        tk.Label(self.root, text="Welcome to Personal Finance Manager", font=self.header_font, bg=self.bg_color, fg=self.fg_color).pack(pady=20)

        income_button = tk.Button(self.root, text="Register Income", command=self.open_income_window, font=self.button_font, bg=self.button_bg, fg=self.fg_color, width=20)
        income_button.pack(pady=10)

        management_button = tk.Button(self.root, text="Manage Money", command=self.open_management_window, font=self.button_font, bg=self.button_bg, fg=self.fg_color, width=20)
        management_button.pack(pady=10)

        reset_month_button = tk.Button(self.root, text="Save/Reset Month", command=self.reset_month, font=self.button_font, bg=self.button_bg, fg=self.fg_color, width=20)
        reset_month_button.pack(pady=10)

    def open_income_window(self):
        income_window = tk.Toplevel(self.root)
        income_window.title("Register Income")
        income_window.geometry("400x150")
        income_window.configure(bg=self.bg_color)

        tk.Label(income_window, text="Enter Income:", font=self.label_font, bg=self.bg_color, fg=self.fg_color).pack(pady=10)
        income_entry = tk.Entry(income_window, font=self.label_font, bg=self.entry_bg, fg=self.entry_fg)
        income_entry.pack(pady=5)

        def add_income():
            try:
                amount = float(income_entry.get())
                self.income.add_income(amount)
                messagebox.showinfo("Success", f"Income of ${amount:.2f} added.")
                income_window.destroy()
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid amount.")

        add_button = tk.Button(income_window, text="Add Income", command=add_income, font=self.button_font, bg=self.button_bg, fg=self.fg_color)
        add_button.pack(pady=10)

    def open_management_window(self):
        management_window = tk.Toplevel(self.root)
        management_window.title("Money Management")
        management_window.geometry("400x300")
        management_window.configure(bg=self.bg_color)

        tk.Label(management_window, text="Enter Expense:", font=self.label_font, bg=self.bg_color, fg=self.fg_color).grid(row=0, column=0, padx=10, pady=10, sticky='e')
        expense_entry = tk.Entry(management_window, font=self.label_font, bg=self.entry_bg, fg=self.entry_fg)
        expense_entry.grid(row=0, column=1, padx=10, pady=10, sticky='w')

        tk.Label(management_window, text="Enter Reason:", font=self.label_font, bg=self.bg_color, fg=self.fg_color).grid(row=1, column=0, padx=10, pady=10, sticky='e')
        reason_entry = tk.Entry(management_window, font=self.label_font, bg=self.entry_bg, fg=self.entry_fg)
        reason_entry.grid(row=1, column=1, padx=10, pady=10, sticky='w')

        tk.Label(management_window, text="Enter Category:", font=self.label_font, bg=self.bg_color, fg=self.fg_color).grid(row=2, column=0, padx=10, pady=10, sticky='e')
        category_entry = tk.Entry(management_window, font=self.label_font, bg=self.entry_bg, fg=self.entry_fg)
        category_entry.grid(row=2, column=1, padx=10, pady=10, sticky='w')

        def add_expense():
            try:
                amount = float(expense_entry.get())
                reason = reason_entry.get()
                category = category_entry.get().lower()
                self.management.add_expense(amount, reason, category)
                messagebox.showinfo("Success", f"Expense of ${amount:.2f} for {reason} was added to {category} category.")
                management_window.destroy()
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid number")

        add_button = tk.Button(management_window, text="Add Expense", command=add_expense, font=self.button_font, bg=self.button_bg, fg=self.fg_color)
        add_button.grid(row=3, column=1, padx=10, pady=10)

        tk.Label(management_window, text="Expenses:", font=self.label_font, bg=self.bg_color, fg=self.fg_color).grid(row=4, column=0, padx=10, pady=10, sticky='e')

        def check_expenses():
            expenses_check = self.management.expenses
            if not expenses_check:
                messagebox.showinfo("Expenses", "No expenses recorded.")
                return

            expense_details = "\n".join([f"{expense['Date']}: ${expense['Amount']:.2f} - {expense['Reason']} ({expense['Category']})" for expense in expenses_check])
            messagebox.showinfo("Expenses", expense_details)

        check_button = tk.Button(management_window, text="Check Expenses", command=check_expenses, font=self.button_font, bg=self.button_bg, fg=self.fg_color)
        check_button.grid(row=4, column=1, padx=10, pady=10)

    def reset_month(self):
        today = datetime.today()
        last_day_month = calendar.monthrange(today.year, today.month)[1]
        if today == last_day_month:
            self.management.reset_month()
            messagebox.showinfo("Success", "Monthly data has been stored and reset")
        else:
            messagebox.showerror("Error", "Today is not the last day of the month.")

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    root = tk.Tk()
    app = FinancialApp(root)
    app.run()

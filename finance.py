from datetime import datetime
import json

class Income:
    def __init__(self, income):
        self.income = float(income)
        self.date = datetime.now()

    def add_income(self, new_income):
        self.income += float(new_income)
    
    def __str__(self) -> str:
        return f"${self.income:.2f} was the income this month\nRegistered on: {self.date.strftime('%Y-%m-%d')}"


class Management:
    def __init__(self, savings_limit, expenses_limit, recurring_limit):
        #limits
        self.savings_limit = float(savings_limit)
        self.expenses_limit = float(expenses_limit)
        self.recurring_expenses = float(recurring_limit)
        #remaining
        self.remaining_savings = self.savings_limit
        self.remaining_expenses = self.expenses_limit
        self.remaining_recurring_expenses = self.recurring_expenses

        #placeholders
        self.expenses = []
        self.total_expenses = 0


    def add_expense(self, amount, reason, category="general"):
        category = category.lower()
        new_expense = {
            "Amount": float(amount),
            "Reason": reason,
            "Category": category,
            "Date": datetime.now().strftime('%Y-%m-%d')
        }

        self.expenses.append(new_expense)
        self.total_expenses += new_expense["Amount"]

        if category == "savings":
            self.remaining_savings -= new_expense["Amount"]
        elif category == "expenses":
            self.remaining_expenses -= new_expense["Amount"]
        elif category == "recurring":
            self.remaining_recurring_expenses -= new_expense["Amount"]
        else:
            raise ValueError("Invalid Category")
        
        return f"${amount:.2f} for {reason} was added to {category} expenses."
    
    def check_limits(self):
        limits_status = {
            "savings_limit":self.savings_limit,
            "remaining_savings":self.remaining_savings,
            "expense_limit":self.expenses_limit,
            "remaining_expenses":self.remaining_expenses,
            "recourring_expenses_limit":self.recurring_expenses,
            "remaining_recourring_expenses":self.remaining_recurring_expenses,
            "total_expenses":self.total_expenses
        }
        return limits_status

    def store_monthly_data(self):
        month = datetime.now().strftime('%Y-%m')

        data = {
            'month':month,
            'expenses:':self.expenses,
            'total_expenses':self.total_expenses,
            "savings_limit":self.savings_limit,
            "expense_limit":self.expenses_limit,
            "recourring_expenses_limit":self.recurring_expenses,
            "remaining_savings":self.remaining_savings,
            "remaining_expenses":self.remaining_expenses,
            "remaining_recourring_expenses":self.remaining_recurring_expenses
        }

        with open(f"financial_data_{month}.json", "w") as file:
            json.dump(data, file)


    def reset_month(self):
        self.store_monthly_data() #store data before resetting
        self.expenses = []
        self.total_expenses = 0
        self.remaining_savings = self.savings_limit
        self.remaining_expenses = self.expenses_limit
        self.remaining_recurring_expenses = self.recurring_expenses




# --- fixed imports ---
import sqlite3
import matplotlib.pyplot as plt
# <--- phase1- setup database connection and create table if not exists

def init_db():
    conn = sqlite3.connect('budget_tracker.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            category TEXT NOT NULL,
            amount REAL NOT NULL,
            description TEXT
        )
    ''')
    conn.commit()
    conn.close()

# <--- phase2- function to add expense

# --- fixed function signature and usage ---
def add_expense(category, amount, date, description=None):
    conn = sqlite3.connect('budget_tracker.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO expenses (date, category, amount, description)
        VALUES (?, ?, ?, ?)
    ''', (date, category, amount, description))
    conn.commit()
    conn.close()
    print("Expense added successfully.")

# <--- phase3- function to view expenses

def view_expenses():
    conn = sqlite3.connect('budget_tracker.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM expenses')
    expenses = cursor.fetchall()
    conn.close()
    
    print("\n current expenses:\n")

    for row in expenses:
        print(f"ID: {row[0]}, Date: {row[1]}, Category: {row[2]}, Amount: {row[3]}, Description: {row[4]}")

def show_chart():
    conn = sqlite3.connect('budget_tracker.db')
    cursor = conn.cursor()
    cursor.execute('SELECT category, SUM(amount) FROM expenses GROUP BY category')
    data = cursor.fetchall()
    conn.close()
    
    categories = [row[0] for row in data]
    amounts = [row[1] for row in data]
    
    plt.bar(categories, amounts)
    plt.xlabel('Category')
    plt.ylabel('Total Amount Spent')
    plt.title('Expenses by Category')
    plt.show()

# <--- phase4- main menu loop



# --- GUI implementation using Tkinter ---
import tkinter as tk
from tkinter import ttk, messagebox


def launch_gui():
    init_db()
    root = tk.Tk()
    root.title("Budget Tracker")
    root.geometry("500x400")

    # Labels and Entry fields
    tk.Label(root, text="Date (YYYY-MM-DD):").grid(row=0, column=0, padx=10, pady=5, sticky='e')
    date_entry = tk.Entry(root)
    date_entry.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(root, text="Category:").grid(row=1, column=0, padx=10, pady=5, sticky='e')
    category_entry = tk.Entry(root)
    category_entry.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(root, text="Amount:").grid(row=2, column=0, padx=10, pady=5, sticky='e')
    amount_entry = tk.Entry(root)
    amount_entry.grid(row=2, column=1, padx=10, pady=5)

    tk.Label(root, text="Description:").grid(row=3, column=0, padx=10, pady=5, sticky='e')
    description_entry = tk.Entry(root)
    description_entry.grid(row=3, column=1, padx=10, pady=5)

    # Placeholder for expenses display
    expenses_text = tk.Text(root, height=10, width=55)
    expenses_text.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

    # --- Button functions ---
    def on_add():
        date = date_entry.get().strip()
        category = category_entry.get().strip()
        amount_str = amount_entry.get().strip()
        description = description_entry.get().strip()
        if not date or not category or not amount_str:
            messagebox.showerror("Input Error", "Date, Category, and Amount are required.")
            return
        try:
            amount = float(amount_str)
        except ValueError:
            messagebox.showerror("Input Error", "Amount must be a number.")
            return
        add_expense(category, amount, date, description)
        messagebox.showinfo("Success", "Expense added successfully.")
        # Clear fields
        date_entry.delete(0, tk.END)
        category_entry.delete(0, tk.END)
        amount_entry.delete(0, tk.END)
        description_entry.delete(0, tk.END)

    # Buttons
    add_btn = tk.Button(root, text="Add Expense", command=on_add)
    add_btn.grid(row=4, column=0, padx=10, pady=10)


    def on_view():
        conn = sqlite3.connect('budget_tracker.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM expenses')
        expenses = cursor.fetchall()
        conn.close()
        expenses_text.delete(1.0, tk.END)
        if not expenses:
            expenses_text.insert(tk.END, "No expenses found.\n")
        else:
            for row in expenses:
                expenses_text.insert(tk.END, f"ID: {row[0]}, Date: {row[1]}, Category: {row[2]}, Amount: {row[3]}, Description: {row[4]}\n")

    view_btn = tk.Button(root, text="View Expenses", command=on_view)
    view_btn.grid(row=4, column=1, padx=10, pady=10)


    def on_chart():
        show_chart()

    chart_btn = tk.Button(root, text="Show Chart", command=on_chart)
    chart_btn.grid(row=5, column=0, padx=10, pady=10)

    exit_btn = tk.Button(root, text="Exit", command=root.destroy)
    exit_btn.grid(row=5, column=1, padx=10, pady=10)

    root.mainloop()

if __name__ == "__main__":
    launch_gui()
                           
	
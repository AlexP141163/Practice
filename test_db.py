import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# Создание или подключение к базе данных
conn = sqlite3.connect('medical_sales.db')
c = conn.cursor()

# Создание таблиц, если они ещё не созданы
c.execute('''
CREATE TABLE IF NOT EXISTS organizations (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    account TEXT NOT NULL,
    bank_name TEXT NOT NULL
)
''')

c.execute('''
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    price REAL NOT NULL
)
''')

c.execute('''
CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY,
    organization_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    status TEXT NOT NULL,
    FOREIGN KEY(organization_id) REFERENCES organizations(id),
    FOREIGN KEY(product_id) REFERENCES products(id)
)
''')

conn.commit()

class MainApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Medical Equipment Sales Service")
        self.geometry("800x600")

        # Основные виджеты
        self.create_widgets()

    def create_widgets(self):
        # Ввод данных организации
        tk.Label(self, text="Organization Name:").grid(row=0, column=0)
        self.org_name_entry = tk.Entry(self)
        self.org_name_entry.grid(row=0, column=1)

        tk.Label(self, text="Account Number:").grid(row=1, column=0)
        self.account_entry = tk.Entry(self)
        self.account_entry.grid(row=1, column=1)

        tk.Label(self, text="Bank Name:").grid(row=2, column=0)
        self.bank_name_entry = tk.Entry(self)
        self.bank_name_entry.grid(row=2, column=1)

        # Кнопки для открытия дополнительных окон
        tk.Button(self, text="Organizations Directory", command=self.open_org_window).grid(row=3, column=0)
        tk.Button(self, text="Products Form", command=self.open_product_window).grid(row=3, column=1)

        # Место для вывода заказов
        self.orders_frame = tk.Frame(self)
        self.orders_frame.grid(row=4, column=0, columnspan=2)
        self.display_orders()

    def open_org_window(self):
        org_window = OrganizationWindow(self)
        org_window.grab_set()

    def open_product_window(self):
        product_window = ProductWindow(self)
        product_window.grab_set()

    def display_orders(self):
        # Очистка предыдущих виджетов
        for widget in self.orders_frame.winfo_children():
            widget.destroy()

        tk.Label(self.orders_frame, text="Orders:").pack()
        rows = c.execute("SELECT * FROM orders").fetchall()
        for row in rows:
            tk.Label(self.orders_frame, text=str(row)).pack()

class OrganizationWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Organizations Directory")
        self.geometry("300x200")
        self.master = master

        tk.Label(self, text="Name:").grid(row=0, column=0)
        self.name_entry = tk.Entry(self)
        self.name_entry.grid(row=0, column=1)

        tk.Label(self, text="Account:").grid(row=1, column=0)
        self.account_entry = tk.Entry(self)
        self.account_entry.grid(row=1, column=1)

        tk.Label(self, text="Bank:").grid(row=2, column=0)
        self.bank_entry = tk.Entry(self)
        self.bank_entry.grid(row=2, column=1)

        tk.Button(self, text="Add Organization", command=self.add_organization).grid(row=3, column=0, columnspan=2)

    def add_organization(self):
        name = self.name_entry.get()
        account = self.account_entry.get()
        bank = self.bank_entry.get()
        c.execute("INSERT INTO organizations (name, account, bank_name) VALUES (?, ?, ?)", (name, account, bank))
        conn.commit()
        self.master.display_orders()

class ProductWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Products Form")
        self.geometry("300x200")

        tk.Label(self, text="Product Name:").grid(row=0, column=0)
        self.name_entry = tk.Entry(self)
        self.name_entry.grid(row=0, column=1)

        tk.Label(self, text="Price:").grid(row=1, column=0)
        self.price_entry = tk.Entry(self)
        self.price_entry.grid(row=1, column=1)

        tk.Button(self, text="Add Product", command=self.add_product).grid(row=2, column=0, columnspan=2)

    def add_product(self):
        name = self.name_entry.get()
        price = float(self.price_entry.get())
        c.execute("INSERT INTO products (name, price) VALUES (?, ?)", (name, price))
        conn.commit()
        self.master.display_orders()

if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()
import sqlite3
import tkinter as tk
from tkinter import ttk, simpledialog

# Подключение к базе данных
conn = sqlite3.connect('medical_equipment.db')
cursor = conn.cursor()

# Главное окно приложения
root = tk.Tk()
root.title("Medical Equipment Sales Management")

# Загрузка данных
def load_data():
    cursor.execute('SELECT id, organization_name FROM customers')
    customers = ["{} - {}".format(id, name) for id, name in cursor.fetchall()]
    customer_combobox['values'] = customers

    cursor.execute('SELECT id, product_name, cost FROM products')
    products = ["{} - {} - {:.2f}".format(id, name, cost) for id, name, cost in cursor.fetchall()]
    product_combobox['values'] = products

# Вычисление общей стоимости заказа
def calculate_total_cost(*args):
    try:
        product_info = product_combobox.get().split(' - ')
        product_id = product_info[0]
        cost = float(product_info[2])
        quantity = int(quantity_entry.get())
        total_cost.set(quantity * cost)
    except (ValueError, IndexError):
        total_cost.set(0)

# Добавление организации
def add_organization():
    organization_name = simpledialog.askstring("Add Organization", "Enter organization name:")
    account_number = simpledialog.askstring("Add Organization", "Enter account number:")
    bank_name = simpledialog.askstring("Add Organization", "Enter bank name:")
    if organization_name and account_number and bank_name:
        cursor.execute('INSERT INTO customers (organization_name, account_number, bank_name) VALUES (?, ?, ?)',
                       (organization_name, account_number, bank_name))
        conn.commit()
        load_data()

# Добавление товара
def add_product():
    product_name = simpledialog.askstring("Add Product", "Enter product name:")
    cost = simpledialog.askfloat("Add Product", "Enter cost:")
    if product_name and cost:
        cursor.execute('INSERT INTO products (product_name, cost) VALUES (?, ?)', (product_name, cost))
        conn.commit()
        load_data()

# Создание заказа
def create_order():
    customer_info = customer_combobox.get().split(' - ')
    product_info = product_combobox.get().split(' - ')
    customer_id = customer_info[0]
    product_id = product_info[0]
    quantity = quantity_entry.get()
    total = total_cost.get()
    status = status_combobox.get()
    cursor.execute('INSERT INTO orders (customer_id, product_id, quantity, total_cost, status) VALUES (?, ?, ?, ?, ?)',
                   (customer_id, product_id, quantity, total, status))
    conn.commit()
    messagebox.showinfo("Success", "Order created successfully!")

# Инициализация виджетов
customer_combobox = ttk.Combobox(root, width=30)
product_combobox = ttk.Combobox(root, width=30)
quantity_entry = ttk.Entry(root)
total_cost = tk.DoubleVar()
total_cost_label = ttk.Label(root, textvariable=total_cost)
status_combobox = ttk.Combobox(root, values=["Active", "Closed"], width=10)
status_combobox.set("Active")

# Расположение виджетов
customer_combobox.grid(row=0, column=0, padx=10, pady=10)
product_combobox.grid(row=0, column=1, padx=10, pady=10)
quantity_entry.grid(row=0, column=2, padx=10, pady=10)
total_cost_label.grid(row=0, column=3, padx=10, pady=10)
status_combobox.grid(row=0, column=4, padx=10, pady=10)
ttk.Button(root, text="Create Order", command=create_order).grid(row=1, column=0, columnspan=5, pady=10)
ttk.Button(root, text="Add Organization", command=add_organization).grid(row=2, column=0, columnspan=2, sticky=tk.W+tk.E, padx=10, pady=10)
ttk.Button(root, text="Add Product", command=add_product).grid(row=2, column=2, columnspan=2, sticky=tk.W+tk.E, padx=10, pady=10)

# Привязка событий
product_combobox.bind('<<ComboboxSelected>>', calculate_total_cost)
quantity_entry.bind('<KeyRelease>', calculate_total_cost)

# Загрузка начальных данных
load_data()

root.mainloop()
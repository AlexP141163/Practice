import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo, showerror
import sqlite3


def create_database():
    try:
        conn = sqlite3.connect('orders.db')
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS companies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                account_number TEXT NOT NULL,
                bank_name TEXT NOT NULL
            )
        ''')
        c.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                price REAL NOT NULL
            )
        ''')
        c.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                company_id INTEGER,
                product_id INTEGER,
                quantity INTEGER,
                total_price REAL,
                status TEXT,
                FOREIGN KEY (company_id) REFERENCES companies (id),
                FOREIGN KEY (product_id) REFERENCES products (id)
            )
        ''')
        conn.commit()
    except sqlite3.Error as e:
        showerror("Database Error", e)
    finally:
        conn.close()


def fetch_companies():
    try:
        conn = sqlite3.connect('orders.db')
        c = conn.cursor()
        c.execute("SELECT id, name FROM companies")
        companies = c.fetchall()
        conn.close()
        return companies
    except sqlite3.Error as e:
        showerror("Database Error", e)
        return []


def fetch_products():
    try:
        conn = sqlite3.connect('orders.db')
        c = conn.cursor()
        c.execute("SELECT id, name, price FROM products")
        products = c.fetchall()
        conn.close()
        return products
    except sqlite3.Error as e:
        showerror("Database Error", e)
        return []


def insert_company(name, account_number, bank_name):
    try:
        conn = sqlite3.connect('orders.db')
        c = conn.cursor()
        c.execute("INSERT INTO companies (name, account_number, bank_name) VALUES (?, ?, ?)",
                  (name, account_number, bank_name))
        conn.commit()
    except sqlite3.Error as e:
        showerror("Database Error", e)
    finally:
        conn.close()


def insert_product(name, price):
    try:
        conn = sqlite3.connect('orders.db')
        c = conn.cursor()
        c.execute("INSERT INTO products (name, price) VALUES (?, ?)", (name, float(price)))
        conn.commit()
    except sqlite3.Error as e:
        showerror("Database Error", e)
    finally:
        conn.close()


def insert_order(company_id, product_id, quantity, total_price, status):
    try:
        conn = sqlite3.connect('orders.db')
        c = conn.cursor()
        c.execute("INSERT INTO orders (company_id, product_id, quantity, total_price, status) VALUES (?, ?, ?, ?, ?)",
                  (company_id, product_id, int(quantity), float(total_price), status))
        conn.commit()
    except sqlite3.Error as e:
        showerror("Database Error", e)
    finally:
        conn.close()
        showinfo("Success", "Order has been added successfully")


def add_company_window(update_callback):
    window = tk.Toplevel()
    window.title("Add New Company")

    ttk.Label(window, text="Company Name:").grid(row=0, column=0)
    name_entry = ttk.Entry(window)
    name_entry.grid(row=0, column=1)

    ttk.Label(window, text="Account Number:").grid(row=1, column=0)
    account_number_entry = ttk.Entry(window)
    account_number_entry.grid(row=1, column=1)

    ttk.Label(window, text="Bank Name:").grid(row=2, column=0)
    bank_name_entry = ttk.Entry(window)
    bank_name_entry.grid(row=2, column=1)

    ttk.Button(window, text="Add Company",
               command=lambda: [insert_company(name_entry.get(), account_number_entry.get(), bank_name_entry.get()),
                                update_callback(), window.destroy()]).grid(row=3, columnspan=2)


def add_product_window(update_callback):
    window = tk.Toplevel()
    window.title("Add New Product")

    ttk.Label(window, text="Product Name:").grid(row=0, column=0)
    name_entry = ttk.Entry(window)
    name_entry.grid(row=0, column=1)

    ttk.Label(window, text="Price:").grid(row=1, column=0)
    price_entry = ttk.Entry(window)
    price_entry.grid(row=1, column=1)

    ttk.Button(window, text="Add Product",
               command=lambda: [insert_product(name_entry.get(), price_entry.get()), update_callback(),
                                window.destroy()]).grid(row=2, columnspan=2)


def main_app_window():
    root = tk.Tk()
    root.title("Order Management System")

    # Элементы управления
    ttk.Label(root, text="Select Company:").grid(row=0, column=0)
    company_cb = ttk.Combobox(root)
    company_cb.grid(row=0, column=1)

    ttk.Label(root, text="Select Product:").grid(row=1, column=0)
    product_cb = ttk.Combobox(root)
    product_cb.grid(row=1, column=1)

    ttk.Label(root, text="Quantity:").grid(row=2, column=0)
    quantity_entry = ttk.Entry(root)
    quantity_entry.grid(row=2, column=1)

    ttk.Label(root, text="Total Price:").grid(row=3, column=0)
    total_price_label = ttk.Label(root, text="0")
    total_price_label.grid(row=3, column=1)

    # Вычисление и обновление общей суммы
    def calculate_total():
        try:
            if product_cb.get() and quantity_entry.get().isdigit():
                _, price, _ = eval(product_cb.get())
                total = float(price) * int(quantity_entry.get())
                total_price_label.config(text=str(total))
                return total
            return 0
        except Exception as e:
            showerror("Calculation Error", "Error calculating total price: " + str(e))
            return 0

    quantity_entry.bind("<KeyRelease>", lambda e: calculate_total())

    ttk.Label(root, text="Order Status:").grid(row=4, column=0)
    status_cb = ttk.Combobox(root, values=["Active", "Closed"], state="readonly")
    status_cb.grid(row=4, column=1)
    status_cb.set("Active")

    # Обновление данных в комбобоксах
    def update_comboboxes():
        company_cb['values'] = [(c[1], c[0]) for c in fetch_companies()]
        product_cb['values'] = [(p[1], p[2], p[0]) for p in fetch_products()]

    ttk.Button(root, text="Add Company", command=lambda: add_company_window(update_comboboxes)).grid(row=5, column=0)
    ttk.Button(root, text="Add Product", command=lambda: add_product_window(update_comboboxes)).grid(row=5, column=1)
    ttk.Button(root, text="Add Order",
               command=lambda: insert_order(eval(company_cb.get())[1], eval(product_cb.get())[2], quantity_entry.get(),
                                            calculate_total(), status_cb.get())).grid(row=5, column=2)

    update_comboboxes()
    root.mainloop()


if __name__ == "__main__":
    main_app_window()
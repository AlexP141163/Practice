import tkinter as tk
from tkinter import ttk
import sqlite3

class OrderManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Управление заказами")

        self.conn = self.create_connection("enterprise.db")
        self.setup_db()

        # Элементы управления для добавления клиента
        self.add_client_frame = tk.Frame(self.root)
        self.add_client_frame.pack(pady=10)

        tk.Label(self.add_client_frame, text="Имя клиента:").pack(side=tk.LEFT)
        self.client_name_var = tk.StringVar()
        tk.Entry(self.add_client_frame, textvariable=self.client_name_var).pack(side=tk.LEFT)
        tk.Button(self.add_client_frame, text="Добавить клиента", command=self.add_client).pack(side=tk.LEFT)

        # Элементы управления для создания заказа
        self.add_order_frame = tk.Frame(self.root)
        self.add_order_frame.pack(pady=10)

        tk.Label(self.add_order_frame, text="Выберите клиента:").pack(side=tk.LEFT)
        self.client_combobox = ttk.Combobox(self.add_order_frame)
        self.client_combobox.pack(side=tk.LEFT)
        self.update_client_list()

        tk.Button(self.add_order_frame, text="Создать заказ", command=self.add_order).pack(side=tk.LEFT)

        # Элементы управления для обновления статуса заказа
        self.update_order_frame = tk.Frame(self.root)
        self.update_order_frame.pack(pady=10)

        tk.Label(self.update_order_frame, text="ID заказа:").pack(side=tk.LEFT)
        self.order_id_var = tk.StringVar()
        tk.Entry(self.update_order_frame, textvariable=self.order_id_var).pack(side=tk.LEFT)

        self.status_var = tk.StringVar()
        tk.OptionMenu(self.update_order_frame, self.status_var, 'выполняется', 'выполнен').pack(side=tk.LEFT)

        tk.Button(self.update_order_frame, text="Обновить статус", command=self.update_order_status).pack(side=tk.LEFT)

    def create_connection(self, db_file):
        conn = None
        try:
            conn = sqlite3.connect(db_file)
        except Exception as e:
            print(e)
        return conn

    def setup_db(self):
        create_clients_table = """CREATE TABLE IF NOT EXISTS clients (
                                      id integer PRIMARY KEY,
                                      name text NOT NULL
                                  );"""
        create_orders_table = """CREATE TABLE IF NOT EXISTS orders (
                                     id integer PRIMARY KEY,
                                     client_id integer NOT NULL,
                                     status text NOT NULL,
                                     FOREIGN KEY (client_id) REFERENCES clients (id)
                                 );"""
        if self.conn:
            self.create_table(create_clients_table)
            self.create_table(create_orders_table)

    def create_table(self, create_table_sql):
        try:
            c = self.conn.cursor()
            c.execute(create_table_sql)
        except Exception as e:
            print(e)

    def add_client(self):
        client_name = self.client_name_var.get()
        if client_name:
            sql = "INSERT INTO clients(name) VALUES(?)"
            cur = self.conn.cursor()
            cur.execute(sql, (client_name,))
            self.conn.commit()
            self.client_name_var.set("")  # Очистить поле ввода
            self.update_client_list()  # Обновить список клиентов

    def update_client_list(self):
        sql = "SELECT id, name FROM clients"
        cur = self.conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        self.client_combobox['values'] = [row[1] for row in rows]

    def add_order(self):
        client_name = self.client_combobox.get()
        if client_name:
            client_id = self.get_client_id(client_name)
            if client_id:
                sql = "INSERT INTO orders(client_id, status) VALUES(?, 'выполняется')"
                cur = self.conn.cursor()
                cur.execute(sql, (client_id,))
                self.conn.commit()

    def get_client_id(self, name):
        sql = "SELECT id FROM clients WHERE name = ?"
        cur = self.conn.cursor()
        cur.execute(sql, (name,))
        result = cur.fetchone()
        return result[0] if result else None

    def update_order_status(self):
        order_id = self.order_id_var.get()
        status = self.status_var.get()
        if order_id and status:
            sql = "UPDATE orders SET status = ? WHERE id = ?"
            cur = self.conn.cursor()
            cur.execute(sql, (status, order_id))
            self.conn.commit()

if __name__ == '__main__':
    root = tk.Tk()
    app = OrderManagementApp(root)
    root.mainloop()


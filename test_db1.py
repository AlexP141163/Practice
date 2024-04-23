import sqlite3
import tkinter as tk
from tkinter import ttk


# Подключаемся к базе данных (или создаем новую)
conn = sqlite3.connect('example.db')
c = conn.cursor()

# Создаем таблицы
c.execute('''CREATE TABLE IF NOT EXISTS categories
             (id INTEGER PRIMARY KEY, name TEXT)''')
c.execute('''CREATE TABLE IF NOT EXISTS products
             (id INTEGER PRIMARY KEY, name TEXT, category_id INTEGER,
              FOREIGN KEY (category_id) REFERENCES categories(id))''')

# Добавляем примеры категорий
c.execute("INSERT INTO categories (name) VALUES ('Electronics')")
c.execute("INSERT INTO categories (name) VALUES ('Clothing')")
c.execute("INSERT INTO categories (name) VALUES ('Books')")

# Сохраняем изменения и закрываем соединение
conn.commit()
conn.close()

# Функция для добавления продукта
def add_product():
    product_name = name_entry.get()
    category = category_combobox.get()
    # Находим id категории
    category_id = category_ids[category]
    # Добавляем продукт в базу
    c.execute("INSERT INTO products (name, category_id) VALUES (?, ?)", (product_name, category_id))
    conn.commit()
    name_entry.delete(0, tk.END)  # Очищаем поле ввода
    result_label.config(text=f"Продукт '{product_name}' добавлен в категорию '{category}'")

# Подключаемся к базе данных
conn = sqlite3.connect('example.db')
c = conn.cursor()

# Загружаем категории из базы данных
c.execute("SELECT id, name FROM categories")
categories = c.fetchall()
category_ids = {name: id for id, name in categories}

# Создаем окно приложения
root = tk.Tk()
root.title("Продуктовый менеджер")

# Элементы управления
tk.Label(root, text="Название продукта:").pack()
name_entry = tk.Entry(root)
name_entry.pack()

tk.Label(root, text="Выберите категорию:").pack()
category_combobox = ttk.Combobox(root, values=[name for _, name in categories])
category_combobox.pack()

tk.Button(root, text="Добавить продукт", command=add_product).pack()

result_label = tk.Label(root, text="")
result_label.pack()

# Запускаем GUI
root.mainloop()

# Не забудьте закрыть соединение с базой данных
conn.close()

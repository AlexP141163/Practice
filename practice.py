
class Book:
    def __init__(self, title, author, year):
        self.title = title      # Название книги:
        self.author = author    # Имя автора:
        self.year = year        # Год издания:
        self.is_available = True   # Книга доступна:

    def set_availability(self, is_available):  # Наличие в библиотеке. "True" - в наличии, "False" - на руках:
        self.is_available = is_available
        return self.is_available

    def get_availability(self):  # Книга отсутствует, взята на руки:
        return self.is_available

class Library:
    def __init__(self):
        self.books = [] # Список для хранения книг:

    # def add_book(self, title, author, year): # Метод добавлять новую книгу:
        #self.books.append(Book(title, author, year))

    def add_book(self, Book): # Метод добалять новую книгу. Думаю это наследование???, запись выше равноценная:
        self.books.append(Book)

    def show_available_books(self):
        available_books = [book for book in self.books if book.get_availability()]
        if available_books: # Эта строка проверяет, не пуст ли список available_books. В Python непустой список
                            # в логическом контексте воспринимается как True. Если есть хотя бы одна доступная
                            #книга, условие истинно, и выполняется блок кода, следующий за if.

        #Вывод списка доступных книг:
            print("Доступные книги:")
            for book in available_books:
                print(f"{book.title} by {book.author}, {book.year}")
        else:
            print("В данный момент нет доступных книг.")

            # Пояснение для меня: Здесь используется списковое включение (list comprehension),
            # чтобы создать список available_books. В этот список включаются только те книги
            # из списка self.books, которые доступны. Доступность книги проверяется с помощью
            # метода get_availability() каждой книги. Если метод возвращает True, книга считается доступной
            # и включается в список available_books.

# Создание некоторых книг и добавление их в библиотеку
library = Library()
library.add_book(Book("Война и мир", "Лев Толстой", 1869))
library.add_book(Book("1984", "Джордж Оруэлл", 1949))

# Демонстрация работы метода показа доступных книг
library.show_available_books()

# Предположим, что книга "1984" была взята, и обновим её статус
library.books[1].set_availability(False)

# Снова показываем доступные книги
library.show_available_books()

import sys
import sqlite3
import hashlib
import pandas as pd
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLineEdit,
    QPushButton, QMessageBox, QComboBox, QTableWidget,
    QTableWidgetItem, QDialog
)


class Database:
    def __init__(self, db_name='bookstore.db'):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def create_tables(self):
        self.cursor.execute("DROP TABLE IF EXISTS orders")
        self.cursor.execute("DROP TABLE IF EXISTS books")
        self.cursor.execute("DROP TABLE IF EXISTS users")

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                username TEXT,
                email TEXT,
                phone TEXT,
                login TEXT UNIQUE,
                password TEXT,
                role TEXT
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY,
                title TEXT,
                author TEXT,
                genre TEXT,
                price REAL,
                stock INTEGER
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY,
                book_id INTEGER,
                user_id INTEGER,
                quantity INTEGER,
                FOREIGN KEY (book_id) REFERENCES books (id),
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        self.conn.commit()

    def close(self):
        self.conn.close()

    def populate_books(self):
        books = [
            ("Преступление и наказание", "Фёдор Достоевский", "Роман", 500.0, 100),
            ("Война и мир", "Лев Толстой", "Роман", 800.0, 50),
            ("Анна Каренина", "Лев Толстой", "Роман", 700.0, 60),
            ("Мастер и Маргарита", "Михаил Булгаков", "Роман", 600.0, 70),
            ("Тихий Дон", "Михаил Шолохов", "Роман", 550.0, 40),
            ("Доктор Живаго", "Борис Пастернак", "Роман", 750.0, 30),
            ("Муму", "Иван Тургенев", "Повесть", 300.0, 90),
            ("Собачье сердце", "Михаил Булгаков", "Повесть", 400.0, 80),
            ("Анна Каренина", "Лев Толстой", "Роман", 500.0, 10),
            ("Семейное счастие", "Лев Толстой", "Роман", 450.0, 5),
            ("Война и мир", "Лев Толстой", "Роман", 200.0, 2),
            ("Воскресение", "Лев Толстой", "Роман", 250.0, 8),
            ("Детство", "Лев Толстой", "Повесть", 300.0, 3),
            ("Отрочество", "Лев Толстой", "Повесть", 350.0, 1),
            ("Юность", "Лев Толстой", "Повесть", 400.0, 4),
            ("Казаки", "Лев Толстой", "Повесть", 450.0, 6),
            ("Хаджи-Мурат", "Лев Толстой", "Повесть", 500.0, 7),
            ("Севастопольские рассказы", "Лев Толстой", "Рассказ", 550.0, 9),
            ("Люцерн", "Лев Толстой", "Рассказ", 100.0, 10),
            ("Набег", "Лев Толстой", "Рассказ", 150.0, 5),
            ("Рубка леса", "Лев Толстой", "Рассказ", 200.0, 2),
            ("Нигилист", "Лев Толстой", "Драма", 250.0, 8),
            ("Зараженное семейство", "Лев Толстой", "Драма", 300.0, 3),
            ("Вишнёвый сад", "Антон Чехов", "Пьеса", 350.0, 1),
            ("Степь", "Антон Чехов", "Повесть", 400.0, 4),
            ("Дуэль", "Антон Чехов", "Повесть", 450.0, 6),
            ("Человек в футляре", "Антон Чехов", "Повесть", 500.0, 7),
            ("Три сестры", "Антон Чехов", "Пьеса", 550.0, 9),
            ("Дядя Ваня", "Антон Чехов", "Пьеса", 100.0, 10),
            ("Письмо к учёному соседу", "Антон Чехов", "Рассказ", 150.0, 5),
            ("Мой юбилей", "Антон Чехов", "Рассказ", 200.0, 2),
            ("Папаша", "Антон Чехов", "Рассказ", 250.0, 8),
            ("Бедные люди", "Федор Достоевский", "Роман", 300.0, 3),
            ("Преступление и наказание", "Федор Достоевский", "Роман", 350.0, 1),
            ("Игрок", "Федор Достоевский", "Роман", 400.0, 4),
            ("Бесы", "Федор Достоевский", "Роман", 450.0, 6),
            ("Двойник", "Федор Достоевский", "Повесть", 500.0, 7),
            ("Хозяйка", "Федор Достоевский", "Повесть", 550.0, 9),
            ("Белые ночи", "Федор Достоевский", "Повесть", 100.0, 10),
            ("Кроткая", "Федор Достоевский", "Повесть", 150.0, 5),
            ("Пушкин", "Федор Достоевский", "Очерк", 200.0, 2),
            ("Столетняя", "Федор Достоевский", "Очерк", 250.0, 8),
            ("Приговор", "Федор Достоевский", "Очерк", 300.0, 3),
            ("Божий дар", "Федор Достоевский", "Стихотворение", 350.0, 1),
            ("На европейские событи в 1854 году", "Федор Достоевский", "Стихотворение", 400.0, 4),
            ("На первое июля 1855 года", "Федор Достоевский", "Стихотворение", 450.0, 6),
            ("На коронацию и заключение мира", "Федор Достоевский", "Стихотворение", 500.0, 7),
            ("Рудин", "Иван Тургенев", "Роман", 550.0, 9),
            ("Жид", "Иван Тургенев", "Повесть", 100.0, 10),
            ("Жид", "Иван Тургенев", "Рассказ", 150.0, 5),
            ("Муму", "Иван Тургенев", "Повесть", 200.0, 2),
            ("Муму", "Иван Тургенев", "Рассказ", 250.0, 8),
            ("Ася", "Иван Тургенев", "Повесть", 300.0, 3),
            ("Ася", "Иван Тургенев", "Рассказ", 350.0, 1),
            ("Вешние воды", "Иван Тургенев", "Повесть", 400.0, 4),
            ("Мертвые души", "Николай Гоголь", "Поэма", 450.0, 6),
            ("Миргород", "Николай Гоголь", "Повесть", 500.0, 7),
            ("Вечера на хуторе близ Диканьки", "Николай Гоголь", "Повесть", 550.0, 9),
            ("Ревизор", "Николай Гоголь", "Пьеса", 500.0, 100),
            ("Ганц Кюхельгартен", "Николай Гоголь", "Поэма", 480.99, 150),
            ("Италия", "Николай Гоголь", "Стихотворение", 370.99, 200),
            ("Гроза", "Александр Островский", "Драма", 260.99, 120),
            ("Бешеные деньги", "Александр Островский", "Комедия", 299.99, 80),
            ("Филомела", "Иван Крылов", "Трагедия", 500.99, 60),
            ("Каиб", "Иван Крылов", "Сатирическая повесть", 399.99, 40),
            ("Ворона и Лисица", "Иван Крылов", "Басня", 149.99, 30),
            ("Евгений Онегин", "Александр Пушкин", "Роман в стихах", 799.99, 20),
            ("Борис Годунов", "Александр Пушкин", "Драсатическое произведение", 600.0, 50),
            ("Жених", "Александр Пушкин", "Сказки", 200.0, 100),
            ("Русалка", "Александр Пушкин", "Драсатическое произведение", 380.99, 150),
            ("Метель", "Александр Пушкин", "Проза", 270.99, 200),
            ("История Пугачёва", "Александр Пушкин", "Исторические произведения", 680.0, 120),
            ("Капитанская дочка", "Александр Пушкин", "Проза", 390.0, 80),
            ("Дубровский", "Александр Пушкин", "Проза", 420.99, 60),
            ("Мать", "Максим Горький", "Роман", 1000.0, 40),
            ("Трое", "Максим Горький", "Роман", 540.0, 30),
            ("Человек", "Максим Горький", "Очерк", 399.99, 20),
            ("Утро", "Максим Горький", "Сказки", 240.0, 50),
            ("Яшка", "Максим Горький", "Сказки", 150.0, 100),
            ("На дне", "Максим Горький", "Пьеса", 1400.0, 150),
            ("Демон", "Михаил Лермонтов", "Поэма", 690.0, 200),
            ("Герой нашего времени", "Михаил Лермонтов", "Роман с элементами светской повести", 700.0, 120),
            ("Беглец", "Михаил Лермонтов", "Поэма", 410.0, 80),
            ("Парус", "Михаил Лермонтов", "Стихотворение", 420.0, 60),
            ("Легенды и мифы Древней Греции", "Николай Кун", "Мифология", 359.0, 40),
            ("Пионовый фонарь", "Санъюэйт Энтё", "Фэнтези", 654.0, 30),
            ("Майор Гром", "Кирилл Кутузов", "Детектив", 235.0, 20),
            ("Маленький принц", "Антуан де Сент-Экзюпери", "Роман", 300.0, 50)
        ]
        self.cursor.executemany(
            "INSERT INTO books (title, author, genre, price, stock) VALUES (?, ?, ?, ?, ?)",
            books
        )
        self.conn.commit()


class LoginWindow(QWidget):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.setWindowTitle("Вход в Интернет-магазин книг")
        self.setGeometry(100, 100, 300, 200)

        layout = QVBoxLayout()

        self.login_input = QLineEdit()
        self.login_input.setPlaceholderText("Логин")
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Пароль")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        layout.addWidget(self.login_input)
        layout.addWidget(self.password_input)

        login_button = QPushButton("Войти")
        login_button.clicked.connect(self.login)
        layout.addWidget(login_button)

        register_button = QPushButton("Регистрация")
        register_button.clicked.connect(self.open_registration_window)
        layout.addWidget(register_button)

        self.setLayout(layout)

    def login(self):
        login = self.login_input.text()
        password = self.password_input.text()
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        self.db.cursor.execute("SELECT * FROM users WHERE login=? AND password=?", (login, hashed_password))
        user = self.db.cursor.fetchone()

        if user:
            if user[6] == "admin":
                QMessageBox.information(self, "Успех", "Добро пожаловать, администратор!")
                self.admin_window = AdminWindow(self.db)
                self.admin_window.show()
            else:
                QMessageBox.information(self, "Успех", "Добро пожаловать!")
                self.user_window = UserWindow(self.db, user[0])
                self.user_window.show()
            self.close()
        else:
            QMessageBox.warning(self, "Ошибка", "Неверный логин или пароль")

    def open_registration_window(self):
        self.registration_window = RegistrationWindow(self.db)
        self.registration_window.show()


class RegistrationWindow(QWidget):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.setWindowTitle("Регистрация")
        self.setGeometry(100, 100, 300, 400)

        layout = QVBoxLayout()

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Имя пользователя")
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Почта")
        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("Телефон")
        self.login_input = QLineEdit()
        self.login_input.setPlaceholderText("Логин")
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Пароль")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        layout.addWidget(self.username_input)
        layout.addWidget(self.email_input)
        layout.addWidget(self.phone_input)
        layout.addWidget(self.login_input)
        layout.addWidget(self.password_input)

        register_button = QPushButton("Зарегистрироваться")
        register_button.clicked.connect(self.register)
        layout.addWidget(register_button)

        self.setLayout(layout)

    def register(self):
        username = self.username_input.text()
        email = self.email_input.text()
        phone = self.phone_input.text()
        login = self.login_input.text()
        password = self.password_input.text()

        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        if not username or not email or not phone or not login or not password:
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, заполните все поля.")
            return

        try:
            self.db.cursor.execute(
                "INSERT INTO users (username, email, phone, login, password, role) VALUES (?, ?, ?, ?, ?, ?)",
                (username, email, phone, login, hashed_password, "user"))
            self.db.conn.commit()
            QMessageBox.information(self, "Успех", "Регистрация прошла успешно!")

            user_id = self.db.cursor.lastrowid
            self.user_window = UserWindow(self.db, user_id)
            self.user_window.show()
            self.close()
        except sqlite3.IntegrityError:
            QMessageBox.warning(self, "Ошибка", "Логин или почта уже используются.")
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", str(e))


class AdminWindow(QWidget):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.setWindowTitle("Личный кабинет Админа")
        self.setGeometry(100, 100, 600, 400)

        layout = QVBoxLayout()

        self.user_combo = QComboBox()
        self.load_users()

        self.role_combo = QComboBox()
        self.role_combo.addItems(["администратор", "работник", "покупатель"])

        layout.addWidget(self.user_combo)
        layout.addWidget(self.role_combo)

        change_role_button = QPushButton("Изменить роль пользователя")
        change_role_button.clicked.connect(self.change_role)
        layout.addWidget(change_role_button)

        update_user_button = QPushButton("Обновить информацию о пользователе")
        update_user_button.clicked.connect(self.update_user_info)
        layout.addWidget(update_user_button)

        delete_user_button = QPushButton("Удалить пользователя")
        delete_user_button.clicked.connect(self.delete_user)
        layout.addWidget(delete_user_button)

        books_button = QPushButton("Управление книгами")
        books_button.clicked.connect(self.show_books)
        layout.addWidget(books_button)

        orders_button = QPushButton("Управление заказами")
        orders_button.clicked.connect(self.show_orders)
        layout.addWidget(orders_button)

        logout_button = QPushButton("Выход")
        logout_button.clicked.connect(self.logout)
        layout.addWidget(logout_button)

        export_button = QPushButton("Выгрузить отчет в Excel")
        export_button.clicked.connect(self.export_to_excel)
        layout.addWidget(export_button)

        self.setLayout(layout)

    def load_users(self):
        self.user_combo.clear()
        self.db.cursor.execute("SELECT username FROM users")
        users = self.db.cursor.fetchall()
        self.user_combo.addItems([user[0] for user in users])

    def change_role(self):
        selected_user = self.user_combo.currentText()
        new_role = self.role_combo.currentText()
        self.db.cursor.execute("UPDATE users SET role = ? WHERE username = ?", (new_role, selected_user))
        self.db.conn.commit()
        QMessageBox.information(self, "Успех", f"Роль пользователя {selected_user} изменена на {new_role}.")

    def update_user_info(self):
        selected_user = self.user_combo.currentText()
        user_dialog = UserDialog(self.db, selected_user)
        user_dialog.exec()
        self.load_users()  # Обновляем список пользователей после изменения

    def delete_user(self):
        selected_user = self.user_combo.currentText()
        self.db.cursor.execute("DELETE FROM users WHERE username = ?", (selected_user,))
        self.db.conn.commit()
        QMessageBox.information(self, "Успех", f"Пользователь {selected_user} удален.")
        self.load_users()

    def show_books(self):
        self.books_window = ManageBooksWindow(self.db)
        self.books_window.show()

    def show_orders(self):
        self.orders_window = ManageOrdersWindow(self.db)
        self.orders_window.show()

    def logout(self):
        self.close()
        self.login_window = LoginWindow(self.db)
        self.login_window.show()

    def export_to_excel(self):
        # Получаем данные о книгах
        self.db.cursor.execute("SELECT * FROM books")
        books = self.db.cursor.fetchall()
        books_columns = [col[0] for col in self.db.cursor.description]

        # Получаем данные о заказах
        self.db.cursor.execute("""
            SELECT o.id, b.title, u.username, o.quantity, (o.quantity * b.price) as total_price 
            FROM orders o 
            JOIN books b ON o.book_id = b.id 
            JOIN users u ON o.user_id = u.id
        """)
        orders = self.db.cursor.fetchall()
        orders_columns = [col[0] for col in self.db.cursor.description]

        # Создание DataFrame и запись в Excel
        books_df = pd.DataFrame(books, columns=books_columns)
        orders_df = pd.DataFrame(orders, columns=orders_columns)

        with pd.ExcelWriter('отчет.xlsx', engine='openpyxl') as writer:
            books_df.to_excel(writer, sheet_name='Книги', index=False)
            orders_df.to_excel(writer, sheet_name='Заказы', index=False)

        QMessageBox.information(self, "Успех", "Отчет успешно выгружен в файл 'отчет.xlsx'!")


class ManageBooksWindow(QWidget):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.setWindowTitle("Управление книгами")
        self.setGeometry(100, 100, 600, 400)

        layout = QVBoxLayout()

        self.books_table = QTableWidget()
        self.books_table.setColumnCount(6)
        self.books_table.setHorizontalHeaderLabels(["ID", "Название", "Автор", "Жанр", "Цена", "Остаток"])
        self.load_books()

        layout.addWidget(self.books_table)

        add_button = QPushButton("Добавить книгу")
        add_button.clicked.connect(self.add_book)
        layout.addWidget(add_button)

        edit_button = QPushButton("Редактировать книгу")
        edit_button.clicked.connect(self.edit_book)
        layout.addWidget(edit_button)

        delete_button = QPushButton("Удалить книгу")
        delete_button.clicked.connect(self.delete_book)
        layout.addWidget(delete_button)

        back_button = QPushButton("Назад")
        back_button.clicked.connect(self.back_to_admin)
        layout.addWidget(back_button)

        self.setLayout(layout)

    def load_books(self):
        self.books_table.setRowCount(0)
        self.db.cursor.execute("SELECT id, title, author, genre, price, stock FROM books")
        books = self.db.cursor.fetchall()
        for row_number, row_data in enumerate(books):
            self.books_table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.books_table.setItem(row_number, column_number, QTableWidgetItem(str(data)))

    def add_book(self):
        dialog = BookDialog(self)
        if dialog.exec():
            title, author, genre, price, stock = dialog.get_book_data()
            try:
                self.db.cursor.execute("INSERT INTO books (title, author, genre, price, stock) VALUES (?, ?, ?, ?, ?)",
                                       (title, author, genre, float(price), int(stock)))
                self.db.conn.commit()
                self.load_books()
                QMessageBox.information(self, "Успех", "Книга добавлена успешно!")
            except ValueError:
                QMessageBox.warning(self, "Ошибка", "Пожалуйста, проверьте введенные данные.")

    def edit_book(self):
        current_row = self.books_table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Ошибка", "Выберите книгу для редактирования.")
            return
        book_id = self.books_table.item(current_row, 0).text()  # ID книги
        title = self.books_table.item(current_row, 1).text()
        author = self.books_table.item(current_row, 2).text()
        genre = self.books_table.item(current_row, 3).text()
        price = self.books_table.item(current_row, 4).text()
        stock = self.books_table.item(current_row, 5).text()

        dialog = BookDialog(self)
        dialog.set_book_data(title, author, genre, price, stock)

        if dialog.exec():
            new_title, new_author, new_genre, new_price, new_stock = dialog.get_book_data()
            try:
                self.db.cursor.execute("UPDATE books SET title=?, author=?, genre=?, price=?, stock=? WHERE id=?",
                                       (new_title, new_author, new_genre, float(new_price), int(new_stock), book_id))
                self.db.conn.commit()
                self.load_books()
                QMessageBox.information(self, "Успех", "Книга обновлена успешно!")
            except ValueError:
                QMessageBox.warning(self, "Ошибка", "Пожалуйста, проверьте введенные данные.")

    def delete_book(self):
        current_row = self.books_table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Ошибка", "Выберите книгу для удаления.")
            return
        book_id = self.books_table.item(current_row, 0).text()  # ID книги
        self.db.cursor.execute("DELETE FROM books WHERE id=?", (book_id,))
        self.db.conn.commit()

        self.load_books()
        QMessageBox.information(self, "Успех", "Книга удалена успешно!")

    def back_to_admin(self):
        self.close()  # Закрываем окно проектов
        self.admin_window = AdminWindow(self.db)  # Возвращаемся к окну администратора
        self.admin_window.show()  # Показываем окно администратора


class BookDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle("Книга")
        self.setGeometry(100, 100, 300, 250)

        layout = QVBoxLayout()

        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Название")
        self.author_input = QLineEdit()
        self.author_input.setPlaceholderText("Автор")
        self.genre_input = QLineEdit()
        self.genre_input.setPlaceholderText("Жанр")
        self.price_input = QLineEdit()
        self.price_input.setPlaceholderText("Цена")
        self.stock_input = QLineEdit()
        self.stock_input.setPlaceholderText("Количество на складе")

        layout.addWidget(self.title_input)
        layout.addWidget(self.author_input)
        layout.addWidget(self.genre_input)
        layout.addWidget(self.price_input)
        layout.addWidget(self.stock_input)

        save_button = QPushButton("Сохранить")
        save_button.clicked.connect(self.accept)
        layout.addWidget(save_button)

        self.setLayout(layout)

    def set_book_data(self, title, author, genre, price, stock):
        self.title_input.setText(title)
        self.author_input.setText(author)
        self.genre_input.setText(genre)
        self.price_input.setText(price)
        self.stock_input.setText(stock)

    def get_book_data(self):
        return (
            self.title_input.text(),
            self.author_input.text(),
            self.genre_input.text(),
            self.price_input.text(),
            self.stock_input.text()
        )


class ManageOrdersWindow(QWidget):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.setWindowTitle("Управление заказами")
        self.setGeometry(100, 100, 600, 400)

        layout = QVBoxLayout()

        self.orders_table = QTableWidget()
        self.orders_table.setColumnCount(5)
        self.orders_table.setHorizontalHeaderLabels(["ID Заказа", "Книга", "Пользователь", "Количество", "Статус"])
        self.load_orders()

        layout.addWidget(self.orders_table)
        self.setLayout(layout)

        delete_order_button = QPushButton("Удалить заказ")
        delete_order_button.clicked.connect(self.delete_order)
        layout.addWidget(delete_order_button)

    def load_orders(self):
        self.orders_table.setRowCount(0)
        self.db.cursor.execute("""
            SELECT o.id, b.title, u.username, o.quantity, 'Активный' as status FROM orders o
            JOIN books b ON o.book_id = b.id
            JOIN users u ON o.user_id = u.id
        """)
        orders = self.db.cursor.fetchall()
        for row_number, row_data in enumerate(orders):
            self.orders_table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.orders_table.setItem(row_number, column_number, QTableWidgetItem(str(data)))

    def delete_order(self):
        current_row = self.orders_table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Ошибка", "Выберите заказ для удаления.")
            return
        order_id = self.orders_table.item(current_row, 0).text()  # ID заказа
        self.db.cursor.execute("DELETE FROM orders WHERE id=?", (order_id,))
        self.db.conn.commit()

        self.load_orders()
        QMessageBox.information(self, "Успех", "Заказ удален успешно!")
        self.notify_admin_new_order()

    def notify_admin_new_order(self):
        # Здесь можно отправить уведомление, например, с сообщением о новом заказе
        QMessageBox.information(self, "Новый заказ", "Поступил новый заказ!")


class UserWindow(QWidget):
    def __init__(self, db, user_id):
        super().__init__()
        self.db = db
        self.user_id = user_id

        self.setWindowTitle("Личный кабинет пользователя")
        self.setGeometry(100, 100, 500, 400)

        layout = QVBoxLayout()

        self.user_books_table = QTableWidget()
        self.user_books_table.setColumnCount(4)
        self.user_books_table.setHorizontalHeaderLabels(["Название", "Автор", "Жанр", "Цена"])
        self.load_user_books()

        layout.addWidget(self.user_books_table)
        self.setLayout(layout)

        self.user_books_table.cellDoubleClicked.connect(self.add_to_cart)

        self.cart_button = QPushButton("Перейти в корзину")
        self.cart_button.clicked.connect(self.open_cart)
        layout.addWidget(self.cart_button)

        self.order_button = QPushButton("Оформить заказ")
        self.order_button.clicked.connect(self.open_order)
        layout.addWidget(self.order_button)

        logout_button = QPushButton("Выйти из аккаунта")
        logout_button.clicked.connect(self.logout)
        layout.addWidget(logout_button)

    def load_user_books(self):
        self.user_books_table.setRowCount(0)
        self.db.cursor.execute("SELECT title, author, genre, price FROM books")
        books = self.db.cursor.fetchall()
        for row_number, row_data in enumerate(books):
            self.user_books_table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.user_books_table.setItem(row_number, column_number, QTableWidgetItem(str(data)))

    def add_to_cart(self, row, column):
        title = self.user_books_table.item(row, 0).text()
        self.db.cursor.execute("SELECT id, stock FROM books WHERE title=?", (title,))
        book = self.db.cursor.fetchone()

        if book and book[1] > 0:
            self.db.cursor.execute("SELECT quantity FROM orders WHERE book_id=? AND user_id=?", (book[0], self.user_id))
            existing_order = self.db.cursor.fetchone()

            if existing_order:
                new_quantity = existing_order[0] + 1
                self.db.cursor.execute("UPDATE orders SET quantity=? WHERE book_id=? AND user_id=?",
                                       (new_quantity, book[0], self.user_id))
            else:
                self.db.cursor.execute("INSERT INTO orders (book_id, user_id, quantity) VALUES (?, ?, ?)",
                                       (book[0], self.user_id, 1))
            self.db.conn.commit()
            QMessageBox.information(self, "Успех", f"Книга '{title}' добавлена в корзину.")
            self.update_book_stock(book[0], book[1] - 1)
        else:
            QMessageBox.warning(self, "Ошибка", "Книга недоступна.")

    def open_cart(self):
        self.cart_window = CartWindow(self.db, self.user_id)
        self.cart_window.show()

    def open_order(self):
        self.order_window = OrderWindow(self.db, self.user_id)
        self.order_window.show()

    def update_book_stock(self, book_id, new_stock):
        self.db.cursor.execute("UPDATE books SET stock = ? WHERE id = ?", (new_stock, book_id))
        self.db.conn.commit()

    def logout(self):
        self.close()  # Закрываем окно пользователя
        self.login_window = LoginWindow(self.db)  # Возвращаемся к окну входа
        self.login_window.show()


class CartWindow(QWidget):
    def __init__(self, db, user_id):
        super().__init__()
        self.db = db
        self.user_id = user_id

        self.setWindowTitle("Корзина")
        self.setGeometry(100, 100, 500, 400)

        layout = QVBoxLayout()

        self.cart_table = QTableWidget()
        self.cart_table.setColumnCount(5)
        self.cart_table.setHorizontalHeaderLabels(["Название", "Автор", "Цена", "Количество", "Итого"])
        self.load_cart_items()

        layout.addWidget(self.cart_table)
        self.setLayout(layout)

        checkout_button = QPushButton("Оформить заказ")
        checkout_button.clicked.connect(self.open_order)
        layout.addWidget(checkout_button)

    def load_cart_items(self):
        self.cart_table.setRowCount(0)
        self.db.cursor.execute(
            "SELECT b.title, b.author, b.price, o.quantity, (o.quantity * b.price) AS total_price FROM orders o "
            "JOIN books b ON o.book_id = b.id WHERE o.user_id = ?", (self.user_id,))
        items = self.db.cursor.fetchall()
        for row_number, row_data in enumerate(items):
            self.cart_table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.cart_table.setItem(row_number, column_number, QTableWidgetItem(str(data)))

    def open_order(self):
        self.order_window = OrderWindow(self.db, self.user_id)
        self.order_window.show()


class OrderWindow(QWidget):
    def __init__(self, db, user_id):
        super().__init__()
        self.db = db
        self.user_id = user_id

        self.setWindowTitle("Оформление заказа")
        self.setGeometry(100, 100, 300, 200)

        layout = QVBoxLayout()

        self.confirm_button = QPushButton("Подтвердить заказ")
        self.confirm_button.clicked.connect(self.confirm_order)
        layout.addWidget(self.confirm_button)

        back_button = QPushButton("Вернуться к покупкам")
        back_button.clicked.connect(self.back_to_user_window)
        layout.addWidget(back_button)

        self.setLayout(layout)

    def confirm_order(self):
        QMessageBox.information(self, "Заказ", "Ваш заказ оформлен!")
        self.close()

    def back_to_user_window(self):
        self.close()  # Закрыть окно оформления заказа
        self.user_window = UserWindow(self.db, self.user_id)  # Вернуться к окну пользователя
        self.user_window.show()


class UserDialog(QDialog):
    def __init__(self, db, username, parent=None):
        super().__init__(parent)
        self.db = db
        self.username = username
        self.setWindowTitle("Обновление информации о пользователе")
        self.setGeometry(100, 100, 300, 300)

        layout = QVBoxLayout()

        self.new_email_input = QLineEdit()
        self.new_email_input.setPlaceholderText("Новая почта")
        self.new_phone_input = QLineEdit()
        self.new_phone_input.setPlaceholderText("Новый телефон")
        self.new_login_input = QLineEdit()
        self.new_login_input.setPlaceholderText("Новый логин")
        self.new_password_input = QLineEdit()
        self.new_password_input.setPlaceholderText("Новый пароль")
        self.new_password_input.setEchoMode(QLineEdit.EchoMode.Password)

        layout.addWidget(self.new_email_input)
        layout.addWidget(self.new_phone_input)
        layout.addWidget(self.new_login_input)
        layout.addWidget(self.new_password_input)

        update_button = QPushButton("Обновить")
        update_button.clicked.connect(self.update_user_info)
        layout.addWidget(update_button)

        self.setLayout(layout)

    def update_user_info(self):
        new_email = self.new_email_input.text()
        new_phone = self.new_phone_input.text()
        new_login = self.new_login_input.text()
        new_password = self.new_password_input.text()

        if new_password:
            new_hashed_password = hashlib.sha256(new_password.encode()).hexdigest()
            self.db.cursor.execute("UPDATE users SET email=?, phone=?, login=?, password=? WHERE username=?",
                                    (new_email, new_phone, new_login, new_hashed_password, self.username))
        else:
            self.db.cursor.execute("UPDATE users SET email=?, phone=?, login=? WHERE username=?",
                                    (new_email, new_phone, new_login, self.username))

        self.db.conn.commit()
        QMessageBox.information(self, "Успех", "Информация о пользователе обновлена!")
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    database: Database = Database()
    database.create_tables()
    database.populate_books()

    admin_login = "admin"
    admin_password = "admin"
    admin_hashed_password = hashlib.sha256(admin_password.encode()).hexdigest()

    # Проверка, существует ли администратор в базе данных
    database.cursor.execute("SELECT * FROM users WHERE login=?", (admin_login,))
    if database.cursor.fetchone() is None:
        database.cursor.execute(
            "INSERT INTO users (username, email, phone, login, password, role) VALUES (?, ?, ?, ?, ?, ?)",
            ("Admin", "admin@example.com", "123456789", admin_login, admin_hashed_password, "admin")
        )
        database.conn.commit()

    login_window = LoginWindow(database)
    login_window.show()

    sys.exit(app.exec())


class Database:
    def __init__(self, db_name='bookstore.db'):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def create_tables(self):
        self.cursor.execute("DROP TABLE IF EXISTS orders")
        self.cursor.execute("DROP TABLE IF EXISTS books")
        self.cursor.execute("DROP TABLE IF EXISTS users")

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                username TEXT,
                email TEXT,
                phone TEXT,
                login TEXT UNIQUE,
                password TEXT,
                role TEXT
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY,
                title TEXT,
                author TEXT,
                genre TEXT,
                price REAL,
                stock INTEGER
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY,
                book_id INTEGER,
                user_id INTEGER,
                quantity INTEGER,
                FOREIGN KEY (book_id) REFERENCES books (id),
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        self.conn.commit()

    def close(self):
        self.conn.close()

    def populate_books(self):
        books = [
            ("Преступление и наказание", "Фёдор Достоевский", "Роман", 500.0, 100),
            ("Война и мир", "Лев Толстой", "Роман", 800.0, 50),
            ("Анна Каренина", "Лев Толстой", "Роман", 700.0, 60),
            ("Мастер и Маргарита", "Михаил Булгаков", "Роман", 600.0, 70),
            ("Тихий Дон", "Михаил Шолохов", "Роман", 550.0, 40),
            ("Доктор Живаго", "Борис Пастернак", "Роман", 750.0, 30),
            ("Муму", "Иван Тургенев", "Повесть", 300.0, 90),
            ("Собачье сердце", "Михаил Булгаков", "Повесть", 400.0, 80),
        ]
        self.cursor.executemany(
            "INSERT INTO books (title, author, genre, price, stock) VALUES (?, ?, ?, ?, ?)",
            books
        )
        self.conn.commit()


class LoginWindow(QWidget):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.setWindowTitle("Вход в Интернет-магазин книг")
        self.setGeometry(100, 100, 300, 200)

        layout = QVBoxLayout()

        self.login_input = QLineEdit()
        self.login_input.setPlaceholderText("Логин")
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Пароль")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        layout.addWidget(self.login_input)
        layout.addWidget(self.password_input)

        login_button = QPushButton("Войти")
        login_button.clicked.connect(self.login)
        layout.addWidget(login_button)

        register_button = QPushButton("Регистрация")
        register_button.clicked.connect(self.open_registration_window)
        layout.addWidget(register_button)

        self.setLayout(layout)

    def login(self):
        login = self.login_input.text()
        password = self.password_input.text()
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        self.db.cursor.execute("SELECT * FROM users WHERE login=? AND password=?", (login, hashed_password))
        user = self.db.cursor.fetchone()

        if user:
            if user[6] == "admin":
                QMessageBox.information(self, "Успех", "Добро пожаловать, администратор!")
                self.admin_window = AdminWindow(self.db)
                self.admin_window.show()
            else:
                QMessageBox.information(self, "Успех", "Добро пожаловать!")
                self.user_window = UserWindow(self.db, user[0])
                self.user_window.show()
            self.close()
        else:
            QMessageBox.warning(self, "Ошибка", "Неверный логин или пароль")

    def open_registration_window(self):
        self.registration_window = RegistrationWindow(self.db)
        self.registration_window.show()


class RegistrationWindow(QWidget):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.setWindowTitle("Регистрация")
        self.setGeometry(100, 100, 300, 400)

        layout = QVBoxLayout()

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Имя пользователя")
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Почта")
        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("Телефон")
        self.login_input = QLineEdit()
        self.login_input.setPlaceholderText("Логин")
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Пароль")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        layout.addWidget(self.username_input)
        layout.addWidget(self.email_input)
        layout.addWidget(self.phone_input)
        layout.addWidget(self.login_input)
        layout.addWidget(self.password_input)

        register_button = QPushButton("Зарегистрироваться")
        register_button.clicked.connect(self.register)
        layout.addWidget(register_button)

        self.setLayout(layout)

    def register(self):
        username = self.username_input.text()
        email = self.email_input.text()
        phone = self.phone_input.text()
        login = self.login_input.text()
        password = self.password_input.text()

        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        if not username or not email or not phone or not login or not password:
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, заполните все поля.")
            return

        try:
            self.db.cursor.execute(
                "INSERT INTO users (username, email, phone, login, password, role) VALUES (?, ?, ?, ?, ?, ?)",
                (username, email, phone, login, hashed_password, "user"))
            self.db.conn.commit()
            QMessageBox.information(self, "Успех", "Регистрация прошла успешно!")

            user_id = self.db.cursor.lastrowid
            self.user_window = UserWindow(self.db, user_id)
            self.user_window.show()
            self.close()
        except sqlite3.IntegrityError:
            QMessageBox.warning(self, "Ошибка", "Логин или почта уже используются.")
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", str(e))


class AdminWindow(QWidget):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.setWindowTitle("Личный кабинет Админа")
        self.setGeometry(100, 100, 600, 400)

        layout = QVBoxLayout()

        self.user_combo = QComboBox()
        self.load_users()

        self.role_combo = QComboBox()
        self.role_combo.addItems(["администратор", "работник", "покупатель"])

        layout.addWidget(self.user_combo)
        layout.addWidget(self.role_combo)

        change_role_button = QPushButton("Изменить роль пользователя")
        change_role_button.clicked.connect(self.change_role)
        layout.addWidget(change_role_button)

        delete_user_button = QPushButton("Удалить пользователя")
        delete_user_button.clicked.connect(self.delete_user)
        layout.addWidget(delete_user_button)

        books_button = QPushButton("Управление книгами")
        books_button.clicked.connect(self.show_books)
        layout.addWidget(books_button)

        orders_button = QPushButton("Управление заказами")
        orders_button.clicked.connect(self.show_orders)
        layout.addWidget(orders_button)

        logout_button = QPushButton("Выход")
        logout_button.clicked.connect(self.logout)
        layout.addWidget(logout_button)

        export_button = QPushButton("Выгрузить отчет в Excel")
        export_button.clicked.connect(self.export_to_excel)
        layout.addWidget(export_button)

        self.setLayout(layout)

    def load_users(self):
        self.user_combo.clear()
        self.db.cursor.execute("SELECT username FROM users")
        users = self.db.cursor.fetchall()
        self.user_combo.addItems([user[0] for user in users])

    def change_role(self):
        selected_user = self.user_combo.currentText()
        new_role = self.role_combo.currentText()
        self.db.cursor.execute("UPDATE users SET role = ? WHERE username = ?", (new_role, selected_user))
        self.db.conn.commit()
        QMessageBox.information(self, "Успех", f"Роль пользователя {selected_user} изменена на {new_role}.")

    def delete_user(self):
        selected_user = self.user_combo.currentText()
        self.db.cursor.execute("DELETE FROM users WHERE username = ?", (selected_user,))
        self.db.conn.commit()
        QMessageBox.information(self, "Успех", f"Пользователь {selected_user} удален.")
        self.load_users()

    def show_books(self):
        self.books_window = ManageBooksWindow(self.db)
        self.books_window.show()

    def show_orders(self):
        self.orders_window = ManageOrdersWindow(self.db)
        self.orders_window.show()

    def logout(self):
        self.close()
        self.login_window = LoginWindow(self.db)
        self.login_window.show()

    def export_to_excel(self):
        # Получаем данные о книгах
        self.db.cursor.execute("SELECT * FROM books")
        books = self.db.cursor.fetchall()
        books_columns = [col[0] for col in self.db.cursor.description]

        # Получаем данные о заказах
        self.db.cursor.execute("""
            SELECT o.id, b.title, u.username, o.quantity, (o.quantity * b.price) as total_price 
            FROM orders o 
            JOIN books b ON o.book_id = b.id 
            JOIN users u ON o.user_id = u.id
        """)
        orders = self.db.cursor.fetchall()
        orders_columns = [col[0] for col in self.db.cursor.description]

        # Создание DataFrame и запись в Excel
        books_df = pd.DataFrame(books, columns=books_columns)
        orders_df = pd.DataFrame(orders, columns=orders_columns)

        with pd.ExcelWriter('отчет.xlsx', engine='openpyxl') as writer:
            books_df.to_excel(writer, sheet_name='Книги', index=False)
            orders_df.to_excel(writer, sheet_name='Заказы', index=False)

        QMessageBox.information(self, "Успех", "Отчет успешно выгружен в файл 'отчет.xlsx'!")


class ManageBooksWindow(QWidget):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.setWindowTitle("Управление книгами")
        self.setGeometry(100, 100, 600, 400)

        layout = QVBoxLayout()

        self.books_table = QTableWidget()
        self.books_table.setColumnCount(6)
        self.books_table.setHorizontalHeaderLabels(["ID", "Название", "Автор", "Жанр", "Цена", "Остаток"])
        self.load_books()

        layout.addWidget(self.books_table)

        add_button = QPushButton("Добавить книгу")
        add_button.clicked.connect(self.add_book)
        layout.addWidget(add_button)

        edit_button = QPushButton("Редактировать книгу")
        edit_button.clicked.connect(self.edit_book)
        layout.addWidget(edit_button)

        delete_button = QPushButton("Удалить книгу")
        delete_button.clicked.connect(self.delete_book)
        layout.addWidget(delete_button)

        back_button = QPushButton("Назад")
        back_button.clicked.connect(self.back_to_admin)
        layout.addWidget(back_button)

        self.setLayout(layout)

    def load_books(self):
        self.books_table.setRowCount(0)
        self.db.cursor.execute("SELECT id, title, author, genre, price, stock FROM books")
        books = self.db.cursor.fetchall()
        for row_number, row_data in enumerate(books):
            self.books_table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.books_table.setItem(row_number, column_number, QTableWidgetItem(str(data)))

    def add_book(self):
        dialog = BookDialog(self)
        if dialog.exec():
            title, author, genre, price, stock = dialog.get_book_data()
            try:
                self.db.cursor.execute("INSERT INTO books (title, author, genre, price, stock) VALUES (?, ?, ?, ?, ?)",
                                       (title, author, genre, float(price), int(stock)))
                self.db.conn.commit()
                self.load_books()
                QMessageBox.information(self, "Успех", "Книга добавлена успешно!")
            except ValueError:
                QMessageBox.warning(self, "Ошибка", "Пожалуйста, проверьте введенные данные.")

    def edit_book(self):
        current_row = self.books_table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Ошибка", "Выберите книгу для редактирования.")
            return
        book_id = self.books_table.item(current_row, 0).text()  # ID книги
        title = self.books_table.item(current_row, 1).text()
        author = self.books_table.item(current_row, 2).text()
        genre = self.books_table.item(current_row, 3).text()
        price = self.books_table.item(current_row, 4).text()
        stock = self.books_table.item(current_row, 5).text()

        dialog = BookDialog(self)
        dialog.set_book_data(title, author, genre, price, stock)

        if dialog.exec():
            new_title, new_author, new_genre, new_price, new_stock = dialog.get_book_data()
            try:
                self.db.cursor.execute("UPDATE books SET title=?, author=?, genre=?, price=?, stock=? WHERE id=?",
                                       (new_title, new_author, new_genre, float(new_price), int(new_stock), book_id))
                self.db.conn.commit()
                self.load_books()
                QMessageBox.information(self, "Успех", "Книга обновлена успешно!")
            except ValueError:
                QMessageBox.warning(self, "Ошибка", "Пожалуйста, проверьте введенные данные.")

    def delete_book(self):
        current_row = self.books_table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Ошибка", "Выберите книгу для удаления.")
            return
        book_id = self.books_table.item(current_row, 0).text()  # ID книги
        self.db.cursor.execute("DELETE FROM books WHERE id=?", (book_id,))
        self.db.conn.commit()

        self.load_books()
        QMessageBox.information(self, "Успех", "Книга удалена успешно!")

    def back_to_admin(self):
        self.close()  # Закрываем окно проектов
        self.admin_window = AdminWindow(self.db)  # Возвращаемся к окну администратора
        self.admin_window.show()  # Показываем окно администратора


class BookDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle("Книга")
        self.setGeometry(100, 100, 300, 250)

        layout = QVBoxLayout()

        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Название")
        self.author_input = QLineEdit()
        self.author_input.setPlaceholderText("Автор")
        self.genre_input = QLineEdit()
        self.genre_input.setPlaceholderText("Жанр")
        self.price_input = QLineEdit()
        self.price_input.setPlaceholderText("Цена")
        self.stock_input = QLineEdit()
        self.stock_input.setPlaceholderText("Количество на складе")

        layout.addWidget(self.title_input)
        layout.addWidget(self.author_input)
        layout.addWidget(self.genre_input)
        layout.addWidget(self.price_input)
        layout.addWidget(self.stock_input)

        save_button = QPushButton("Сохранить")
        save_button.clicked.connect(self.accept)
        layout.addWidget(save_button)

        self.setLayout(layout)

    def set_book_data(self, title, author, genre, price, stock):
        self.title_input.setText(title)
        self.author_input.setText(author)
        self.genre_input.setText(genre)
        self.price_input.setText(price)
        self.stock_input.setText(stock)

    def get_book_data(self):
        return (
            self.title_input.text(),
            self.author_input.text(),
            self.genre_input.text(),
            self.price_input.text(),
            self.stock_input.text()
        )


class ManageOrdersWindow(QWidget):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.setWindowTitle("Управление заказами")
        self.setGeometry(100, 100, 600, 400)

        layout = QVBoxLayout()

        self.orders_table = QTableWidget()
        self.orders_table.setColumnCount(5)
        self.orders_table.setHorizontalHeaderLabels(["ID Заказа", "Книга", "Пользователь", "Количество", "Статус"])
        self.load_orders()

        layout.addWidget(self.orders_table)
        self.setLayout(layout)

        delete_order_button = QPushButton("Удалить заказ")
        delete_order_button.clicked.connect(self.delete_order)
        layout.addWidget(delete_order_button)

    def load_orders(self):
        self.orders_table.setRowCount(0)
        self.db.cursor.execute("""
            SELECT o.id, b.title, u.username, o.quantity, 'Активный' as status FROM orders o
            JOIN books b ON o.book_id = b.id
            JOIN users u ON o.user_id = u.id
        """)
        orders = self.db.cursor.fetchall()
        for row_number, row_data in enumerate(orders):
            self.orders_table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.orders_table.setItem(row_number, column_number, QTableWidgetItem(str(data)))

    def delete_order(self):
        current_row = self.orders_table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Ошибка", "Выберите заказ для удаления.")
            return
        order_id = self.orders_table.item(current_row, 0).text()  # ID заказа
        self.db.cursor.execute("DELETE FROM orders WHERE id=?", (order_id,))
        self.db.conn.commit()

        self.load_orders()
        QMessageBox.information(self, "Успех", "Заказ удален успешно!")


class UserWindow(QWidget):
    def __init__(self, db, user_id):
        super().__init__()
        self.db = db
        self.user_id = user_id

        self.setWindowTitle("Личный кабинет пользователя")
        self.setGeometry(100, 100, 500, 400)

        layout = QVBoxLayout()

        self.user_books_table = QTableWidget()
        self.user_books_table.setColumnCount(4)
        self.user_books_table.setHorizontalHeaderLabels(["Название", "Автор", "Жанр", "Цена"])
        self.load_user_books()

        layout.addWidget(self.user_books_table)
        self.setLayout(layout)

        self.user_books_table.cellDoubleClicked.connect(self.add_to_cart)

        self.cart_button = QPushButton("Перейти в корзину")
        self.cart_button.clicked.connect(self.open_cart)
        layout.addWidget(self.cart_button)

        self.order_button = QPushButton("Оформить заказ")
        self.order_button.clicked.connect(self.open_order)
        layout.addWidget(self.order_button)

        logout_button = QPushButton("Выйти из аккаунта")
        logout_button.clicked.connect(self.logout)
        layout.addWidget(logout_button)

    def load_user_books(self):
        self.user_books_table.setRowCount(0)
        self.db.cursor.execute("SELECT title, author, genre, price FROM books")
        books = self.db.cursor.fetchall()
        for row_number, row_data in enumerate(books):
            self.user_books_table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.user_books_table.setItem(row_number, column_number, QTableWidgetItem(str(data)))

    def add_to_cart(self, row, column):
        title = self.user_books_table.item(row, 0).text()
        self.db.cursor.execute("SELECT id, stock FROM books WHERE title=?", (title,))
        book = self.db.cursor.fetchone()

        if book and book[1] > 0:
            self.db.cursor.execute("SELECT quantity FROM orders WHERE book_id=? AND user_id=?", (book[0], self.user_id))
            existing_order = self.db.cursor.fetchone()

            if existing_order:
                new_quantity = existing_order[0] + 1
                self.db.cursor.execute("UPDATE orders SET quantity=? WHERE book_id=? AND user_id=?",
                                       (new_quantity, book[0], self.user_id))
            else:
                self.db.cursor.execute("INSERT INTO orders (book_id, user_id, quantity) VALUES (?, ?, ?)",
                                       (book[0], self.user_id, 1))
            self.db.conn.commit()
            QMessageBox.information(self, "Успех", f"Книга '{title}' добавлена в корзину.")
            self.update_book_stock(book[0], book[1] - 1)
        else:
            QMessageBox.warning(self, "Ошибка", "Книга недоступна.")

    def open_cart(self):
        self.cart_window = CartWindow(self.db, self.user_id)
        self.cart_window.show()

    def open_order(self):
        self.order_window = OrderWindow(self.db, self.user_id)
        self.order_window.show()

    def update_book_stock(self, book_id, new_stock):
        self.db.cursor.execute("UPDATE books SET stock = ? WHERE id = ?", (new_stock, book_id))
        self.db.conn.commit()

    def logout(self):
        self.close()  # Закрываем окно пользователя
        self.login_window = LoginWindow(self.db)  # Возвращаемся к окну входа
        self.login_window.show()


class CartWindow(QWidget):
    def __init__(self, db, user_id):
        super().__init__()
        self.db = db
        self.user_id = user_id

        self.setWindowTitle("Корзина")
        self.setGeometry(100, 100, 500, 400)

        layout = QVBoxLayout()

        self.cart_table = QTableWidget()
        self.cart_table.setColumnCount(5)
        self.cart_table.setHorizontalHeaderLabels(["Название", "Автор", "Цена", "Количество", "Итого"])
        self.load_cart_items()

        layout.addWidget(self.cart_table)
        self.setLayout(layout)

        checkout_button = QPushButton("Оформить заказ")
        checkout_button.clicked.connect(self.open_order)
        layout.addWidget(checkout_button)

    def load_cart_items(self):
        self.cart_table.setRowCount(0)
        self.db.cursor.execute(
            "SELECT b.title, b.author, b.price, o.quantity, (o.quantity * b.price) AS total_price FROM orders o "
            "JOIN books b ON o.book_id = b.id WHERE o.user_id = ?", (self.user_id,))
        items = self.db.cursor.fetchall()
        for row_number, row_data in enumerate(items):
            self.cart_table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.cart_table.setItem(row_number, column_number, QTableWidgetItem(str(data)))

    def open_order(self):
        self.order_window = OrderWindow(self.db, self.user_id)
        self.order_window.show()


class OrderWindow(QWidget):
    def __init__(self, db, user_id):
        super().__init__()
        self.db = db
        self.user_id = user_id

        self.setWindowTitle("Оформление заказа")
        self.setGeometry(100, 100, 300, 200)

        layout = QVBoxLayout()

        self.confirm_button = QPushButton("Подтвердить заказ")
        self.confirm_button.clicked.connect(self.confirm_order)
        layout.addWidget(self.confirm_button)

        back_button = QPushButton("Вернуться к покупкам")
        back_button.clicked.connect(self.back_to_user_window)
        layout.addWidget(back_button)

        self.setLayout(layout)

    def confirm_order(self):
        QMessageBox.information(self, "Заказ", "Ваш заказ оформлен!")
        self.close()

    def back_to_user_window(self):
        self.close()  # Закрыть окно оформления заказа
        self.user_window = UserWindow(self.db, self.user_id)  # Вернуться к окну пользователя
        self.user_window.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    database = Database()
    database.create_tables()
    database.populate_books()

    admin_login = "admin"
    admin_password = "admin"
    admin_hashed_password = hashlib.sha256(admin_password.encode()).hexdigest()

    # Проверка, существует ли администратор в базе данных
    database.cursor.execute("SELECT * FROM users WHERE login=?", (admin_login,))
    if database.cursor.fetchone() is None:
        database.cursor.execute(
            "INSERT INTO users (username, email, phone, login, password, role) VALUES (?, ?, ?, ?, ?, ?)",
            ("Admin", "admin@example.com", "123456789", admin_login, admin_hashed_password, "admin")
        )
        database.conn.commit()

    login_window = LoginWindow(database)
    login_window.show()

    sys.exit(app.exec())


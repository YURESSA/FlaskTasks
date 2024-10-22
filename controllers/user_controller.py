import sqlite3
import bcrypt
import os


class UserManager:
    def __init__(self, db_name='flask-users.db3'):
        self.db_name = db_name
        self.create_table()

    def create_table(self):
        with self.get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    username TEXT PRIMARY KEY,
                    password TEXT NOT NULL
                )
            ''')
            connection.commit()

    def get_connection(self):
        return sqlite3.connect(self.db_name)

    def hash_password(self, password):
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

    def check_password(self, stored_password, provided_password):
        return bcrypt.checkpw(provided_password.encode('utf-8'), stored_password.encode('utf-8'))

    def is_password_strong(self, password):
        return True, "Пароль достаточно сложный."

    def register_user(self, username, password1, password2):
        with self.get_connection() as connection:
            cursor = connection.cursor()

            if self.user_exists(username, cursor):
                return False, 'Имя пользователя уже занято!'
            if password1 != password2:
                return False, 'Пароли не совпадают!'

            is_strong, message = self.is_password_strong(password1)
            if not is_strong:
                return False, message

            hashed_password = self.hash_password(password1)
            cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed_password))
            connection.commit()
            return True, 'Пользователь успешно зарегистрирован!'

    def user_exists(self, username, cursor):
        cursor.execute('SELECT COUNT(*) FROM users WHERE username = ?', (username,))
        return cursor.fetchone()[0] > 0

    def login_user(self, username, password):
        with self.get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute('SELECT password FROM users WHERE username = ?', (username,))
            result = cursor.fetchone()

            if result is None:
                return False, 'Пользователь не найден!'
            stored_password = result[0]
            if not self.check_password(stored_password, password):
                return False, 'Неверный пароль!'

            return True, 'Вход выполнен успешно!'

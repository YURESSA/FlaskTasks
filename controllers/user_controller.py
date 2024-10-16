import json
import os
import re
import bcrypt


class UserManager:
    def __init__(self, users_file='data/users.json'):
        self.users_file = users_file
        self.users = self.load_users()

    def load_users(self):
        if os.path.exists(self.users_file):
            with open(self.users_file, 'r') as file:
                try:
                    return json.load(file)
                except json.JSONDecodeError:
                    return {}
        return {}

    def save_users(self):
        with open(self.users_file, 'w') as file:
            json.dump(self.users, file, indent=4)

    def hash_password(self, password):
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

    def check_password(self, stored_password, provided_password):
        return bcrypt.checkpw(provided_password.encode('utf-8'), stored_password.encode('utf-8'))

    def is_password_strong(self, password):


        return True, "Пароль достаточно сложный."

    def register_user(self, username, password1, password2):
        if username in self.users:
            return False, 'Имя пользователя уже занято!'
        if password1 != password2:
            return False, 'Пароли не совпадают!'

        is_strong, message = self.is_password_strong(password1)
        if not is_strong:
            return False, message
        self.users[username] = self.hash_password(password1)
        self.save_users()
        return True, 'Пользователь успешно зарегистрирован!'

    def login_user(self, username, password):
        if username not in self.users:
            return False, 'Пользователь не найден!'
        if not self.check_password(self.users[username], password):
            return False, 'Неверный пароль!'

        return True, 'Вход выполнен успешно!'

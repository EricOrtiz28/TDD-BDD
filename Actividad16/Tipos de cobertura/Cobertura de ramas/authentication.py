# authentication.py

class Authentication:
    def __init__(self):
        self.users = {}
        self.logged_in_users = {}

    def register_user(self, username, password, role='user'):
        if username in self.users:
            raise ValueError("El usuario ya existe.")
        if not self._validate_password(password):
            raise ValueError("La contraseña no cumple con los requisitos.")
        self.users[username] = {'password': password, 'role': role}

    def login(self, username, password):
        if username not in self.users:
            raise ValueError("Usuario no encontrado.")
        if self.users[username]['password'] != password:
            raise ValueError("Contraseña incorrecta.")
        self.logged_in_users[username] = True

    def logout(self, username):
        if username in self.logged_in_users:
            del self.logged_in_users[username]
        else:
            raise ValueError("El usuario no está logueado.")

    def is_admin(self, username):
        if username not in self.users:
            raise ValueError("Usuario no encontrado.")
        return self.users[username]['role'] == 'admin'

    def _validate_password(self, password):
        if len(password) < 8:
            return False
        has_number = any(char.isdigit() for char in password)
        has_letter = any(char.isalpha() for char in password)
        return has_number and has_letter

    def change_password(self, username, old_password, new_password):
        if username not in self.users:
            raise ValueError("Usuario no encontrado.")
        if self.users[username]['password'] != old_password:
            raise ValueError("Contraseña antigua incorrecta.")
        if not self._validate_password(new_password):
            raise ValueError("La nueva contraseña no cumple con los requisitos.")
        self.users[username]['password'] = new_password

    def delete_user(self, admin_username, target_username):
        if admin_username not in self.users:
            raise ValueError("Usuario administrador no encontrado.")
        if not self.is_admin(admin_username):
            raise PermissionError("Permiso denegado. Solo administradores pueden eliminar usuarios.")
        if target_username not in self.users:
            raise ValueError("Usuario objetivo no encontrado.")
        del self.users[target_username]
        if target_username in self.logged_in_users:
            del self.logged_in_users[target_username]
# user_management.py

class User:
    def __init__(self, username, password, role='user'):
        if not isinstance(username, str) or not isinstance(password, str):
            raise TypeError("Username y password deben ser cadenas.")
        if not username:
            raise ValueError("Username no puede estar vacío.")
        if not self._validate_password(password):
            raise ValueError("Password no cumple con los requisitos.")
        if role not in ['user', 'admin']:
            raise ValueError("Role debe ser 'user' o 'admin'.")
        self.username = username
        self.password = password
        self.role = role
        self.is_active = True

    def _validate_password(self, password):
        if len(password) < 8:
            return False
        has_digit = any(char.isdigit() for char in password)
        has_alpha = any(char.isalpha() for char in password)
        return has_digit and has_alpha

    def deactivate(self):
        if not self.is_active:
            raise ValueError("El usuario ya está inactivo.")
        self.is_active = False

    def change_password(self, old_password, new_password):
        if self.password != old_password:
            raise ValueError("Password antigua incorrecta.")
        if not self._validate_password(new_password):
            raise ValueError("La nueva password no cumple con los requisitos.")
        self.password = new_password

    def promote_to_admin(self):
        if self.role == 'admin':
            raise ValueError("El usuario ya es admin.")
        self.role = 'admin'

    def demote_to_user(self):
        if self.role == 'user':
            raise ValueError("El usuario ya es user.")
        self.role = 'user'


class UserManager:
    def __init__(self):
        self.users = {}

    def add_user(self, username, password, role='user'):
        if username in self.users:
            raise ValueError("El usuario ya existe.")
        user = User(username, password, role)
        self.users[username] = user

    def remove_user(self, username):
        if username not in self.users:
            raise ValueError("El usuario no existe.")
        del self.users[username]

    def get_user(self, username):
        return self.users.get(username, None)

    def authenticate(self, username, password):
        user = self.get_user(username)
        if not user or not user.is_active:
            return False
        return user.password == password

    def promote_user(self, admin_username, target_username):
        admin = self.get_user(admin_username)
        if not admin or admin.role != 'admin':
            raise PermissionError("Permiso denegado. Solo admins pueden promover usuarios.")
        target = self.get_user(target_username)
        if not target:
            raise ValueError("El usuario objetivo no existe.")
        target.promote_to_admin()

    def demote_user(self, admin_username, target_username):
        admin = self.get_user(admin_username)
        if not admin or admin.role != 'admin':
            raise PermissionError("Permiso denegado. Solo admins pueden demover usuarios.")
        target = self.get_user(target_username)
        if not target:
            raise ValueError("El usuario objetivo no existe.")
        target.demote_to_user()

    def deactivate_user(self, admin_username, target_username):
        admin = self.get_user(admin_username)
        if not admin or admin.role != 'admin':
            raise PermissionError("Permiso denegado. Solo admins pueden desactivar usuarios.")
        target = self.get_user(target_username)
        if not target:
            raise ValueError("El usuario objetivo no existe.")
        target.deactivate()

    def list_active_users(self):
        return [user.username for user in self.users.values() if user.is_active]

    def list_admins(self):
        return [user.username for user in self.users.values() if user.role == 'admin']
# test_authentication.py

import pytest
from authentication import Authentication

@pytest.fixture
def auth():
    return Authentication()

def test_register_user_success(auth):
    auth.register_user('john_doe', 'Password123')
    assert 'john_doe' in auth.users

def test_register_existing_user(auth):
    auth.register_user('jane_doe', 'Password123')
    with pytest.raises(ValueError) as excinfo:
        auth.register_user('jane_doe', 'NewPass456')
    assert "El usuario ya existe." in str(excinfo.value)

def test_register_user_invalid_password(auth):
    with pytest.raises(ValueError) as excinfo:
        auth.register_user('alice', 'short')
    assert "La contraseña no cumple con los requisitos." in str(excinfo.value)

def test_login_success(auth):
    auth.register_user('bob', 'SecurePass1')
    auth.login('bob', 'SecurePass1')
    assert 'bob' in auth.logged_in_users

def test_login_nonexistent_user(auth):
    with pytest.raises(ValueError) as excinfo:
        auth.login('charlie', 'AnyPass123')
    assert "Usuario no encontrado." in str(excinfo.value)

def test_login_incorrect_password(auth):
    auth.register_user('dave', 'ValidPass1')
    with pytest.raises(ValueError) as excinfo:
        auth.login('dave', 'WrongPass')
    assert "Contraseña incorrecta." in str(excinfo.value)

def test_logout_success(auth):
    auth.register_user('eve', 'Password1')
    auth.login('eve', 'Password1')
    auth.logout('eve')
    assert 'eve' not in auth.logged_in_users

def test_logout_not_logged_in(auth):
    with pytest.raises(ValueError) as excinfo:
        auth.logout('frank')
    assert "El usuario no está logueado." in str(excinfo.value)

def test_is_admin_true(auth):
    auth.register_user('admin_user', 'AdminPass1', role='admin')
    assert auth.is_admin('admin_user') == True

def test_is_admin_false(auth):
    auth.register_user('regular_user', 'UserPass1')
    assert auth.is_admin('regular_user') == False

def test_is_admin_nonexistent_user(auth):
    with pytest.raises(ValueError) as excinfo:
        auth.is_admin('ghost')
    assert "Usuario no encontrado." in str(excinfo.value)

def test_change_password_success(auth):
    auth.register_user('henry', 'OldPass1')
    auth.change_password('henry', 'OldPass1', 'NewPass2')
    assert auth.users['henry']['password'] == 'NewPass2'

def test_change_password_incorrect_old(auth):
    auth.register_user('irene', 'InitialPass1')
    with pytest.raises(ValueError) as excinfo:
        auth.change_password('irene', 'WrongOldPass', 'NewPass2')
    assert "Contraseña antigua incorrecta." in str(excinfo.value)

def test_change_password_invalid_new(auth):
    auth.register_user('jack', 'OldPass1')
    with pytest.raises(ValueError) as excinfo:
        auth.change_password('jack', 'OldPass1', 'short')
    assert "La nueva contraseña no cumple con los requisitos." in str(excinfo.value)

def test_delete_user_as_admin(auth):
    auth.register_user('admin', 'AdminPass1', role='admin')
    auth.register_user('kate', 'UserPass1')
    auth.delete_user('admin', 'kate')
    assert 'kate' not in auth.users

def test_delete_user_as_non_admin(auth):
    auth.register_user('leo', 'UserPass1')
    auth.register_user('mia', 'UserPass2')
    with pytest.raises(PermissionError) as excinfo:
        auth.delete_user('leo', 'mia')
    assert "Permiso denegado" in str(excinfo.value)

def test_delete_nonexistent_user(auth):
    auth.register_user('nina', 'UserPass1', role='admin')
    with pytest.raises(ValueError) as excinfo:
        auth.delete_user('nina', 'oliver')
    assert "Usuario objetivo no encontrado." in str(excinfo.value)

def test_delete_user_non_admin_username(auth):
    with pytest.raises(ValueError) as excinfo:
        auth.delete_user('peter', 'quincy')
    assert "Usuario administrador no encontrado." in str(excinfo.value)
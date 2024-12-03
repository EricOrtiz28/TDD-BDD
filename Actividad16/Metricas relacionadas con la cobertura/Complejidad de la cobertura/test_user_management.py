# test_user_management.py

import pytest
from user_management import User, UserManager

# Fixtures
@pytest.fixture
def user_manager():
    return UserManager()

@pytest.fixture
def valid_user_data():
    return {'username': 'john_doe', 'password': 'Passw0rd'}

@pytest.fixture
def admin_user_data():
    return {'username': 'admin', 'password': 'AdminPass1', 'role': 'admin'}

# Pruebas para la clase User
def test_user_initialization_valid(valid_user_data):
    user = User(**valid_user_data)
    assert user.username == 'john_doe'
    assert user.password == 'Passw0rd'
    assert user.role == 'user'
    assert user.is_active == True

def test_user_initialization_invalid_type():
    with pytest.raises(TypeError):
        User(username=123, password='Passw0rd')

def test_user_initialization_empty_username(valid_user_data):
    with pytest.raises(ValueError):
        User(username='', password='Passw0rd')

def test_user_initialization_invalid_password():
    with pytest.raises(ValueError):
        User(username='jane_doe', password='short')

def test_user_initialization_invalid_role(valid_user_data):
    with pytest.raises(ValueError):
        User(username='jane_doe', password='Passw0rd', role='superuser')

def test_user_deactivate(valid_user_data):
    user = User(**valid_user_data)
    user.deactivate()
    assert user.is_active == False

def test_user_deactivate_already_inactive(valid_user_data):
    user = User(**valid_user_data)
    user.deactivate()
    with pytest.raises(ValueError):
        user.deactivate()

def test_user_change_password_success(valid_user_data):
    user = User(**valid_user_data)
    user.change_password(old_password='Passw0rd', new_password='NewPass1')
    assert user.password == 'NewPass1'

def test_user_change_password_incorrect_old(valid_user_data):
    user = User(**valid_user_data)
    with pytest.raises(ValueError):
        user.change_password(old_password='WrongPass', new_password='NewPass1')

def test_user_change_password_invalid_new(valid_user_data):
    user = User(**valid_user_data)
    with pytest.raises(ValueError):
        user.change_password(old_password='Passw0rd', new_password='short')

def test_user_promote_to_admin(valid_user_data):
    user = User(**valid_user_data)
    user.promote_to_admin()
    assert user.role == 'admin'

def test_user_promote_to_admin_already_admin(admin_user_data):
    user = User(**admin_user_data)
    with pytest.raises(ValueError):
        user.promote_to_admin()

def test_user_demote_to_user(admin_user_data):
    user = User(**admin_user_data)
    user.demote_to_user()
    assert user.role == 'user'

def test_user_demote_to_user_already_user(valid_user_data):
    user = User(**valid_user_data)
    with pytest.raises(ValueError):
        user.demote_to_user()

# Pruebas para la clase UserManager
def test_add_user_success(user_manager, valid_user_data):
    user_manager.add_user(**valid_user_data)
    assert 'john_doe' in user_manager.users
    user = user_manager.get_user('john_doe')
    assert user.username == 'john_doe'

def test_add_user_existing_username(user_manager, valid_user_data):
    user_manager.add_user(**valid_user_data)
    with pytest.raises(ValueError):
        user_manager.add_user(**valid_user_data)

def test_add_user_invalid_data(user_manager):
    with pytest.raises(TypeError):
        user_manager.add_user(username='jane_doe', password=12345678)

def test_remove_user_success(user_manager, valid_user_data):
    user_manager.add_user(**valid_user_data)
    user_manager.remove_user('john_doe')
    assert 'john_doe' not in user_manager.users

def test_remove_user_nonexistent(user_manager):
    with pytest.raises(ValueError):
        user_manager.remove_user('nonexistent')

def test_authenticate_success(user_manager, valid_user_data):
    user_manager.add_user(**valid_user_data)
    assert user_manager.authenticate('john_doe', 'Passw0rd') == True

def test_authenticate_incorrect_password(user_manager, valid_user_data):
    user_manager.add_user(**valid_user_data)
    assert user_manager.authenticate('john_doe', 'WrongPass') == False

def test_authenticate_nonexistent_user(user_manager):
    assert user_manager.authenticate('ghost', 'NoPass') == False

def test_authenticate_inactive_user(user_manager, valid_user_data):
    user_manager.add_user(**valid_user_data)
    user = user_manager.get_user('john_doe')
    user.deactivate()
    assert user_manager.authenticate('john_doe', 'Passw0rd') == False

def test_promote_user_as_admin(user_manager, admin_user_data, valid_user_data):
    user_manager.add_user(**admin_user_data)
    user_manager.add_user(**valid_user_data)
    user_manager.promote_user(admin_username='admin', target_username='john_doe')
    user = user_manager.get_user('john_doe')
    assert user.role == 'admin'

def test_promote_user_as_non_admin(user_manager, valid_user_data):
    user_manager.add_user(**valid_user_data)
    with pytest.raises(PermissionError):
        user_manager.promote_user(admin_username='john_doe', target_username='john_doe')

def test_promote_user_nonexistent_target(user_manager, admin_user_data):
    user_manager.add_user(**admin_user_data)
    with pytest.raises(ValueError):
        user_manager.promote_user(admin_username='admin', target_username='ghost')

def test_demote_user_as_admin(user_manager, admin_user_data, valid_user_data):
    user_manager.add_user(**admin_user_data)
    user_manager.add_user(**valid_user_data)
    user_manager.promote_user(admin_username='admin', target_username='john_doe')
    user_manager.demote_user(admin_username='admin', target_username='john_doe')
    user = user_manager.get_user('john_doe')
    assert user.role == 'user'

def test_demote_user_as_non_admin(user_manager, valid_user_data):
    user_manager.add_user(**valid_user_data)
    with pytest.raises(PermissionError):
        user_manager.demote_user(admin_username='john_doe', target_username='john_doe')

def test_demote_user_nonexistent_target(user_manager, admin_user_data):
    user_manager.add_user(**admin_user_data)
    with pytest.raises(ValueError):
        user_manager.demote_user(admin_username='admin', target_username='ghost')

def test_deactivate_user_as_admin(user_manager, admin_user_data, valid_user_data):
    user_manager.add_user(**admin_user_data)
    user_manager.add_user(**valid_user_data)
    user_manager.deactivate_user(admin_username='admin', target_username='john_doe')
    user = user_manager.get_user('john_doe')
    assert user.is_active == False

def test_deactivate_user_as_non_admin(user_manager, valid_user_data):
    user_manager.add_user(**valid_user_data)
    with pytest.raises(PermissionError):
        user_manager.deactivate_user(admin_username='john_doe', target_username='john_doe')

def test_deactivate_user_nonexistent_target(user_manager, admin_user_data):
    user_manager.add_user(**admin_user_data)
    with pytest.raises(ValueError):
        user_manager.deactivate_user(admin_username='admin', target_username='ghost')

def test_list_active_users(user_manager, admin_user_data, valid_user_data):
    user_manager.add_user(**admin_user_data)
    user_manager.add_user(**valid_user_data)
    active_users = user_manager.list_active_users()
    assert 'admin' in active_users
    assert 'john_doe' in active_users

def test_list_admins(user_manager, admin_user_data, valid_user_data):
    user_manager.add_user(**admin_user_data)
    user_manager.add_user(**valid_user_data)
    admins = user_manager.list_admins()
    assert 'admin' in admins
    assert 'john_doe' not in admins

def test_multiple_admins(user_manager):
    user_manager.add_user(username='admin1', password='AdminPass1', role='admin')
    user_manager.add_user(username='admin2', password='AdminPass2', role='admin')
    admins = user_manager.list_admins()
    assert 'admin1' in admins
    assert 'admin2' in admins

def test_promote_and_demote_user(user_manager, admin_user_data, valid_user_data):
    user_manager.add_user(**admin_user_data)
    user_manager.add_user(**valid_user_data)
    user_manager.promote_user(admin_username='admin', target_username='john_doe')
    user = user_manager.get_user('john_doe')
    assert user.role == 'admin'
    user_manager.demote_user(admin_username='admin', target_username='john_doe')
    assert user.role == 'user'

def test_deactivate_then_authenticate(user_manager, admin_user_data, valid_user_data):
    user_manager.add_user(**admin_user_data)
    user_manager.add_user(**valid_user_data)
    user_manager.deactivate_user(admin_username='admin', target_username='john_doe')
    assert user_manager.authenticate('john_doe', 'Passw0rd') == False

def test_change_password_success(user_manager, valid_user_data):
    user_manager.add_user(**valid_user_data)
    user = user_manager.get_user('john_doe')
    user.change_password(old_password='Passw0rd', new_password='NewPass1')
    assert user.password == 'NewPass1'
    assert user_manager.authenticate('john_doe', 'NewPass1') == True

def test_change_password_incorrect_old(user_manager, valid_user_data):
    user_manager.add_user(**valid_user_data)
    user = user_manager.get_user('john_doe')
    with pytest.raises(ValueError):
        user.change_password(old_password='WrongPass', new_password='NewPass1')

def test_change_password_invalid_new(user_manager, valid_user_data):
    user_manager.add_user(**valid_user_data)
    user = user_manager.get_user('john_doe')
    with pytest.raises(ValueError):
        user.change_password(old_password='Passw0rd', new_password='short')
# test_bank_account.py

import pytest
from bank_account import BankAccount

@pytest.fixture
def account():
    return BankAccount(owner='Alice', balance=1000)

def test_initialization_valid():
    acc = BankAccount('Bob', 500)
    assert acc.owner == 'Bob'
    assert acc.balance == 500
    assert acc.transaction_history == []

def test_initialization_negative_balance():
    with pytest.raises(ValueError) as excinfo:
        BankAccount('Charlie', -100)
    assert "El saldo inicial no puede ser negativo." in str(excinfo.value)

def test_deposit_positive_amount(account):
    account.deposit(500)
    assert account.balance == 1500
    assert account.transaction_history[-1] == {'type': 'deposit', 'amount': 500}

def test_deposit_zero_amount(account):
    with pytest.raises(ValueError) as excinfo:
        account.deposit(0)
    assert "El monto a depositar debe ser positivo." in str(excinfo.value)

def test_deposit_negative_amount(account):
    with pytest.raises(ValueError) as excinfo:
        account.deposit(-200)
    assert "El monto a depositar debe ser positivo." in str(excinfo.value)

def test_withdraw_valid_amount(account):
    account.withdraw(300)
    assert account.balance == 700
    assert account.transaction_history[-1] == {'type': 'withdraw', 'amount': 300}

def test_withdraw_zero_amount(account):
    with pytest.raises(ValueError) as excinfo:
        account.withdraw(0)
    assert "El monto a retirar debe ser positivo." in str(excinfo.value)

def test_withdraw_negative_amount(account):
    with pytest.raises(ValueError) as excinfo:
        account.withdraw(-100)
    assert "El monto a retirar debe ser positivo." in str(excinfo.value)

def test_withdraw_insufficient_balance(account):
    with pytest.raises(ValueError) as excinfo:
        account.withdraw(1500)
    assert "Saldo insuficiente." in str(excinfo.value)

def test_transfer_valid(account):
    target = BankAccount('Dave', 500)
    account.transfer(200, target)
    assert account.balance == 800
    assert target.balance == 700
    assert account.transaction_history[-1] == {'type': 'transfer', 'amount': 200, 'to': 'Dave'}

def test_transfer_zero_amount(account):
    target = BankAccount('Eve', 300)
    with pytest.raises(ValueError) as excinfo:
        account.transfer(0, target)
    assert "El monto a transferir debe ser positivo." in str(excinfo.value)

def test_transfer_negative_amount(account):
    target = BankAccount('Frank', 300)
    with pytest.raises(ValueError) as excinfo:
        account.transfer(-50, target)
    assert "El monto a transferir debe ser positivo." in str(excinfo.value)

def test_transfer_insufficient_balance(account):
    target = BankAccount('Grace', 300)
    with pytest.raises(ValueError) as excinfo:
        account.transfer(2000, target)
    assert "Saldo insuficiente para la transferencia." in str(excinfo.value)

def test_transfer_invalid_target(account):
    with pytest.raises(TypeError) as excinfo:
        account.transfer(100, "NotAnAccount")
    assert "La cuenta objetivo debe ser una instancia de BankAccount." in str(excinfo.value)

def test_get_balance(account):
    assert account.get_balance() == 1000
    account.deposit(500)
    assert account.get_balance() == 1500

def test_get_transaction_history(account):
    account.deposit(200)
    account.withdraw(100)
    expected_history = [
        {'type': 'deposit', 'amount': 200},
        {'type': 'withdraw', 'amount': 100}
    ]
    assert account.get_transaction_history() == expected_history

def test_multiple_operations(account):
    account.deposit(300)
    account.withdraw(200)
    target = BankAccount('Hank', 400)
    account.transfer(100, target)
    assert account.balance == 1000
    assert target.balance == 500
    expected_history = [
        {'type': 'deposit', 'amount': 300},
        {'type': 'withdraw', 'amount': 200},
        {'type': 'transfer', 'amount': 100, 'to': 'Hank'}
    ]
    assert account.get_transaction_history() == expected_history

def test_transfer_chain(account):
    target1 = BankAccount('Ivy', 600)
    target2 = BankAccount('Jack', 700)
    account.transfer(100, target1)
    target1.transfer(200, target2)
    
    assert account.balance == 900
    assert target1.balance == 500
    assert target2.balance == 900
    
    expected_history_acc = [
        {'type': 'transfer', 'amount': 100, 'to': 'Ivy'}
    ]
    expected_history_target1 = [
        {'type': 'received_transfer', 'amount': 100, 'from': 'Alice'},
        {'type': 'transfer', 'amount': 200, 'to': 'Jack'}
    ]
    expected_history_target2 = [
        {'type': 'received_transfer', 'amount': 200, 'from': 'Ivy'}
    ]
    
    assert account.get_transaction_history() == expected_history_acc
    assert target1.get_transaction_history() == expected_history_target1
    assert target2.get_transaction_history() == expected_history_target2

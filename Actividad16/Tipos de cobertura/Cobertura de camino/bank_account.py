# bank_account.py

class BankAccount:
    def __init__(self, owner, balance=0):
        self.owner = owner
        if balance < 0:
            raise ValueError("El saldo inicial no puede ser negativo.")
        self.balance = balance
        self.transaction_history = []

    def deposit(self, amount, record_transaction=True):
        if amount <= 0:
            raise ValueError("El monto a depositar debe ser positivo.")
        self.balance += amount
        if record_transaction:
            self.transaction_history.append({'type': 'deposit', 'amount': amount})

    def withdraw(self, amount, record_transaction=True):
        if amount <= 0:
            raise ValueError("El monto a retirar debe ser positivo.")
        if amount > self.balance:
            raise ValueError("Saldo insuficiente.")
        self.balance -= amount
        if record_transaction:
            self.transaction_history.append({'type': 'withdraw', 'amount': amount})

    def transfer(self, amount, target_account):
        if not isinstance(target_account, BankAccount):
            raise TypeError("La cuenta objetivo debe ser una instancia de BankAccount.")
        if amount <= 0:
            raise ValueError("El monto a transferir debe ser positivo.")
        if amount > self.balance:
            raise ValueError("Saldo insuficiente para la transferencia.")
        
        self.withdraw(amount, record_transaction=False)
        target_account.deposit(amount, record_transaction=False)
        
        self.transaction_history.append({'type': 'transfer', 'amount': amount, 'to': target_account.owner})
        target_account.transaction_history.append({'type': 'received_transfer', 'amount': amount, 'from': self.owner})

    def get_balance(self):
        return self.balance

    def get_transaction_history(self):
        return self.transaction_history
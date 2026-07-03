class InsufficientFundsError(Exception):
    pass


class BankAccount:

    def __init__(self, owner, balance=0):
        if not isinstance(owner, str) or owner.strip() == "":
            raise ValueError("Owner must be a non-empty string")
        if balance < 0:
            raise ValueError("Initial balance cannot be negative")
        self.owner = owner
        self.balance = balance
        self.transactions = []

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        self.balance += amount
        self.transactions.append(("deposit", amount))

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")
        if amount > self.balance:
            raise InsufficientFundsError("Insufficient funds")
        self.balance -= amount
        self.transactions.append(("withdraw", amount))

    def transfer(self, other_account, amount):
        if not isinstance(other_account, BankAccount):
            raise TypeError("Target must be a BankAccount instance")
        self.withdraw(amount)
        other_account.deposit(amount)

    def get_balance(self):
        return self.balance

    def get_transaction_count(self):
        return len(self.transactions)
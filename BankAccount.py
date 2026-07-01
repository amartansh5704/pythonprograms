class BankAccount:
    bank_name = "Bank of kk"
    total_accounts = 0

    def __init__(self, owner_name, account_number, initial_balance):
        self.owner_name = owner_name
        self.account_number = account_number
        self.balance = initial_balance
        self.transaction_history = []
        BankAccount.total_accounts += 1
        print(f"Account created for {self.owner_name}.")

    def deposit(self, amount):
        if amount <= 0:
            print("Deposit amount must be positive.")
            return
        self.balance += amount
        self.transaction_history.append(f"Deposited: ${amount:.2f}")
        print(f"Deposited ${amount:.2f}.")
        print(f"New balance: ${self.balance:.2f}")

    def withdraw(self, amount):
        if amount <= 0:
            print("Withdrawal amount must be positive.")
            return
        if amount > self.balance:
            print("Insufficient funds for this withdrawal.")
            return
        self.balance -= amount
        self.transaction_history.append(f"Withdrew: ${amount:.2f}")
        print(f"Withdrew ${amount:.2f}.")
        print(f"New balance: ${self.balance:.2f}")

    def check_balance(self):
        print(f"="*30)
        print(f"Account Owner: {self.owner_name}")
        print(f"Account Number: {self.account_number}")
        print(f"Current Balance: ${self.balance:.2f}")
        print(f"="*30)
    
    def show_transaction_history(self):
        if len(self.transaction_history) == 0:
            print("No transactions yet.")
            return
        print(f"Transaction History for {self.owner_name}:")
        print(f"="*30)
        for i, transaction in enumerate(self.transaction_history, start=1):
            print(f"{i}. {transaction}")
        print(f"="*30)

    def transfer(self, amount, target_account):
        print(f"Transferring ${amount:.2f} from {self.owner_name} to {target_account.owner_name}")
        if amount > self.balance:
            print("Insufficient funds for this transfer.")
            return
        self.balance -= amount
        target_account.balance += amount
        self.transaction_history.append(f"Transferred: ${amount:.2f} to {target_account.owner_name}")
        target_account.transaction_history.append(f"Received: ${amount:.2f} from {self.owner_name}")
        print(f"Transfer complete.")

    def __str__(self):
        return f"BankAccount(owner_name='{self.owner_name}', account_number='{self.account_number}', balance=${self.balance:.2f})"

    @classmethod
    def get_total_accounts(cls):
        print(f"{cls.bank_name} has a total of {cls.total_accounts} accounts.")

print("Welcome to the Bank Account Management System!")

account1 = BankAccount("Alice", "123456789", 1000.0)
account2 = BankAccount("Bob", "987654321", 500.0)

print()
account1.deposit(200.0)
account1.withdraw(150.0)
account1.withdraw(2000.0)

print()
account1.check_balance()
account2.check_balance()

print()
account1.transfer(300.0, account2)
account2.check_balance()

print()
account1.show_transaction_history()
account2.show_transaction_history()

print()
BankAccount.get_total_accounts()

print()
print(account1)
print(account2)
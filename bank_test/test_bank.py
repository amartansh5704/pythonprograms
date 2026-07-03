import unittest
from bank import BankAccount, InsufficientFundsError


class TestBankAccountCreation(unittest.TestCase):

    def test_create_account_with_owner(self):
        account = BankAccount("Alice")
        self.assertEqual(account.owner, "Alice")

    def test_default_balance_is_zero(self):
        account = BankAccount("Alice")
        self.assertEqual(account.get_balance(), 0)

    def test_create_account_with_initial_balance(self):
        account = BankAccount("Alice", balance=500)
        self.assertEqual(account.get_balance(), 500)

    def test_negative_initial_balance_raises_error(self):
        with self.assertRaises(ValueError):
            BankAccount("Alice", balance=-100)

    def test_empty_owner_raises_error(self):
        with self.assertRaises(ValueError):
            BankAccount("")


class TestDeposit(unittest.TestCase):

    def setUp(self):
        self.account = BankAccount("Alice", balance=100)

    def test_deposit_increases_balance(self):
        self.account.deposit(50)
        self.assertEqual(self.account.get_balance(), 150)

    def test_deposit_zero_raises_error(self):
        with self.assertRaises(ValueError):
            self.account.deposit(0)

    def test_deposit_negative_raises_error(self):
        with self.assertRaises(ValueError):
            self.account.deposit(-50)

    def test_deposit_records_transaction(self):
        self.account.deposit(50)
        self.assertEqual(self.account.get_transaction_count(), 1)

    def test_multiple_deposits(self):
        self.account.deposit(50)
        self.account.deposit(25)
        self.assertEqual(self.account.get_balance(), 175)


class TestWithdraw(unittest.TestCase):

    def setUp(self):
        self.account = BankAccount("Alice", balance=200)

    def test_withdraw_decreases_balance(self):
        self.account.withdraw(50)
        self.assertEqual(self.account.get_balance(), 150)

    def test_withdraw_entire_balance(self):
        self.account.withdraw(200)
        self.assertEqual(self.account.get_balance(), 0)

    def test_withdraw_zero_raises_error(self):
        with self.assertRaises(ValueError):
            self.account.withdraw(0)

    def test_withdraw_negative_raises_error(self):
        with self.assertRaises(ValueError):
            self.account.withdraw(-50)

    def test_withdraw_more_than_balance_raises_error(self):
        with self.assertRaises(InsufficientFundsError):
            self.account.withdraw(500)

    def test_withdraw_records_transaction(self):
        self.account.withdraw(50)
        self.assertEqual(self.account.get_transaction_count(), 1)


class TestTransfer(unittest.TestCase):

    def setUp(self):
        self.alice = BankAccount("Alice", balance=500)
        self.bob = BankAccount("Bob", balance=100)

    def test_transfer_deducts_from_sender(self):
        self.alice.transfer(self.bob, 200)
        self.assertEqual(self.alice.get_balance(), 300)

    def test_transfer_adds_to_receiver(self):
        self.alice.transfer(self.bob, 200)
        self.assertEqual(self.bob.get_balance(), 300)

    def test_transfer_insufficient_funds(self):
        with self.assertRaises(InsufficientFundsError):
            self.alice.transfer(self.bob, 1000)

    def test_transfer_invalid_target_raises_error(self):
        with self.assertRaises(TypeError):
            self.alice.transfer("not_an_account", 100)

    def test_transfer_does_not_alter_balances_on_failure(self):
        try:
            self.alice.transfer(self.bob, 1000)
        except InsufficientFundsError:
            pass
        self.assertEqual(self.alice.get_balance(), 500)
        self.assertEqual(self.bob.get_balance(), 100)


if __name__ == "__main__":
    unittest.main()
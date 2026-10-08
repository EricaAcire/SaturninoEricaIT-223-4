import unittest
from decimal import Decimal

from bank_account import BankAccount


class TestBankAccount(unittest.TestCase):
    def setUp(self):
        self.account = BankAccount("Анна Иванова", "123456")

    def test_new_account_stores_details_and_starts_empty(self):
        self.assertEqual(self.account.owner, "Анна Иванова")
        self.assertEqual(self.account.account_number, "123456")
        self.assertEqual(self.account.get_balance(), Decimal("0"))
        self.assertTrue(self.account.is_empty())

    def test_deposit_increases_balance(self):
        self.account.deposit("125.50")
        self.assertEqual(self.account.get_balance(), Decimal("125.50"))
        self.assertFalse(self.account.is_empty())

    def test_deposit_rejects_invalid_amount_without_changing_balance(self):
        for amount in (0, -5, "not a number", float("inf")):
            with self.subTest(amount=amount):
                with self.assertRaises((TypeError, ValueError)):
                    self.account.deposit(amount)
                self.assertEqual(self.account.get_balance(), Decimal("0"))

    def test_withdraw_decreases_balance(self):
        self.account.deposit("100")
        self.account.withdraw("35.25")
        self.assertEqual(self.account.get_balance(), Decimal("64.75"))

    def test_withdraw_rejects_negative_and_excessive_amounts(self):
        self.account.deposit("50")
        for amount in (-1, "50.01"):
            with self.subTest(amount=amount):
                with self.assertRaises(ValueError):
                    self.account.withdraw(amount)
                self.assertEqual(self.account.get_balance(), Decimal("50"))

    def test_transfer_updates_both_accounts_by_same_amount(self):
        recipient = BankAccount("Борис Петров", "654321")
        self.account.deposit("100")

        self.account.transfer(recipient, "40.25")

        self.assertEqual(self.account.get_balance(), Decimal("59.75"))
        self.assertEqual(recipient.get_balance(), Decimal("40.25"))

    def test_failed_transfer_does_not_change_either_account(self):
        recipient = BankAccount("Борис Петров", "654321")
        self.account.deposit("20")

        with self.assertRaises(ValueError):
            self.account.transfer(recipient, "25")

        self.assertEqual(self.account.get_balance(), Decimal("20"))
        self.assertEqual(recipient.get_balance(), Decimal("0"))

    def test_transfer_rejects_non_positive_amount(self):
        recipient = BankAccount("Борис Петров", "654321")
        self.account.deposit("20")

        with self.assertRaises(ValueError):
            self.account.transfer(recipient, 0)

        self.assertEqual(self.account.get_balance(), Decimal("20"))
        self.assertEqual(recipient.get_balance(), Decimal("0"))

    def test_transfer_to_same_account_does_not_change_balance(self):
        self.account.deposit("20")
        self.account.transfer(self.account, "5")
        self.assertEqual(self.account.get_balance(), Decimal("20"))

    def test_empty_account_after_withdrawing_full_balance(self):
        self.account.deposit("15")
        self.account.withdraw("15")
        self.assertTrue(self.account.is_empty())
        self.assertEqual(self.account.get_balance(), Decimal("0"))


if __name__ == "__main__":
    unittest.main()
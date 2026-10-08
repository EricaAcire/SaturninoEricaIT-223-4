from decimal import Decimal, InvalidOperation


class BankAccount:
    def __init__(self, owner, account_number):
        if not isinstance(owner, str) or not owner.strip():
            raise ValueError("Owner name must be a non-empty string")
        if not isinstance(account_number, str) or not account_number.strip():
            raise ValueError("Account number must be a non-empty string")

        self._owner = owner
        self._account_number = account_number
        self._balance = Decimal("0")

    @property
    def owner(self):
        return self._owner

    @property
    def account_number(self):
        return self._account_number

    @staticmethod
    def _to_amount(amount):
        if isinstance(amount, bool):
            raise TypeError("Amount must be a number")
        try:
            converted = Decimal(str(amount))
        except (InvalidOperation, ValueError):
            raise TypeError("Amount must be a number") from None
        if not converted.is_finite():
            raise ValueError("Amount must be a finite number")
        return converted

    def deposit(self, amount):
        amount = self._to_amount(amount)
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        self._balance += amount

    def withdraw(self, amount):
        amount = self._to_amount(amount)
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")
        if amount > self._balance:
            raise ValueError("Insufficient funds")
        self._balance -= amount

    def transfer(self, recipient, amount):
        if not isinstance(recipient, BankAccount):
            raise TypeError("Recipient must be a bank account")
        amount = self._to_amount(amount)
        if amount <= 0:
            raise ValueError("Transfer amount must be positive")
        if amount > self._balance:
            raise ValueError("Insufficient funds")

        if recipient is self:
            return
        self._balance -= amount
        recipient._balance += amount

    def get_balance(self):
        return self._balance

    def is_empty(self):
        return self._balance == 0


def run_terminal():
    accounts = {}

    while True:
        print("\n=== Bank Accounts ===")
        print("1. Create an account")
        print("2. Deposit money")
        print("3. Withdraw money")
        print("4. Transfer money")
        print("5. Show balance and check account")
        print("0. Exit")

        choice = input("Choose an option: ").strip()
        if choice == "0":
            print("Goodbye.")
            return

        try:
            if choice == "1":
                owner = input("Owner name: ").strip()
                account_number = input("Account number: ").strip()
                if account_number in accounts:
                    print("An account with that number already exists.")
                    continue
                accounts[account_number] = BankAccount(owner, account_number)
                print("Account created.")
            elif choice in {"2", "3", "4", "5"}:
                account_number = input("Account number: ").strip()
                account = accounts.get(account_number)
                if account is None:
                    print("Account not found.")
                    continue

                if choice == "2":
                    account.deposit(input("Deposit amount: "))
                    print("Deposit successful.")
                elif choice == "3":
                    account.withdraw(input("Withdrawal amount: "))
                    print("Withdrawal successful.")
                elif choice == "4":
                    recipient_number = input("Recipient account number: ").strip()
                    recipient = accounts.get(recipient_number)
                    if recipient is None:
                        print("Recipient account not found.")
                        continue
                    account.transfer(recipient, input("Transfer amount: "))
                    print("Transfer successful.")
                else:
                    print(f"Balance: {account.get_balance()}")
                    print("Account is empty." if account.is_empty() else "Account is not empty.")
            else:
                print("Invalid option. Choose an option from the menu.")
        except (TypeError, ValueError) as error:
            print(f"Operation failed: {error}")


if __name__ == "__main__":
    run_terminal()
from decimal import Decimal, InvalidOperation


class BankAccount:
    def __init__(self, owner, account_number):
        if not isinstance(owner, str) or not owner.strip():
            raise ValueError("Имя владельца должно быть непустой строкой")
        if not isinstance(account_number, str) or not account_number.strip():
            raise ValueError("Номер счёта должен быть непустой строкой")

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
            raise TypeError("Сумма должна быть числом")
        try:
            converted = Decimal(str(amount))
        except (InvalidOperation, ValueError):
            raise TypeError("Сумма должна быть числом") from None
        if not converted.is_finite():
            raise ValueError("Сумма должна быть конечным числом")
        return converted

    def deposit(self, amount):
        amount = self._to_amount(amount)
        if amount <= 0:
            raise ValueError("Сумма пополнения должна быть положительной")
        self._balance += amount

    def withdraw(self, amount):
        amount = self._to_amount(amount)
        if amount <= 0:
            raise ValueError("Сумма снятия должна быть положительной")
        if amount > self._balance:
            raise ValueError("Недостаточно средств на счёте")
        self._balance -= amount

    def transfer(self, recipient, amount):
        if not isinstance(recipient, BankAccount):
            raise TypeError("Получатель должен быть банковским счётом")
        amount = self._to_amount(amount)
        if amount <= 0:
            raise ValueError("Сумма перевода должна быть положительной")
        if amount > self._balance:
            raise ValueError("Недостаточно средств на счёте")

        if recipient is self:
            return
        self._balance -= amount
        recipient._balance += amount

    def get_balance(self):
        return self._balance

    def is_empty(self):
        return self._balance == 0
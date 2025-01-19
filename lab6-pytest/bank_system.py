import asyncio
import random

class InsufficientFundsError(Exception):
    """Wyjątek rzucany w przypadku niewystarczającego salda."""
    pass


async def external_authorization_service():
    """
    Symulacja zewnętrznego systemu autoryzacji – zwraca True, ale można go zmockować.
    """
    delay = random.uniform(0.01, 0.09)
    await asyncio.sleep(delay)
    return True


class Account:
    """
    Klasa reprezentująca konto bankowe.
    """
    def __init__(self, account_number: str, owner: str, initial_balance: float = 0.0):
        self.account_number = account_number
        self.owner = owner
        self.balance = initial_balance

    def deposit(self, amount: float):
        """
        Metoda wpłaty środków na konto.
        """
        if amount < 0:
            raise ValueError("Kwota wpłaty nie może być ujemna.")
        self.balance += amount

    def withdraw(self, amount: float):
        """
        Metoda wypłaty środków z konta.
        Jeśli saldo jest mniejsze niż kwota wypłaty, rzuca InsufficientFundsError.
        """
        if amount > self.balance:
            raise InsufficientFundsError("Niewystarczające środki na koncie.")
        self.balance -= amount

    async def transfer(self, to_account: 'Account', amount: float):
        """
        Asynchroniczna metoda transferu środków na inne konto.
        """
        delay = random.uniform(0.01, 0.09)
        await asyncio.sleep(delay)

        if amount > self.balance:
            raise InsufficientFundsError("Niewystarczające środki na koncie do przelewu.")

        authorized = await external_authorization_service()
        if not authorized:
            raise PermissionError("Transakcja nieautoryzowana przez zewnętrzny system.")

        self.balance -= amount
        to_account.balance += amount


class Bank:
    """
    Klasa reprezentująca bank jako zbiór kont i operacje na nich.
    """
    def __init__(self):
        self.accounts = {}

    def create_account(self, account_number: str, owner: str, initial_balance: float):
        """
        Tworzy nowe konto bankowe i dodaje je do słownika accounts.
        """
        if account_number in self.accounts:
            raise ValueError(f"Konto o numerze {account_number} już istnieje.")
        account = Account(account_number, owner, initial_balance)
        self.accounts[account_number] = account
        return account

    def get_account(self, account_number: str):
        """
        Zwraca konto na podstawie numeru konta.
        Rzuca ValueError, jeśli konto nie istnieje.
        """
        if account_number not in self.accounts:
            raise ValueError(f"Konto o numerze {account_number} nie istnieje.")
        return self.accounts[account_number]

    async def process_transaction(self, transaction_func):
        """
        Metoda procesująca transakcję asynchronicznie.
        """
        await asyncio.sleep(0.01)
        await transaction_func()

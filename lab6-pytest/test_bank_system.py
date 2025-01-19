import asyncio
from unittest.mock import patch, AsyncMock

import pytest
import pytest_asyncio

from bank_system import Account, Bank, InsufficientFundsError


@pytest.fixture
def sample_account():
    """
    Fixture tworzący przykładowe konto z początkowym saldem 100.
    """
    return Account("12345", "Jan Kowalski", 100.0)


@pytest.mark.parametrize("deposit_amount,expected_balance", [
    (50, 150),
    (0, 100),
    (25.5, 125.5),
])
def test_deposit_param(sample_account, deposit_amount, expected_balance):
    """
    Test wpłaty z użyciem parametryzacji danych.
    """
    sample_account.deposit(deposit_amount)
    assert sample_account.balance == pytest.approx(expected_balance)


def test_deposit_negative_amount(sample_account):
    """
    Test wpłaty ujemnej kwoty, oczekiwany wyjątek ValueError.
    """
    with pytest.raises(ValueError):
        sample_account.deposit(-10.0)


@pytest.mark.parametrize("withdraw_amount,expected_balance", [
    (50, 50),
    (100, 0),
    (99.99, 0.01),
])
def test_withdraw_success_param(sample_account, withdraw_amount, expected_balance):
    """
    Test wypłat z użyciem parametryzacji danych.
    """
    sample_account.withdraw(withdraw_amount)
    assert sample_account.balance == pytest.approx(expected_balance)


def test_withdraw_insufficient_funds(sample_account):
    """
    Test wypłaty większej kwoty niż dostępne saldo.
    Oczekiwany wyjątek InsufficientFundsError.
    """
    with pytest.raises(InsufficientFundsError):
        sample_account.withdraw(200.0)


@pytest_asyncio.fixture
async def accounts_for_transfer():
    """
    Fixture tworzący dwa konta na potrzeby testów przelewów.
    """
    acc1 = Account("A1", "Marek", 500.0)
    acc2 = Account("A2", "Zosia", 300.0)
    return acc1, acc2


@pytest.mark.asyncio
async def test_transfer_success(accounts_for_transfer):
    """
    Test poprawnego przelewu między dwoma kontami.
    """
    acc1, acc2 = accounts_for_transfer
    await acc1.transfer(acc2, 200.0)
    assert acc1.balance == 300.0
    assert acc2.balance == 500.0


@pytest.mark.asyncio
async def test_transfer_insufficient_funds(accounts_for_transfer):
    """
    Test przelewu, gdy saldo jest niewystarczające.
    Oczekiwany wyjątek InsufficientFundsError.
    """
    acc1, acc2 = accounts_for_transfer
    with pytest.raises(InsufficientFundsError):
        await acc2.transfer(acc1, 400.0)


@pytest.mark.asyncio
async def test_transfer_not_authorized(accounts_for_transfer):
    """
    Przykład testu pokazującego jak zmockować zewnętrzny system autoryzacji,
    aby symulować brak autoryzacji (False).
    """
    acc1, acc2 = accounts_for_transfer

    # Mockujemy usługę autoryzacji, żeby zwróciła False
    with patch("bank_system.external_authorization_service",
               new_callable=AsyncMock,
               return_value=False):
        with pytest.raises(PermissionError):
            await acc1.transfer(acc2, 100.0)


@pytest.mark.asyncio
async def test_parallel_transfers():
    """
    Test równoległego wykonywania kilku przelewów.
    Symulujemy np. sytuację, w której jedno konto robi przelewy do kilku innych kont
    jednocześnie.
    """
    acc1 = Account("Main", "Główny", 1000.0)
    acc2 = Account("Second", "Drugi", 100.0)
    acc3 = Account("Third", "Trzeci", 200.0)

    async def transfer1():
        await acc1.transfer(acc2, 300)

    async def transfer2():
        await acc1.transfer(acc3, 100)

    await asyncio.gather(transfer1(), transfer2())
    # Kalkulacje:
    assert acc1.balance == 600.0  # 1000 - 300 - 100
    assert acc2.balance == 400.0  # 100 + 300
    assert acc3.balance == 300.0  # 200 + 100


@pytest.fixture
def bank_with_accounts():
    """
    Fixture tworzący obiekt Bank i kilka kont do testów.
    """
    bank = Bank()
    bank.create_account("111", "Alice", 1000.0)
    bank.create_account("222", "Bob", 500.0)
    return bank


def test_bank_create_account(bank_with_accounts):
    """
    Test tworzenia konta w banku.
    """
    account = bank_with_accounts.create_account("333", "Charlie", 300.0)
    assert account.account_number == "333"
    assert account.balance == 300.0
    assert bank_with_accounts.get_account("333") is account


def test_bank_create_account_already_exists(bank_with_accounts):
    """
    Test tworzenia konta z numerem, który już istnieje.
    Oczekiwany wyjątek ValueError.
    """
    with pytest.raises(ValueError):
        bank_with_accounts.create_account("111", "Zbyszek", 700.0)


def test_bank_get_account_not_found(bank_with_accounts):
    """
    Test pobierania nieistniejącego konta z banku.
    Oczekiwany wyjątek ValueError.
    """
    with pytest.raises(ValueError):
        bank_with_accounts.get_account("9999999")


@pytest.mark.asyncio
async def test_bank_process_transaction(bank_with_accounts):
    """
    Test asynchronicznego przetwarzania transakcji w banku.
    """
    acc1 = bank_with_accounts.get_account("111")
    acc2 = bank_with_accounts.get_account("222")

    async def transaction():
        await acc1.transfer(acc2, 200.0)

    await bank_with_accounts.process_transaction(transaction)

    assert acc1.balance == 800.0
    assert acc2.balance == 700.0

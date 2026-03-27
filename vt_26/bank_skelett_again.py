from dataclasses import dataclass
from enum import Enum
from datetime import datetime
from typing import Optional
from pathlib import Path

############ GLOBALS ###################
ACCOUNTS_FILE = "accounts.txt"
TRANSACTIONS_DIR = "transactions"
DT_FORMAT = "%Y%m%d-%H:%M:%S"
############ END GLOBALS ###############

############ CLASSES ###################
class TransactionType(Enum):
    WITHDRAW = 1
    DEPOSIT = 2
    TRANSFER = 3

class AccountType(Enum):
    SALARY = 1
    SAVING = 2
    CREDIT = 3

@dataclass
class Transaction:
    account_number: int
    amount:int
    type:TransactionType
    time:datetime

class TransactionDB:
    def __init__(self):
        self._transactions:dict[int, list[Transaction]]

class InsufficientFundsError(Exception):
    ...

class Account:
    def __init__(self,
                 account_number:int,
                 saldo:int,
                 account_type:AccountType,
                 transactions:Optional[list[Transaction]]=None):

        self._account_number:int = account_number
        self._saldo:int = saldo
        self._type:TransactionType = account_type
        self._transactions:list[Transaction] = transactions or []

    @property
    def account_number(self) -> int:
        return self._account_number

    @property
    def saldo(self) -> int:
        return self._saldo

    @property
    def type(self) -> AccountType:
        return self._type

    @property
    def transactions(self) -> list[Transaction]:
        return self._transactions.copy()

    def withdraw(self, amount:int):
        assert amount > 0

        if self.saldo < amount:
            raise InsufficientFundsError

        self._make_transaction(amount, TransactionType.WITHDRAW)
        self._saldo -= amount

    def deposit(self, amount:int):

        assert amount > 0

        self._make_transaction(amount, TransactionType.DEPOSIT)
        self._saldo += amount

    def _make_transaction(self, amount:int, trans_type:TransactionType):
        transaction_time = datetime.now()
        new_transaction = Transaction(
            account_number=self.account_number,
            amount=amount,
            type=trans_type,
            time=transaction_time
            )
        self._transactions.append(new_transaction)
        transaction_path = Path(TRANSACTIONS_DIR) / Path(str(self.account_number)+".txt")

        with open(transaction_path, "a") as f:
            f.write(f"{trans_type.value},{transaction_time.strftime(DT_FORMAT)},{amount}\n")


    def __str__(self) -> str:
        return  f"Account Number: {self._account_number}\n" \
                f"Account Type:   {self._type.name}\n" \
                f"Account Saldo:  {self._saldo}\n"

class Bank:
    def __init__(self):
        self._accounts:dict[int,Account] = {}

    def get_account(self, account_number:int) -> Optional[Account]:
        return self._accounts.get(account_number, None)

    def create_account(self,
            new_account_number:int,
            account_type:AccountType):

        if new_account_number in self._accounts:
            raise ValueError(f"Account number {new_account_number} already exist!")

        new_account = Account(new_account_number, 0, account_type)
        self._accounts[new_account_number] = new_account

    def _parse_transactions(self, s:str, acc_nr:int) -> list[Transaction]:
        list_of_transactions = []
        for transaction_row in s.split("\n"):
            t_type, t_time, amount = transaction_row.split(",")
            list_of_transactions.append(
                Transaction(
                    acc_nr, 
                    int(amount),
                    TransactionType(int(t_type)),
                    datetime.strptime(t_time, DT_FORMAT)
                ))

        return list_of_transactions

    def load_accounts(self, accounts_file=ACCOUNTS_FILE):
        if self._accounts:
            raise ValueError("Accounts already loaded?????")

        with open(accounts_file, "r") as f:
            for acc_row in f.readlines():
                acc_num, saldo, type_v = acc_row.strip().split(",")
                trans_path = Path(TRANSACTIONS_DIR) / Path(acc_num + ".txt")
                if trans_path.exists():
                    with open(trans_path, "r") as f:
                        trans_string = f.read().strip()
    
                    transactions = self._parse_transactions(trans_string,int(acc_num))
                else:
                    transactions = []

                new_acc = Account(
                    int(acc_num), 
                    int(saldo), 
                    AccountType(int(type_v)),
                    transactions)
                

                self._accounts[int(acc_num)] = new_acc
            

    

    def save_accounts(self, accounts_file=ACCOUNTS_FILE):
        with open(accounts_file, "w") as f:
            for acc in self._accounts.values():
                f.write(f"{acc.account_number},{acc.saldo},{acc.type.value}\n")


############ END Classes###############

############ FUNCTIONS ################

def withdraw(acc:Account):
    try:
        amount = int(input("Enter amount:"))
    except ValueError:
        print("Amount must be a integer!")
        return
    if amount > 0:
        if amount < acc.saldo:
            acc.withdraw(amount)
        else:
            print("Insufficient fund! Poor bastard!")
    else:
        print("Amount must be more then zero!")



def deposit(acc:Account):
    try:
        amount = int(input("Enter amount:"))
    except ValueError:
        print("Amount must be a integer!")
        return
    if amount > 0:
        acc.deposit(amount)
    else:
        print("Amount must be more then zero!")

def print_transactions(acc:Account):
    for trans in acc.transactions:
        print(trans)

def account_menu(acc:Account) -> None:
    while True:
        print("1. Withdraw")
        print("2. Deposit")
        print("3. Saldo")
        print("4. Transactions")
        print("0. Return")

        acc_choice = input("Enter choice: ")

        match acc_choice:
            case "1":
                withdraw(acc)
            case "2":
                deposit(acc)
            case "3":
                print(acc.saldo)
            case "4":
                print_transactions(acc)
            case "0":
                return
            case _:
                ...

def run_atm(bank_connection:Bank) -> None:
    print("Welcome to the best ATM ever! Enjoy!")

    while True:
        print("1. Login")
        print("2. Create account")
        print("0. Shutdown")

        choice = input("Enter choice: ")

        if choice == "1":
            try:
                account_number = int(input("Enter account number: "))
            except ValueError:
                print("Must be integer!")
            else:
                acc = bank_connection.get_account(account_number)
                if acc:
                    account_menu(acc)
                else:
                    print("Account does not exist!")

        if choice == "2":
            try:
                new_account_number = int(input("Enter new account number: "))
            except ValueError:
                print("Invalid accountnumber! Must be a account number!")
                continue
            
            try:
                bank_connection.create_account(new_account_number, AccountType.CREDIT)
            except ValueError:
                continue
            
            print("Account Created!")
            
        if choice == "0": break
                            

def main():
    acc_file = Path(ACCOUNTS_FILE)
    bank = Bank()
    if acc_file.exists:
        bank.load_accounts()
    else:
        acc_file.touch()
    run_atm(bank)
    # acc1 = bank.get_account(1)
    # print(acc1)
    # acc1.deposit(50)
    # print(acc1)
    bank.save_accounts()


############ END FUNCTIONS ############


############ ENTRY ####################
if __name__ == "__main__":
    main()
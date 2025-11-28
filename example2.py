from dataclasses import dataclass
from enum import Enum
from datetime import datetime
from typing import Optional

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
        

    def __str__(self) -> str:
        return  f"Account Number: {self._account_number}\n" \
                f"Account Type:   {self._type.name}\n" \
                f"Account Saldo:  {self._saldo}\n"
    

class A:
    def my_method(self):
        print("my_method in a!")

class B:
    def my_method(self):
        print("my_method in b!")

class C(B):
    def my_method(self):
        print("overide B my_method with C my_method")
        print("my_method in c!")

def run_my_method(objects:list):
    for ob in objects:
        ob.my_method()

if __name__ == "__main__":
    # now = datetime.now()
    # t1 = Transaction(2, 20, TransactionType.WITHDRAW, now)
    # print(t1)
    # t2 = Transaction(2, 20, TransactionType.WITHDRAW, now)
    # print(f"{t1 == t2=}")

    # a1 = Account(2, 0, AccountType.SALARY)

    # print(a1)
    a = A()
    b = B()
    c = C()

    # a.my_method()
    # b.my_method()
    # c.my_method()
    run_my_method([a,b,c, "hejsan"])
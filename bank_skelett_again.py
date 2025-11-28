from dataclasses import dataclass
from enum import Enum
from datetime import datetime
from typing import Optional

############ GLOBALS ###################
ACCOUNTS_FILE = "accounts.txt"
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

    def _make_transaction(self, amount:int, type:TransactionType):
        new_transaction = Transaction(
            account_number=self.account_number,
            amount=amount,
            type=type,
            time=datetime.now()
            )
        self._transactions.append(new_transaction)

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

    def _parse_transactions(self, s:str) -> list[Transaction]:
        if s[0] != "[" or s[-1] != "]":
            raise ValueError("Not correct format!")
        s = s[1:-1]
        t = []
        if not s: return []

        lts = s.split("|")
        lts = lts[:-1]
        
        for st in lts:
            acc_nr, amount, t_type, time = st.strip().split(",")
            acc_nr = int(acc_nr)
            amount = int(amount)
            t_type = TransactionType(int(t_type))
            time = datetime.strptime(time, DT_FORMAT)
            t.append(Transaction(acc_nr, amount, t_type, time))

        return t

    def _serialize_transactions(self, lt:list[Transaction]) -> list[str]:
        st = []
        for t in lt:
            s = f"{t.account_number},{t.amount},{t.type.value},{t.time.strftime(DT_FORMAT)}|"
            st.append(s)
            
        return st
    
    def load_accounts(self, accounts_file=ACCOUNTS_FILE):
        if self._accounts:
            raise ValueError("Accounts already loaded?????")
        
        with open(accounts_file, "r") as f:
            for line in f.readlines():
                try:
                    line = line.strip() 
                    t_start = line.index("[")
                    acc_data = line[:t_start]
                
                    acc_nr, saldo, a_type = acc_data[:-1].split(",")
                    acc_nr = int(acc_nr)
                    saldo = int(saldo)
                    a_type = AccountType(int(a_type))

                    trans = line[t_start:].replace("'","")
                    trans = self._parse_transactions(trans)

                    account = Account(acc_nr, saldo, a_type, trans)
                    self._accounts[acc_nr] = account

                except ValueError as e:
                    print("All go to hell! Shutdown needed")
                    exit(-1)

    def save_accounts(self, accounts_file=ACCOUNTS_FILE):
        with open(accounts_file, "w") as f:
            for acc in self._accounts.values():
                s_acc = f"{acc.account_number},{acc.saldo},{acc.type.value},"
                s_acc += f"{self._serialize_transactions(acc.transactions)}"
                f.write(s_acc + "\n")


############ END Classes###############

############ FUNCTIONS ################



def main():
    bank = Bank()
    bank.load_accounts()

    acc1 = bank.get_account(1)
    print(acc1)
    acc1.deposit(50)
    print(acc1)
    bank.save_accounts()
    
    
############ END FUNCTIONS ############


############ ENTRY ####################
if __name__ == "__main__":
    main()
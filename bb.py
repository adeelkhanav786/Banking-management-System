import pymongo
from datetime import datetime
import hashlib
import sys

MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "bank_db"
COLLECTION_NAME = "bank_detail"

try:
    client = pymongo.MongoClient(MONGO_URI, serverSelectionTimeoutMS=3000)
    print("connected to mongo db")
    DB = client[DB_NAME]
    user_bank = DB[COLLECTION_NAME]
except Exception as e:
    print(f"error connecting to mongo db: {e}")
    sys.exit(1)


class bank:
    def __init__(self, user="default_user"):
        self.balance = self.user_bank.find_one({"username":self.user},get(balance)
        )
        self.user = user
        self.user_bank = user_bank  # Set user_bank as an instance attribute

    def deposit(self, amount):
        self.balance += amount
        # Update balance and add to transaction history in MongoDB
        self.user_bank.update_one(
            {"username": self.user},
            {
                "$inc": {"balance": amount},
                "$push": {
                    "history": {
                        "type": "deposit",
                        "amount": amount,
                        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }
                }
            },
            upsert=True
        )
        print(f"Deposited {amount}. Current balance: {self.balance}")

    def withdraw(self, amount):
        if self.balance >= amount:
            self.balance -= amount
            self.user_bank.update_one(
                 {"username": self.user},
                 {
                    "$inc": {"balance": -amount},
                    "$push": {
                        "history": {
                            "type": "withdrawal",
                            "amount": amount,
                            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        }
                    }
                },
                upsert=True
            )
            print("Transaction successful")
            print(f"Current balance is {self.balance}")
        else:
             print("Insufficient balance")

    def transactionhis(self):
        record = self.user_bank.find_one({"username": self.user})
        if record and "history" in record:
            print("--- Transaction History ---")
            for tx in record["history"]:
                print(tx)
        else:
            print("No transaction history found.")

    def show(self):
        record = self.user_bank.find_one({"username": self.user})
        if record:
            print("Your balance is rs. ", record.get("balance", self.balance))
        else:
            print("Your balance is rs. ", self.balance)


def main():
    account = bank(user="test_user")
    while True:
        print("\n welcome \n")
        print("press 1. to deposit money")
        print("press 2. to withdraw money")
        print("press 3. to check balance")
        print("press 4. transaction history")
        print("press 5. to exit")
        n = int(input("enter your choice : "))
        if n == 1:
            amount = int(input("enter amount : "))
            account.deposit(amount)
        elif n == 2:
            amount = int(input("enter amount : "))
            account.withdraw(amount)
        elif n == 3:
            account.show()
        elif n==4:
            account.transactionhis()
        elif n == 5:
            print("Exiting")
            break
        else:
            print("Invalid choice")


if __name__ == "__main__":
    main()
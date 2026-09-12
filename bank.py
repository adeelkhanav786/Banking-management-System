import sys
import hashlib
from datetime import datetime

try:
    import pymongo
except ImportError:
    print("PyMongo is not installed. Please run: pip install pymongo")
    sys.exit(1)

# Connect to MongoDB
MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "bank_db"
COLLECTION_NAME = "users"

try:
    client = pymongo.MongoClient(MONGO_URI, serverSelectionTimeoutMS=3000)
    db = client[DB_NAME]
    users_collection = db[COLLECTION_NAME]
    # Ping database to confirm connection
    client.admin.command('ping')
    print("Connected to MongoDB successfully!")
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")
    sys.exit(1)


def hash_password(password: str) -> str:
    """Hash password using SHA-256 for secure storage."""
    return hashlib.sha256(password.encode('utf-8')).hexdigest()


class BankAccount:
    def __init__(self, username):
        self.username = username

    def get_user_data(self):
        return users_collection.find_one({"username": self.username})

    def deposit(self, amount):
        if amount <= 0:
            print("Please enter a valid positive amount.")
            return

        tx = {
            "type": "deposit",
            "amount": amount,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        users_collection.update_one(
            {"username": self.username},
            {
                "$inc": {"balance": amount},
                "$push": {"transactions": tx}
            }
        )
        updated_user = self.get_user_data()
        print(f"Successfully deposited {amount}. Current Bank Balance : {updated_user['balance']}")

    def withdraw(self, amount):
        if amount <= 0:
            print("Please enter a valid positive amount.")
            return

        user = self.get_user_data()
        current_balance = user.get("balance", 0.0)

        if current_balance < amount:
            print("Insufficient bank balance")
            return

        tx = {
            "type": "withdraw",
            "amount": amount,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        users_collection.update_one(
            {"username": self.username},
            {
                "$inc": {"balance": -amount},
                "$push": {"transactions": tx}
            }
        )
        updated_user = self.get_user_data()
        print(f"Successfully withdrew {amount}. Current Bank Balance : {updated_user['balance']}")

    def show_balance(self):
        user = self.get_user_data()
        print(f"Current balance for {self.username} is : {user.get('balance', 0.0)}")

    def show_history(self):
        user = self.get_user_data()
        transactions = user.get("transactions", [])
        print(f"\n--- Transaction History for {self.username} ---")
        if not transactions:
            print("No transactions found.")
        else:
            for tx in transactions:
                print(f"[{tx.get('date')}] {tx.get('type').upper()}: {tx.get('amount')}")


def authenticate_user():
    """Handles username lookup, password check, or new user registration."""
    while True:
        print("\n=== User Login / Registration ===")
        username = input("Enter username: ").strip()
        if not username:
            print("Username cannot be empty.")
            continue

        existing_user = users_collection.find_one({"username": username})

        if existing_user:
            # User exists -> Prompt for password
            if "password" in existing_user and existing_user["password"]:
                attempts = 3
                while attempts > 0:
                    password = input(f"Enter password for [{username}]: ")
                    if hash_password(password) == existing_user["password"]:
                        print(f"\nLogin successful! Welcome back, {username}.")
                        return username
                    else:
                        attempts -= 1
                        print(f"Incorrect password! ({attempts} attempts remaining)")
                print("Too many failed attempts. Returning to login screen.")
            else:
                # Security update for legacy users without a password
                print(f"No password set for account [{username}]. Please set a password now.")
                while True:
                    password = input("Create a password: ")
                    confirm_pwd = input("Confirm password: ")
                    if password != confirm_pwd:
                        print("Passwords do not match. Please try again.")
                        continue
                    if not password:
                        print("Password cannot be empty.")
                        continue
                    users_collection.update_one(
                        {"username": username},
                        {"$set": {"password": hash_password(password)}}
                    )
                    print("Password created successfully! Welcome.")
                    return username
        else:
            # User does not exist -> Offer registration
            print(f"User '{username}' not found.")
            choice = input("Would you like to create a new account? (y/n): ").strip().lower()
            if choice == 'y' or choice == 'yes':
                while True:
                    password = input("Create a password: ")
                    confirm_pwd = input("Confirm password: ")
                    if password != confirm_pwd:
                        print("Passwords do not match. Please try again.")
                        continue
                    if not password:
                        print("Password cannot be empty.")
                        continue
                    
                    new_user = {
                        "username": username,
                        "password": hash_password(password),
                        "balance": 0.0,
                        "transactions": [],
                        "created_at": datetime.now().isoformat()
                    }
                    users_collection.insert_one(new_user)
                    print(f"Account successfully created for user: {username}!")
                    return username
            else:
                print("Registration cancelled.")


def main():
    print("=== Welcome to MongoDB Bank Management System ===")
    
    current_username = authenticate_user()
    if not current_username:
        print("Authentication failed. Goodbye!")
        return

    account = BankAccount(current_username)

    while True:
        print(f"\nLogged in as: [{current_username}]")
        print("1. Deposit in bank account")
        print("2. Withdraw money")
        print("3. Show the bank balance")
        print("4. Show transaction history")
        print("5. Switch user / Logout")
        print("6. Exit")

        try:
            choice = int(input("Enter what you want to do, select serial number from above : "))
        except ValueError:
            print("Invalid input. Please enter a valid number.")
            continue

        if choice == 1:
            try:
                a = float(input("Enter amount to deposit : "))
                account.deposit(a)
            except ValueError:
                print("Invalid amount.")
        elif choice == 2:
            try:
                a = float(input("Enter amount to withdraw : "))
                account.withdraw(a)
            except ValueError:
                print("Invalid amount.")
        elif choice == 3:
            account.show_balance()
        elif choice == 4:
            account.show_history()
        elif choice == 5:
            print("\nLogging out...")
            new_username = authenticate_user()
            if new_username:
                current_username = new_username
                account = BankAccount(current_username)
        elif choice == 6:
            print("Exiting Bank System. Goodbye!")
            break
        else:
            print("Invalid selection")


if __name__ == "__main__":
    main()


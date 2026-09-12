# 🏦 Banking Management System

> **A Python + MongoDB based banking management system for handling user accounts, authentication, deposits, withdrawals, balances, and transaction history.**

![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white)
![MongoDB](https://img.shields.io/badge/MongoDB-Database-47A248?style=for-the-badge&logo=mongodb&logoColor=white)
![PyMongo](https://img.shields.io/badge/PyMongo-MongoDB%20Driver-13AA52?style=for-the-badge&logo=mongodb&logoColor=white)
![CLI](https://img.shields.io/badge/Interface-CLI-111827?style=for-the-badge)

## 📌 Description

**Banking Management System** is a command-line banking application developed in **Python** with **MongoDB** as its database. The project demonstrates how a Python application can connect to a NoSQL database and perform common banking operations while maintaining persistent user and transaction data.

The application includes **user registration and login, password hashing, deposits, withdrawals, balance checking, transaction history, logout/user switching, and account creation**. MongoDB stores user information, account balances, passwords, account creation timestamps, and transaction records.

This project is useful for learning **Python OOP, MongoDB CRUD operations, database connectivity, authentication logic, exception handling, and transaction management** in a practical application.

## ✨ Key Features

- 🔐 **User Authentication** — Login with username and password.
- 🆕 **User Registration** — Create a new bank account directly from the application.
- 🔒 **Password Hashing** — Passwords are hashed using SHA-256 before storage.
- 💰 **Deposit Money** — Add funds to a user's bank balance.
- 💸 **Withdraw Money** — Withdraw funds with insufficient-balance validation.
- 📊 **Check Balance** — View the current account balance.
- 🧾 **Transaction History** — View recorded deposits and withdrawals with timestamps.
- 🔄 **User Switching / Logout** — Log out and authenticate as another user.
- 🗄️ **MongoDB Persistence** — Account and transaction data remain stored in MongoDB.
- ⚠️ **Input Validation** — Handles invalid menu choices, amounts, empty usernames, and invalid numeric input.
- 🔌 **Database Connection Check** — Pings MongoDB when starting the application to verify connectivity.

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| **Python** | Application logic and object-oriented programming |
| **MongoDB** | NoSQL database for users, balances, and transactions |
| **PyMongo** | Python driver used to connect and interact with MongoDB |
| **SHA-256 / hashlib** | Password hashing |
| **datetime** | Transaction and account timestamps |
| **sys** | Program exit and system-level handling |

## 📚 Python Libraries / Modules Used

### 1. `pymongo`
Used to connect Python with MongoDB and perform database operations.

Important APIs used:
- `pymongo.MongoClient()` — Creates a MongoDB client connection.
- `client[DB_NAME]` — Selects the database.
- `db[COLLECTION_NAME]` — Selects a collection.
- `find_one()` — Retrieves a single user/account document.
- `insert_one()` — Creates a new user document.
- `update_one()` — Updates account data and transactions.
- `$inc` — Increases or decreases the account balance.
- `$push` — Adds a transaction to the transaction array.
- `client.admin.command('ping')` — Checks whether MongoDB is reachable.

### 2. `hashlib`
Used for password hashing.

- `hashlib.sha256()` — Creates a SHA-256 hash.
- `.encode('utf-8')` — Converts the password string to bytes.
- `.hexdigest()` — Converts the hash into a hexadecimal string for storage/comparison.

### 3. `datetime`
Used to generate timestamps for transactions and account creation.

- `datetime.now()` — Gets the current local date and time.
- `.strftime()` — Formats transaction timestamps.
- `.isoformat()` — Stores the account creation timestamp in ISO format.

### 4. `sys`
Used for controlled program termination when required dependencies or MongoDB connectivity are unavailable.

- `sys.exit(1)` — Exits the program with an error status.

## 🧩 Methods & Functions Used

### 🔑 Authentication & Utility Functions

| Function | Purpose |
|---|---|
| `hash_password(password)` | Creates a SHA-256 hash of a password. |
| `authenticate_user()` | Handles login, registration, password verification, and legacy password setup. |
| `main()` | Starts the application and controls the main menu loop. |

### 🏦 `BankAccount` Class

| Method | Purpose |
|---|---|
| `__init__(username)` | Initializes a bank account object for a username. |
| `get_user_data()` | Retrieves the user's account document from MongoDB. |
| `deposit(amount)` | Validates and deposits money, updates balance, and records the transaction. |
| `withdraw(amount)` | Validates withdrawal, checks balance, updates MongoDB, and records the transaction. |
| `show_balance()` | Displays the current account balance. |
| `show_history()` | Displays the user's complete transaction history. |

## 🗃️ Database Structure

The main application connects to a local MongoDB server using:

```text
MongoDB Server
└── bank_db
    └── users
        ├── username
        ├── password
        ├── balance
        ├── transactions[]
        │   ├── type
        │   ├── amount
        │   └── date
        └── created_at
```

### Example User Document

```json
{
  "username": "example_user",
  "password": "<sha256_hash>",
  "balance": 5000.0,
  "transactions": [
    {
      "type": "deposit",
      "amount": 5000,
      "date": "2026-09-12 20:00:00"
    }
  ],
  "created_at": "2026-09-12T20:00:00"
}
```

## 🔄 Application Workflow

```text
                ┌──────────────────────┐
                │     Start Program    │
                └──────────┬───────────┘
                           ↓
                ┌──────────────────────┐
                │ Connect to MongoDB   │
                └──────────┬───────────┘
                           ↓
                ┌──────────────────────┐
                │ Login / Registration │
                └──────────┬───────────┘
                           ↓
                ┌──────────────────────┐
                │    Banking Menu      │
                └──────────┬───────────┘
                           ↓
       ┌──────────┬────────┼─────────┬────────────┐
       ↓          ↓        ↓         ↓            ↓
    Deposit    Withdraw  Balance   History     Logout
       │          │        │         │            │
       └──────────┴────────┴─────────┴────────────┘
                           ↓
                    MongoDB Update
                           ↓
                    Continue / Exit
```

## 💻 Available Operations

After successful authentication, the application provides the following menu:

```text
1. Deposit in bank account
2. Withdraw money
3. Show the bank balance
4. Show transaction history
5. Switch user / Logout
6. Exit
```

## 🚀 Getting Started

### Prerequisites

Make sure you have:

- Python 3.x installed
- MongoDB installed and running locally
- `pip` available in your terminal

### 1. Clone the Repository

```bash
git clone https://github.com/adeelkhanav786/Banking-management-System.git
cd Banking-management-System
```

### 2. Install PyMongo

```bash
pip install pymongo
```

### 3. Start MongoDB

The current application expects MongoDB at:

```text
mongodb://localhost:27017/
```

Make sure your local MongoDB service is running before starting the application.

### 4. Run the Application

```bash
python bank.py
```

## 🔐 Security Note

The project hashes passwords with SHA-256 rather than storing them as plain text. This is a useful demonstration of password hashing, but **plain SHA-256 is not recommended for production password storage**. A production banking application should use a password-specific password-hashing algorithm such as **Argon2id, bcrypt, or scrypt**, together with appropriate security controls.

Also, the current project uses a local MongoDB connection string directly in the source code. For a production system, database credentials and connection strings should be stored in environment variables or a secure secrets manager.

> ⚠️ **Important:** This project is an educational/demo banking application and should not be used to process real financial transactions without substantial additional security, auditing, authorization, validation, and infrastructure controls.

## 📁 Project Structure

```text
Banking-management-System/
│
├── bank.py              # Main banking management application
├── bb.py                # Earlier/prototype banking implementation
├── list.py              # Supporting file
├── README.md            # Project documentation
├── .bsp/                # Scala tooling metadata
├── .scala-build/        # Scala build/IDE metadata
└── __pycache__/         # Python generated bytecode cache
```

> **Recommended cleanup:** Generated folders such as `__pycache__`, `.scala-build`, and `.bsp` generally should not be committed to a Python project. Adding them to `.gitignore` will keep the repository cleaner.

## 🎯 Learning Objectives

This project demonstrates practical use of:

- Python classes and objects
- Constructors and instance attributes
- Functions and methods
- Conditional statements and loops
- Exception handling with `try/except`
- User input validation
- MongoDB database connectivity
- MongoDB CRUD operations
- MongoDB update operators such as `$inc` and `$push`
- Password hashing
- Date/time handling
- Persistent transaction records
- Command-line application design

## 🔮 Future Improvements

Potential improvements for a more production-oriented version include:

- 👤 Role-based access control for customers and administrators
- 🔐 Argon2id/bcrypt/scrypt password hashing with stronger authentication controls
- 🔑 Secure environment-based configuration for MongoDB credentials
- 💳 Account numbers and multiple account types
- 📋 Transfer money between accounts
- 🧾 Downloadable account statements
- 🔎 Transaction search and filtering
- 📈 Admin dashboard and reporting
- 🛡️ Audit logs and stronger authorization
- 🌐 REST API or web interface
- 🧪 Automated unit and integration tests
- 🐳 Docker-based deployment
- ☁️ MongoDB Atlas support

## 📌 Project Highlights

**Python + MongoDB + OOP + Authentication + Banking Operations + Transaction Tracking**

A compact project that combines core Python programming concepts with real database persistence in a practical banking scenario.

## 👨‍💻 Author

**Adeel Khan**

GitHub: [@adeelkhanav786](https://github.com/adeelkhanav786)

## ⭐ Support

If you find this project useful for learning Python and MongoDB, consider giving the repository a ⭐ on GitHub.

---

<p align="center">
  <b>🏦 Banking Management System</b><br>
  Built with Python 🐍 and MongoDB 🍃
</p>

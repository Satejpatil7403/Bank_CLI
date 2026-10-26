"""
🏦 Bank Management System - Complete OOP Concepts in Python
Demonstrates: Classes, Objects, Inheritance, Polymorphism, Encapsulation,
Abstraction, Composition, Method Overriding, Class/Static Methods, and more!
WITH INTERACTIVE USER INPUT
"""

from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Optional
import random
import time


# =============================================================================
# 1. ABSTRACTION - Abstract Base Class
# =============================================================================
class Account(ABC):
    """
    Abstract base class for all account types
    Demonstrates: Abstraction, Encapsulation
    """

    # Class variable (shared by all instances)
    _total_accounts = 0

    def __init__(self, account_number: str, account_holder: str, initial_balance: float = 0):
        # Private attributes (Encapsulation with name mangling)
        self.__account_number = account_number
        self.__account_holder = account_holder
        self.__balance = initial_balance
        self.__transactions = []
        self.__is_active = True
        Account._total_accounts += 1
        self._add_transaction("Account opened", initial_balance)

    # Getter methods (Encapsulation)
    def get_account_number(self) -> str:
        return self.__account_number

    def get_account_holder(self) -> str:
        return self.__account_holder

    def get_balance(self) -> float:
        return self.__balance

    def is_account_active(self) -> bool:
        return self.__is_active

    # Protected method (can be used by subclasses)
    def _add_transaction(self, description: str, amount: float):
        """Record a transaction"""
        transaction = {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "description": description,
            "amount": amount,
            "balance": self.__balance
        }
        self.__transactions.append(transaction)

    def deposit(self, amount: float) -> bool:
        """Deposit money into account"""
        if amount <= 0:
            print("❌ Deposit amount must be positive!")
            return False

        self.__balance += amount
        self._add_transaction(f"Deposit", amount)
        print(f"✅ Deposited ${amount:.2f}. New balance: ${self.__balance:.2f}")
        return True

    # Abstract method (must be implemented by subclasses)
    @abstractmethod
    def withdraw(self, amount: float) -> bool:
        """Abstract method for withdrawal - each account type implements differently"""
        pass

    # Abstract method for account-specific fees
    @abstractmethod
    def calculate_fees(self) -> float:
        """Calculate monthly fees for the account"""
        pass

    def get_transaction_history(self) -> List[dict]:
        """Get all transactions"""
        return self.__transactions.copy()

    def close_account(self):
        """Close the account"""
        self.__is_active = False
        print(f"🔒 Account {self.__account_number} has been closed.")

    # Class method (operates on class, not instance)
    @classmethod
    def get_total_accounts(cls) -> int:
        """Get total number of accounts created"""
        return cls._total_accounts

    # Static method (doesn't access instance or class)
    @staticmethod
    def generate_account_number(prefix: str) -> str:
        """Generate a random account number"""
        return f"{prefix}{random.randint(10000, 99999)}"

    # String representation (Polymorphism)
    def __str__(self) -> str:
        status = "Active" if self.__is_active else "Closed"
        return f"Account: {self.__account_number} | Holder: {self.__account_holder} | Balance: ${self.__balance:.2f} | Status: {status}"

    # Operator overloading
    def __eq__(self, other) -> bool:
        """Check if two accounts are equal"""
        if isinstance(other, Account):
            return self.__account_number == other.__account_number
        return False


# =============================================================================
# 2. INHERITANCE - Subclasses inheriting from Account
# =============================================================================
class SavingsAccount(Account):
    """
    Savings Account with interest rate
    Demonstrates: Inheritance, Method Overriding
    """

    def __init__(self, account_number: str, account_holder: str, initial_balance: float = 0,
                 interest_rate: float = 0.02):
        super().__init__(account_number, account_holder, initial_balance)
        self.interest_rate = interest_rate
        self.withdrawal_limit = 3
        self.withdrawals_this_month = 0

    # Method overriding
    def withdraw(self, amount: float) -> bool:
        """Withdraw with monthly limit"""
        if not self.is_account_active():
            print("❌ Account is closed!")
            return False

        if amount <= 0:
            print("❌ Withdrawal amount must be positive!")
            return False

        if self.withdrawals_this_month >= self.withdrawal_limit:
            print(f"❌ Monthly withdrawal limit ({self.withdrawal_limit}) reached!")
            return False

        if amount > self.get_balance():
            print("❌ Insufficient funds!")
            return False

        self._Account__balance -= amount  # Access private attribute from parent
        self.withdrawals_this_month += 1
        self._add_transaction(f"Withdrawal", -amount)
        print(f"✅ Withdrew ${amount:.2f}. New balance: ${self.get_balance():.2f}")
        print(f"   Withdrawals left this month: {self.withdrawal_limit - self.withdrawals_this_month}")
        return True

    def calculate_fees(self) -> float:
        """No monthly fees for savings account"""
        return 0.0

    def add_interest(self):
        """Add monthly interest"""
        interest = self.get_balance() * self.interest_rate
        self._Account__balance += interest
        self._add_transaction(f"Interest ({self.interest_rate * 100}%)", interest)
        print(f"💰 Interest added: ${interest:.2f}. New balance: ${self.get_balance():.2f}")

    def __str__(self) -> str:
        return super().__str__() + f" | Type: Savings | Interest Rate: {self.interest_rate * 100}%"


class CheckingAccount(Account):
    """
    Checking Account with overdraft protection
    Demonstrates: Inheritance, Method Overriding
    """

    def __init__(self, account_number: str, account_holder: str, initial_balance: float = 0,
                 overdraft_limit: float = 500):
        super().__init__(account_number, account_holder, initial_balance)
        self.overdraft_limit = overdraft_limit
        self.monthly_fee = 10.0

    # Method overriding
    def withdraw(self, amount: float) -> bool:
        """Withdraw with overdraft protection"""
        if not self.is_account_active():
            print("❌ Account is closed!")
            return False

        if amount <= 0:
            print("❌ Withdrawal amount must be positive!")
            return False

        available_balance = self.get_balance() + self.overdraft_limit

        if amount > available_balance:
            print(f"❌ Insufficient funds! Available (with overdraft): ${available_balance:.2f}")
            return False

        self._Account__balance -= amount
        self._add_transaction(f"Withdrawal", -amount)

        if self.get_balance() < 0:
            print(f"⚠️  Withdrew ${amount:.2f}. Balance: ${self.get_balance():.2f} (Using overdraft)")
        else:
            print(f"✅ Withdrew ${amount:.2f}. New balance: ${self.get_balance():.2f}")
        return True

    def calculate_fees(self) -> float:
        """Calculate monthly maintenance fee"""
        return self.monthly_fee

    def charge_monthly_fee(self):
        """Charge monthly maintenance fee"""
        self._Account__balance -= self.monthly_fee
        self._add_transaction(f"Monthly fee", -self.monthly_fee)
        print(f"💳 Monthly fee charged: ${self.monthly_fee:.2f}")

    def __str__(self) -> str:
        return super().__str__() + f" | Type: Checking | Overdraft Limit: ${self.overdraft_limit:.2f}"


class BusinessAccount(Account):
    """
    Business Account with transaction fees
    Demonstrates: Inheritance, Method Overriding
    """

    def __init__(self, account_number: str, business_name: str, initial_balance: float = 0):
        super().__init__(account_number, business_name, initial_balance)
        self.transaction_fee = 2.0
        self.free_transactions = 10
        self.transactions_this_month = 0

    def withdraw(self, amount: float) -> bool:
        """Withdraw with transaction fees"""
        if not self.is_account_active():
            print("❌ Account is closed!")
            return False

        if amount <= 0:
            print("❌ Withdrawal amount must be positive!")
            return False

        # Calculate fee
        fee = 0 if self.transactions_this_month < self.free_transactions else self.transaction_fee
        total_amount = amount + fee

        if total_amount > self.get_balance():
            print(f"❌ Insufficient funds! Need ${total_amount:.2f} (amount + fee)")
            return False

        self._Account__balance -= total_amount
        self.transactions_this_month += 1
        self._add_transaction(f"Withdrawal (Fee: ${fee:.2f})", -total_amount)

        if fee > 0:
            print(f"✅ Withdrew ${amount:.2f} (+ ${fee:.2f} fee). Balance: ${self.get_balance():.2f}")
        else:
            print(f"✅ Withdrew ${amount:.2f}. Balance: ${self.get_balance():.2f}")
        return True

    def calculate_fees(self) -> float:
        """Calculate transaction fees"""
        if self.transactions_this_month <= self.free_transactions:
            return 0.0
        return (self.transactions_this_month - self.free_transactions) * self.transaction_fee

    def __str__(self) -> str:
        return super().__str__() + f" | Type: Business | Free Transactions: {self.free_transactions}/month"


# =============================================================================
# 3. COMPOSITION - Customer has multiple accounts
# =============================================================================
class Customer:
    """
    Customer class that owns multiple accounts
    Demonstrates: Composition, Aggregation
    """

    def __init__(self, customer_id: str, name: str, email: str):
        self.customer_id = customer_id
        self.name = name
        self.email = email
        self.__accounts: List[Account] = []  # Composition - customer HAS accounts
        self.created_date = datetime.now()

    def add_account(self, account: Account):
        """Add an account to customer"""
        self.__accounts.append(account)
        print(f"✅ Account {account.get_account_number()} added to {self.name}")

    def get_accounts(self) -> List[Account]:
        """Get all customer accounts"""
        return self.__accounts.copy()

    def get_total_balance(self) -> float:
        """Get total balance across all accounts"""
        return sum(account.get_balance() for account in self.__accounts if account.is_account_active())

    def find_account(self, account_number: str) -> Optional[Account]:
        """Find an account by account number"""
        for account in self.__accounts:
            if account.get_account_number() == account_number:
                return account
        return None

    def __str__(self) -> str:
        return f"Customer: {self.name} | ID: {self.customer_id} | Accounts: {len(self.__accounts)} | Total Balance: ${self.get_total_balance():.2f}"


# =============================================================================
# 4. COMPOSITION - Bank manages customers and accounts
# =============================================================================
class Bank:
    """
    Bank class - main system
    Demonstrates: Composition, Class Methods, Static Methods
    """

    def __init__(self, bank_name: str):
        self.bank_name = bank_name
        self.__customers: List[Customer] = []
        self.__all_accounts: List[Account] = []

    def create_customer(self, name: str, email: str) -> Customer:
        """Create a new customer"""
        customer_id = f"CUST{random.randint(1000, 9999)}"
        customer = Customer(customer_id, name, email)
        self.__customers.append(customer)
        print(f"✅ Customer created: {name} (ID: {customer_id})")
        return customer

    def find_customer(self, customer_id: str) -> Optional[Customer]:
        """Find customer by ID"""
        for customer in self.__customers:
            if customer.customer_id == customer_id:
                return customer
        return None

    def open_savings_account(self, customer: Customer, initial_balance: float = 0) -> SavingsAccount:
        """Open a savings account for customer"""
        account_number = Account.generate_account_number("SAV")
        account = SavingsAccount(account_number, customer.name, initial_balance)
        customer.add_account(account)
        self.__all_accounts.append(account)
        return account

    def open_checking_account(self, customer: Customer, initial_balance: float = 0) -> CheckingAccount:
        """Open a checking account for customer"""
        account_number = Account.generate_account_number("CHK")
        account = CheckingAccount(account_number, customer.name, initial_balance)
        customer.add_account(account)
        self.__all_accounts.append(account)
        return account

    def open_business_account(self, customer: Customer, initial_balance: float = 0) -> BusinessAccount:
        """Open a business account for customer"""
        account_number = Account.generate_account_number("BUS")
        account = BusinessAccount(account_number, customer.name, initial_balance)
        customer.add_account(account)
        self.__all_accounts.append(account)
        return account

    def transfer_money(self, from_account: Account, to_account: Account, amount: float) -> bool:
        """Transfer money between accounts"""
        print(f"\n💸 Transferring ${amount:.2f}...")

        if from_account.withdraw(amount):
            to_account.deposit(amount)
            print(f"✅ Transfer completed!")
            return True
        else:
            print(f"❌ Transfer failed!")
            return False

    def get_all_customers(self) -> List[Customer]:
        """Get all customers"""
        return self.__customers.copy()

    def get_bank_summary(self):
        """Print bank summary"""
        print(f"\n{'=' * 60}")
        print(f"🏦 {self.bank_name} - Summary Report")
        print(f"{'=' * 60}")
        print(f"Total Customers: {len(self.__customers)}")
        print(f"Total Accounts: {Account.get_total_accounts()}")
        print(f"Active Accounts: {sum(1 for acc in self.__all_accounts if acc.is_account_active())}")

        total_deposits = sum(acc.get_balance() for acc in self.__all_accounts if acc.is_account_active())
        print(f"Total Deposits: ${total_deposits:.2f}")
        print(f"{'=' * 60}")


# =============================================================================
# 5. INTERACTIVE USER INTERFACE
# =============================================================================
class BankingSystem:
    """Interactive banking system with user input"""

    def __init__(self):
        self.bank = Bank("Python National Bank")
        self.current_customer: Optional[Customer] = None
        self.running = True

    def clear_screen(self):
        """Clear screen effect"""
        print("\n" * 2)

    def print_header(self, title: str):
        """Print formatted header"""
        print("\n" + "=" * 60)
        print(f"  {title}")
        print("=" * 60)

    def get_float_input(self, prompt: str) -> Optional[float]:
        """Get and validate float input"""
        try:
            value = float(input(prompt))
            return value
        except ValueError:
            print("❌ Invalid amount! Please enter a number.")
            return None

    def get_int_input(self, prompt: str) -> Optional[int]:
        """Get and validate integer input"""
        try:
            value = int(input(prompt))
            return value
        except ValueError:
            print("❌ Invalid input! Please enter a number.")
            return None

    def pause(self):
        """Pause for user to read"""
        input("\n⏎ Press Enter to continue...")

    # Main Menu
    def main_menu(self):
        """Display main menu"""
        while self.running:
            self.print_header("🏦 PYTHON NATIONAL BANK - MAIN MENU")
            print("1. 👤 Create New Customer")
            print("2. 🔑 Login as Existing Customer")
            print("3. 📊 View Bank Summary")
            print("4. 🚪 Exit")
            print("=" * 60)

            choice = input("Select option (1-4): ").strip()

            if choice == "1":
                self.create_new_customer()
            elif choice == "2":
                self.login_customer()
            elif choice == "3":
                self.bank.get_bank_summary()
                self.pause()
            elif choice == "4":
                print("\n👋 Thank you for banking with us! Goodbye!")
                self.running = False
            else:
                print("❌ Invalid option! Please try again.")
                time.sleep(1)

    # Customer Management
    def create_new_customer(self):
        """Create a new customer"""
        self.print_header("👤 CREATE NEW CUSTOMER")

        name = input("Enter your full name: ").strip()
        if not name:
            print("❌ Name cannot be empty!")
            self.pause()
            return

        email = input("Enter your email: ").strip()
        if not email:
            print("❌ Email cannot be empty!")
            self.pause()
            return

        customer = self.bank.create_customer(name, email)
        print(f"\n✅ Welcome, {name}! Your Customer ID: {customer.customer_id}")
        print("💡 Please remember your Customer ID for future logins.")

        self.current_customer = customer
        self.pause()
        self.customer_menu()

    def login_customer(self):
        """Login as existing customer"""
        self.print_header("🔑 CUSTOMER LOGIN")

        # Show all customers
        customers = self.bank.get_all_customers()
        if not customers:
            print("❌ No customers found! Please create a new customer first.")
            self.pause()
            return

        print("\n📋 Available Customers:")
        for i, customer in enumerate(customers, 1):
            print(f"{i}. {customer.name} (ID: {customer.customer_id})")

        customer_id = input("\nEnter your Customer ID: ").strip()

        customer = self.bank.find_customer(customer_id)
        if customer:
            self.current_customer = customer
            print(f"\n✅ Welcome back, {customer.name}!")
            self.pause()
            self.customer_menu()
        else:
            print("❌ Customer ID not found!")
            self.pause()

    # Customer Menu
    def customer_menu(self):
        """Display customer menu"""
        while self.current_customer:
            self.print_header(f"👤 {self.current_customer.name}'s Account")
            print("1. 💳 Open New Account")
            print("2. 💰 Deposit Money")
            print("3. 💸 Withdraw Money")
            print("4. 🔄 Transfer Money")
            print("5. 📊 View All Accounts")
            print("6. 📜 View Transaction History")
            print("7. ➕ Add Interest (Savings Only)")
            print("8. 🔙 Logout")
            print("=" * 60)

            choice = input("Select option (1-8): ").strip()

            if choice == "1":
                self.open_account_menu()
            elif choice == "2":
                self.deposit_money()
            elif choice == "3":
                self.withdraw_money()
            elif choice == "4":
                self.transfer_money()
            elif choice == "5":
                self.view_accounts()
            elif choice == "6":
                self.view_transaction_history()
            elif choice == "7":
                self.add_interest()
            elif choice == "8":
                print(f"\n👋 Goodbye, {self.current_customer.name}!")
                self.current_customer = None
                self.pause()
            else:
                print("❌ Invalid option! Please try again.")
                time.sleep(1)

    # Account Operations
    def open_account_menu(self):
        """Menu for opening new account"""
        self.print_header("💳 OPEN NEW ACCOUNT")
        print("1. 💰 Savings Account (2% interest, 3 withdrawals/month)")
        print("2. 💳 Checking Account (Overdraft protection, $10/month fee)")
        print("3. 🏢 Business Account (10 free transactions/month)")
        print("4. 🔙 Back")

        choice = input("\nSelect account type (1-4): ").strip()

        if choice == "4":
            return

        initial_balance = self.get_float_input("Enter initial deposit amount: $")
        if initial_balance is None or initial_balance < 0:
            print("❌ Invalid amount!")
            self.pause()
            return

        if choice == "1":
            account = self.bank.open_savings_account(self.current_customer, initial_balance)
        elif choice == "2":
            account = self.bank.open_checking_account(self.current_customer, initial_balance)
        elif choice == "3":
            account = self.bank.open_business_account(self.current_customer, initial_balance)
        else:
            print("❌ Invalid choice!")
            self.pause()
            return

        print(f"\n{account}")
        self.pause()

    def select_account(self) -> Optional[Account]:
        """Helper to select an account"""
        accounts = self.current_customer.get_accounts()

        if not accounts:
            print("❌ You don't have any accounts! Please open an account first.")
            return None

        print("\n📋 Your Accounts:")
        for i, account in enumerate(accounts, 1):
            print(f"{i}. {account}")

        choice = self.get_int_input("\nSelect account number: ")
        if choice and 1 <= choice <= len(accounts):
            return accounts[choice - 1]

        print("❌ Invalid selection!")
        return None

    def deposit_money(self):
        """Deposit money into account"""
        self.print_header("💰 DEPOSIT MONEY")

        account = self.select_account()
        if not account:
            self.pause()
            return

        amount = self.get_float_input("Enter deposit amount: $")
        if amount:
            account.deposit(amount)

        self.pause()

    def withdraw_money(self):
        """Withdraw money from account"""
        self.print_header("💸 WITHDRAW MONEY")

        account = self.select_account()
        if not account:
            self.pause()
            return

        amount = self.get_float_input("Enter withdrawal amount: $")
        if amount:
            account.withdraw(amount)

        self.pause()

    def transfer_money(self):
        """Transfer money between accounts"""
        self.print_header("🔄 TRANSFER MONEY")

        print("\n📤 FROM Account:")
        from_account = self.select_account()
        if not from_account:
            self.pause()
            return

        print("\n📥 TO Account:")
        to_account = self.select_account()
        if not to_account:
            self.pause()
            return

        if from_account == to_account:
            print("❌ Cannot transfer to the same account!")
            self.pause()
            return

        amount = self.get_float_input("Enter transfer amount: $")
        if amount:
            self.bank.transfer_money(from_account, to_account, amount)

        self.pause()

    def view_accounts(self):
        """View all customer accounts"""
        self.print_header("📊 YOUR ACCOUNTS")

        accounts = self.current_customer.get_accounts()
        if not accounts:
            print("❌ You don't have any accounts!")
        else:
            for account in accounts:
                print(f"\n{account}")
            print(f"\n💰 Total Balance: ${self.current_customer.get_total_balance():.2f}")

        self.pause()

    def view_transaction_history(self):
        """View transaction history"""
        self.print_header("📜 TRANSACTION HISTORY")

        account = self.select_account()
        if not account:
            self.pause()
            return

        transactions = account.get_transaction_history()
        print(f"\n📊 Transaction History for {account.get_account_number()}")
        print("-" * 80)

        for trans in transactions:
            print(
                f"{trans['date']} | {trans['description']:30} | ${trans['amount']:8.2f} | Balance: ${trans['balance']:.2f}")

        self.pause()

    def add_interest(self):
        """Add interest to savings account"""
        self.print_header("➕ ADD INTEREST")

        account = self.select_account()
        if not account:
            self.pause()
            return

        if isinstance(account, SavingsAccount):
            account.add_interest()
        else:
            print("❌ Only Savings Accounts earn interest!")

        self.pause()

    def run(self):
        """Start the banking system"""
        print("\n" + "=" * 60)
        print("🏦 WELCOME TO PYTHON NATIONAL BANK")
        print("   Complete Banking System with OOP")
        print("=" * 60)
        time.sleep(1)
        self.main_menu()


# =============================================================================
# 6. MAIN PROGRAM
# =============================================================================
def main():
    """Main function to run the interactive banking system"""
    system = BankingSystem()
    system.run()


if __name__ == "__main__":
    main()
import json
import os

DATA_FILE = "bank_accounts.json"

def load_data():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'w') as file:
            json.dump({}, file)
    with open(DATA_FILE, 'r') as file:
        return json.load(file)

def save_data(data):
    with open(DATA_FILE, 'w') as file:
        json.dump(data, file, indent=4)

def create_account():
    data = load_data()
    username = input("Enter a username: ").strip()
    password = input("Enter a password: ").strip()
    data[username] = {
        "password": password,
        "balance": 0.0,
        "transactions": []
    }

    save_data(data)
    print(f"Account created successfully!")

def login():
    data = load_data()
    username = input("Enter your username: ").strip()
    password = input("Enter your password: ").strip()

    if username in data and data[username]['password'] == password:
        print(f"\nWelcome, {username}!")
        return username
    else:
        print("\nUser not found. Please create an account first.")
        return None

def check_balance(username):
    data = load_data()
    print(f"\nYour balance is: {data[username]['balance']:.2f}")

def deposit(username):
    data = load_data()
    amount = float(input("\nInput amount to deposit: "))

    if amount <= 0:
        print("Can't deposit negative amount.")
        return

    data[username]['balance'] += amount
    data[username]['transactions'].append(f"Deposited {amount:.2f}")
    save_data(data)
    print(f"Successfully deposited {amount:.2f}. New balance is: {data[username]['balance']:.2f}")

def withdraw(username):
    data = load_data()
    amount = float(input("\nEnter amount to withdraw: "))

    if amount <= 0:
        print("Amount must be greater than 0.")
        return

    if data[username]['balance'] < amount:
        print("Insufficient balance.")
        return

    data[username]['balance'] -= amount
    data[username]['transactions'].append(f"Withdrew {amount:.2f}")
    save_data(data)
    print(f"Successfully withdrew {amount:.2f}. Current balance: {data[username]['balance']:.2f}")

def transfer(username):
    data = load_data()
    recipient = input("\nEnter the recipient's username: ").strip()

    if recipient not in data:
        print("Recipient account not found.")
        return

    amount = float(input("Enter amount to transfer: "))

    if amount <= 0:
        print("Unable to input a negative number.")
        return

    if data[username]['balance'] < amount:
        print("Insufficient balance.")
        return

    data[username]['balance'] -= amount
    data[recipient]['balance'] += amount

    data[username]['transactions'].append(f"Transferred {amount:.2f} to {recipient}")
    data[recipient]['transactions'].append(f"Received {amount:.2f} from {username}")

    save_data(data)
    print(f"Successfully transferred {amount:.2f} to {recipient}.")

def view_transactions(username):
    data = load_data()
    print("\nTransaction History:\n")
    for transaction in data[username]['transactions']:
        print(transaction)

def main():
    while True:
        print("\nWelcome to your Banking System, please select one of the options: ")
        print("1. Create Account")
        print("2. Login")
        print("3. Exit")
        choice = input("\nChoose an option: ").strip()

        if choice == '1':
            create_account()
        elif choice == '2':
            username = login()
            if username:
                while True:
                    print("\n1. Check Balance")
                    print("2. Deposit")
                    print("3. Withdraw")
                    print("4. Transfer")
                    print("5. View Transactions")
                    print("6. Logout")
                    action = input("Choose an option: ").strip()

                    if action == '1':
                        check_balance(username)
                    elif action == '2':
                        deposit(username)
                    elif action == '3':
                        withdraw(username)
                    elif action == '4':
                        transfer(username)
                    elif action == '5':
                        view_transactions(username)
                    elif action == '6':
                        print("Logged out.")
                        break
                    else:
                        print("Invalid choice. Please try again.")
        elif choice == '3':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()

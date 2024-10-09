# Function to import user data from a file and create a user accounts dictionary
def import_and_create_users(filename):
    users = {}
    try:
        with open(filename, 'r') as f:
            lines = f.readlines()

        for line in lines:
            line = line.strip()
            if line:  # Only process non-empty lines
                parts = line.split(' - ')
                if len(parts) == 2:  # Ensure the line has a name and password
                    name, password = parts
                    users[name.strip()] = password.strip()
    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")
    return users

# Function to import bank data from a file and create a bank accounts dictionary
def import_and_create_bank(filename):
    bank = {}
    try:
        with open(filename, 'r') as f:
            lines = f.readlines()

        for line in lines:
            line = line.strip()
            if line:  # Only process non-empty lines
                parts = line.split(':')
                if len(parts) == 2:  # Ensure the line has a name and deposit amount
                    name = parts[0].strip()
                    deposit_amount = parts[1].strip()
                    try:
                        deposit_value = float(deposit_amount)
                        bank[name] = bank.get(name, 0) + deposit_value
                    except ValueError:
                        print(f"Warning: Invalid deposit amount for {name}: '{deposit_amount}'")
    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")
    return bank

# Function to sign up a new user
def sign_up(users):
    name = input("Enter a username for sign-up: ")
    password = input("Enter a password: ")
    if name in users:
        print("User already exists.")
    else:
        users[name] = password
        print("User signed up successfully.")

# Function to log in a user
def log_in(users):
    name = input("Enter your username: ")
    password = input("Enter your password: ")
    if name in users and users[name] == password:
        print("Login successful.")
        return name
    else:
        print("Invalid username or password.")
        return None

# Function to change user password
def change_password(users, name):
    old_password = input("Enter your current password: ")
    if name in users and users[name] == old_password:
        new_password = input("Enter your new password: ")
        users[name] = new_password
        print("Password changed successfully.")
    else:
        print("Invalid username or password.")

# Function to delete a user account
def delete_account(users, name):
    password = input("Enter your password to confirm deletion: ")
    if name in users and users[name] == password:
        del users[name]
        print("Account deleted successfully.")
    else:
        print("Invalid username or password.")

# Function to update bank account balance
def update_balance(bank, name):
    amount = float(input("Enter the amount to update (positive to deposit, negative to withdraw): "))
    if name in bank:
        bank[name] += amount
        print(f"Updated balance for {name} is {bank[name]:.2f}.")
    else:
        print("User not found.")

# Function to transfer money between accounts
def transfer_money(bank, from_user):
    to_user = input("Enter the username to transfer money to: ")
    amount = float(input("Enter the amount to transfer: "))
    
    if from_user not in bank or to_user not in bank:
        print("Transfer failed: One or both users not found.")
        return
    
    if bank[from_user] < amount:
        print("Transfer failed: Insufficient funds.")
        return
    
    bank[from_user] -= amount
    bank[to_user] += amount
    print(f"Transferred {amount:.2f} from {from_user} to {to_user}.")

# Main function to run the banking system
def main():
    users = import_and_create_users("users.txt")
    bank = import_and_create_bank("bank.txt")

    while True:
        print("\n--- Welcome to the Online Banking System ---")
        print("1. Sign Up")
        print("2. Log In")
        print("3. Exit")
        choice = input("Choose an option (1-3): ")

        if choice == '1':
            sign_up(users)
        elif choice == '2':
            logged_in_user = log_in(users)
            if logged_in_user:
                while True:
                    print("\n--- User Menu ---")
                    print("1. Change Password")
                    print("2. Delete Account")
                    print("3. Update Balance")
                    print("4. Transfer Money")
                    print("5. Logout")
                    user_choice = input("Choose an option (1-5): ")

                    if user_choice == '1':
                        change_password(users, logged_in_user)
                    elif user_choice == '2':
                        delete_account(users, logged_in_user)
                        break  # Log out after deletion
                    elif user_choice == '3':
                        update_balance(bank, logged_in_user)
                    elif user_choice == '4':
                        transfer_money(bank, logged_in_user)
                    elif user_choice == '5':
                        print("Logged out.")
                        break
                    else:
                        print("Invalid option.")
        elif choice == '3':
            print("Exiting the system.")
            break
        else:
            print("Invalid option.")

if __name__ == "__main__":
    main()

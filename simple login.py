# Author: Gelos
# Date: 2024-06-27
# Purpose: Simple login program with options for registration, password management, and account viewing

import random
import string
import time

# Global variables
User_data = {}
max_attempts = 3
ACCOUNTS_FILE = 'accounts.txt'

def save_accounts():
    """Saves accounts to accounts.txt file."""
    with open(ACCOUNTS_FILE, 'w') as file:
        for username, details in User_data.items():
            file.write(f"{username}:{details['password']}\n")

def load_accounts():
    """Loads accounts from accounts.txt file."""
    try:
        with open(ACCOUNTS_FILE, 'r') as file:
            for line in file:
                if ':' in line:
                    username, password = line.strip().split(':')
                    User_data[username] = {'password': password}
    except FileNotFoundError:
        pass

def generate_password(length=8, use_numbers=True, use_symbols=True, use_letters=True):
    """Generates a random password based on the chosen character types."""
    characters = ''
    if use_numbers:
        characters += string.digits
    if use_symbols:
        characters += string.punctuation
    if use_letters:
        characters += string.ascii_letters

    if not characters:
        characters = string.ascii_letters  # Default to letters if no option is selected

    # Ensure the length does not exceed 12
    length = min(length, 12)

    return ''.join(random.choice(characters) for _ in range(length))

def get_yes_no_input(prompt):
    """Handles input for 'Y' or 'N' with loop for invalid responses."""
    while True:
        choice = input(prompt).strip().upper()
        if choice == 'Y' or choice == 'N':
            return choice
        else:
            print("Invalid choice. Please enter 'Y' for Yes or 'N' for No.")

def register_user():
    """Registers a new user."""
    username = input("Enter new username: ").strip()
    if username in User_data:
        print("Username already exists. Please choose a different username.")
        return

    choice = get_yes_no_input("Do you want to enter your own password? (Y/N): ")
    if choice == 'Y':
        password = input("Enter your password: ").strip()
    elif choice == 'N':
        print("Generating a password...")
        length = input("Enter desired password length (default is 8, maximum is 12): ").strip()
        length = int(length) if length.isdigit() else 8

        use_numbers = get_yes_no_input("Include numbers? (Y/N): ") == 'Y'
        use_symbols = get_yes_no_input("Include symbols? (Y/N): ") == 'Y'
        use_letters = get_yes_no_input("Include letters? (Y/N): ") == 'Y'

        password = generate_password(length, use_numbers, use_symbols, use_letters)
        print(f"Your generated password is: {password}")
    else:
        print("Invalid choice. Please select 'Y' or 'N'.")
        return

    User_data[username] = {'password': password}
    save_accounts()
    print("Registration successful.")

def view_profile(username):
    """Displays the username and password of the logged-in user."""
    if username in User_data:
        print(f"Username: {username}")
        print(f"Password: {User_data[username]['password']}")
    else:
        print("User not found.")

def login():
    """Logs in an existing user."""
    username = input("Enter username: ").strip()
    password = input("Enter password: ").strip()

    if username in User_data and User_data[username]['password'] == password:
        print("Login successful.")
        while True:
            print("\nLogged In Menu")
            print("1. View Profile")
            print("2. Exit")

            choice = input("Choose an option: ").strip().lower()

            if choice == '1':
                view_profile(username)
            elif choice == '2':
                print("Logging out...")
                time.sleep(2)
                break
            else:
                print("Invalid option. Please try again.")
    else:
        print("Invalid username or password.")

def main_menu():
    """Displays the main menu and processes user choices."""
    load_accounts()

    while True:
        print("\nMain Menu")
        print("1. Login")
        print("2. Register")
        print("3. Exit")

        choice = input("Choose an option: ").strip().lower()

        if choice == '1':
            login()
        elif choice == '2':
            register_user()
        elif choice == '3':
            print("Exiting...")
            time.sleep(2)
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main_menu()

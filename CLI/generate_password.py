""" A function to check if a password is strong, based on a set of criteria such as having at least one uppercase letter, one lowercase letter, one digit, one special character, and being at least 8 characters long.
A function to get user input for password length.
A menu option to save a generated password to a file.
A menu option to read saved passwords from a file.
This script should be quite robust and offer a range of """


import random


def generate_password(length):
    password = ""
    characters = (
        "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!@#$%^&*()_+"
    )
    for i in range(length):
        password += random.choice(characters)
    return password


def is_strong_password(password):
    if not any(char.isupper() for char in password):
        return False

    if not any(char.islower() for char in password):
        return False

    if not any(char.isdigit() for char in password):
        return False

    special_characters = "!@#$%^&*()_+"
    if not any(char in special_characters for char in password):
        return False

    if len(password) < 8:
        return False

    return True


def get_password_length():
    length = input("Enter password length (minimum 8): ")
    while not length.isdigit() or int(length) < 8:
        length = input("Invalid input. Enter password length (minimum 8): ")
    return int(length)


def print_menu():
    print("\nMenu:")
    print("1. Generate a password")
    print("2. Check if a password is strong")
    print("3. Save a password to file")
    print("4. Read a password from file")
    print("5. Exit")


def save_password_to_file(password):
    with open("passwords.txt", "a") as f:
        f.write(password + "\n")


def read_password_from_file():
    with open("passwords.txt", "r") as f:
        passwords = f.readlines()
    if len(passwords) == 0:
        print("No passwords saved.")
    else:
        for password in passwords:
            print(password.strip())


while True:
    print_menu()
    option = input("Enter an option: ")

    if option == "1":
        length = get_password_length()
        password = generate_password(length)
        print("Generated password:", password)

    elif option == "2":
        password = input("Enter password to check: ")
        if is_strong_password(password):
            print("Password is strong.")
        else:
            print("Password is weak.")

    elif option == "3":
        length = get_password_length()
        password = generate_password(length)
        save_password_to_file(password)
        print("Password saved to file.")

    elif option == "4":
        read_password_from_file()

    elif option == "5":
        print("Goodbye!")
        break

    else:
        print("Invalid option. Try again.")

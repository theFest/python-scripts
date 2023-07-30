""" This code is a basic implementation of reading the content of a file.
The program prompts the user to enter the name of a file and then tries to open the file in read mode.
If the file does not exist, it displays an error message indicating that the file was not found. If there is any other error in opening the file, it also displays an error message. If the file is successfully opened, the content of the file is displayed.
The try-except block is used to handle any exceptions that may occur when trying to open the file. If an exception occurs, the program exits.
The if __name__ == "__main__": block ensures that the main function is only executed if the code is run as the main program and not imported as a module in another program. """

import os
import sys

def main():
    file_name = input("Enter the name of the file: ")
    try:
        with open(file_name, "r") as file:
            data = file.read()
    except FileNotFoundError:
        print(f"Error: {file_name} not found")
        sys.exit()
    except:
        print(f"Error opening {file_name}")
        sys.exit()
    print(f"Content of {file_name}:")
    print(data)

if __name__ == "__main__":
    main()
    
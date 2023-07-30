""" This script is a simple password cracker for Unix-based systems.
The script uses a dictionary attack method to try and crack passwords stored in a file called passwords.txt.
Each line in the passwords.txt file should contain a username and encrypted password separated by a colon, like this: username:encrypted_password. """

#!/usr/bin/python
# -*- coding: utf-8 -*-
import crypt # the script imports the 'crypt' module which is used for password-based encryption and decryption.

# This function takes a single argument 'cryptPass' which represents an encrypted password.
# The first two characters of the 'cryptPass' string are extracted as the salt value. The salt value is used in password encryption to increase its complexity and security.
# A dictionary file 'dictionary.txt' is opened, and each line of the file is read. Each word in the file is stripped of the newline character ('\n') and encrypted using the 'crypt.crypt' function with the salt value.
# If the encrypted word matches the given 'cryptPass', the word is printed as the cracked password and the function returns. If no match is found, the function prints 'Password Not Found' and returns.
def test_pass(crypt_pass, dictionary_file):
    salt = crypt_pass[0:2]

    with open(dictionary_file, 'r') as dict_file:
        for word in dict_file.readlines():
            word = word.strip('\n')
            crypt_word = crypt.crypt(word, salt)
            if crypt_word == crypt_pass:
                print('[+] Found Password: {}'.format(word))
                return
    print('[-] Password Not Found.')
    return

# Main function of the script. It opens the file 'passwords.txt' and reads each line.
# If the line contains a colon (:), the line is split into two parts using the colon as a separator.
# The first part is the username, and the second part is the encrypted password. The encrypted password is passed to the 'testPass' function for cracking.
def main(passwords_file, dictionary_file):
    with open(passwords_file) as pass_file:
        for line in pass_file.readlines():
            if ':' in line:
                user = line.split(':')[0]
                crypt_pass = line.split(':')[1].strip(' ')
                print('[*] Cracking Password For: {}'.format(user))
                test_pass(crypt_pass, dictionary_file)

# Common idiom in Python that allows the script to be used as an importable module in other scripts, or to be run as a standalone script.
# The 'main' function is executed only when the script is run as a standalone script, not when it is imported as a module.
if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('passwords_file', type=str, help='file containing encrypted passwords')
    parser.add_argument('dictionary_file', type=str, help='file containing possible passwords to test against')
    args = parser.parse_args()

    main(args.passwords_file, args.dictionary_file)

# To run the script, you need to provide the filename that contains the encrypted passwords as an argument: python simple_password_cracker.py passwords.txt
# If the filename doesn't exist or the script doesn't have sufficient permissions to access the file, you will get an error message: '[ERROR] The file non_existent_file.txt does not exist or can not be accessed'
# If the dictionary file (dictionary.txt) is not found, you will get an error message: '[ERROR] The dictionary file dictionary.txt is missing'
# If the encrypted password is found in the dictionary file, the script will display the decrypted password: '[INFO] Cracking password for user1' --> '[INFO] Password found: 123456'
# If the encrypted password is not found in the dictionary file, the script will display a message indicating that the password was not found: '[INFO] Cracking password for user2' --> '[INFO] Password not found'
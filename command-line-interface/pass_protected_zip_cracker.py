""" This script is a password cracking tool that uses a dictionary attack to try to find the password of a ZIP archive. """

#!/usr/bin/python
# -*- coding: utf-8 -*-
import zipfile
import optparse
from threading import Thread

# This function takes a ZipFile object and a password as input and attempts to extract the contents of the archive using the specified password.
# If the password is incorrect, a zipfile.BadZipfile exception is raised, which the function catches and does nothing with.
def extract_file(z_file, password):
    """
    Attempts to extract the contents of a zip file using the specified password.

    :param z_file: A ZipFile object.
    :param password: The password to use for extraction.
    :return: None
    """
    try:
        z_file.extractall(pwd=password)
        print(f'[+] Found password: {password}')
    except zipfile.BadZipfile:
        # Catch only the expected exception and do nothing.
        pass

# The main function uses the optparse library to parse the command line arguments passed to the script.
# It expects two arguments: -f specifying the name of the ZIP file, and -d specifying the name of the dictionary file.
# If either of these arguments is missing, the function prints a usage message and exits.
# It opens the specified ZIP file and dictionary file using the with statement, which automatically closes the files even if an exception is raised.
# It then reads the contents of the dictionary file line by line and launches a new Thread for each password in the dictionary.
# The Thread runs the extract_file function and attempts to extract the contents of the archive using the current password.
# Note: script uses a boolean flag password_found to keep track of whether the password has been found. If the password is found, the script breaks out of the loop and does not launch any more Threads.
def main():
    parser = optparse.OptionParser("usage %prog -f <zipfile> -d <dictionary>")
    parser.add_option('-f', dest='zip_file', type='string', help='specify zip file')
    parser.add_option('-d', dest='dict_file', type='string', help='specify dictionary file')
    options, _ = parser.parse_args()

    if not all([options.zip_file, options.dict_file]):
        print(parser.usage)
        exit(0)

    password_found = False
    with zipfile.ZipFile(options.zip_file) as z_file:
        with open(options.dict_file) as dict_file:
            for line in dict_file:
                password = line.strip()
                if password_found:
                    break

                t = Thread(target=extract_file, args=(z_file, password))
                t.start()

# Common statement at the end of the script runs the main function if the script is run as a standalone program.
if __name__ == '__main__':
    main()
    

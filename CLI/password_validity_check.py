#!/usr/bin/python
# -*- coding: utf-8 -*-

""" The code checks the validity of a password entered by the user. It does so by using a loop that continues until the entered password meets all of the specified conditions. The conditions are:
The length of the password should be between 6 and 12 characters.
The password should contain at least one upper-case letter [A-Z].
The password should contain at least one lower-case letter [a-z].
The password should contain at least one digit [1-9].
The password should contain at least one special character [~!@#$%^&*].
The password should not contain any spaces.
If any of the above conditions are not met, the user is informed of the issue and the loop continues. If all conditions are met, the loop terminates and the password is considered to be valid. """

import re

while True:
  user_input = input("Enter a password : ")
  is_valid = False

  if (len(user_input)<6 or len(user_input)>12):
    print("Not valid ! Total characters should be between 6 and 12")
    continue
  elif not re.search("[A-Z]",user_input):
    print("Not valid ! It should contain one letter between [A-Z]")
    continue
  elif not re.search("[a-z]",user_input):
    print("Not valid ! It should contain one letter between [a-z]")
    continue
  elif not re.search("[1-9]",user_input):
    print("Not valid ! It should contain one letter between [1-9]")
    continue
  elif not re.search("[~!@#$%^&*]",user_input):
    print("Not valid ! It should contain at least one letter in [~!@#$%^&*]")
    continue
  elif re.search("[\s]",user_input):
    print("Not valid ! It should not contain any space")
    continue
  else:
    is_valid = True
    break

if(is_valid):
  print("Password is valid")

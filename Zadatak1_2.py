"""
The following rules apply to blood transfusions:
*blood group 0 can only receive blood group 0
*blood group A can receive blood group A or 0
*blood group B can receive blood group B or 0
*blood group AB can receive all blood groups
*person with a negative Rh factor can only receive a blood group with also a negative Rh factor
*person with a positive Rh factor can receive any blood type Rh factor
Eg. a person with blood group A + can receive A +, A-, 0+ and 0-, a person with
B- can receive B- and 0-, while someone with blood group 0- can receive only
0- blood type. Ask the user's blood type and Rh factor of the donor and recipient,
and print if a blood transfusion is allowed for that combination.
Note: as a simplification, it is allowed to name the blood group "AB" to "C".
"""

import autopy


bg = str(input("Enter Blood Group (0, a, b or ab) :"))
rhd = str(input("Enter Donor RH (positive or negative)  :"))
rhr = str(input("Enter Recepient RH (positive or negative)  :"))

if bg == "0" and rhr != "negative":
    print("Group 0 only | Donor can accept both RH's")
elif bg == "0" and rhr == "negative":
    print("Group 0 only | Donor can only accept RH negative")
elif bg == "a" and rhr != "negative":
    print("Group 0 or A only | Donor can accept both RH's")
elif bg == "a" and rhr == "negative":
    print("Group 0 or A only | Donor can only accept RH negative")
elif bg == "b" and rhr != "negative":
    print("0 or B only | Donor can accept both RH's")
elif bg == "b" and rhr == "negative":
    print("Group 0 or B only | Donor can only accept RH negative")
elif bg == "ab" and rhr == "negative":
    print("All groups | Donor can only accept RH negative")
elif bg == "ab" and rhr != "negative":
    print("All groups | Donor can accept both RH's")
else:
    print("Try again with specified types")
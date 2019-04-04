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


# -*- coding: utf-8 -*-
"""
Created on Sat Mar 18 00:13:20 2023

@author: fwhite
"""


""" Check the weight of a piece of luggage and determine if any additional fees are required
-between 0 and 15 (inclusive), additional fee and that the luggage can be brought on board
-between 15 and 30 (inclusive), additional fee is 20.00 euros will be checked and loaded into the cargo hold
-between 30 and 50 (inclusive), additional fee is 50.00 euros will be checked and loaded into the cargo hold
-if the weight is over 50 kilograms, the code indicates that the luggage cannot be accepted """

print("Luggage weight check")

weight = float(
    input("\tPlease enter the weight of your luggage (in kilograms): "))

while weight <= 0 or weight > 50:
    weight = float(input("\tInvalid input. Please enter the weight again: "))

if weight > 0 and weight <= 15:
    print("\tNo additional fee")
    print("\tYou can bring your luggage on board.")
elif weight > 15 and weight <= 30:
    print("\tAdditional fee of 20.00 euros")
    print("\tYour luggage will be checked and loaded into the cargo hold.")
elif weight > 30 and weight <= 50:
    print("\tAdditional fee of 50.00 euros")
    print("\tYour luggage will be checked and loaded into the cargo hold.")
else:
    print("\tSorry, we cannot accept luggage over 50 kilograms.")

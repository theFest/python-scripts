# -*- coding: utf-8 -*-
"""
Created on Mon Mar 20 23:46:46 2023

@author: fwhite
"""

# calculate the number of Euro bills and coins needed for a given amount of money.


def calculate_euros(amount):
    euro_bills = {
        500: 0,
        200: 0,
        100: 0,
        50: 0,
        20: 0,
        10: 0,
        5: 0
    }

    euro_coins = {
        2: 0,
        1: 0,
        0.5: 0,
        0.2: 0,
        0.1: 0,
        0.05: 0,
        0.02: 0,
        0.01: 0
    }

    # Calculate the number of euro bills
    for bill in euro_bills.keys():
        while amount >= bill:
            euro_bills[bill] += 1
            amount -= bill

    # Calculate the number of euro coins
    for coin in euro_coins.keys():
        while amount >= coin:
            euro_coins[coin] += 1
            amount -= coin

    # Print the results
    print(f"Amount: {amount}")
    for bill, count in euro_bills.items():
        if count > 0:
            print(f"{count} x {bill} euro bill")
    for coin, count in euro_coins.items():
        if count > 0:
            print(f"{count} x {coin} euro coin")


# Examples
# calculate_euros(10)
# calculate_euros(1234.56)
# calculate_euros(325.67)

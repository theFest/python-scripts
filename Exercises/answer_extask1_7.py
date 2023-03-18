# -*- coding: utf-8 -*-
"""
Created on Sat Mar 18 00:40:01 2023

@author: fwhite
"""

""" Prints a pattern of numbers in a triangular shape """

start = 1
end = 2
rows = int(input("Enter the number of rows: "))

for i in range(rows):
    for j in range(1, end):
        print(start, end=' ')
        start += 1
    print("")
    end += 1

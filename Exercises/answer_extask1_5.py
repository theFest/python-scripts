# -*- coding: utf-8 -*-
"""
Created on Sat Mar 18 00:13:20 2023

@author: fwhite
"""


""" Prompts the user to enter the dimensions of a triangle by providing the lengths of its three sides
-of all three sides are equal, the code indicates that the triangle is equilateral.
-if all three sides are different, the code indicates that the triangle is scalene
-if two sides are equal and the third is different, the code indicates that the triangle is isosceles
"""

print("Enter the dimensions of a triangle")

side_a = int(input("\tSide a: "))
side_b = int(input("\tSide b: "))
side_c = int(input("\tSide c: "))

if side_a == side_b == side_c:
    print("\tThe triangle is equilateral")
elif side_a == side_b or side_b == side_c or side_a == side_c:
    print("\tThe triangle is isosceles")
else:
    print("\tThe triangle is scalene")

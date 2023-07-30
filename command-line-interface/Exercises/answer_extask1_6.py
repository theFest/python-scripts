# -*- coding: utf-8 -*-
"""
Created on Sat Mar 18 00:22:27 2023

@author: fwhite
"""

""" Calculates the age of a dog in "dog years" based on its age in human years.
first year of a dog's life is equivalent to 10.5 human years, while each additional year after that is equivalent to 4 human years.
"""

print("Dog Years")

human_years = 4
first_years = 10.5
years = int(input("How old is the dog? "))

if years <= 0:
    print("That dog hasn't been born yet")
elif years > 2:
    dog_years = first_years * 2 + ((years - 2) * human_years)
    print("A dog that is " + str(years) + " human years old is " +
        str(dog_years) + " dog years old.")
elif years <= 2:
    dog_years = first_years * years
    print("A dog that is " + str(years) + " human years old is " +
        str(dog_years) + " dog years old.")

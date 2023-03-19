# -*- coding: utf-8 -*-
"""
Created on Sun Mar 19 15:53:39 2023

@author: fwhite
"""

""" prompts the user to input their current salary and years of experience. If the years of experience meet the condition for a salary increase (i.e. 10 or more years), the program calculates the percent increase and new salary
 """

salary = int(input("Enter your current salary amount: "))
years_of_experience = int(input("Enter your years of experience: "))

if years_of_experience >= 10:
    percent_increase = 0.01 * years_of_experience
    new_salary = salary + (salary * percent_increase)

    print("Congratulations! Your new salary is:", new_salary)
    increase_amount = new_salary - salary
    print("Your salary has increased by:", increase_amount)

    job_title = input("Please enter your job title: ")

    if job_title.lower() == "manager" or job_title.lower() == "director":
        print("As a", job_title, "you may also be eligible for a bonus.")

        department = input("Please enter your department: ")
        if department.lower() == "sales" or department.lower() == "marketing":
            print("Your department is eligible for a bonus!")
        else:
            print("Unfortunately, your department is not eligible for a bonus.")
    else:
        print("As a", job_title, "you are not eligible for a bonus.")
else:
    print("Sorry, your years of experience do not meet the requirements for a salary increase.")

""" check the weight of a piece of luggage and determine if any additional fees are required """

print("Luggage weight check")

weight = float(input("\tPlease enter the weight of your luggage: "))

while weight <= 0 or weight > 50:
    weight = float(input("\tInvalid input. Please enter the weight again: "))

if weight > 0 and weight <= 15:
    print("\tNo additional fee")
elif weight > 15 and weight <= 50:
    print("\tAdditional fee of 100.00 €")

""" New version, the calculator functions have been separated into their own functions and a calculate function has been added to call the appropriate function based on the selected operator.
The script includes includes error handling for division by 0 and for invalid operators and has been made into a loop so that the user can perform multiple calculations without having to restart the script. The loop will only end when the user decides to stop performing calculations. """

def add(x, y):
    return x + y

def subtract(x, y):
    return x - y

def multiply(x, y):
    return x * y

def divide(x, y):
    return x / y

def calculate(x, y, operation):
    if operation == "+":
        return add(x, y)
    elif operation == "-":
        return subtract(x, y)
    elif operation == "*":
        return multiply(x, y)
    elif operation == "/":
        if y == 0:
            return "Error: Division by 0 is not allowed."
        return divide(x, y)
    else:
        return "Error: Invalid operator."

while True:
    x = int(input("First value: "))
    y = int(input("Second value: "))
    operation = input("Choose operation (+, -, *, /): ")
    result = calculate(x, y, operation)
    print("Result: ", result)

    repeat = input("Do you want to perform another calculation? (yes/no): ")
    if repeat.lower() != "yes":
        break

print("Ending Calculator!")

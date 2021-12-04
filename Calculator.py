x = int(input("First value: "))

y = int(input("Second value: "))

operation = input("Choose operation (+, -, *, /:")

if operation == "+":
    print(x + y)
elif operation == "-":
    print(x - y)
elif operation == "*":
    print(x * y)
elif operation == "/":
    print(x / y)
else:
    print("You did not provide the correct math operation.")
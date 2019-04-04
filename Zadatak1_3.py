import pyautogui


print()
pyautogui.displayMousePosition()

print("Current mouse x/y positions;")
print(pyautogui.position())

print("Current screen resolution width and height;")
print(pyautogui.size())


u = str(input("Press Up, Right, Down, Left or Quit :"))


if u == "up":
    pyautogui.move(0, -200)
elif u == "down":
    pyautogui.move(0, 100)
elif u == "left":
    pyautogui.move(-200, 0)
elif u == "right":
    pyautogui.move(200, 0)
elif u == "quit":
    print()
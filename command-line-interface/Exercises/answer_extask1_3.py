# -*- coding: utf-8 -*-
"""
Created on Fri Mar 17 23:51:52 2023

@author: fwhite
"""

import pyautogui
# pip install pyautogui
# pip3 install pyautogui
# pip install pyautogui --upgrade
# pip install Pillow --upgrade


def get_mouse_position():
    """
    Displays the current position of the mouse.
    """
    print("Current mouse position:")
    pyautogui.displayMousePosition()


def get_screen_resolution():
    """
    Displays the screen resolution width and height.
    """
    print("Screen resolution width and height:")
    print(pyautogui.size())


def move_mouse(direction):
    """
    Moves the mouse in the specified direction.
    Args:
        direction (str): The direction to move the mouse. Can be one of: up, down, left, right.
    """
    if direction == "up":
        pyautogui.move(0, -200)
    elif direction == "down":
        pyautogui.move(0, 100)
    elif direction == "left":
        pyautogui.move(-200, 0)
    elif direction == "right":
        pyautogui.move(200, 0)
    else:
        print("Invalid direction")


if __name__ == "__main__":
    get_mouse_position()
    get_screen_resolution()
    while True:
        u = input("Press Up, Right, Down, Left or Quit: ").lower()
        if u == "up" or u == "down" or u == "left" or u == "right":
            move_mouse(u)
        elif u == "quit":
            break
        else:
            print("Invalid input. Please try again.")

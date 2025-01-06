import time
import random
import pyautogui

while True:
    time.sleep(50)

    current_x, current_y = pyautogui.position()
    print("x =", current_x, ", y =", current_y)

    offset_x = random.randint(-100, 100)
    offset_y = random.randint(-100, 100)

    new_x = current_x + offset_x
    new_y = current_y + offset_y

    pyautogui.moveTo(new_x, new_y)

    pyautogui.click()

    time.sleep(15)

    pyautogui.scroll(-2)
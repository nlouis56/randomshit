import pyautogui
import time
import random

pyautogui.FAILSAFE = True
screenWidth, screenHeight = pyautogui.size()
currentMouseX, currentMouseY = pyautogui.position()

def AltTab():
    pyautogui.keyDown('alt')
    pyautogui.press('tab')
    pyautogui.keyUp('alt')


def RandomAltTab():
    tabQty = random.randint(1, 5)
    pyautogui.keyDown('alt')
    for i in range(tabQty):
        pyautogui.press('tab')
    pyautogui.keyUp('alt')


def RandomMouseMovement():
    x = random.randint(0, screenWidth)
    y = random.randint(0, screenHeight)
    pyautogui.moveTo(x, y, duration=2, tween=pyautogui.easeInOutQuad)


def main():
    while True:
        time.sleep(5)
        case = random.randint(1, 3)
        if case == 1:
            AltTab()
        elif case == 2:
            RandomAltTab()
        elif case == 3:
            RandomMouseMovement()

if __name__ == '__main__':
    main()

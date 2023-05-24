import pyautogui
import time
import random

pyautogui.FAILSAFE = True

keys = [
    ## Using an AZERTY keyboard
    {'key': 'a', 'surrounding': ['q', 's', 'z']},
    {'key': 'b', 'surrounding': ['v', 'g', 'h', 'n']},
    {'key': 'c', 'surrounding': ['x', 'd', 'f', 'v']},
    {'key': 'd', 'surrounding': ['s', 'e', 'r', 'f', 'c', 'x']},
    {'key': 'e', 'surrounding': ['z', 's', 'd', 'r']},
    {'key': 'f', 'surrounding': ['d', 'r', 't', 'g', 'v', 'c']},
    {'key': 'g', 'surrounding': ['f', 't', 'y', 'h', 'b', 'v']},
    {'key': 'h', 'surrounding': ['g', 'y', 'u', 'j', 'n', 'b']},
    {'key': 'i', 'surrounding': ['u', 'j', 'k', 'o']},
    {'key': 'j', 'surrounding': ['h', 'u', 'i', 'k', 'm', 'n']},
    {'key': 'k', 'surrounding': ['j', 'i', 'o', 'l', 'm']},
    {'key': 'l', 'surrounding': ['k', 'o', 'p', 'm']},
    {'key': 'm', 'surrounding': ['n', 'j', 'k', 'l']},
    {'key': 'n', 'surrounding': ['b', 'h', 'j', 'm']},
    {'key': 'o', 'surrounding': ['i', 'k', 'l', 'p']},
    {'key': 'p', 'surrounding': ['o', 'l', 'm']},
    {'key': 'q', 'surrounding': ['a', 'w', 's']},
    {'key': 'r', 'surrounding': ['e', 'd', 'f', 't']},
    {'key': 's', 'surrounding': ['a', 'z', 'e', 'd', 'x', 'w']},
    {'key': 't', 'surrounding': ['r', 'f', 'g', 'y']},
    {'key': 'u', 'surrounding': ['y', 'h', 'j', 'i']},
    {'key': 'v', 'surrounding': ['c', 'f', 'g', 'b']},
    {'key': 'w', 'surrounding': ['q', 'a', 's', 'x']},
    {'key': 'x', 'surrounding': ['z', 's', 'd', 'c', 'w']},
    {'key': 'y', 'surrounding': ['t', 'g', 'h', 'u']},
    {'key': 'z', 'surrounding': ['a', 'e', 's', 'x']},
]

precision = 92

def floatRandInt(min, max) -> float:
    return random.randint(min * 10, max * 10) / 10

def clumsyWrite(text: str, clumsyFactor: float = 1.00):
    for letter in text :
        randomDelay = floatRandInt(0.2, 0.5)
        print (f"delay : {randomDelay}")
        if letter == ' ':
            pyautogui.press('space')
            continue
        actualPrecision = precision * clumsyFactor
        if random.randint(1, 100) <= actualPrecision:
            pyautogui.press(letter)
        else:
            surroundingKeys = [key for key in keys if key['key'] == letter][0]['surrounding']
            pyautogui.press(random.choice(surroundingKeys))
            time.sleep(floatRandInt(0.2, 0.5))
            pyautogui.press('backspace')
            time.sleep(floatRandInt(0.2, 0.5))
            pyautogui.press(letter)

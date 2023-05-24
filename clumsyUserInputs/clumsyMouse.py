import pyautogui
import time
import random

pyautogui.FAILSAFE = True

def clumsyMouseMoveTo(x: int, y: int, duration: float = 1.00, randomness: float = 0.50):
    lineLength = ((x - pyautogui.position().x) ** 2 + (y - pyautogui.position().y) ** 2) ** 0.5
    partitions = lineLength // 50
    print (f"line length : {lineLength}, partitions : {partitions}")
    originalLineCoords = []
    for i in range(int(partitions)):
        originalPoint = (pyautogui.position().x + (x - pyautogui.position().x) / partitions * i, pyautogui.position().y + (y - pyautogui.position().y) / partitions * i)
        originalLineCoords.append(originalPoint)
        #print (f"original point : {originalPoint}")
    randomizedLineCoords = []
    for point in originalLineCoords:
        randomizedPoint = (point[0] + randomness * 10, point[1] + randomness * 10)
        randomizedLineCoords.append(randomizedPoint)
        print (f"original point : {point}")
        print (f"randomized point : {randomizedLineCoords[-1]}")
    randomizedLineCoords.append((x, y))
    moveDuration = duration / partitions
    print (f"move duration : {moveDuration}")
    for point in randomizedLineCoords:
        pyautogui.moveTo(point[0], point[1], moveDuration)

if __name__ == "__main__":
    while True:
        clumsyMouseMoveTo(random.randint(0, 1920), random.randint(0, 1080), duration=0.5)
        time.sleep(5)

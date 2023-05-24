# clumsyUserInputs

## Description

These are simple python scripts to simulate a real human with pyautogui.

## ClumsyKeyboard

The clumsyKeyboard will write the given string of characters at around 50-60 words per minute, with a precision of 92%. The precision is the probability that the character will be typed correctly. If the key is determined to not be typed properly, a character from the surrounding keys will be typed instead. It will then be erased and the correct character will be typed.

This functionnality is based off of an AZERTY keyboard, but can be easily modified to work with other keyboard layouts.

## ClumsyMouse

The clumsyMouse will move the mouse to the given coordinates without following a straight line. The mouse will always end up at the given coordinates, but will take a random path to get there.

If you launch the clumsyMouse script as-is, the mouse will move randomly around your screen.

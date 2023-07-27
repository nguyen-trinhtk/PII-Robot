#robot going randomly
#interruption from keyboard can manually navigate robot


import random
import serial
import time
ser = serial.Serial('COM8', 9600)
from pynput import keyboard
actions = [b'f', b'b', b'r', b'l']

interrupt = False
def on_press(key):
    global interrupt
    if key == keyboard.Key.down:
        ser.write(b'2')
        interrupt = True
    elif key == keyboard.Key.left:
        ser.write(b'4')
        interrupt = True
    elif key == keyboard.Key.right:
        ser.write(b'6')
        interrupt = True
    elif key == keyboard.Key.up:
        ser.write(b'8')
        interrupt = True

                                                     
def on_release(key):
    ser.write(b'0')
    global interrupt
    interrupt = False

def goRandomly():
    nextAction = random.choice(actions)
    ser.write(nextAction)
    if actions.index(nextAction) < 2:
        time.sleep(random.randint(1,5))
    else:
        time.sleep(random.randint(1,10)/10)
    ser.write(b'0')

def bottleFound():
    data = ser.readline().decode().strip()
    if (data == 'bottle found'):
        return True
    return False
def bottleCollected():
    data = ser.readline().decode().strip()
    if (data == 'bottle collected'):
        return True
    return False

def main():
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        while True:
            if not interrupt or bottleFound():
                goRandomly()
            if bottleFound():
                while not bottleCollected():
                    pass
            

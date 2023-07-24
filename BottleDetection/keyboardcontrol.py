import keyboard
import serial
ser = serial.Serial(port='COM8', baudrate=9600, timeout=.1)
ignore_keypress = False
def on_press(event):
    global ignore_keypress
    if not ignore_keypress:
        if event.name == 'up':
            ser.write(b'8')
        elif event.name == 'down':
            ser.write(b'2')
        elif event.name == 'left':
            ser.write(b'4')
        elif event.name == 'right':
            ser.write(b'6')
def on_release(event):
    if not ignore_keypress:
        ser.write(b'0')
keyboard.on_press(on_press)
keyboard.on_release(on_release)
while True:
    if ser.in_waiting:
        message = ser.readline().decode().strip()
        if message.lower() == 'done executing':
            ignore_keypress = False
        else:
            ignore_keypress = True

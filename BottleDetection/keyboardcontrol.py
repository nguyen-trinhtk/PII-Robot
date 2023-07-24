import serial
from pynput import keyboard

# Open the serial connection
ser = serial.Serial('COM8', 9600)  # Replace 'COM0' with the appropriate serial port

# Key press event handlers
def on_key_press(key):
    if key == keyboard.Key.down:
        ser.write(b'2')
    elif key == keyboard.Key.left:
        ser.write(b'4')
    elif key == keyboard.Key.right:
        ser.write(b'6')
    elif key == keyboard.Key.up:
        ser.write(b'8')

def on_key_release(key):
    if key in [keyboard.Key.down, keyboard.Key.left, keyboard.Key.right, keyboard.Key.up]:
        ser.write(b'0')

# Create listener
listener = keyboard.Listener(on_press=on_key_press, on_release=on_key_release)

# Start the listener
listener.start()

# Keep the program running until interrupted
listener.join()
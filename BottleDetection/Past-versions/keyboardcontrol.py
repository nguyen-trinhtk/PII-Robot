import serial
from pynput import keyboard
# Open the serial connection
ser = serial.Serial('COM13', 9600)
# Key press event handlers
# When key is pressed and hold, Arduino action is executed
def on_key_press(key):
    if key == keyboard.Key.down:
        ser.write(b"backward\n")
    elif key == keyboard.Key.left:
        ser.write(b"turnLeft\n")
    elif key == keyboard.Key.right:
        ser.write(b"turnRight\n")
    elif key == keyboard.Key.up:
        ser.write(b"forward\n")

# The action (forward, backward, left, right)
# continues until key is release
def on_key_release(key):
    if key in [keyboard.Key.down, keyboard.Key.left, keyboard.Key.right, keyboard.Key.up]:
        ser.write(b"stop\n")
# Keep the program running
listener = keyboard.Listener(on_press=on_key_press, on_release=on_key_release)
listener.start()
listener.join()
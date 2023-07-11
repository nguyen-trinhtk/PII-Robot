import keyboard,serial

ser = serial.Serial(port='COM13', baudrate=9600, timeout=.1)
while True:
    if keyboard.is_pressed('up arrow') or keyboard.is_pressed('w'):
        ser.write(b'8')
    if keyboard.is_pressed("down arrow") or keyboard.is_pressed('s'):
        ser.write(b'2')
    if keyboard.is_pressed("right arrow") or keyboard.is_pressed('d'):
        ser.write(b'6')
    if keyboard.is_pressed("left arrow") or keyboard.is_pressed('a'):
        ser.write(b'4')

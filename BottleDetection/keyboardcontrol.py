import keyboard,serial

ser = serial.Serial(port='COM8', baudrate=9600, timeout=.1)
while True:
    if keyboard.is_pressed('up arrow') or keyboard.is_pressed('w'):
        print('8')
    elif keyboard.is_pressed("down arrow") or keyboard.is_pressed('s'):
        print('2')
    elif keyboard.is_pressed("right arrow") or keyboard.is_pressed('d'):
        print('6')
    elif keyboard.is_pressed("left arrow") or keyboard.is_pressed('a'):
        print('4')
    while True:
        data = ser.readline().decode().strip()
        if (data.lower()=='done executing'):
            break
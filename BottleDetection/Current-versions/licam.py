from imageai.Detection import ObjectDetection
import os
import cv2
import math
import random
import serial
import time
from pynput import keyboard
import threading

ser = serial.Serial('COM13', 9600)
# ser = serial.Serial('/dev/ttyACM0/', 9600)
execution_path = os.getcwd()
cam = cv2.VideoCapture(0)
if not cam.isOpened():
    ser.write('e')
    exit()

actions = [b'forward\n']

bottleFound = False
bottleCollected  = False

detector = ObjectDetection()
# detector.setModelTypeAsYOLOv3()
# detector.setModelPath(os.path.join(execution_path, "BottleDetection\Current-versions\models\yolov3.pt"))
detector.setModelTypeAsTinyYOLOv3()
detector.setModelPath(os.path.join(execution_path, "BottleDetection/Current-versions/models/tiny-yolov3.pt"))
detector.loadModel()

def on_press(key):
    global interrupt
    if key == keyboard.Key.down:
        ser.write(b'backward\n')
        interrupt = True
        print("kb-backward")
    elif key == keyboard.Key.left:
        ser.write(b'turnLeft\n')
        interrupt = True
        print("kb-left")
    elif key == keyboard.Key.right:
        ser.write(b'turnRight\n')
        interrupt = True
        print("kb-right")
    elif key == keyboard.Key.up:
        ser.write(b'forward\n')
        interrupt = True
        print("kb-forward")
                                      
def on_release(key):
    ser.write(b'stop\n')
    global interrupt
    interrupt = False

def goRandomly():
    nextAction = random.choice(actions)
    ser.write(nextAction)
    print("randomizing actions")
    if actions.index(nextAction) < 2:
        for i in range(random.randint(10,20)):
            time.sleep(0.1)
            if (bottleFound):
                break
    else:
        for i in range(random.randint(1,10)):
            time.sleep(0.1)
            if (bottleFound):
                break
    ser.write(b'stop\n')

def lidar():
    print('lding')

def movement():
        while True:
            if not bottleFound:
                lidar()
            if bottleFound:
                while not bottleCollected:
                    pass

def info(frame,object):
    endX = frame.shape[1]
    midY = int(frame.shape[0]//2)
    difY = midY - (object["box_points"][1] + object["box_points"][3])//2
    difX = endX - (object["box_points"][0] + object["box_points"][2])//2
    dX = endX - max(object["box_points"][0],object["box_points"][2])
    distanceX = (309.059*(math.e**(1.04215*(dX/endX)))+130.13)/10
    absAngle = 0 if difX == 0 else math.atan(difY/difX)
    distance = distanceX/math.cos(absAngle)
    print(f"Distance: {distance} cm")
    return int(math.degrees(absAngle)), int(distance)

def detect(frame):
    detections =  detector.detectObjectsFromImage(input_image=frame,
                                                    minimum_percentage_probability=80,
                                                    display_percentage_probability = True,
                                                    display_object_name = True)
    return next((eachObject for eachObject in detections if eachObject['name']=='bottle'), None)

def waitForExecution():
    while True:
                data = ser.readline().decode().strip()
                if (data.lower()=='done executing'):
                    break

def center():
    frc = 0
    while True:
        ser.write(0)
        frc += 1
        ret, frame = cam.read()
        frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
        if (frc%20 == 0):
            object = detect(frame)
            if (object):
                angle = info(frame,object)[0]
                print('Current angle: ' + str(angle))
                if (abs(angle) <= 10):
                    print('center')
                    ser.write(b'centered\n')
                    return
                elif (angle > 45):
                    print('fR')
                    ser.write(b'farRight\n')
                elif (angle > 0):
                    print('nR')
                    ser.write(b'nearRight\n')
                elif (angle > -45):
                    print('nL')
                    ser.write(b'nearLeft\n')
                else:
                    print('fL')
                    ser.write(b'farLeft\n')
            else:
                ser.write(b'outFrame\n')
                print('outFr')
            waitForExecution()
            if not ret:
                break
        cv2.imshow('frame', cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE))

def runTo():
    ret, frame = cam.read()
    frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
    object = detect(frame)
    if (object):
        distance = info(frame, object)[1]
        ser.write(b'forward\n')
        time.sleep(distance/40)
        ser.write(b'stop\n')
    else:
        runTo()
    if not ret:
        pass

def collectedCheck():
    ser.write(b'backward\n')
    time.sleep(0.5)
    ret, frame = cam.read()
    object = detect(frame)
    if not object:
        print('bottle collected')
        return
    else:
        center()
        runTo()
        collectedCheck()

def mainCamera():
    print('camera') 
    cnt = -1
    while True:
        ret, frame = cam.read()
        frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
        ser.write(0)
        cnt += 1
        if (cnt%20==0):
            object = detect(frame)
            if object:
                print('Bottle found')
                global bottleFound 
                bottleFound = True
                center()
                runTo()
                collectedCheck()
                global bottleCollected 
                bottleCollected = True
            else:
                print('No bottle found')
        if not ret:
            break
        if cv2.waitKey(1)==ord('q'):
            break
        cv2.imshow('frame', cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE))
    cam.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    thr1 = threading.Thread(target = mainCamera)
    # thr2 = threading.Thread(target = movement)
    thr1.start()
    # thr2.start()
    thr1.join()
    # thr2.join()

#robot going randomly
#interruption from keyboard can manually navigate robot
from imageai.Detection import ObjectDetection
import os
import cv2
import math
import random
import serial
import time
from pynput import keyboard
import multiprocessing

ser = serial.Serial('COM8', 9600)

execution_path = os.getcwd()
cam = cv2.VideoCapture(0)
if not cam.isOpened():
    ser.write('e')
    exit()

actions = [b'forward\n', b'backward\n', b'turnRight\n', b'turnLeft\n']
bottleFound = False
bottleCollected  = False
interrupt = False

detector = ObjectDetection()
detector.setModelTypeAsYOLOv3()
detector.setModelPath(os.path.join(execution_path, "BottleDetection\Current-versions\models\yolov3.pt"))
detector.loadModel()

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
    ser.write(b'stop\n')
    global interrupt
    interrupt = False

def goRandomly():
    nextAction = random.choice(actions)
    ser.write(nextAction)
    if actions.index(nextAction) < 2:
        time.sleep(random.randint(1,5))
    else:
        time.sleep(random.randint(1,10)/10)
    ser.write(b'stop\n')

def movement():
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        while True:
            if not interrupt or bottleFound:
                goRandomly()
            if bottleFound:
                while not bottleCollected:
                    pass

def info(frame,object):
    endX = frame.shape[1]
    midY = int(frame.shape[0]//2)
    difY = midY - (object["box_points"][1] + object["box_points"][3])//2
    difX = endX - (object["box_points"][0] + object["box_points"][2])//2
    dX = endX - max(object["box_points"][0],object["box_points"][2])
    distanceX = (142.902*(math.e**(2.512*(dX/endX)))-132.985+400)
    absAngle = 0 if difX == 0 else math.atan(difY/difX)
    distance = distanceX/math.cos(absAngle)
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
                    ser.write(b'centered\n')
                    return
                elif (angle < -45):
                    ser.write(b'farRight\n')
                elif (angle < 0):
                    ser.write(b'nearRight\n')
                elif (angle < 45):
                    ser.write(b'nearLeft\n')
                else:
                    ser.write(b'farLeft\n')
            else:
                ser.write(b'outFrame\n')
            waitForExecution()
            if not ret:
                break

def runTo():
    ret, frame = cam.read()
    frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
    object = detect(frame)
    if (object):
        distance = info(frame, object)[1]
        ser.write(b'forward\n')
        time.sleep(distance/10) #adjust the division constant 
        ser.write(b'stop\n')
    else:
        runTo()
    if not ret:
        pass

def collectedCheck():
    #Check if bottle is collected
    ser.write(b'backward\n')
    time.sleep(1)
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
                print('no bottle found')
        if not ret:
            break
        if cv2.waitKey(1)==ord('q'):
            break
        cv2.imshow('frame', cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE))
    cam.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    p1 = multiprocessing.Process(target = mainCamera())
    p2 = multiprocessing.Process(target = movement())
    p1.start()
    p2.start()
    p1.join()
    p2.join()

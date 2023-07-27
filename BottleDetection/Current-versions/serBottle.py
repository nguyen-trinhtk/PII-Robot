from imageai.Detection import ObjectDetection
import os
import cv2
import math
import serial
import time
ser = serial.Serial(port='COM8', baudrate=9600, timeout=.1)

execution_path = os.getcwd()
cam = cv2.VideoCapture(0)
if not cam.isOpened():
    ser.write('e')
    exit()

# Initialize the object detector
detector = ObjectDetection()
detector.setModelTypeAsYOLOv3()
detector.setModelPath(os.path.join(execution_path, "BottleDetection\Current-versions\models\yolov3.pt"))
detector.loadModel()
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
        return
    else:
        center()
        runTo()
        collectedCheck()

def main():   
    cnt = -1
    ret, frame = cam.read()
    frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
    while True:
        ser.write(0)
        cnt += 1
        if (cnt%20==0):
            object = detect(frame)
            if object:
                print('Bottle found')
                ser.write(b'bottle found\n')
                center()
                runTo()
                collectedCheck()
                ser.write(b'bottle collected\n')
        if not ret:
            break
        if cv2.waitKey(1)==ord('q'):
            break
        cv2.imshow('frame', cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE))
    cam.release()
    cv2.destroyAllWindows()
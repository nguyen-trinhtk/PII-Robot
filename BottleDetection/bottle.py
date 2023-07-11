from imageai.Detection import ObjectDetection
import os
import cv2
import math 
import serial


execution_path = os.getcwd()
ser = serial.Serial(port='COM13', baudrate=9600, timeout=.1)

cam = cv2.VideoCapture(0)

if not cam.isOpened():
    print('cam is not opening')
    exit()
 
cnt = -1

#divide frame to form a relation btw distance irl and in img
def markupY(frame, section):
    x = frame.shape[1]//2
    y = frame.shape[0]
    xleft = x - 5
    xright = x + 5
    cv2.line(frame, (x,0), (x,y), (0,0,255), 2)
    for i in range(section-1):
         yTemp = int((i+1)*y/section)
         cv2.line(frame, (xleft,yTemp), (xright, yTemp), (0,0,255), 2)

def markupX(frame, section):
    x = frame.shape[1]
    y = frame.shape[0]
    yUp = y - 7
    cv2.line(frame, (0,y), (x,y), (0,0,255), 2)
    for i in range(section-1):
         xTemp = int((i+1)*x/section)
         cv2.line(frame, (xTemp,yUp), (xTemp, y), (0,0,255), 2)

#calculate distance and angle based on found formula
def distance(frame,object):
    endY = frame.shape[0]
    midX = int(frame.shape[1]//2)
    difX = midX - (object["box_points"][0] + object["box_points"][2])//2
    difY = endY - max(object["box_points"][1],object["box_points"][3])
    #formula
    distanceY = (142.902*(math.e**(2.512*(difY/endY)))-132.985+400)
    if difY == 0:
         absAngle = 0
    else: absAngle = math.atan(difX/difY)
    distance = distanceY/math.cos(absAngle)
    return int(math.degrees(absAngle)), int(distance)

def position(frame,object):
    angle = distance(frame,object)[0]
    if (abs(angle)<=5):
        print('centered')
        return '8'
    #if object is on the left-hand side
    elif angle > 0: 
        print('turn left')
        return '4' #turn left
    elif angle < 0:
        print('turn right')
        return '6'
    
def center(object):
    adjust = True
    while (adjust == True):
        frame = cam.read()
        msg = position(frame, object)
        if (msg == '8'):
            adjust = False
        else:
            ser.write(b'{}'.format(msg))

def runTo(object):
    adjust = True
    while (adjust == True):
        frame = cam.read()
        distance = distance(frame, object)[1]
        if (distance > 410):
            ser.write(b'8')
        else:
            ser.write(b'5')

while True:
    cnt += 1
    ret, frame = cam.read()
    # dim = (int(frame.shape[1]*70/100), int(frame.shape[0]*70/100))
    # frame = cv2.resize(frame, dim)
    # markupX(frame, 8)
    # markupY(frame, 8)
    if (cnt%15==0):
        detector = ObjectDetection()
        detector.setModelTypeAsYOLOv3()
        detector.setModelPath(os.path.join(execution_path, "BottleDetection/models/yolov3.pt"))
        detector.loadModel()
        detections = detector.detectObjectsFromImage(input_image=frame,
                                                    minimum_percentage_probability=30,
                                                    display_percentage_probability = True,
                                                    display_object_name = True)

        for eachObject in detections:
            if eachObject['name']=='bottle':
                print ('Object {} mm away at an angle of {} degrees'.format(distance(frame,eachObject)[1], distance(frame,eachObject)[0]))
                position(frame,eachObject)
                print('Bottle detected with probability: {}%'.format(eachObject["percentage_probability"]))
                print("--------------------------------")
                
                # start_point = [eachObject["box_points"][0], eachObject["box_points"][1]]
                # end_point = [eachObject["box_points"][2], eachObject["box_points"][3]]
                # color = (255, 0, 0)
                # thickness = 2
                # frame = cv2.rectangle(frame, start_point, end_point, color, thickness)
                

    if not ret:
            break

    cv2.imshow('frame', frame)
    if cv2.waitKey(1)==ord('q'):
        break

cam.release()
cv2.destroyAllWindows()
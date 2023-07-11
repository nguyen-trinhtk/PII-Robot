from imageai.Detection import ObjectDetection
import os
import cv2
import math 

execution_path = os.getcwd()

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
def distance1(frame,object):
    endY = frame.shape[0]
    midX = int(frame.shape[1]//2)
    difX = midX - (object["box_points"][0] + object["box_points"][2])//2
    difY = endY - (object["box_points"][1] + object["box_points"][3])//2
    #formula
    distanceY = (142.902*(math.e**(2.512*int(difY/endY)))+467.015)/10
    if difX == 0:
         absAngle = 0
    else: absAngle = math.atan(difY/difX)
    distance = distanceY/math.cos(absAngle)
    return math.degrees(absAngle), distance
    
#calculate distance using focal length
def distance2(object):
    bottleLen = max(abs(object["box_points"][0] - object["box_points"][2]), abs(object["box_points"][1] - object["box_points"][3]))
    realLen = 250
    focalLen = 1465
    distance = focalLen*realLen/bottleLen
    return distance/10

def position(frame,object):
    angle = distance1(frame,object)[0]
    #if object is on the left-hand side
    if (abs(angle)<=1):
        print('centered')
        return '8'
    elif angle < 0: 
        print('turn left')
        return '4' #turn left
    elif angle > 0:
        print('turn right')
        return '6'
    
# def center(object):
#     adjust = True
#     while (adjust == True):
#         ret, frame = cam.read()
#         dim = (int(frame.shape[1]*70/100), int(frame.shape[0]*70/100))
#         frame = cv2.resize(frame, dim)
#         msg = position(frame, object)
#         if (msg == '8'):
#             adjust = False
#         else:
#             ser.write(b'{}'.format(msg))
#     return True

while True:
    cnt += 1
    ret, frame = cam.read()
    dim = (int(frame.shape[1]*70/100), int(frame.shape[0]*70/100))
    frame = cv2.resize(frame, dim)
    # markupX(frame, 8)
    # markupY(frame, 8)
    if (cnt%1==0):
        detector = ObjectDetection()
        detector.setModelTypeAsYOLOv3()
        detector.setModelPath(os.path.join(execution_path , "BottleDetection\yolov3.pt"))
        detector.loadModel()
        detections = detector.detectObjectsFromImage(input_image=frame, 
                                                    minimum_percentage_probability=30,
                                                    display_percentage_probability = True,
                                                    display_object_name = True)

        for eachObject in detections:
            if eachObject['name']=='bottle':
                # print ('Object {} cm away at an angle of {} degrees'.format(distance1(frame,eachObject)[1], distance1(frame,eachObject)[0]))
                position(frame, eachObject)
                print('Bottle detected with probability: {}%'.format(eachObject["percentage_probability"]))
                # print(eachObject["name"] , " : ", eachObject["percentage_probability"], " : ", eachObject["box_points"] )
                print("--------------------------------")
                
                start_point = [eachObject["box_points"][0], eachObject["box_points"][1]]
                end_point = [eachObject["box_points"][2], eachObject["box_points"][3]]
                
                # Blue color in BGR
                color = (255, 0, 0)
                # Line thickness of 2 px
                thickness = 2
                frame = cv2.rectangle(frame, start_point, end_point, color, thickness)
                

    if not ret:
            break

    cv2.imshow('frame', frame)
    if cv2.waitKey(1) == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()
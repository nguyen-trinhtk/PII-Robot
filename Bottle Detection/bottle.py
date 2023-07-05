from imageai.Detection import ObjectDetection
import os
import cv2
import math 

execution_path = os.getcwd()

cam = cv2.VideoCapture(0)

if not cam.isOpened():
    exit()
 
cnt = 0

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
    difY = endY - (object["box_points"][1] + object["box_points"][3])//2
    #formula
    distanceY = 2*(int(difY/endY)*4+1)
    distanceX = 2*(int(difX/midX)*4+1)
    if difX == 0:
         absAngle = 90
    else: absAngle = math.atan(distanceY/distanceX)*180 / math.pi
    hypoDistance = (distanceY**2 + distanceX**2)**0.5
    return (absAngle, hypoDistance)

    

while True:
    ret, frame = cam.read()
    cnt += 1
    if (cnt%30==0):
        dim = (int(frame.shape[1]*70/100), int(frame.shape[0]*70/100))
        frame = cv2.resize(frame, dim)

        detector = ObjectDetection()
        detector.setModelTypeAsYOLOv3()
        detector.setModelPath(os.path.join(execution_path , "Bottle Detection\yolov3.pt"))
        detector.loadModel()
        detections = detector.detectObjectsFromImage(input_image=frame, 
                                                    minimum_percentage_probability=30,
                                                    display_percentage_probability = True,
                                                    display_object_name = True)

        for eachObject in detections:
            if eachObject['name']=='bottle':
                print ('Object {} cm away at an angle of {} degrees'.format(distance(frame,eachObject)[1], distance(frame,eachObject)[0]))
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
from imageai.Detection import ObjectDetection
import os
import cv2

execution_path = os.getcwd()

cam = cv2.VideoCapture(0)

if not cam.isOpened():
    exit()
 
cnt = 0
while True:
    ret, frame = cam.read()
    cnt += 1
    if (cnt%30==0):
        dim = (int(frame.shape[1]*70/100), int(frame.shape[0]*70/100))
        frame = cv2.resize(frame, dim)

        detector = ObjectDetection()
        detector.setModelTypeAsYOLOv3()
        detector.setModelPath(os.path.join(execution_path , "yolov3.pt"))
        detector.loadModel()
        detections = detector.detectObjectsFromImage(input_image=frame, 
                                                    minimum_percentage_probability=30,
                                                    display_percentage_probability = True,
                                                    display_object_name = True)

        for eachObject in detections:
            if eachObject['name']=='bottle':
                print('Bottle detected with probability: {}%'.format(eachObject["percentage_probability"]))
                # print(eachObject["name"] , " : ", eachObject["percentage_probability"], " : ", eachObject["box_points"] )
                print("--------------------------------")
                
                # start_point = [eachObject["box_points"][0], eachObject["box_points"][1]]
                # end_point = [eachObject["box_points"][2], eachObject["box_points"][3]]
                
                # # Blue color in BGR
                # color = (255, 0, 0)
                # # Line thickness of 2 px
                # thickness = 2

                # frame = cv2.rectangle(frame, start_point, end_point, color, thickness)

    if not ret:
            break

    cv2.imshow('frame', frame)
    if cv2.waitKey(1) == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()
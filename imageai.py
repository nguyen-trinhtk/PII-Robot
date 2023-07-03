import opencv
from imageai.Detection import ObjectDetection
import os

execution_path = os.getcwd()
image = opencv.cvimage(0)

detector = ObjectDetection()
detector.setModelTypeAsYOLOv3()
detector.setModelPath( os.path.join(execution_path , "yolov3.pt"))
detector.loadModel()
detections = detector.detectObjectsFromImage(input_image=image, output_image_path=os.path.join(execution_path , "imagenew.jpg"), minimum_percentage_probability=30)

for eachObject in detections:
    print(eachObject["name"] , " : ", eachObject["percentage_probability"], " : ", eachObject["box_points"] )
    print("--------------------------------")
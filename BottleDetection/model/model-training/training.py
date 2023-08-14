from imageai.Detection.Custom import DetectionModelTrainer

trainer = DetectionModelTrainer()
trainer.setModelTypeAsTinyYOLOv3()
trainer.setDataDirectory(data_directory="dataset")
trainer.setTrainConfig(object_names_array=["Plastic-Bottle"], batch_size=4, num_experiments=10, train_from_pretrained_model="models/tiny-yolov3.pt")
trainer.trainModel()
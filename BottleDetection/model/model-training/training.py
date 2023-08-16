from imageai.Detection.Custom import DetectionModelTrainer

trainer = DetectionModelTrainer()
trainer.setModelTypeAsTinyYOLOv3()
trainer.setDataDirectory(data_directory="BottleDetection\model\model-training\dataset")
trainer.setTrainConfig(object_names_array=["Plastic-Bottle"], batch_size=4, num_experiments=10, train_from_pretrained_model="BottleDetection\model\model-training\models\tiny-yolov3_dataset_last.pt")
trainer.trainModel()
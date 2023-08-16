
water bottle - v4 04
==============================

This dataset was exported via roboflow.com on November 15, 2022 at 7:09 AM GMT

Roboflow is an end-to-end computer vision platform that helps you
* collaborate with your team on computer vision projects
* collect & organize images
* understand unstructured image data
* annotate, and create datasets
* export, train, and deploy computer vision models
* use active learning to improve your dataset over time

It includes 249 images.
Water-bottle are annotated in Pascal VOC format.

The following pre-processing was applied to each image:
* Auto-orientation of pixel data (with EXIF-orientation stripping)
* Resize to 416x416 (Stretch)

The following augmentation was applied to create 3 versions of each source image:
* 50% probability of horizontal flip
* Equal probability of one of the following 90-degree rotations: none, clockwise, counter-clockwise
* Randomly crop between 0 and 20 percent of the image
* Random rotation of between -15 and +15 degrees
* Random shear of between -15° to +15° horizontally and -15° to +15° vertically
* Salt and pepper noise was applied to 5 percent of pixels



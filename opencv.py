import cv2 as cv

#0:webcam, 1:default cam


def cvimage(port):
    cam = cv.VideoCapture(port)
    result, image = cam.read()
    if result:
        return image
    else: 
        print("none")

def cvvideo(port):
    cam = cv.VideoCapture(port)
    if not cam.isOpened():
        exit()
    while True:
        ret, frame = cam.read()

        if not ret:
            break

        cv.imshow('frame', frame)
        if cv.waitKey(1) == ord('q'):
            break

    cam.release()
    cv.destroyAllWindows()

# def cvpixel():
#     #takepixelvalue (Blue Greed Red)
#     px = image[100,100]
#     print(px)

#     #modify pixel value
#     image[200, 200] = [255, 255, 255]

#     #accessing RED value
#     image.item(10,10,2)

#     #image properties (row, column, channels (colored))
#     print(image.shape)

#     #image size (pixels)
#     print(image.size)

#     #image datatype
#     print(image.dtype)

#     #copy a region to replace another (RoI)
#     sample = image[280:340, 330:390]
#     image[273:333, 100:160] = sample

#     #split & merge channel
#     #split cost time
#     b, g, r = cv.split(image)
#     image = cv.merge((b,g,r))

#     #set all red pixels to 0
#     #(allrow, allcolumn, channel#2 (R))
#     image[:, :, 2] = 0
    
#     #makeborder
#     example = cv.copyMakeBorder(image, 10, 10, 10, 10, cv.BORDER_CONSTANT(), value=[255,0,0])
#     #parameters: source(image), top, bot, left, right, borderType, value(color only if type is constant)
#     #borderType
#     #cv.BORDER_CONSTANT
#     #cv.BORDER_REFLECT
#     #cv.BORDER_REFLECT_101/cv.BORDER_DEFAULT
#     #cv.BORDER_REPLICATE
#     #cv.BORDER_WRAP
#     #see more at https://docs.opencv.org/3.4/d3/df2/tutorial_py_basic_ops.html

# def cvdetectbycolor():
#     #hsv: hue 0->179, s, v: 0->255

#     #objecttrackingcolor
#     while(1):
#         _, frame = cam.read()
#         hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
#         lower_blue = np.array([110,50,50])
#         upper_blue = np.array([130,255,255])
#         mask = cv.inRange(hsv, lower_blue, upper_blue)
#         res = cv.bitwise_and(frame, frame, mask = mask)

#         cv.imshow('frame', frame)
#         cv.imshow('mask', mask)
#         cv.imshow('res', res)
#         k = cv.waitKey(5) & 0xFF
#         if k == 27:
#             break
#     cv.destroyAllWindows()

from math import sqrt

import numpy
import cv2

imgPath = '3.png'


def get_gray_scale(img_path):
    rgb_image = cv2.imread(img_path)
    return cv2.cvtColor(rgb_image, cv2.COLOR_BGR2GRAY)


def detect_faces(img_path):
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    gray_scale = get_gray_scale(img_path)
    return face_cascade.detectMultiScale(gray_scale, scaleFactor=1.2, minNeighbors=5, minSize=(30, 30),
                                         flags=cv2.CASCADE_SCALE_IMAGE)


def crop_face(img_path, x_axis, y_axis, width, height):
    grayScale = get_gray_scale(img_path)
    cv2.rectangle(grayScale, (x_axis, y_axis), (x_axis + width, y_axis + height), (255, 0, 0), 1)
    return grayScale[y_axis:y_axis + height, x_axis:x_axis + width]


def localBinaryPattern(imagePath):
    faces = detect_faces(imagePath)
    maxArea = 0
    bound = (0, 0, 0, 0)

    for (x, y, w, h) in faces:
        area = w * h
        if area > maxArea:
            bound = (x, y, w, h)


    '''
    roi = faces[bound[1]:bound[2], bound[0]:bound[3]]
    cv2.imshow("sea", roi)
    cv2.waitKey(0)
    '''

    crop = crop_face(imagePath, bound[0], bound[1], bound[2], bound[3])
    cropH = crop.shape[0]
    cropW = crop.shape[1]
    lbpImg = numpy.zeros(shape=(cropH, cropW))

    for i in range(crop.shape[0]):  # traverses through height of the image
        for j in range(crop.shape[1]):  # traverses through width of the image
            if i != 0 and i != cropH - 1 and j != 0 and j != cropW - 1:
                threshold = crop[i][j]
                binary: str = ''
                for k in range(3):
                    for m in range(3):
                        if k != 1 or 1 != m:
                            if crop[i + k - 1][j + m - 1] >= threshold:
                                binary = binary + '1'
                            else:
                                binary = binary + '0'
                lbpImg[i][j] = int(binary, 2) / 255
                # print(lbpImg[i][j] * 255)
            else:
                lbpImg[i][j] = crop[i][j] / 255
    return lbpImg


def calculate(image, refImage):
    lbpImage1 = localBinaryPattern(image)
    refImage = localBinaryPattern(refImage)

    his1 = cal_histogram(lbpImage1)
    his2 = cal_histogram(refImage)

    print(his1)
    print(his2)

    print(compare_histograms(his1, his2))


'''
faces = detect_faces(imgPath)
maxArea = 0
bound = (0, 0, 0, 0)

for (x, y, w, h) in faces:
    area = w * h
    if area > maxArea:
        bound = (x, y, w, h)

crop = crop_face(imgPath, bound[0], bound[1], bound[2], bound[3])
cropH = crop.shape[0]
cropW = crop.shape[1]
lbpImg = numpy.zeros(shape=(cropH, cropW))

for i in range(crop.shape[0]):  # traverses through height of the image
    for j in range(crop.shape[1]):  # traverses through width of the image
        if i != 0 and i != cropH - 1 and j != 0 and j != cropW - 1:
            threshold = crop[i][j]
            binary: str = ''
            for k in range(3):
                for m in range(3):
                    if k != 1 or 1 != m:
                        if crop[i + k - 1][j + m - 1] >= threshold:
                            binary = binary + '1'
                        else:
                            binary = binary + '0'
            lbpImg[i][j] = int(binary, 2) / 255
            print(lbpImg[i][j] * 255)
        else:
            lbpImg[i][j] = crop[i][j] / 255

'''


def cal_histogram(lbp_img):
    imgArea = lbp_img.shape[0] * lbp_img.shape[1]
    histogram = numpy.zeros(shape=256)
    for a in range(lbp_img.shape[0]):
        for b in range(lbp_img.shape[1]):
            index = int(lbp_img[a][b] * 255)
            histogram[index] = histogram[index] + 1
    for d in range(256):
        histogram[d] = histogram[d] / imgArea
    return histogram


def compare_histograms(his1, his2):
    if len(his1) != len(his2):
        return -1
    distance = 0
    for ite in range(len(his2)):
        distance = distance + sqrt((his1[ite] - his2[ite]) * (his1[ite] - his2[ite]))
    return distance

'''
image = cv2.imread('alexdeneme.jpg')
faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
faces = faceCascade.detectMultiScale(
                    gray,
                    scaleFactor=1.1,
                    minNeighbors=5,
                    minSize=(30, 30),
                    flags=cv2.CASCADE_SCALE_IMAGE
                )
for (x,y,w,h) in faces:
    cv2.imshow("a",cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2))
    cv2.waitKey(0)
'''


calculate('alexdeneme.png', './histograms/deneme1.png')

# hist = cal_histogram(lbpImg)
#
# for c in range(len(hist)):
#     print('hist' + str(c) + ':' + str(hist[c]))
#
# cv2.imshow('img', lbpImg)
# cv2.imwrite("./histograms/deneme1.png", 255 * lbpImg)
#
# cv2.waitKey(0)

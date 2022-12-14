import cv2
from detectclass import detect
import os
import numpy as np
import time
from scipy import ndimage

                         ####I have to put this  ++diff_frame=cv2.absdiff(static_back,gray)++ in the  detect class

frameWidth = 540
frameHeight = 380
cap = cv2.VideoCapture(0)
cap.set(3, frameWidth)
cap.set(4, frameHeight)


def empty(a):
    pass

cv2.namedWindow("Parameters")
cv2.resizeWindow("Parameters",640,240)
cv2.createTrackbar("Threshold1","Parameters",23,444,empty)
cv2.createTrackbar("Threshold2","Parameters",20,555,empty)
cv2.createTrackbar("AreaMin","Parameters",5000,30000,empty)
cv2.createTrackbar("AreaMax","Parameters",5000,30000,empty)
cv2.createTrackbar("Average","Parameters",0,100,empty)
cv2.createTrackbar("TIMER","Parameters",0,100,empty)
cv2.createTrackbar("X2","Parameters",0,190,empty)


# mog = cv2.createBackgroundSubtractorMOG2()
mog= cv2.createBackgroundSubtractorKNN(detectShadows = True)

while True:
    success,img=cap.read()
    img_copy = img.copy()
    roiR = img_copy[0:400, 200:400]
    End_area=img_copy[0:400,210:220]
    End_area[0:]=(255,0,0)

    #----------------MOG--------------------------
    img=mog.apply(img)
    y1=0
    y2=400
    x1=200

    x2= cv2.getTrackbarPos("X2", "Parameters")


    roi=img[y1:y2,x1:400-x2]
    # imgBlur = cv2.GaussianBlur(img, (7, 7), 1)

    # imgGray = cv2.cvtColor(imgBlur, cv2.COLOR_BGR2GRAY)

    threshold1 = cv2.getTrackbarPos("Threshold1", "Parameters")
    threshold2 = cv2.getTrackbarPos("Threshold2", "Parameters")
    areaMn=cv2.getTrackbarPos("AreaMin", "Parameters")
    areaMx= cv2.getTrackbarPos("AreaMax", "Parameters")
    average = cv2.getTrackbarPos("Average", "Parameters")

    Timer = cv2.getTrackbarPos("TIMER", "Parameters")
    # canny1 = cv2.Canny(imgGray, threshold1, threshold2)
    cv2.imwrite("cutted image.jpg", roi)
    time.sleep(0.100)
    img_file = cv2.imread('cutted image.jpg')

    success, img = cap.read()

    img=mog.apply(img)
    roi2 = img[y1:y2, x1:400-x2]

    # imgBlur = cv2.GaussianBlur(img, (7, 7), 1)

    # imgGray = cv2.cvtColor(imgBlur, cv2.COLOR_BGR2GRAY)
    # canny2 = cv2.Canny(imgGray, threshold1, threshold2)
    cv2.imwrite("cutted image2.jpg", roi2)
    # time.sleep(0.100)
    img_file2 = cv2.imread('cutted image2.jpg')
    #img_sub = img_file2 - img_file
    img_sub=(cv2.subtract(img_file2,img_file))

    print(f"the average is ======={np.average(img_sub)}")

    # pix=cv2.countNonZero(canny)
    if np.average(img_sub)>average:


        print(detect(img_file,img_file2,threshold1,threshold2,areaMn,areaMx,roiR,Timer,End_area).getContours())


    else:
        try:
            os.remove("cutted image.jpg")
        except:
            pass

    cv2.imshow("img_file",img_file)
    # cv2.imshow("canny", canny1)
    cv2.imshow("camera",img_copy)
    cv2.imshow("roi",roi)
    cv2.imshow("roiR", roiR)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
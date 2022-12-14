import signal

import cv2
import numpy as np
import time
import signal
from tracking import *

track=EuclideanDistTracker()



class detect:


    def __init__(self,img_file,img_file2,threshol1,threshol2,areaMn,areaMx,roi,Timer,End_area):
        self.img=img_file
        self.img2=img_file2
        self.Threshold1=threshol1
        self.Threshold2=threshol2
        self.AreaMn=areaMn
        self.AreaMax = areaMx
        self.ROI=roi
        self.timer=Timer

        self.end=End_area


    def Bad(self):

        print("fgGDDFGDFGDGDFGDFGFDGDFGDFGDF")





    def getContours(self):

        i=0
        imgBlur = cv2.GaussianBlur(self.img, (21, 21), 1)
        imgBlur2 = cv2.GaussianBlur(self.img2, (21, 21), 1)
        imgGray = cv2.cvtColor(imgBlur, cv2.COLOR_BGR2GRAY)
        imgGray2 = cv2.cvtColor(imgBlur2, cv2.COLOR_BGR2GRAY)
        imgCanny = cv2.Canny(imgGray, self.Threshold1, self.Threshold2)
        imgCanny2 = cv2.Canny(imgGray2, self.Threshold1, self.Threshold2)
        kernel = np.ones((11, 11))
        imgDil = cv2.dilate(imgCanny, kernel, iterations=2)
        imgDil2 = cv2.dilate(imgCanny2, kernel, iterations=2)
        cv2.imshow("Dill",imgDil2)
        contours, hierarchy = cv2.findContours(imgDil, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        detections = []
        for cnt in contours:
            area = cv2.contourArea(cnt)


            areaMin = self.AreaMn
            areaMax=self.AreaMax


            if area> areaMin and area < areaMax:
                # cv2.drawContours(self.ROI, cnt, -1, (255, 0, 255), 7)
                peri = cv2.arcLength(cnt, True)

                approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)

                x, y, w, h = cv2.boundingRect(approx)
                detections.append([x, y, w, h])


                cv2.rectangle(self.ROI, (x, y), (x + w, y + h), (0, 255, 0), 5)

                imgDil=imgDil[y:y+h,x:x+w]
                cv2.imshow("img2 cutte",imgDil)

                cv2.putText(self.ROI, "Points: " + str(len(approx)), (x + w-200 , y+80 ), cv2.FONT_HERSHEY_COMPLEX,
                            .7,
                            (200, 255, 200), 2)
                cv2.putText(self.ROI, "Area: " + str(int(area)), (x + w-200 , y+110 ), cv2.FONT_HERSHEY_COMPLEX, 0.7,
                            (255, 0, 0), 2)

                print("OKOKOKOK")
                img_sub = (cv2.subtract(self.img,self.img2))
                print(f"the average is ======={np.average(img_sub)}")

            elif area<areaMin and area>areaMin+1000 or area>areaMax:
                peri = cv2.arcLength(cnt, True)

                approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)

                x, y, w, h = cv2.boundingRect(approx)
                cv2.rectangle(self.ROI, (x, y), (x + w, y + h), (255, 0, 0), 5)
                # imgDil = imgDil[0:400,200:400]
                cv2.imshow("img2 cutte", imgDil)
                img_sub = (cv2.subtract(self.img, self.img2))
                print(f"the average is ======={np.average(img_sub)}")

                cv2.putText(self.ROI, "Points: " + str(len(approx)), (x + w - 200, y + 80), cv2.FONT_HERSHEY_COMPLEX,
                            .7,
                            (200, 255, 200), 2)
                cv2.putText(self.ROI, "Area: " + str(int(area)), (x + w - 200, y + 110), cv2.FONT_HERSHEY_COMPLEX, 0.7,
                            (255, 0, 0), 2)



                if x<(self.end.shape[1]):
                    self.Bad()

        boxes_ids = track.update(detections)
        for box_id in boxes_ids:
            x, y, w, h, id = box_id
            cv2.putText(self.ROI, str(id), (x, y - 15), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
            cv2.rectangle(self.ROI, (x, y), (x + w, y + h), (0, 255, 0), 3)


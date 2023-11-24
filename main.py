import os
import cv2
from cvzone.HandTrackingModule import HandDetector
import numpy as np

# Variables
width,height = 1280, 720

folderPath = "Presentation"

# Camera Setup
cap = cv2.VideoCapture(0)
cap.set(3,width)
cap.set(4,height)

# List of Presentation Images
pathImages = sorted(os.listdir(folderPath), key=len)


# Variables
imgNumber = 0
hs, ws = int(120 * 1), int(213 * 1)
gestureThreshold = 300
buttonPressed = False
buttoncounter = 0
buttondelay = 30
annotation = [[]]
annotationNumber = -1
annotationStart = False


# Hand Detector
detector = HandDetector(detectionCon=0.8,maxHands=1)


while True:
    # Import Images

    success,img = cap.read()
    img = cv2.flip(img, 1)
    pathFullImage = os.path.join(folderPath,pathImages[imgNumber])
    imgCurrent = cv2.imread(pathFullImage)

    hands, img = detector.findHands(img)
    cv2.line(img,(0,gestureThreshold),(width,gestureThreshold),(0,255,0),1)

    if hands and buttonPressed is False:
        hand = hands[0]
        fingers = detector.fingersUp(hand)
        cx , cy = hand['center']
        # lmlist -> land mark list
        lmList = hand['lmList']

        # Constraints Values for easier drawing
        xVal = int(np.interp(lmList[8][0], [width // 2 , width], [0,width]))
        yVal = int(np.interp(lmList[8][1],[150,height -150],[0,height]))
        indexFinger = lmList[8][0],lmList[8][1]

        # if hand is at the height of the face
        if cy <= gestureThreshold:
            annotationStart = False
            # Gesture 1- left
            if fingers == [1,0,0,0,0]:
                annotationNumber = False
                print("Left")

                if imgNumber > 0:
                    buttonPressed = True
                    annotation = [[]]
                    annotationNumber = -1
                    imgNumber -= 1

            # Gesture 2 - Right
            if fingers == [0, 0, 0, 0, 1]:
                annotationNumber = False
                print("Right")

                if imgNumber < len(pathImages):
                    buttonPressed = True
                    annotation = [[]]
                    annotationNumber = -1
                    imgNumber +=1

         # Gesture 3 -Show  Pointer

        if fingers ==[0,1,1,0,0]:
            cv2.circle(imgCurrent,indexFinger ,12,(0,0,255),cv2.FILLED)
            annotationStart = False

        # Gesture 4 - Draw Circle
        if fingers == [0,1,0,0,0]:
            if annotationStart is False:
                annotationStart = True
                annotationNumber += 1
                annotation.append([])
            cv2.circle(imgCurrent, indexFinger, 12, (0, 0, 255), cv2.FILLED)
            annotation[annotationNumber].append(indexFinger)

        else:
            annotationStart = False

        #Gesture 5 - Erase
        if fingers==[0,1,1,1,0]:
            if annotation:
                if annotationNumber >= 0:
                    annotation.pop(-1)
                    annotationNumber -=1
                    buttonPressed = True
    else:
        annotationStart = False


    # Button Press Iteration
    if buttonPressed:
        buttoncounter +=1
        if buttoncounter > buttondelay:
            buttoncounter = 0
            buttonPressed = False

    for i in range(len(annotation)):
        for j in range(len(annotation[i])):
            if j!=0:
                cv2.line(imgCurrent,annotation[i][j-1],annotation[i][j],(0,0,200),12)

    # Adding webcam image on the slides
    imgSmall = cv2.resize(img,(ws,hs))
    h, w , _ = imgCurrent.shape
    imgCurrent[0:hs,w - ws:w]=imgSmall




    cv2.imshow("Image",img)
    cv2.imshow("Slides", imgCurrent)
    key=cv2.waitKey(1)

    if key == ord('q'):
        break
# Release the camera and close OpenCV windows

cap.release()
cv2.destroyAllWindows()

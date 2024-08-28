import cv2
import numpy as np
from cvzone.HandTrackingModule import HandDetector
import math
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)
volumeRange = volume.GetVolumeRange() #-96.0, 0.0
minVolume = volumeRange[0]
maxVolume = volumeRange[1]

vol = 0

hCam, wCam = 480, 720

url = 'http://192.168.1.10:4747/video'

cam = cv2.VideoCapture(0)
cam.set(3, wCam) #width
cam.set(4, hCam) #height

detector = HandDetector(maxHands= 1, detectionCon= 0.8)

while True:
    success, img = cam.read()

    hands, img = detector.findHands(img)

  
    

    if len(hands) != 0:
        lmList = detector.fingersUp(hands[0])

        if lmList[0] and lmList[1] == 1:
            # plmList = detector.findPosition(img, draw=False)

            # print(hands[0]['lmList'][4][1])

            x1, y1 = hands[0]['lmList'][4][0], hands[0]['lmList'][4][1]
            x2, y2 = hands[0]['lmList'][8][0], hands[0]['lmList'][8][1]
            cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

            cv2.circle(img, (x1, y1), 13, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), 13, (255, 0, 255), cv2.FILLED)
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
            cv2.circle(img, (cx, cy), 13, (255, 0, 255), cv2.FILLED)

            length = math.hypot(x2 - x1, y2 - y1)

            vol = np.interp(length, [50, 270], [minVolume, maxVolume])
            volPer = np.interp(length, [50, 270], [0, 100])

            print(vol)

            volume.SetMasterVolumeLevel(vol, None)

            cv2.putText(img, f'Volume: {int(volPer)} %', (400, 70), cv2.FONT_HERSHEY_PLAIN,
                 1, (255, 0, 0), 3)


            if length < 50:
                cv2.circle(img, (cx, cy), 13, (0, 0, 255), cv2.FILLED)





 
            # print(length)
            # print(hands)


    cv2.imshow("Image",img)
    cv2.waitKey(1)

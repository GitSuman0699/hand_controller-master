import cv2 
from cvzone.HandTrackingModule import HandDetector

# Height and width of cam window
hCam, wCam = 720, 1280

url = 'http://192.168.1.10:4747/video'

#webcam
cap = cv2.VideoCapture(url)
cap.set(3, hCam)
cap.set(4, hCam)

#hand detector
detector = HandDetector(maxHands=1, detectionCon=0.8)
count = 0
while True:
    # Get the web cam
    success, img = cap.read()
    # Hands
    hands, img = detector.findHands(img=img)
    print(hands)
    # Printing hand with tracking
  
    count = 0

    if len(hands) != 0 :
     lmList = detector.fingersUp(myHand=hands[0])

     count = lmList.count(1)

    cv2.putText(img, str(count), (400, 70), cv2.FONT_HERSHEY_PLAIN,
                3, (255, 0, 0), 3)

    cv2.imshow("Image", img)
    cv2.waitKey(1)

    # print(lmList[])


import cv2
from cvzone.HandTrackingModule import HandDetector
import numpy as np
import math
import time

cap = cv2.VideoCapture(0)
detector = HandDetector(maxHands=2)  # Allow two hands
offset = 20
imgSize = 300
counter = 0

folder = "D:/Sign-Language-detection/Data/nice"

while True:
    success, img = cap.read()
    hands, img = detector.findHands(img)

    if hands:  
        imgWhite = np.ones((imgSize, imgSize, 3), np.uint8) * 255
        
        for i, hand in enumerate(hands):  # Loop through detected hands
            x, y, w, h = hand['bbox']

            imgCrop = img[y - offset:y + h + offset, x - offset:x + w + offset]
            aspectRatio = h / w

            if aspectRatio > 1:
                k = imgSize / h
                wCal = math.ceil(k * w)
                imgResize = cv2.resize(imgCrop, (wCal, imgSize))
                wGap = math.ceil((imgSize - wCal) / 2)
                imgWhite[:, wGap: wCal + wGap] = imgResize
            else:
                k = imgSize / w
                hCal = math.ceil(k * h)
                imgResize = cv2.resize(imgCrop, (imgSize, hCal))
                hGap = math.ceil((imgSize - hCal) / 2)
                imgWhite[hGap: hCal + hGap, :] = imgResize

            cv2.imshow(f'Hand {i + 1} Crop', imgCrop)
            cv2.imshow(f'Hand {i + 1} White', imgWhite)

    cv2.imshow('Image', img)
    key = cv2.waitKey(1)

    if key == ord("s") and hands:
        for i, hand in enumerate(hands):
            x, y, w, h = hand['bbox']
            imgCrop = img[y - offset:y + h + offset, x - offset:x + w + offset]

            # Resize and save each hand
            imgCrop = cv2.resize(imgCrop, (imgSize, imgSize))
            cv2.imwrite(f'{folder}/Hand_{i + 1}_{time.time()}.jpg', imgCrop)

        counter += 1
        print(f"Captured {counter} images")

cap.release()
cv2.destroyAllWindows()

import cv2
import numpy as np
import time
import pyautogui          # Can be installed using "pip install pyautogui"
import HandTracking as ht 
import autopy             # Can be installed using "pip install autopy"


### Variables Declaration
pTime = 0               # Used to calculate frame rate
width = 640             # Width of Camera
height = 480            # Height of Camera
frameR = 100            # Frame Rate
smoothening = 10         # Smoothening Factor
prev_x, prev_y = 0, 0   # Previous coordinates
curr_x, curr_y = 0, 0   # Current coordinates

cap = cv2.VideoCapture(0)   # Getting video feed from the webcam
cap.set(3, width)           # Adjusting size
cap.set(4, height)

detector = ht.handDetector(maxHands=1)                  # Detecting one hand at max
screen_width, screen_height = autopy.screen.size()      # Getting the screen size


while True:
    success, img = cap.read()
    img = detector.findHands(img)                       # Finding the hand
    lmlist, bbox = detector.findPosition(img)           # Getting position of hand

    if len(lmlist)!=0:
        x1, y1 = lmlist[8][1:]
        x2, y2 = lmlist[12][1:]

        fingers = detector.fingersUp()                                                              # Checking if fingers are upwards
        cv2.rectangle(img, (frameR, frameR), (width - frameR, height - frameR), (255, 0, 255), 2)   # Creating boundary box
        



        #Move coursor if finger 1 is up
        if fingers[1] == 1 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 0:     
            x3 = np.interp(x1, (frameR,width-frameR), (0,screen_width))
            y3 = np.interp(y1, (frameR, height-frameR), (0, screen_height))

            curr_x = prev_x + (x3 - prev_x)/smoothening
            curr_y = prev_y + (y3 - prev_y) / smoothening

            autopy.mouse.move(screen_width - curr_x, curr_y)                            # Moving the cursor
            cv2.circle(img, (x1, y1), 7, (255, 0, 255), cv2.FILLED)
            prev_x, prev_y = curr_x, curr_y


        # Double click if four or five finger are up
        if fingers[0]==1 and fingers[1] == 1 and fingers[2]==1 and fingers[3]==1 and fingers[4]==1:     
          pyautogui.click(button='left',clicks=2, interval=0.25) 


         # Right click if 3 finger is up
        elif fingers[1] == 1 and fingers[2]==1 and fingers[3]==1 and fingers[4]==0:  
         pyautogui.click(button='right',clicks=1, interval=0.5)
                

         # Leftclick ff fore finger & middle finger both are up
        elif fingers[1] == 1 and fingers[2] == 1: 
            length, img, lineInfo = detector.findDistance(8, 12, img)

            if length < 40:     # If both fingers are really close to each other
                cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (0, 255, 0), cv2.FILLED)
                pyautogui.click(button='left',clicks=1, interval=0.25) # Perform Click

        #Scroll
        if fingers[0] == 1 and fingers[1] == 0 and fingers[2]==0 and fingers[3]==0 and fingers[4]==0:   
            pyautogui.scroll(120)

        if fingers[0] == 0 and fingers[1] == 0 and fingers[2]==0 and fingers[3]==0 and fingers[4]==0:    
            pyautogui.scroll(-120) 




    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
    cv2.imshow("Image", img)
    cv2.waitKey(1)
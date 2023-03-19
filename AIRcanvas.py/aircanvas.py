import cv2
import numpy as np
from collections import deque

def princess(x):
    print("")

cv2.namedWindow("bars")

cv2.createTrackbar("upper_hue","bars",128,100,princess)
cv2.createTrackbar("upper_saturation","bars",255,5,princess)
cv2.createTrackbar("upper_value","bars",255,255,princess)
cv2.createTrackbar("lower_saturation","bars",50,180,princess)
cv2.createTrackbar("lower_hue","bars",90,255,princess)
cv2.createTrackbar("lower_value","bars",70,255,princess)

bpoints=[deque(maxlen=1024)]
gpoints=[deque(maxlen=1024)]
rpoints=[deque(maxlen=1024)]
ypoints=[deque(maxlen=1024)]

blue_index=0
green_index=0
red_index=0
yellow_index=0

kernel=np.ones((5,5),np.uint8)

colors=[[255,0,0],[0,255,0],[0,0,255],[0,255,255]]
colorIndex=0

paintWindow=np.zeros((500,600,3))+255
paintWindow=cv2.rectangle(paintWindow,(40,1),(140,65),(0,0,0),2)
paintWindow=cv2.rectangle(paintWindow,(160,1),(255,65),colors[0],2)
paintWindow=cv2.rectangle(paintWindow,(275,1),(370,65),colors[1],2)
paintWindow=cv2.rectangle(paintWindow,(390,1),(485,65),colors[2],2)
paintWindow=cv2.rectangle(paintWindow,(565,1),(600,65),colors[3],2)

cv2.putText(paintWindow,"CLEAR",(49,33),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,0),2)
cv2.putText(paintWindow,"BLUE",(185,33),cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,255,255),2)
cv2.putText(paintWindow,"GREEN",(298,33),cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,255,255),2)
cv2.putText(paintWindow,"RED",(420,33),cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,255,255),2)
cv2.putText(paintWindow,"YELLOW",(520,33),cv2.FONT_HERSHEY_SIMPLEX,0.5,(150,150,150),2)
cv2.namedWindow("Paint",cv2.WINDOW_AUTOSIZE)

cap=cv2.VideoCapture(0)

while True:
    ret,frame=cap.read()
    frame=cv2.flip(frame,1)
    hsv=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    
    upper_hue=cv2.getTrackbarPos("upper_hue","bars")
    upper_saturation=cv2.getTrackbarPos("upper_saturation","bars")
    upper_value=cv2.getTrackbarPos("upper_value","bars")
    lower_hue=cv2.getTrackbarPos("lower_hue","bars")
    lower_saturation=cv2.getTrackbarPos("lower_saturation","bars")
    lower_value=cv2.getTrackbarPos("lower_value","bars")
      
    upper_hsv=np.array([upper_hue,upper_saturation,upper_value])
    lower_hsv=np.array([lower_hue,lower_saturation,lower_value])
    
    frame=cv2.rectangle(frame,(40,1),(140,65),(0,0,0),-1)
    frame=cv2.rectangle(frame,(160,1),(255,65),colors[0],-1)
    frame=cv2.rectangle(frame,(275,1),(370,65),colors[1],-1)
    frame=cv2.rectangle(frame,(390,1),(485,65),colors[2],-1)
    frame=cv2.rectangle(frame,(505,1),(600,65),colors[3],-1)

    cv2.putText(frame, "CLEAR ALL", (49, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(frame, "BLUE", (185, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(frame, "GREEN", (298, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(frame, "RED", (420, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(frame, "YELLOW", (520, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (150,150,150), 2, cv2.LINE_AA)



    mask=cv2.inRange(hsv,lower_hsv,upper_hsv)
    mask=cv2.erode(mask,kernel,iterations=1)
    mask=cv2.morphologyEx(mask,cv2.MORPH_OPEN,kernel)
    mask=cv2.dilate(mask,kernel,iterations=1)

    cnts,_=cv2.findContours(mask.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    center=None

    if len(cnts)>0:
        cnts=sorted(cnts,key=cv2.contourArea,reverse=True)[0]
        ((x,y),radius)=cv2.minEnclosingCircle(cnts)

        cv2.circle(frame,(int(x),int(y)),int(radius),(0,255,255),2)
        M = cv2.moments(cnts)
        center = (int(M['m10'] / M['m00']), int(M['m01'] / M['m00']))

        if center[1]==65:
            if 40 <= center[0] <=140:
                bpoints=[deque(maxlen=512)]
                gpoints=[deque(maxlen=512)]
                rpoints=[deque(maxlen=512)]
                ypoints=[deque(maxlen=512)]

                blue_index=0
                green_index=0
                yellow_index=0
                red_index=0

                paintWindow[67:,:,:]=255
            elif 160<=center[0]<=255:
                colorIndex=0
            elif 275<=center[0]<=370:
                colorIndex=1
            elif 390<=center[0]<=485:
                colorIndex=2
            elif 585<=center[0]<=600:
                colorIndex=3
        else:
            if colorIndex==0:
                bpoints[blue_index].appendleft(center)
            elif colorIndex==1:
                gpoints[green_index].appendleft(center)
            elif colorIndex==2:
                rpoints[red_index].appendleft(center)
            elif colorIndex==3:
                ypoints[yellow_index].appendleft(center)
    else:
        bpoints.append(deque(maxlen=512))
        blue_index+=1
        gpoints.append(deque(maxlen=512))
        green_index+=1
        rpoints.append(deque(maxlen=512))
        red_index+=1
        ypoints.append(deque(maxlen=512))
        yellow_index+=1

    points=[bpoints,gpoints,rpoints,ypoints]
    for i in range(len(points)):
        for j in range(len(points[i])):
            for k in range(1,len(points[i][j])):
                if points[i][j][k-1] is None or points[i][j][k] is None:
                    continue
                cv2.line(frame,points[i][j][k-1],points[i][j][k],colors[i],2)
                cv2.line(paintWindow,points[i][j][k-1],points[i][j][k],colors[i],2)

    cv2.imshow('track',frame)
    cv2.imshow('paint',paintWindow)
    cv2.imshow('mask',mask)

    if cv2.waitKey(4)==ord('q'):
        break

cap.release()
cv2.destroyAllWindows()



        
import cv2
import apriltag
import math
from motorcontrol import move
#from .../motor-control/motor-control.py import moveup, moveback, movestop

'''
0 - foward
1 - stop
2 - reverse
3 - right
4 - left
'''
LINE_LENGTH = 5
CENTER_COLOR = (0, 255, 0)
CORNER_COLOR = (255, 0, 255)

#crosshair for apriltag
def plotPoint(image, center, color):
    center = (int(center[0]), int(center[1]))
    image = cv2.line(image,
                     (center[0] - LINE_LENGTH, center[1]),
                     (center[0] + LINE_LENGTH, center[1]),
                     color,
                     3)
    image = cv2.line(image,
                     (center[0], center[1] - LINE_LENGTH),
                     (center[0], center[1] + LINE_LENGTH),
                     color,
                     3)
    return image

#id of apriltag
def plotText(image, center, color, text):
    center = (int(center[0]) + 4, int(center[1]) - 4)
    return cv2.putText(image, str(text), center, cv2.FONT_HERSHEY_SIMPLEX,
                       1, color, 3)

detector = apriltag.Detector()
cam = cv2.VideoCapture(0)

looping = True
cornersList = [[0,0],[0,0],[0,0],[0,0]]
while looping:
    result, image = cam.read()
    grayimg = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    detections = detector.detect(grayimg)
    if not detections:
        pass
    else:
        for detect in detections:
            cornersList.clear()
            #print("tag_id: %s, center: %s" % (detect.tag_id, detect.center))
            image = plotPoint(image, detect.center, CENTER_COLOR)
            image = plotText(image, detect.center, CENTER_COLOR, detect.tag_id)
            for corner in detect.corners:
                print("Added {}".format(corner))
                cornersList.append(corner)
                image = plotPoint(image, corner, CORNER_COLOR)
            print((cornersList[0][0]-cornersList[1][0]))
            if(abs((cornersList[0][0]-cornersList[1][0]))<=300):
                #print("MOVING UP")
                move(0)
            elif(abs((cornersList[0][0]-cornersList[1][0]))>300):
                #print("STOPPING")
                move(1)
                looping=False
    cv2.imshow('Result', image)
    key = cv2.waitKey(100)
    if key == 13: #press return
        looping = False

cv2.destroyAllWindows()

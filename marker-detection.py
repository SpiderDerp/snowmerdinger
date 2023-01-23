import cv2
import numpy as np
from apriltag import apriltag


vid = cv2.VideoCapture(1)
detector = apriltag("tagStandard52h13")


while True:
    
    ret, frame = vid.read()

    image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    detections = detector.detect(image)

    cv2.imshow('frame', image)
    
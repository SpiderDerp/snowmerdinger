import cv2
import numpy as np
from apriltag import apriltag

imagepath = 'tags/tag52_13_00001.png'
image = cv2.imread(imagepath, cv2.IMREAD_GRAYSCALE)
detector = apriltag("tagStandard52h13")

detections = detector.detect(image)
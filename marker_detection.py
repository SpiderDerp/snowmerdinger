import cv2
import numpy as np
from pupil_apriltags import Detector


vid = cv2.VideoCapture(0)

at_detector = Detector(
   families="tagStandard52h13",
   nthreads=1,
   quad_decimate=1.0,
   quad_sigma=0.0,
   refine_edges=1,
   decode_sharpening=0.25,
   debug=0
)


while True:
   ret, frame = vid.read()
   cv2.imshow('frame', frame)
   image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
   detections = at_detector.detect(image)

   cv2.imshow('frame', image)

   if cv2.waitKey(1) & 0xFF == ord('q'):
      break
    
import matplotlib
matplotlib.use('tkagg')
import matplotlib.pyplot as plt 
import cv2
import numpy as np
from pupil_apriltags import Detector
import copy
import time



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

def gen_perp(x, y, i): #function generates perpendicular line assuming the plot is a square


    slope = abs((y[2] - y[1])/(x[2] - x[1]))
    perp_slop = -1/slope

    intercept = y[i] - perp_slop * x[i]
    xMin = min(x[1], x[2])
    xMax = max(x[1], x[2])
    xSeries = np.array([xMin, xMax])
    ySeries = perp_slop * xSeries + intercept

    return xSeries, ySeries


def draw_tags(
    image,
    tags
):
	x = [0]
	z = [0]
	for tag in tags:
		tag_family = tag.tag_family
		tag_id = tag.tag_id
		center = tag.center
		corners = tag.corners
		dist = '%.2f'%tag.pose_t[2] #gets the z-coordinate 

		center = (int(center[0]), int(center[1]))
		corner_01 = (int(corners[0][0]), int(corners[0][1]))
		corner_02 = (int(corners[1][0]), int(corners[1][1]))
		corner_03 = (int(corners[2][0]), int(corners[2][1]))    
		corner_04 = (int(corners[3][0]), int(corners[3][1]))

		cv2.circle(image, (center[0], center[1]), 5, (0, 0, 255), 2)

		cv2.line(image, (corner_01[0], corner_01[1]),
				(corner_02[0], corner_02[1]), (255, 0, 0), 2)
		cv2.line(image, (corner_02[0], corner_02[1]),
				(corner_03[0], corner_03[1]), (255, 0, 0), 2)
		cv2.line(image, (corner_03[0], corner_03[1]),
				(corner_04[0], corner_04[1]), (0, 255, 0), 2)
		cv2.line(image, (corner_04[0], corner_04[1]),
				(corner_01[0], corner_01[1]), (0, 255, 0), 2)

		cv2.putText(image, f"{tag_id}", (center[0] - 10, center[1] - 10),
					cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2, cv2.LINE_AA)

		cv2.putText(image, f"{dist}", (center[0] - 30, center[1] - 30),
					cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2, cv2.LINE_AA)

		x.append(float('%.2f'%(tag.pose_t[0] - 0.16))) # change 0.16 based on the values, it is half the max x-value and ensures that the camera is at x=0
		z.append(float('%.2f'%tag.pose_t[2]))
		
	return image, x, z

plt.ion()
x = np.array(0)
z = np.array(0)

figure, ax = plt.subplots(figsize=(10, 10))
line1 = ax.scatter(x, z)
#ax.axis('scaled')

while True:
    ret, image = vid.read()

    debug_image = copy.deepcopy(image)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    tags = at_detector.detect(
        image,
        estimate_tag_pose=True,
        camera_params= (640, 480, 1, 1),
        tag_size=0.0508
    )

    debug_image, x, z = draw_tags(debug_image, tags)    

    ax.clear()
    ax.scatter(x,z)
    ax.plot(x[1:], z[1:], 'b--')

    """
    if (len(x) > 2 and len(z) > 2):
        try:
            xSeries, ySeries = gen_perp(x, z, 1)
            print("Line 1", xSeries, ySeries)
            ax.plot(xSeries, ySeries, 'r--')
            xSeries, ySeries = gen_perp(x, z, 2)
            print("Line 2", xSeries, ySeries)
            ax.plot(xSeries, ySeries, 'r--')
        except:
            pass
    """

    ax.plot()
    print(x)	
    figure.canvas.draw()
    figure.canvas.flush_events()
    time.sleep(0.1)

    cv2.imshow('frame', debug_image)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
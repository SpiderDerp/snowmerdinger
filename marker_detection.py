import matplotlib
matplotlib.use('tkagg')
import matplotlib.pyplot as plt 
import cv2
import numpy as np
from pupil_apriltags import Detector
import copy



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
		x.append(int(float('%.2f'%tag.pose_t[0])*(18/0.64)))
		z.append(int(float('%.2f'%tag.pose_t[2])*(18/0.64)))
		
	return image, x, z

plt.ion()
x = np.array(0)
z = np.array(0)
line1, = plt.plot(x, z, 'bo')

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

    print(x, z)
    line1.set_xdata(x)
    line1.set_ydata(z)
    plt.draw()

    cv2.imshow('frame', debug_image)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    


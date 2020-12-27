"""
This script allows to create the student database by capturing
student faces and storing them into database folder.
"""

import cv2, sys, numpy, os, time
from picamera.array import PiRGBArray
from picamera import PiCamera
count = 0
size = 4
fn_haar = 'haarcascade_frontalface_default.xml'
fn_dir = 'database'
fn_name = raw_input("Enter student roll no: ")
path = os.path.join(fn_dir, fn_name)
(im_width, im_height) = (112, 92)
haar_cascade = cv2.CascadeClassifier(fn_haar)
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))
time.sleep(0.1)


for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    try:    
		image = frame.array
		im = cv2.flip(image, 1, 0)
		gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
		mini = cv2.resize(gray, (gray.shape[1] / size, gray.shape[0] / size))
		faces = haar_cascade.detectMultiScale(mini)
		faces = sorted(faces, key=lambda x: x[3])
		
		if faces:
			face_i = faces[0]
			(x, y, w, h) = [v * size for v in face_i]
			face = gray[y:y + h, x:x + w]
			face_resize = cv2.resize(face, (im_width, im_height))
			filename="/home/pi/Desktop/attendence_sys/database/"+str(fn_name)+"_"+str(count)+".png"
			cv2.imwrite(filename, face_resize)
			cv2.rectangle(im, (x, y), (x + w, y + h), (0, 255, 0), 3)
			cv2.putText(im, fn_name, (x - 10, y - 10), cv2.FONT_HERSHEY_PLAIN,
				1,(0, 255, 0))
		time.sleep(0.38)        
		count += 1
	   
		cv2.imshow('OpenCV', im)
		key = cv2.waitKey(10)
		if key == ord("q") or count > 20:
			break
		rawCapture.truncate(0)
	except Exception as e:
            print(e)
print str(count)

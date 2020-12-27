"""
This script allows to detect multiple faces at realtime and 
saving them into database folder.  
"""

from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import multiprocessing
from datetime import datetime

timee=datetime.now().strftime('%H')
sb_name = raw_input("Enter subject name: ")
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))
size=4
face_cascade = cv2.CascadeClassifier('/home/pi/attendence_sys/haarcascade_frontalface_default.xml')
time.sleep(0.1)
count=0

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    try:    
        count=count+1
        image = frame.array
        gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(gray, 1.1, 5)
        print "Found "+str(len(faces))+" face(s)"
        for (x, y, w, h) in faces:
                cv2.rectangle(image,(x,y),(x+w,y+h),(255,255,0),2)
                sub_face = gray[y:y+h, x:x+w]
                FaceFileName = "/home/pi/Desktop/attendence_sys/live/"+str(sb_name)+"_"+str(timee)+"_"+str(count) + ".png"
                cv2.imwrite(FaceFileName, sub_face)
                
        cv2.imshow("Frame", image)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q") or count > 20:
                break
        rawCapture.truncate(0)
        time.sleep(0.5)
    except Exception as e:
            print(e)

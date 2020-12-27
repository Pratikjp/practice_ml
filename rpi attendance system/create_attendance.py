"""
This script taking live captured images from live folder
and and stores the attendance in mysql db for a given subject.  
"""

import cv2, os
import numpy as np
from PIL import Image
import time
import datetime
import MySQLdb
from datetime import datetime

global c
global db



def diff(first,second):
    second = set(second)
    return [item for item in first if item not in second]
	
def main():
    insert_to_db()
    
def insert_to_db():
    query = "INSERT INTO attendance_sys(`Date`, `Subject`, `Present`, `Absent`) VALUES ('%s', '%s', '%s', '%s')" % (current_date,sb_name,present,absent)
    try:
       c.execute(query)
       db.commit()
    except:
       print "failed"
    
def get_images_and_labels(path):
    
    image_paths = [os.path.join(path, f) for f in os.listdir(path) ]
    #print image_paths
    images = []
   
    labels = []

    for image_path in image_paths:
        image_pil = Image.open(image_path).convert('L')
        image = np.array(image_pil, 'uint8')
        #
        head, tail = os.path.split(image_path)
        taill=tail.split("_")[0]
        images.append(image)
        labels.append(int(taill))
        cv2.waitKey(50)
    return images,labels
	
	
cascadePath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath)
recognizer = cv2.face.createLBPHFaceRecognizer()
roll_nos=[ i for i in range(1,65)]
present=[]
absent=[]

if __name__ == '__main__':
	#input subject name
	sb_name = raw_input("Enter subject name: ")
	current_date=datetime.now().strftime("%y-%m-%d")
	#get the training images 
	path = '/home/pi/Desktop/attendence_sys/database/'
	images, labels=get_images_and_labels(path)
	#train the model
	recognizer.train(images, np.array(labels))
	live_path='/home/pi/Desktop/attendence_sys/live/'
	image_paths = [os.path.join(live_path, f) for f in os.listdir(live_path)]

	for image_path in image_paths:
		predict_image_pil = Image.open(image_path).convert('L')
		predict_image = np.array(predict_image_pil, 'uint8')
		#predict
		nbr_predicted, conf = recognizer.predict(predict_image)
		#print (nbr_predicted,conf)
		present.append(nbr_predicted)
		#cv2.imshow("Recognizing Face", predict_image)
		cv2.waitKey(1000)

	absent=diff(roll_nos,present)
	present=list(set(present))
    try:
        db = MySQLdb.connect("localhost","root","asd","attendance")
        c= db.cursor()
    except Exception as e:
        print e
             
    try:
      main()
    except KeyboardInterrupt:
      print "bye bye..."
      pass    

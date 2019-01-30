#import libraries of python op
import paho.mqtt.client as client
import paho.mqtt.publish as publish
import cv2
import numpy as np
import time
import logging
from picamera.array import PiRGBArray
from picamera import PiCamera


logging.basicConfig(filename='./spooty.log', format='%(asctime)s %(message)s', level=logging.INFO)
#create VideoCapture object and read from video file
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))
time.sleep(0.1)
#use trained cars XML classifiers
car_cascade = cv2.CascadeClassifier('cars.xml')

#read until video is completed
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    #capture frame by frame
    
    image = frame.array

    (w,h ) = image.shape[:2]
    center = w/2
    #M = cv2.getRotationMatrix2D(center, 90, 1)
    #image = cv2.warpAffine(image, M, (w, h))

    #convert video into gray scale of each frames
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    #detect cars in the video
    cars = car_cascade.detectMultiScale(gray, 1.1, 3)

    #to draw arectangle in each cars 
    for (x,y,w,h) in cars:
        cv2.rectangle(image,(x,y),(x+w,y+h),(0,255,0),2)
        print("x: {}, x+w: {}, obsah: {}".format(x, x+w, w*h))
        logging.info("W: {}, H: {}".format(w, h))

        lng1 = center - x
        lng2 = (x + w) - center

        if lng1 > lng2:
            print("Sending RIGHT THREAT")
            publish.single("command", "r", hostname="raspberrypi")
            time.sleep(1)
            publish.single("command", "0", hostname="raspberrypi")
        else:
            print("Sending LEFT THREAT")
            publish.single("command", "l", hostname="raspberrypi")
            time.sleep(1)
            publish.single("command", "0", hostname="raspberrypi")

    #display the resulting frame
    #cv2.imshow('video', image)
    rawCapture.truncate(0)
    #press Q on keyboard to exit
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break
#release the videocapture object
    
cap.release()
#close all the frames
cv2.destroyAllWindows()

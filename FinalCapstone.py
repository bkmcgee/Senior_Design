import time
import RPi.GPIO as GPIO
import _thread
from threading import Thread
import cv2
import numpy as np
from picamera.array import PiRGBArray
from picamera import PiCamera
from PIL import Image
import logging
import threading

GPIO.setmode(GPIO.BCM)
#Camera setup for video and overlays
camera = PiCamera()
camera.resolution = (800, 480)
camera.framerate = 32
img = Image.open('bg_overlay480x320.png')
img_overlay=camera.add_overlay(img.tobytes(),size=img.size)
img_overlay.alpha=128
img_overlay.layer=3
rawCapture = PiRGBArray(camera, size=(800, 480))
kernel = np.ones((2,2),np.uint8)
event = threading.Event()
#GPIO Pin Setup for Sensors & Buzzers

TRIG_1 = 17
ECHO_1 = 27
TRIG_2 = 22
ECHO_2 = 10
TRIG_3 = 9
ECHO_3 = 11
Left_buzzer = 20
Right_buzzer = 21

GPIO.setup(TRIG_1,GPIO.OUT)                  #Set pin as GPIO out
GPIO.setup(ECHO_1,GPIO.IN)                   #Set pin as GPIO in
GPIO.setup(TRIG_2,GPIO.OUT)                  #Set pin as GPIO out
GPIO.setup(ECHO_2,GPIO.IN)                   #Set pin as GPIO in
GPIO.setup(TRIG_3,GPIO.OUT)                  #Set pin as GPIO out
GPIO.setup(ECHO_3,GPIO.IN)                   #Set pin as GPIO in
GPIO.setup(Left_buzzer,GPIO.OUT)                  #Set pin as GPIO out
GPIO.setup(Right_buzzer,GPIO.OUT)                   #Set pin as GPIO in

time.sleep(0.1)
# Main Execution Loop
for still in camera.capture_continuous(rawCapture, format= "bgr", use_video_port=True):

    # sensor warning overlays begin
    image = still.array
    overlay1 = image.copy()
    #color coded in BGR, not RGB
    #overlay rectangles that will contain warnings
    cv2.rectangle(image,(319,399),(479,479),(0,0,0),-1)
    cv2.rectangle(image,(0,399),(319,479),(0,0,0),4)
    cv2.rectangle(image,(481,399),(799,479),(0,0,0),4)
    opacity = 0.4
    cv2.addWeighted(overlay1,opacity,image,1-opacity,0,image)
    font = cv2.FONT_HERSHEY_DUPLEX
    while(1):

        GPIO.output(TRIG_1, False)                 #Set TRIG as LOW
        event.wait(.2)                            #Delay of 2 seconds

        GPIO.output(TRIG_1, True)                  #Set TRIG as HIGH
        event.wait(0.0000001)                      #Delay of 0.00001 seconds
        GPIO.output(TRIG_1, False)                 #Set TRIG as LOW

        while GPIO.input(ECHO_1)==0:               #Check if Echo is LOW
            pulse_start1 = time.time()             #Time of the last  LOW pulse

        while GPIO.input(ECHO_1)==1:               #Check whether Echo is HIGH
            pulse_end1 = time.time()                #Time of the last HIGH pulse
        pulse_duration1 = pulse_end1 - pulse_start1 #pulse duration to a variable

        GPIO.output(TRIG_2, True)                  #Set TRIG as HIGH
        event.wait(0.0000001)                      #Delay of 0.00001 seconds
        GPIO.output(TRIG_2, False)                 #Set TRIG as LOW

        while GPIO.input(ECHO_2)==0:               #Check if Echo is LOW
            pulse_start2 = time.time()              #Time of the last  LOW pulse

        while GPIO.input(ECHO_2)==1:               #Check whether Echo is HIGH
            pulse_end2 = time.time()                #Time of the last HIGH pulse
        pulse_duration2 = pulse_end2 - pulse_start2 #pulse duration to a variable

        GPIO.output(TRIG_3, True)                  #Set TRIG as HIGH
        event.wait(0.0000001)                      #Delay of 0.00001 seconds
        GPIO.output(TRIG_3, False)                 #Set TRIG as LOW

        while GPIO.input(ECHO_3)==0:               #Check if Echo is LOW
            pulse_start3 = time.time()              #Time of the last  LOW pulse

        while GPIO.input(ECHO_3)==1:               #Check whether Echo is HIGH
            pulse_end3 = time.time()                #Time of the last HIGH pulse
        pulse_duration3 = pulse_end3 - pulse_start3 #pulse duration to a variable

        distance1 = round(pulse_duration1 * 17150, 2)            #Round to two decimal points
        distance2 = round(pulse_duration2 * 17150, 2)            #Round to two decimal points
        distance3 = round(pulse_duration3 * 17150, 2)            #Round to two decimal points

        # create distances for each color to change & buzzer to sound
        if distance2 >= 5 and distance2 <= 40: #below 40 cm
                if distance2 < (distance1 and distance3):
                        cv2.putText(image,str(distance2),(379,439),font,0.5,(255,255,255),2,cv2.LINE_AA)
                        cv2.rectangle(image,(0,399),(319,479),(0,20,100),-1) #red rect
                        cv2.rectangle(image,(481,399),(799,479),(0,20,100),-1) #red rect
                        GPIO.output(Left_buzzer,True)
                        GPIO.output(Right_buzzer,True)
                        event.wait(0.5)                      #Delay of 0.00001 seconds
                        event.wait(0.5)                      #Delay of 0.00001 seconds
                        GPIO.output(Left_buzzer,False)
                        GPIO.output(Right_buzzer,False)
                        break
        if distance1 >= 5 and distance1 <= 40: #below 40 cm
                if distance1 < (distance2 and distance3):
                        cv2.putText(image,str(distance1),(379,439),font,0.5,(255,255,255),2,cv2.LINE_AA)
                        cv2.rectangle(image,(0,399),(319,479),(0,20,100),-1) #red rect
                        GPIO.output(Left_buzzer,True)
                        event.wait(0.5)                      #Delay of 0.00001 seconds
                        GPIO.output(Left_buzzer, False)
                        break
        if distance3 >= 5 and distance3 <= 40: #below 40 cm
                if distance3 < (distance1 and distance2):
                        cv2.putText(image,str(distance3),(379,439),font,0.5,(255,255,255),2,cv2.LINE_AA)
                        cv2.rectangle(image,(481,399),(799,479),(0,20,100),-1) #red rect
                        GPIO.output(Right_buzzer,True)                 #Set TRIG as HIGH
                        event.wait(0.5)                      #Delay of 0.00001 seconds
                        GPIO.output(Right_buzzer,False)
                        break

        if distance2 < 80 and distance2 > 40: #between 40 to 80 cm
                if distance2 < (distance1 and distance3):
                        cv2.putText(image,str(distance2),(379,439),font,0.5,(255,255,255),2,cv2.LINE_AA)
                        cv2.rectangle(image,(0,399),(319,479),(0,165,255),-1) #orange rect
                        cv2.rectangle(image,(481,399),(799,479),(0,165,255),-1) #orange rect
                        GPIO.output(Left_buzzer,True)
                        GPIO.output(Right_buzzer,True)
                        event.wait(0.5)                      #Delay of 0.00001 seconds
                        event.wait(0.5)                      #Delay of 0.00001 seconds
                        GPIO.output(Left_buzzer,False)
                        GPIO.output(Right_buzzer,False)
                        break
        if(distance1 < 80 and distance1 > 40): #between 40 to 80 cm
                if distance1 < (distance2 and distance3):
                        cv2.putText(image,str(distance1),(379,439),font,0.5,(255,255,255),2,cv2.LINE_AA)
                        cv2.rectangle(image,(0,399),(319,479),(0,165,255),-1) #orange rect
                        GPIO.output(Left_buzzer,True)
                        event.wait(0.5)                      #Delay of 0.00001 seconds
                        GPIO.output(Left_buzzer, False)                 #Set TRIG as LOW
                        break
                # RIGHT RECTANGLE OPTIONS insert here
        if distance3 < 80 and distance3 > 40: #between 40 to 80 cm
                if distance3 < (distance1 and distance2):
                        cv2.putText(image,str(distance3),(379,439),font,0.5,(255,255,255),2,cv2.LINE_AA)
                        cv2.rectangle(image,(481,399),(799,479),(0,165,255),-1) #orange rect
                        GPIO.output(Right_buzzer,True)                 #Set TRIG as HIGH
                        event.wait(0.5)                      #Delay of 0.00001 seconds
                        GPIO.output(Right_buzzer,False)
                        break
        #if distances exist, break out of while loop
        if(distance1 and distance2 and distance3): break
    # display options on 5" display to be fullscreen
    cv2.namedWindow("Display",cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("Display",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
    cv2.imshow("Display", image)
    rawCapture.truncate(0)
	# press 'q' key to stop video stream
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        cv2.destroyWindow("Display")
        break

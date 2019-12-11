
import RPi.GPIO as GPIO
import time
import _thread
from threading import Thread

GPIO.setwarnings(False)

GPIO.setmode(GPIO.BCM)

keepRunning = True
distance1= 0

GPIO_T1 = 18 # trigger left 1
GPIO_E1 = 24 # echo left 1
GPIO_T2 = 22 #trigg left 2
GPIO_E2 = 27
GPIO_T3 = 21
GPIO_E3 = 20
GPIO_T4 = 10
GPIO_E4 = 9
GPIO_B1 = 4 #buzzer 1
GPIO_B2= 17 # buzzer 2
GPIO_B3 = 16 #buzzer 3
GPIO_B4= 11 # buzzer 4

#trigger
GPIO.setup(GPIO_T1, GPIO.OUT)
GPIO.setup(GPIO_T2, GPIO.OUT)
GPIO.setup(GPIO_T3, GPIO.OUT)
GPIO.setup(GPIO_T4, GPIO.OUT)
#Echo
GPIO.setup(GPIO_E1, GPIO.IN)
GPIO.setup(GPIO_E2, GPIO.IN)
GPIO.setup(GPIO_E3, GPIO.IN)
GPIO.setup(GPIO_E4, GPIO.IN)
#Buzzer
GPIO.setup(GPIO_B1, GPIO.OUT)
GPIO.setup(GPIO_B2, GPIO.OUT)
GPIO.setup(GPIO_B3, GPIO.OUT)
GPIO.setup(GPIO_B4, GPIO.OUT)

def measureDistance1():
	GPIO.output(GPIO_T1, False)
	time.sleep(0.5)
	GPIO.output(GPIO_T1, True)
	time.sleep(0.00001)
	GPIO.output(GPIO_T1, False)
	start = time.time()
	while GPIO.input(GPIO_E1) == 0:
		start = time.time()

	while GPIO.input(GPIO_E1) ==1:
		stop = time.time()

	elapsed = stop-start
	distance1 = elapsed * 17150
	return distance1

def playSound1(threadName, delay):
	keepRunning	
	distance1
	while keepRunning:
		if distance1 <= 30:
			GPIO.output(GPIO_B1, True)
			time.sleep(0.01 * distance1)
			GPIO.output(GPIO_B1,False)
			time.sleep(0.05 * distance1)

		time.sleep(delay)
		
		
def measureDistance2():
	GPIO.output(GPIO_T2, False)
	time.sleep(0.5)
	GPIO.output(GPIO_T2, True)
	time.sleep(0.00001)
	GPIO.output(GPIO_T2, False)
	start = time.time()
	while GPIO.input(GPIO_E2) == 0:
		start = time.time()

	while GPIO.input(GPIO_E2) ==1:
		stop = time.time()

	elapsed = stop-start
	distance2 = elapsed * 17150
	return distance2
    
def playSound2(threadName, delay):
	keepRunning	
	distance2
	while keepRunning:
		if distance2 <= 30:
			GPIO.output(GPIO_B2, True)
			time.sleep(0.01 * distance2)
			GPIO.output(GPIO_B2,False)
			time.sleep(0.05 * distance2)

		time.sleep(delay)  
    
def measureDistance3():
	GPIO.output(GPIO_T3, False)
	time.sleep(0.5)
	GPIO.output(GPIO_T3, True)
	time.sleep(0.00001)
	GPIO.output(GPIO_T3, False)
	start = time.time()
	while GPIO.input(GPIO_E3) == 0:
		start = time.time()

	while GPIO.input(GPIO_E3) ==1:
		stop = time.time()

	elapsed = stop-start
	distance3 = elapsed * 17150
	return distance3
    
def playSound3(threadName, delay):
	keepRunning	
	distance3
	while keepRunning:
		if distance3 <= 30:
			GPIO.output(GPIO_B3, True)
			time.sleep(0.01 * distance3)
			GPIO.output(GPIO_B3,False)
			time.sleep(0.05 * distance3)

		time.sleep(delay)  
    
def measureDistance4():
	GPIO.output(GPIO_T4, False)
	time.sleep(0.5)
	GPIO.output(GPIO_T4, True)
	time.sleep(0.00001)
	GPIO.output(GPIO_T4, False)
	start = time.time()
	while GPIO.input(GPIO_E4) == 0:
		start = time.time()

	while GPIO.input(GPIO_E4) ==1:
		stop = time.time()

	elapsed = stop-start
	distance4 = elapsed * 17150
	return distance4
    
def playSound4(threadName, delay):
	keepRunning	
	distance4
	while keepRunning:
		if distance4 <= 30:
			GPIO.output(GPIO_B4, True)
			time.sleep(0.01 * distance4)
			GPIO.output(GPIO_B4,False)
			time.sleep(0.05 * distance4)

		time.sleep(delay)  
    
    
while(1):
	distance1 = measureDistance1()
	distance2 = measureDistance2()
	distance3 = measureDistance3()
	distance4 = measureDistance4()
	_thread.start_new_thread(playSound1, ("Buzzer1" , 0.01))
	_thread.start_new_thread(playSound2, ("Buzzer2" , 0.015))
	_thread.start_new_thread(playSound3, ("Buzzer3" , 0.012))
	_thread.start_new_thread(playSound4, ("Buzzer4" , 0.013))
	while True:
		print ("buzzer 1",distance1)
		print ("buzzer 2",distance2)
		print ("buzzer 3",distance3)
		print ("buzzer 4",distance4)
		time.sleep(0.5)
		distance1 = measureDistance1()
		time.sleep(0.5)
		distance2 = measureDistance2()
		time.sleep(0.5)
		distance3 = measureDistance3()
		time.sleep(0.5)
		distance4 = measureDistance4()
   

    



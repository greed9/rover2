import pigpio
import time
import pyrebase
import sys
import RPi.GPIO as GPIO


config = {"apiKey": "AIzaSyBc7qqxaJiXJ9FlZlDrEqdPoVyA1JM5vlY","authDomain": "learningserver-1abd7.firebaseapp.com","databaseURL": "https://learningserver-1abd7.firebaseio.com","projectId": "learningserver-1abd7","storageBucket": "learningserver-1abd7.appspot.com","messagingSenderId": "658436185485"}
firebase = pyrebase.initialize_app(config)
db = firebase.database()



"""___________________Variables___________________"""

#objects
gpio = pigpio.pi()
db = firebase.database()

#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)
 
#set GPIO Pins
GPIO_TRIGGER = 24
GPIO_ECHO = 25
 
#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

#SIGNALS
MAX_SIGNAL = 2000
MIN_SIGNAL = 1000
IDLE_SIGNAL = 1500
OFF_SIGNAL = 0
android_signal = 0



#PINS
LEFT_MOTOR_PIN = 23
RIGHT_MOTOR_PIN = 17


"""____________________FUNCTIONS____________________"""

#ESSENTIALS
def start():
	GPIO.setwarnings(False)
	idle()
	time.sleep(2)
	start_loop()
	stop()
	
def start_loop():
	is_running = True
	while is_running:
		dist = distance()
				
		speed_left = db.child("speedLeft").get()
		left_speed = speed_left.val()[-1]
		
		speed_right = db.child("speedRight").get()
		right_speed = speed_right.val()[-1]

		

		
		if dist <= 25:
			gpio.set_servo_pulsewidth(LEFT_MOTOR_PIN, 1800)
			gpio.set_servo_pulsewidth(RIGHT_MOTOR_PIN, 1800)
			time.sleep(1)
		else:	
			gpio.set_servo_pulsewidth(LEFT_MOTOR_PIN, float(right_speed))
			gpio.set_servo_pulsewidth(RIGHT_MOTOR_PIN, float(left_speed))	

		number_boolean = db.child("running").get()
		number = number_boolean.val()
		if number == 0:
			is_running = False


def distance():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
 
    return distance	


def stop():
	disarm()
	gpio.stop()
	sys.exit()


def idle():
	gpio.set_servo_pulsewidth(LEFT_MOTOR_PIN, IDLE_SIGNAL)
	gpio.set_servo_pulsewidth(RIGHT_MOTOR_PIN, IDLE_SIGNAL)
	
def disarm():
	gpio.set_servo_pulsewidth(LEFT_MOTOR_PIN, OFF_SIGNAL)
	gpio.set_servo_pulsewidth(RIGHT_MOTOR_PIN, OFF_SIGNAL)




"""____________________EXECUTION____________________"""
start()

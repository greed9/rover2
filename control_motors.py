import pigpio
import time
import pyrebase
import sys



config = {"apiKey": "AIzaSyBc7qqxaJiXJ9FlZlDrEqdPoVyA1JM5vlY","authDomain": "learningserver-1abd7.firebaseapp.com","databaseURL": "https://learningserver-1abd7.firebaseio.com","projectId": "learningserver-1abd7","storageBucket": "learningserver-1abd7.appspot.com","messagingSenderId": "658436185485"}
firebase = pyrebase.initialize_app(config)
db = firebase.database()




"""___________________Variables___________________"""

#objects
gpio = pigpio.pi()
db = firebase.database()
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
	idle()
	time.sleep(2)
	start_loop()

def start_loop():
	while 1:
		
		speeds_now = db.child("speeds").get()
		android_signal = speeds_now.val()[-1]

		gpio.set_servo_pulsewidth(LEFT_MOTOR_PIN, float(android_signal))
		gpio.set_servo_pulsewidth(RIGHT_MOTOR_PIN, float(android_signal))	

		if float(android_signal) == 0:
			stop()


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

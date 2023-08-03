## INITIALIZE JOYSTICK
import RPi.GPIO as GPIO  
import time  
from evdev import UInput, ecodes as e

# INTIALIZE PINS
JOY_LEFT = 6
JOY_RIGHT = 13
JOY_UP = 19
JOY_DOWN = 5
BUTTON_1 = 12
BUTTON_2 = 16

bounce_time_value = 1

# SETUP
GPIO.setmode(GPIO.BCM)  #bcm is pin names
GPIO.setup(JOY_LEFT, GPIO.IN, pull_up_down = GPIO.PUD_UP)  
GPIO.setup(JOY_RIGHT, GPIO.IN, pull_up_down = GPIO.PUD_UP)  
GPIO.setup(JOY_UP, GPIO.IN, pull_up_down = GPIO.PUD_UP)  
GPIO.setup(JOY_DOWN, GPIO.IN, pull_up_down = GPIO.PUD_UP)  
GPIO.setup(BUTTON_1,GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(BUTTON_2,GPIO.IN, pull_up_down = GPIO.PUD_UP)

ui = UInput()

def buttonJOY_LEFT(channel):
    ui.write(e.EV_KEY, e.KEY_LEFT ,1)
    ui.write(e.EV_KEY, e.KEY_LEFT ,0)
    ui.syn()

def buttonJOY_RIGHT(channel):
    ui.write(e.EV_KEY, e.KEY_RIGHT ,1)
    ui.write(e.EV_KEY, e.KEY_RIGHT ,0)
    ui.syn()

def buttonJOY_UP(channel):
    ui.write(e.EV_KEY, e.KEY_UP ,1)
    ui.write(e.EV_KEY, e.KEY_UP ,0)
    ui.syn()

def buttonJOY_DOWN(channel):
    ui.write(e.EV_KEY, e.KEY_DOWN ,1)
    ui.write(e.EV_KEY, e.KEY_DOWN ,0)
    ui.syn()

def buttonBUTTON_1(channel):
    ui.write(e.EV_KEY, e.KEY_ENTER ,1)
    ui.write(e.EV_KEY, e.KEY_ENTER ,0)
    ui.syn()

def buttonBUTTON_2(channel):
    ui.write(e.EV_KEY, e.KEY_SPACE ,1)
    ui.write(e.EV_KEY, e.KEY_SPACE ,0)
    ui.syn()

GPIO.add_event_detect(JOY_LEFT, GPIO.FALLING, callback = buttonJOY_LEFT, bouncetime = bounce_time_value)   
GPIO.add_event_detect(JOY_RIGHT, GPIO.FALLING, callback = buttonJOY_RIGHT, bouncetime = bounce_time_value)   
GPIO.add_event_detect(JOY_UP, GPIO.FALLING, callback = buttonJOY_UP, bouncetime = bounce_time_value)   
GPIO.add_event_detect(JOY_DOWN, GPIO.FALLING, callback = buttonJOY_DOWN, bouncetime = bounce_time_value) 
GPIO.add_event_detect(BUTTON_1, GPIO.FALLING, callback = buttonBUTTON_1, bouncetime = bounce_time_value) 
GPIO.add_event_detect(BUTTON_2, GPIO.FALLING, callback = buttonBUTTON_2, bouncetime = bounce_time_value) 

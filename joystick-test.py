from time import sleep
import RPi.GPIO as GPIO
import pygame
GPIO.setmode(GPIO.BCM)

JOY_LEFT = 6
JOY_RIGHT = 13
JOY_UP = 19
JOY_DOWN = 5
BUTTON_1 = 12
BUTTON_2 = 16

GPIO.setup(JOY_LEFT,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(JOY_RIGHT,GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(JOY_UP,GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(JOY_DOWN,GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUTTON_1,GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUTTON_2,GPIO.IN, pull_up_down=GPIO.PUD_UP)

while(1):
        if GPIO.input(JOY_LEFT)==0:
                print ("LEFT")
                sleep(0.1)
        if GPIO.input(JOY_RIGHT)==0:
                print ("RIGHT")
                sleep(0.1)
        if GPIO.input(JOY_UP)==0:
                print ("UP")
                sleep(0.1)
        if GPIO.input(JOY_DOWN)==0:
                print ("DOWN")
                sleep(0.1)
        if GPIO.input(BUTTON_1)==0:
                print ("BUTTON_1")
                sleep(0.1)
        if GPIO.input(BUTTON_2)==0:
                print ("BUTTON_2")
                sleep(0.1)



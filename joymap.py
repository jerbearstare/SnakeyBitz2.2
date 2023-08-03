import RPi.GPIO as GPIO
from evdev import UInput, ecodes as e


class GPIO_to_Keyboard:
    def __init__(self, joy_left_pin, joy_right_pin, joy_up_pin, joy_down_pin, button_1_pin, button_2_pin, bounce_time_value):
        self.joy_left_pin = joy_left_pin
        self.joy_right_pin = joy_right_pin
        self.joy_up_pin = joy_up_pin
        self.joy_down_pin = joy_down_pin
        self.button_1_pin = button_1_pin
        self.button_2_pin = button_2_pin
        self.bounce_time_value = bounce_time_value
        
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.joy_left_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.joy_right_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.joy_up_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.joy_down_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.button_1_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.button_2_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        self.ui = UInput()
        
        GPIO.add_event_detect(self.joy_left_pin, GPIO.FALLING, callback=self.buttonJOY_LEFT, bouncetime=self.bounce_time_value)   
        GPIO.add_event_detect(self.joy_right_pin, GPIO.FALLING, callback=self.buttonJOY_RIGHT, bouncetime=self.bounce_time_value)   
        GPIO.add_event_detect(self.joy_up_pin, GPIO.FALLING, callback=self.buttonJOY_UP, bouncetime=self.bounce_time_value)   
        GPIO.add_event_detect(self.joy_down_pin, GPIO.FALLING, callback=self.buttonJOY_DOWN, bouncetime=self.bounce_time_value) 
        GPIO.add_event_detect(self.button_1_pin, GPIO.FALLING, callback=self.buttonBUTTON_1, bouncetime=self.bounce_time_value) 
        GPIO.add_event_detect(self.button_2_pin, GPIO.FALLING, callback=self.buttonBUTTON_2, bouncetime=self.bounce_time_value) 


    def buttonJOY_LEFT(self, channel):
        self.ui.write(e.EV_KEY, e.KEY_LEFT ,1)
        self.ui.write(e.EV_KEY, e.KEY_LEFT ,0)
        self.ui.syn()

    def buttonJOY_RIGHT(self, channel):
        self.ui.write(e.EV_KEY, e.KEY_RIGHT ,1)
        self.ui.write(e.EV_KEY, e.KEY_RIGHT ,0)
        self.ui.syn()

    def buttonJOY_UP(self, channel):
        self.ui.write(e.EV_KEY, e.KEY_UP ,1)
        self.ui.write(e.EV_KEY, e.KEY_UP ,0)
        self.ui.syn()

    def buttonJOY_DOWN(self, channel):
        self.ui.write(e.EV_KEY, e.KEY_DOWN ,1)
        self.ui.write(e.EV_KEY, e.KEY_DOWN ,0)
        self.ui.syn()

    def buttonBUTTON_1(self, channel):
        self.ui.write(e.EV_KEY, e.KEY_ENTER ,1)
        self.ui.write(e.EV_KEY, e.KEY_ENTER ,0)
        self.ui.syn()

    def buttonBUTTON_2(self, channel):
        self.ui.write(e.EV_KEY, e.KEY_SPACE ,1)
        self.ui.write(e.EV_KEY, e.KEY_ENTER ,0)
        self.ui.syn()
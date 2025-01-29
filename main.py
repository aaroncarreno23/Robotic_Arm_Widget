# ////////////////////////////////////////////////////////////////
# //                     IMPORT STATEMENTS                      //
# ////////////////////////////////////////////////////////////////

import os
import math
import sys
import time

os.environ["DISPLAY"] = ":0.0"

from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import *
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.slider import Slider
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from kivy.clock import Clock
from kivy.animation import Animation
from functools import partial
from kivy.config import Config
from kivy.core.window import Window
from pidev.kivy import DPEAButton
from pidev.kivy import PauseScreen
import time
from time import sleep
from dpeaDPi.DPiComputer import *
from dpeaDPi.DPiStepper import *

dpiComputer = DPiComputer()
dpiStepper = DPiStepper()
dpiStepper.setBoardNumber(0)

if dpiComputer.initialize():
    print("Successfully communicating with DPiComputer")
else:
    print("Failed to communicate with DPiComputer.")

if dpiStepper.initialize():
    print("Successfully communicating with DPiStepper board")
else:
    print("Failed to communicate with DPiStepper board.")

# ////////////////////////////////////////////////////////////////
# //                     HARDWARE SETUP                         //
# ////////////////////////////////////////////////////////////////
"""Stepper goes into MOTOR 0
   Limit Sensor for Stepper Motor goes into HOME 0
   Talon Motor Controller for Magnet goes into SERVO 0
   Talon Motor Controller for Air Piston goes into SERVO 1
   Tall Tower Limit Sensor goes in IN 2
   Short Tower Limit Sensor goes in IN 1

/////////////////////////////////////////////////////////////////
from time import sleep
from dpeaDPi.DPiComputer import *
from dpeaDPi.DPiStepper import *

dpiComputer = DPiComputer()
dpiStepper = DPiStepper()
dpiStepper.setBoardNumber(0)
dpiComputer.initialize()
dpiStepper.initialize()

if dpiComputer.initialize():
    print("Successfully communicating with DPiComputer")
else:
    print("Failed to communicate with DPiComputer.")

if dpiStepper.initialize():
    print("Successfully communicating with DPiStepper board")
else:
    print("Failed to communicate with DPiStepper board.")   
/////////////////////////////////////////////////////////////////
   
dpiComputer.writeServo(1, 90)
dpiComputer.writeServo(1, 0)
dpiComputer.writeServo(1, 180)





 //value1 is short tower 
 // value2 is tall tower 
 
value1 = dpiComputer.readDigitalIn(dpiComputer.IN_CONNECTOR__IN_1)
print(str(value1))
            
value2 = dpiComputer.readDigitalIn(dpiComputer.IN_CONNECTOR__IN_2)
print(str(value2))
  
print(str(value1)) 
print(str(value2))

# Number of times to check the sensor values
iterations = 20

for i in range(iterations):
    # Read sensor values
    value1 = dpiComputer.readDigitalIn(dpiComputer.IN_CONNECTOR__IN_1)
    value2 = dpiComputer.readDigitalIn(dpiComputer.IN_CONNECTOR__IN_2)

    # Print the sensor states
    print(f"Short Tower Sensor (Value1): {value1}, Tall Tower Sensor (Value2): {value2}")

    # Add a delay to make the output readable
    time.sleep(1)

   
1 = nothing
0 = something



NEGATIVE FOR LOWER TO UPPER 
POSITIVE TO UPPER TO LOWER 
0.3333 revolutions between the towers 

wait_to_finish_moving_flg = True
dpiStepper.enableMotors(True)
dpiStepper.setSpeedInRevolutionsPerSecond(0, 1)
dpiStepper.moveToRelativePositionInRevolutions(0, 0.3333, wait_to_finish_moving_flg)

dpiStepper.setSpeedInRevolutionsPerSecond(0, 1)
dpiStepper.moveToRelativePositionInRevolutions(0, -0.3333, wait_to_finish_moving_flg)

dpiComputer.writeServo(1, 90) for lower 
dpiComputer.writeServo(1, 0) for raise 

dpiComputer.writeServo(0, 0) for magnet on 
dpiComputer.writeServo(0, 90) for magnet off 


   
   """

# ////////////////////////////////////////////////////////////////
# //                      GLOBAL VARIABLES                      //
# //                         CONSTANTS                          //
# ////////////////////////////////////////////////////////////////
START = True
STOP = False
UP = False
DOWN = True
ON = True
OFF = False
YELLOW = .180, 0.188, 0.980, 1
BLUE = 0.917, 0.796, 0.380, 1
CLOCKWISE = 0
COUNTERCLOCKWISE = 1
ARM_SLEEP = 2.5
DEBOUNCE = 0.10

lowerTowerPosition = 60
upperTowerPosition = 76


# ////////////////////////////////////////////////////////////////
# //            DECLARE APP CLASS AND SCREENMANAGER             //
# //                     LOAD KIVY FILE                         //
# ////////////////////////////////////////////////////////////////
class MyApp(App):

    def build(self):
        self.title = "Robotic Arm"
        return sm

Builder.load_file('main.kv')
Window.clearcolor = (.1, .1,.1, 1) # (WHITE)


# ////////////////////////////////////////////////////////////////
# //                    SLUSH/HARDWARE SETUP                    //
# ////////////////////////////////////////////////////////////////
sm = ScreenManager()



# ////////////////////////////////////////////////////////////////
# //                       MAIN FUNCTIONS                       //
# //             SHOULD INTERACT DIRECTLY WITH HARDWARE         //
# ////////////////////////////////////////////////////////////////
	
class MainScreen(Screen):
    armPosition = 0
    lastClick = time.perf_counter()

    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.initialize()
        self.servo_magnet = 0
        self.servo_air = 1
        self.arm_up = False
        self.magnet = False
        self.enableMotor = False

    def debounce(self):
        processInput = False
        currentTime = time.perf_counter()
        if ((currentTime - self.lastClick) > DEBOUNCE):
            processInput = True
        self.lastClick = currentTime
        return processInput

    def toggleMotor(self):

        if self.enableMotor:
            dpiStepper.enableMotors(False)
            self.ids.motor.text = "Motor off"
            self.enableMotor = False
            print("Motor Disabled")

        else:
            dpiStepper.enableMotors(True)
            self.ids.motor.text = "Motor on"
            self.enableMotor = True
            print("Motor Enabled")


    def toggleArm(self):

        if self.arm_up:
            dpiComputer.writeServo(self.servo_air, 0)
            self.ids.armControl.text = "Lower Arm"
            self.arm_up = False
            print("Raised Arm")

        else:
            dpiComputer.writeServo(self.servo_air, 90)
            self.ids.armControl.text = "Raise Arm"
            self.arm_up = True
            print("Lowered Arm")

    def toggleMagnet(self):

        if self.magnet:
            dpiComputer.writeServo(0, 0)
            self.ids.magnetControl.text = "Release Ball"
            self.magnet = False
            print("Magnet ON")
        else:
            dpiComputer.writeServo(0, 90)
            self.ids.magnetControl.text = "Hold Ball"
            self.magnet = True
            print("Magent OFF")
        
    def auto(self):
        print("Run the arm automatically here")

    def setArmPosition(self, slider, value):
        stepper_num = 0
        wait_to_finsh_moving_flg = True
        motor_value = value * 0.3333
        self.ids.armControlLabel.text = f"Arm Position: {value:.2f}"
        dpiStepper.moveToAbsolutePositionInRevolutions(stepper_num, -motor_value, wait_to_finsh_moving_flg)
        print(f"Arm Position: {value:.2f}")


    def homeArm(self, arm=None):
        arm.home(self.homeDirection)

    def start_update(self):
        Clock.schedule_interval(self.update_value, 1)

    def update_value(self, dt):
        nothing = 1
        something = 0
        value1 = dpiComputer.readDigitalIn(dpiComputer.IN_CONNECTOR__IN_1)
        value2 = dpiComputer.readDigitalIn(dpiComputer.IN_CONNECTOR__IN_2)
        print(f"Short Tower Sensor (Value1): {value1}, Tall Tower Sensor (Value2): {value2}")

        if value1 == something:
            self.ids.towerSensor.text = "Ball on Lower Tower"

        elif value2 == something:
            self.ids.towerSensor.text = "Ball on Upper Tower"

        else:
            self.ids.towerSensor.text = "Ball on no Tower"

    def initialize(self):
        print("Home arm and turn off magnet")

    def resetColors(self):
        self.ids.armControl.color = YELLOW
        self.ids.magnetControl.color = YELLOW
        self.ids.auto.color = BLUE

    def quit(self):
        MyApp().stop()
    
sm.add_widget(MainScreen(name = 'main'))


# ////////////////////////////////////////////////////////////////
# //                          RUN APP                           //
# ////////////////////////////////////////////////////////////////
if __name__ == "__main__":
    # Window.fullscreen = True
    # Window.maximize()
    MyApp().run()

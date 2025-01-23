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
   Talon Motor Controller for Magnet goes into SERVO 1
   Talon Motor Controller for Air Piston goes into SERVO 0
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
   
1 = nothing
0 = something












   
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

    def debounce(self):
        processInput = False
        currentTime = time.perf_counter()
        if ((currentTime - self.lastClick) > DEBOUNCE):
            processInput = True
        self.lastClick = currentTime
        return processInput

    def toggleArm(self):
        print("Process arm movement here")

    def toggleMagnet(self):
        print("Process magnet here")
        
    def auto(self):
        print("Run the arm automatically here")

    def setArmPosition(self, position):
        print("Move arm here")

    def homeArm(self, arm=None):
        arm.home(self.homeDirection)
        
    def isBallOnTallTower(self):
        print("Determine if ball is on the top tower")

    def isBallOnShortTower(self):
        print("Determine if ball is on the bottom tower")
        
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

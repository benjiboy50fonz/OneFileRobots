#!/usr/bin/env python3

# Currently written for the execute speed test.

import os, sys

from robotpy_ext.misc import NotifierDelay

from commands2 import TimedCommandRobot, SequentialCommandGroup, CommandBase, WaitCommand

from commands2.button import JoystickButton

from wpilib import XboxController, Joystick

from wpilib._impl.main import run

class Infinite(CommandBase):
    def __init__(self):
        super().__init__()
        
    def execute(self):
        print('looping')

    def isFinished(self):
        return False

class Test(CommandBase):
    def __init__(self):
        super().__init__()
             
        self.toAdd = []
        self.count = 0
                   
    def execute(self):
        with NotifierDelay(0.02) as delay:
            self.toAdd.append(self.count)
            self.count += 1
            delay.wait()
    
    def end(self, interrupted):
        with open(os.path.dirname(__file__) + '/data.txt', 'w') as f:
            for line in self.toAdd:
                f.write(str(line) + '\n')
                
            f.close()
                            
class SecondTest(CommandBase):
    def __init__(self):
        super().__init__()
        
        self.count = 0
        
    def execute(self):
        with NotifierDelay(0.02) as delay:
            self.count += 1
            with open(os.path.dirname(__file__) + '/data.txt', 'r') as f:
                print(f.readlines()[self.count])
            delay.wait()
                        
    def isFinished(self):
        return False
        

class Robot(TimedCommandRobot):
    """Implements a Command Based robot design"""

    def robotInit(self):
        """Set up everything we need for a working robot."""
        self.stick = Joystick(0)
                
        self.toLoop = Infinite()
                
        JoystickButton(self.stick, 1).whenHeld(Test())
        JoystickButton(self.stick, 2).whenHeld(SecondTest())
        
    def teleopInit(self):
        self.toLoop.schedule()
        
    def autonomousInit(self):
        """Auto beginning"""
   
if __name__ == "__main__":
    run(Robot)
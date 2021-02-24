#!/usr/bin/env python3

# Currently written for the 'alongWith()' test.

from commands2 import TimedCommandRobot, SequentialCommandGroup, CommandBase

from wpilib._impl.main import run

class Test(CommandBase):
    def __init__(self):
        super().__init__()
        
    def execute(self):
        print('executing in first')
        
class SecondTest(CommandBase):
    def __init__(self):
        super().__init__()
        
    def execute(self):
        print('executing in second')
        
    def isFinished(self):
        return False

class Auto(SequentialCommandGroup):
        
    def __init__(self):
        super().__init__()

        commandOne = Test()
        commandTwo = SecondTest()
        
        self.addCommands(
            commandTwo.alongWith(commandOne)
        )

class Robot(TimedCommandRobot):
    """Implements a Command Based robot design"""

    def robotInit(self):
        """Set up everything we need for a working robot."""
        self.auto = Auto()
        
    def autonomousInit(self):
        self.auto.schedule(False)
   
if __name__ == "__main__":
    run(Robot)
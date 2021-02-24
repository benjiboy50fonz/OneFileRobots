#!/usr/bin/env python3

from commands2 import TimedCommandRobot, RamseteCommand, RunCommand, SubsystemBase, CommandBase

from wpilib._impl.main import run
from wpilib import RobotBase, SmartDashboard, Encoder, PWMVictorSPX, XboxController, SpeedControllerGroup, ADXRS450_Gyro

from wpilib.interfaces import GenericHID

from wpilib.controller import RamseteController, PIDController

from wpilib.drive import DifferentialDrive

from wpimath.controller import *

from wpimath.geometry import *
from wpimath.kinematics import *

from wpimath.trajectory import *
from wpimath.trajectory.constraint import *

import shutil, sys

class TestCommand(CommandBase):
    
    def __init__(self, d):
        super().__init__()
        
        self.addRequirements(d)

class Drivetrain(SubsystemBase):
    
    def __init__(self, controller: XboxController):
        super().__init__()
                
        frontLeftMotor, backLeftMotor = PWMVictorSPX(0), PWMVictorSPX(1)
        frontRightMotor, backRightMotor = PWMVictorSPX(2), PWMVictorSPX(3)
        
        self.leftMotors = SpeedControllerGroup(
            frontLeftMotor,
            backLeftMotor
        )
        
        self.rightMotors = SpeedControllerGroup(
            frontRightMotor,
            backRightMotor
        )
        
        self.drivetrain = DifferentialDrive(self.leftMotors, self.rightMotors)
        
        self.controller = controller
        
    def arcadeDrive(self):
        self.drivetrain.arcadeDrive(
            self.controller.getY(GenericHID.Hand.kLeftHand), 
            self.controller.getX(GenericHID.Hand.kRightHand)
        )
        
class Robot(TimedCommandRobot):
    """Implements a Command Based robot design"""

    def robotInit(self):
        """Set up everything we need for a working robot."""
                
        self.driverController = XboxController(1)

        self.driveSubsystem = Drivetrain(self.driverController)
        
        do = RunCommand(
                self.driveSubsystem.arcadeDrive,
                self.driveSubsystem
            )
                                
        self.driveSubsystem.setDefaultCommand(do)        
        
    def teleopInit(self):
        pass
        
    def autonomousInit(self):
        pass
   
if __name__ == "__main__":
    run(Robot)

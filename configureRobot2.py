import buttonManager
import robot
import info


def configureRobotX( joystick, screen, font):
    # Set up robot and its info instances
    robotX = robot.Robot( joystick, position = (550, 200), color = "red")  #define robot X
    robotX.info = info.Info( screen, (400, 10), font, robotX )

    # set up the mapping of chords and commands
    robotX.joystickManager.buttonManager.onWhile( [buttonManager.A_BUTTON],
        lambda : robotX.turnCCW())
    robotX.joystickManager.buttonManager.onWhile( [buttonManager.B_BUTTON],
        lambda : robotX.turnCW())
    robotX.joystickManager.buttonManager.onPress( [buttonManager.XBOX_BUTTON],
        lambda : robotX.rotationMode.advanceCyclic())
    robotX.joystickManager.buttonManager.onPress( [buttonManager.VIEW_BUTTON],
        lambda : robotX.setSpecial( 'Start'))
    robotX.joystickManager.buttonManager.onRelease( [buttonManager.VIEW_BUTTON],
        lambda : robotX.setSpecial( ''))
    robotX.joystickManager.buttonManager.onPress( [buttonManager.MENU_BUTTON],
        lambda : robotX.setSpecial(' Back'))
    robotX.joystickManager.buttonManager.onRelease( [buttonManager.MENU_BUTTON],
        lambda : robotX.setSpecial( ''))
    
    # map the joystick and trigger commands
    robotX.driveByAxis = [
        lambda : robotX.turnCWBy( robotX.joystickManager.rightTrigger),
        lambda : robotX.turnCCWBy( robotX.joystickManager.leftTrigger)
    ]

    # set startup modes
    robotX.rotationMode.setMode( robot.tankFieldMode )
    robotX.spinSpeedMode.setMode( robot.spinSpeedHigh)
    robotX.driveByJoystick =  lambda : robotX.rotationMode.command(
        robotX.joystickManager.combineJoys( [
            robotX.joystickManager.leftJoy ]))
    return robotX
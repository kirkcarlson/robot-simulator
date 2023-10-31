### IMPORTS ####
import buttonManager
import robot
import info


### Function to define a particular robot 

def configureRobotX ( joystick, screen, font):
    # Set up robot and its info instances
    robotX = robot.Robot( joystick, position = (350, 200), color = "royalblue")  #define robot 1
    # Info ( screen, upper_left, font, robot, line_size=LINE_SIZE, color=TEXT_COLOR):
    robotX.info = info.Info( screen, (10, 10), font, robotX )
                        
    # set up the mapping of chords and commands
    robotX.joystickManager.buttonManager.onPress(
        [buttonManager.A_BUTTON, buttonManager.B_BUTTON],
        lambda : robotX.rotationMode.setMode( robot.autoRotateSouthMode ))
    robotX.joystickManager.buttonManager.onPress(
        [buttonManager.X_BUTTON, buttonManager.Y_BUTTON],
        lambda : robotX.rotationMode.setMode( robot.autoRotateNorthMode ))
    robotX.joystickManager.buttonManager.onPress(
        [buttonManager.A_BUTTON, buttonManager.X_BUTTON],
        lambda : robotX.rotationMode.setMode( robot.autoRotateWestMode ))
    robotX.joystickManager.buttonManager.onPress(
        [buttonManager.B_BUTTON, buttonManager.Y_BUTTON],
        lambda : robotX.rotationMode.setMode( robot.autoRotateEastMode ))
    robotX.joystickManager.buttonManager.onPress(
        [buttonManager.A_BUTTON, buttonManager.B_BUTTON,
        buttonManager.X_BUTTON, buttonManager.Y_BUTTON],
        lambda : robotX.rotationMode.setMode( robot.autoRotateFrontMode ))
    robotX.joystickManager.buttonManager.onPress(
        [buttonManager.A_BUTTON, buttonManager.X_BUTTON,
        buttonManager.LEFT_BUTTON],
        lambda : robotX.rotationMode.setMode( robot.spinCWMode ))
    robotX.joystickManager.buttonManager.onPress(
        [buttonManager.B_BUTTON, buttonManager.Y_BUTTON,
        buttonManager.LEFT_BUTTON],
        lambda : robotX.rotationMode.setMode( robot.spinCCWMode ))
    robotX.joystickManager.buttonManager.onWhile( [buttonManager.A_BUTTON],
        lambda : robotX.turnCCW())
    robotX.joystickManager.buttonManager.onWhile( [buttonManager.B_BUTTON],
        lambda : robotX.turnCW())
    robotX.joystickManager.buttonManager.onPress( [buttonManager.LEFT_BUTTON],
        lambda : robotX.elevatorMode.advanceCyclic())
    robotX.joystickManager.buttonManager.onPress( [buttonManager.XBOX_BUTTON],
        lambda : robotX.rotationMode.advanceCyclic())
    robotX.joystickManager.buttonManager.onPress( [buttonManager.X_BUTTON],
        lambda : robotX.rotationMode.advanceCyclic())
    robotX.joystickManager.buttonManager.onPress( [buttonManager.RIGHT_BUTTON],
        lambda : robotX.spinSpeedMode.advanceCyclic())
    robotX.joystickManager.buttonManager.onPress( [buttonManager.VIEW_BUTTON],
        lambda : robotX.setSpecial( 'Start'))
    robotX.joystickManager.buttonManager.onRelease( [buttonManager.VIEW_BUTTON],
        lambda : robotX.setSpecial( ''))
    robotX.joystickManager.buttonManager.onPress( [buttonManager.MENU_BUTTON],
        lambda : robotX.setSpecial( ' Back'))
    robotX.joystickManager.buttonManager.onRelease( [buttonManager.MENU_BUTTON],
        lambda : robotX.setSpecial( ''))
    
    # map the joystick and trigger commands
    robotX.driveByAxis = [
        lambda : robotX.turnCWBy( robotX.joystickManager.rightTrigger),
        lambda : robotX.turnCCWBy( robotX.joystickManager.leftTrigger)
    ]

    # set startup modes
    robotX.rotationMode.setMode( robot.manualRotationMode )
    robotX.spinSpeedMode.setMode( robot.spinSpeedHigh)
    robotX.driveByJoystick =  lambda : robotX.rotationMode.command(
        robotX.joystickManager.combineJoys( [
            robotX.joystickManager.rightJoy,
            robotX.joystickManager.leftJoy,
            robotX.joystickManager.hat]))
    
    return robotX
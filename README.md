Robot Simulation -- video simulation of robots for exploring software and joystick controls

### The Program
Requirements:
- Python 3.x
- pygame library (for the game and joystick interfaces and sprite methods)
- math library (for trigometric and square root math operators)
- One or two Xbox controllers
  - first one is the ***blue*** robot
    - this robot has the experimental button map as follows:
        - left joystick controls motion of robot
        - right joystick controls motion of robot
        - hat controls motion of robot
        - left paddle or A button controls CCW rotation
        - right paddle or B button controls CCW rotation
        - rotation modes
          - X button selects rotation mode
          - chord of A and B buttons selects rotate to south mode
          - chord of X and Y buttons selects rotate to north mode
          - chord of A and X buttons selects rotate to west mode
          - chord of B and Y buttons selects rotate to east mode
          - chord of A, B, X, and Y buttons selects rotate to front mode
          - chord of A, X, and LEFT buttons selects CW spin
          - chord of B, Y, and LEFT buttons selects CCW spin
          - using manual rotation commands overriding of specified rotation mode (except for tank modes)
        - view button controls 'back'
        - menu button controls 'start'
        - left button selects elevator and arm presets (yes, this is a co-pilot function, but trying to see how the control might work. The hat seems like it might be a better control for this forward=up, back=down, right=out, left=in.)
        - right button selects rotation speed
  - second one is the ***red*** robot
    - this robot is configured to use the FRC 4513 pilot robot controls.
        - left joystick controls motion of robot
        - left trigger controls CCW rotation
        - right trigger controls CCW rotation
        - view button controls 'back'
        - menu button controls 'start'

- Some machine to run the program on

To run the program:
``` bash
    python3 robotSim.py
```
### IMPORTANT NOTE

This program is not robust and does not have very much input validation.

### The Files

The following files are used (indentation shows general structure):

- robotSim.py -- main program including mapping of controller inputs to robot actions.
  - joystickManager.py -- interfaces the Xbox controller and normalizes the inputs.
    - buttonManger.py -- maps button press, depress and while events to defined actions.
        - mode.py -- provides for modal controls.
  - robot.py -- defines robot actions.
  - info.py -- displays information about the joystick controller and robot.
  - rmath.py -- provides specialized math functions for robots.
  - field.py -- future module to define field elements for more realistic simulation.

### Goals
This simulation has a few goals:
- Explore differences  tank drive and swerve drive.
- Explore mechanisms for mapping joystick controls to robot commands.
- Explore robot commands to help sort out the good from the bad.
- Prepare drivers for driving a real robot by practicing on a simulation.
- Learn about Object Oriented Programming by having multiple robots, controllers, and information displays.

### Mapping Joystick to Robot Commands
- Includes a mode module to have a button with multiple modes.
- Includes a button manager module to perform actions on the pressing, releasing or holding of one or more keys.
- Includes a way to map a joystick or hat device to a directionally controlled device.
- Includes a way to normalize trigger devices to be between 0 and 1 rather than their native -1 and +1.
- Commands are mapped using lamda functions to pass their address to the joystick event detection module.
- A list of one or more joysticks may be assigned to control the same function to evaluate the best joystick for the job.
- Several values are displayed over the robot field and allow evaluation of the raw and processed values

### Sorting out the Good and Bad
Several command modes have been provided. These allow rapid evaluation by switching between them. Likewise button assigment and joystick assignment can occur rapidly for evaluation.
This is a fairly subjective exercise, but it does provide a laboratory for exploring ideas.

#### Some observatons to date
- Swerve drive robots are easier to drive than tank drives and have better motion efficiency. (Duh)
- Tank drive with traditional skip loader joy stick (forward-backward-left-right) is very hard to drive a moving robot.
- Minimizing the spinning or rotation of a robot may be a way to optimize motion and time.
- Auto spin to front does not seem useful because it can force unneeded rotations.
- Auto spin to one of the cardiinal directions seems useful.
- Xbox controllers with paddle buttons are useful in general.
- Mapping the paddle buttons, where available, to a chord is not a good idea as it get invoked when not wanted.
    - the PowerA controller paddle buttons can be reassinged to any button. Since the joystick buttons are not used, this is a good assignment.
    - the AfterGlow controller paddle buttons are permanently assigned to the A and B buttons, which is a conflict as both are useful control locations.
- The mechanisms for assigning joysticks and buttons to functions is compact and fairly easy to modify if not understand. 
- Chords, pressing of multiple buttons simutaneously, can be a useful feature.

#### Other things to evaluate (play with)
- A reverse button for tank drives
- Some sort of auto reverse mechanism for tank drives

### Possible Improvements
- Convert to python arcade to have improved collision detection and some physics
- Add game elements with collisions to better improve game conditions
- Add collision with the second robot
- Just move on to the real simulation offered by WPI
- simplification of button to action assignment code or expression (shorter names, initialization table, or something else...)
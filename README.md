Robot Simulation -- video simulation of robots for exploring software and joystick controls

### Goals
This simulation has a few goals:
- prepare drivers for driving a real robot by practicing on a simulation
- explore mechanisms for mapping joystick controls to robot commands
- explore differences between tank drive and swerve drive
- explore robot commands to sort out the good from the bad

### Mapping Joystick to Robot Commands
- includes a mode module to have a button with multiple modes.
- includes a button manager module to perform actions on the pressing, releasing or holding of one or more keys.
- includes a way to map a joystick or hat device to a directionally controlled device.
- includes a way to normalize trigger devices to be between 0 and 1 rather than their native -1 and +1.
- commands are mapped using lamda functions to pass their address to the joystick event detection module.
- a list of one or more joysticks may be assigned to control the same function to evaluate the best joystick for the job.
- several values are displayed over the robot field and allow evaluation of the raw and processed values

### Sorting out the Good and Bad
Several command modes have been provided. These allow rapid evaluation by switching between them. Likewise button assigment and joystick assignment can occur rapidly for evaluation.
This is a fairly subjective exercise, but it does provide a laboratory for exploring ideas.
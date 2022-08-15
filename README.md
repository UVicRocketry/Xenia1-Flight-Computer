# Xenia1-flight-Computer

## Requirements/Imports
To pip install all the necessary imports run
`$ pip install -r requirements.txt`
*Please Update requirements.txt with new imports if you add any*

## Style

- Class names: starting with Pascal Case (capital then camel)
- method: lower snake
- vars: lower snake
- private methods: \_\_ for private methods

Please document your code in the following format:

for classes:

```
  """
  Description of class

  ...

  Attributes
  ----------
  an_attribute(variable)
    Description:
      write description

  Methods
  -------
    Description:
      write description
     Parm:
      parm_name: write point of parameter

  """
```

## Setup and Installation

This system is designed to run on a raspberry pi zero W. To set up clone the repository and run `$ pip install -r requirements.txt`, this will install all necessary dependencies. 

## Design 

The flight computer has two purposes: to store, and to simulate. The system is designed to run on a raspberry pi 0 W running rasbian (Ubuntu ~10). Connected to the pi are multiple senors and devices. The sensor suite contains a adafruit BME280, adafruit LSM..., adafruit Adx..., adafruit ADS... all of which are connected to the pi using 1 I2C bus. A mirco stepper driver is used to control the airbrakes assembly's motor and feedback is given through a potentiometer which is fed into the analog to digital converter. A buzzer is connected to a single GPIO pin on the pi and give auditable feedback to the user. All other electrical components connected to the flight computer can be found in the KiCAD schematic in the source directory.

Due to the nature of embedded systems




Beep codes

## File structure

The Project is broken into two folders a source folder (src) and a sub sensors folders
```
> Xenia1-flight-computer
  > drag_data 
    > cda_no_airbrakes.csv

  > src
    > airbrakes.py
    > suborbit.py
    > rehearsal.py
    > main.py
    > rocketData.py
    > flight_computer.py

  > sensors
    > adx.py
    > bme.py
    > hx711.py
    > lsm.py
```

1. src/airbrakes.py


  Suborbit 

   Computes a the next value to set the airbrakes to position to. Also provides a simple interface for controlling the hardware that Airbrakes uses to  deploy the brakes. It does this through a kalman filter algorithm. Please look at the kalman filter algorithm connected    to the issue X1-AV-6 [](https://github.com/UVicRocketry/Xenia1-flight-Computer/issues/14)

2. src/suboribit.py


3. src/gpioReader.py

   This file reads all the data from the sensor and updates rocketData.

4. src/main.py

   Runs flight computer class

5. src/rocketData.py

   This class holds all the data of the rocket and has functions to manipulate the data.


## Flow of the Program

   <deprecated>
![Main State Diagram](/state%20daigram.drawio.png)

Sequence Flow of initial design. This was changed into a class containing different phases 

![Sequence Diagram of main](/sequence%20diagram.drawio.png)


## Air Brakes

The airbrakes assembly ...

For Xenia-1 we over spec'd our motor 

### Kalman Filter

As an suggestion from the MECH 400 report for airbrakes we explored the Kalman filter option for the predictive element of controlling airbrakes. A Kalman filter as shown in the diagram below predicts new state based on previous state. In the case of airbrakes this is a change in flap opening percentage determined by how the drag produced will impact the final altidute of the flight.   

![Kalman Filter Image](/KalmanFilter.drawio.png)

### Suborbit

## Results and Reflection

After a almost nominal flight Xenia-1 was recovered with somewhat minimal data loss. See (link to post flight analysis) for a post flight analysis break down. Based on these results and barriers during development the following conclusions were made. _A raspberry pi is not a suitable processing unit for a rockets avionics system_. A raspberry pi runs an OS for more general purpose computing, what is needed is a device that only runs processes specific to its purpose. Another problem faced during development was the lack 

Developmentation:

This project should have been designed with proper requirements gathering from all subsystems and all core members involved. In addition a new development strategy was used in the middle of the development. This made the 


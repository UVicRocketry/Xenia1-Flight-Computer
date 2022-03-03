# 10K-flight-Computer

## Style

- Class names: starting with capital then camel 
- method: camel starting with lowercase 
- vars: lower snake 
- private methods: \_\_ for private methods 

Please document your code in the following format:

for classes:

```
  """
  Discription of class
  
  ...
  
  Attributes
  ----------
  an_attribute(varaible)
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



## File structure

The Project is broken into two folders a source folder (src) and a tests folder. 
```
> Xenia1-flight-computer
  > src 
    > airbrakes.py
    > dataHandler.py
    > gpioReader.py
    > main.py
    > rocketData.py

  > tests (currently empty)
    > 
```

1. src/airbrakes.py
   Computes a the next value to set the airbrakes to position to. Also provides a simple interface for controlling the hardware that Airbrakes uses to  deploy the brakes. It does this through a kalman filter algorithm. Please look at the kalman filter algorithm connected    to the issue X1-AV-6 [](https://github.com/UVicRocketry/Xenia1-flight-Computer/issues/14)
   
   
2. src/dataHandler.py

   This file deals with redirecting the data to the to where is suppose to go. There are methods for each sensor to send there data to either, ground, air brakes, or    blackbox. In order send data they are formatted according to the protocol.

3. src/gpioReader.py
   
   This file reads all the data from the sensor and updates rocketData.
   
4. src/main.py
  
   Connects everything together. 
   
5. src/rocketData.py

   This class holds all the data of the rocket and has functions to manipulate the data. 

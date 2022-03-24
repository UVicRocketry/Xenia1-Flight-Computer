import pytest
import sys
sys.path.append(r"C:\Users\jackw\uvic\rocketry\Xenia1-flight-Computer\src")
from gpioReader import GPIOReader


#tests are initialised using pytest <testfile>. Use the -vv flag to obtain verbose output
#this test is an example of how to write tests

#tests must have the word "test" in them so pytest can identify it is a test function
def test_gpioReader_01(capsys):
    #input the values that you wish to simulate coming from the BME and LSM sensors. The input goes as follows:
    #   first value must be <True> to initialise testing mode
    #   BME: second value = BME Temperature int Reading
    #   third value = BME Humidity int Reading
    #   fourth value = BME Pressure int Reading
    #   LSM: fifth value = LSM Acceleration list [x, y, z]
    #   sixth value = LSM Magnetometer list [x, y, z]
    #   seventh value = LSM Gyroscope list [x, y, z]
    #   eigth value = LSM Temperature int Reading
    gpio = GPIOReader(True, 1, 2, 3, [1, 2, 3], [4, 5, 6], [7, 8, 9], 29)
    #call gpio.retrieveData() to obtain stdout output from retrieveData
    gpio.retrieveData()
    #capsys.readouterr() captures current output to stdout and stderr and stores it in an object
    captured = capsys.readouterr()
    #captured.out returns string of stdout
    #to assert a passed test use the following string and replace <X> with desired output values:
    #"Temperature: X.0 C\nHumidity: X.0 %\nPressure: X.0 hPa\nAcceleration (m/s^2): (X.000, X.000, X.000)\nMagnetometer (gauss: (X.000, X.000, X.000)\nGyroscope (degrees/sec): (X.000, X.000, X.000)\nTemperature: X.000\n"
    #use assert Keyword to determine if test passes or not
    assert captured.out == "Temperature: 1.0 C\nHumidity: 2.0 %\nPressure: 3.0 hPa\nAcceleration (m/s^2): (1.000, 2.000, 3.000)\nMagnetometer (gauss: (4.000, 5.000, 6.000)\nGyroscope (degrees/sec): (7.000, 8.000, 9.000)\nTemperature: 29.000\n"
    #test passes! (Poggers)
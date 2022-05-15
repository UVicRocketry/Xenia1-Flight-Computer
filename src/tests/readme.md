Create all stubs and the script to run them in this folder

## Test Mode

Tests are initialized by typing pytest <testfile> into the command line. The pytest library is used to individually test output of functions to certain inputs. All testing files must be of format test_XX.py and all testing functions must have keyword "test" in function name. 

Tests will be pass/fail.
A test will be determined as a pass or fail if data is read and written correctly. The test writer will pass arguments into a function and use assert keyword to determine if the function outputted as desired. 
  
This approach allows for rigorous testing of functions with a variety of inputs. test_01.py is an example that should be looked at when writing other tests.

The path is currently appending to src so that gpioReader.py can be accessed, but a function will be written in order to make the path work on multiple devices.
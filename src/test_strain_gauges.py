from HX711Multi import HX711_Multi
from time import sleep

# Pins
clk1 = 1
clk2 = 2
clk3 = 3

ring1 = [4,5,6,7]
ring2 = [8,9,10,11]
ring3 = [12,13,14,15]

hx1 = HX711_Multi(ring1, clk1)
hx2 = HX711_Multi(ring2, clk1)
hx3 = HX711_Multi(ring3, clk1)

HX711s = [hx1, hx2, hx3]

def get_readings():

	# List of int 
	readings = []

	for HX in HX711s:

		# Wait till ready
		while not HX.isReady():
			sleep(0.005)

		values = HX.readRaw()

		for value in values:
			readings.append(value)

	return readings

# Returns a bar string 100chars wide that starts the bar at the center
# of a 100char wide terminal. Large scale means low sensitivity.

# +ve values mean bar is to the right of center,
# -ve values mean bar is to the left of center
def get_bar(value, scale):
	bar = "#"
	bar *= int(abs(value/scale))

	if len(bar) > 49:
		bar = "#"*49

	if value > 0:
		whitespace = " "*50
		return whitespace+bar
	else:
		whitespace = " "*(50 - len(bar))
		return whitespace+bar

def get_offsets():

	# Let the gauges settle
	for i in range(10):
		get_readings()

	return get_readings()
	
def clear_console():
	print("\n"*100)

offsets = get_offsets()
sensitivity = 100

while True:
	clear_console()
	
	readings = get_readings()

	for i,reading in enumerate(readings):
		print(get_bar(reading-offsets[i]), sensitivity)
		
		# Seperate rings
		if i%4 == 0:
			print("\n")
		

		

		




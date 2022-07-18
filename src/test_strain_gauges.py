from HX711Multi import HX711_Multi
from time import sleep

# Pins
clk1 = 26
clk2 = 5
clk3 = 16
clk4 = 21

ring1 = [27,9]
ring2 = [11,20,17]
ring3 = [0,19,6]
ring4 = [4,22]

hx1 = HX711_Multi(ring1, clk1)
hx2 = HX711_Multi(ring2, clk2)
hx3 = HX711_Multi(ring3, clk3)
hx4 = HX711_Multi(ring4, clk4)

HX711s = [hx1, hx2, hx3, hx4]

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
	print("\n"*50)

offsets = get_offsets()
sensitivity = 100

readings = get_readings()

while True:

	for i,reading in enumerate(readings):
		print(get_bar(reading-offsets[i]), sensitivity)
		
		# Seperate rings
		if i%4 == 0:
			print("\n")

	readings = get_readings()
	clear_console()
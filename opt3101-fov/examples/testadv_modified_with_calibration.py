# Advanced test for the Pololu 3412
#    3-Channel Wide FOV Time-of-Flight Distance Sensor Using OPT3101
#
# This example shows how to read from all three channels on the OPT3101 and
# store the results in arrays.  It also shows how to use the sensor in a
# non-blocking way: instead of waiting for a sample to complete.
# The sensor code runs quickly so that the main loop can take care of other
# tasks at the same time.
#
# See project repository and library at https://github.com/mchobby/esp8266-upy/tree/master/opt3101-fov
#
# History:
#   12/01/2022 - DMeurisse - Initial portage from Arduino code
#

from machine import I2C
from opt3101 import OPT3101, BRIGHTNESS_ADAPTIVE

# Some testing code for Pico
i2c = I2C(0)
# for PYBStick-RP2040
# i2c = I2C(0, sda=Pin(16), scl=Pin(17))

sensor = OPT3101( i2c )

amplitudes = list([0,0,0])
distances  = list([0,0,0]) # in mm


sensor.set_frame_timing(256)
sensor.set_channel(0)
sensor.set_brightness( BRIGHTNESS_ADAPTIVE )
sensor.start_sample()

# Dummy Calibration method
def calibrate_distance(raw_mm):
    if 330 <= raw_mm <= 450:
        return 300
    elif 500 <= raw_mm <= 600:
        return 400
    elif 600 <= raw_mm <= 750:
        return 500
    elif 700 <= raw_mm <= 800:
        return 600
    elif 850 <= raw_mm <= 1000:
        return 700
    elif 1000 <= raw_mm <= 1200:
        return 800
    elif 1200 <= raw_mm <= 1350:
        return 900
    elif 1350 <= raw_mm <= 1500:
        return 1000
    else:
        return raw_mm  # unchanged if outside defined zones

# Main program loop
print( '           :     TX0 :     TX1 :     TX2' )
print( '-'*40 )
while True:
	if sensor.is_sample_done():
		sensor.read_output_regs() # Read data from board
		# stored into array
		amplitudes[sensor.channel_used] = sensor.amplitude
		distances[sensor.channel_used] = calibrate_distance(sensor.distance) # in mm
		# Display data (or perform processing on the data)
		if sensor.channel_used == 2: # if we did read the 3 sensors
			print( 'Amplitudes : %7i : %7i : %7i' % (amplitudes[0], amplitudes[1], amplitudes[2]) )
			print( 'Distancess : %7i : %7i : %7i' % (distances[0], distances[1], distances[2]) )
			print( '-'*40 )
		# loop to next channel + acquire
		sensor.next_channel()
		sensor.start_sample()

	# Perform other tasks here

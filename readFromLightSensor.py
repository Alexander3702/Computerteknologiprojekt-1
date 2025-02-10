import smbus
import time

# Get I2C bus
bus = smbus.SMBus(1) # or smbus.SMBus(0)

# ISL29125 address, 0x44(68)
# Select configuation-1register, 0x01(01)
# 0x0D(13) Operation: RGB, Range: 360 lux, Res: 16 Bits
bus.write_byte_data(0x44, 0x01, 0x05)

time.sleep(1)

print("Reading colour values and displaying them in a new window\n")



def getAndUpdateColour():
    while True:
	# Read the data from the sensor
        # reading 6 bytes from the sensor, starting at the index 0x09
        data = bus.read_i2c_block_data(0x44, 0x09, 6)


        # Convert the data to green, red and blue integer values
        green = data[1] + data[0] / 256 # index 1 is green high, index 0 is green low
        red = data[3] + data[2] / 256 # index 3 is red high, index 2 is red low
        blue = (data[5] + data[4] / 256) * 2 # index 5 is blue high, index 4 is blue low. multiply by 2 to get the correct value
        
        # Output data to the console RGB values
        # print("RGB(%d %d %d)" % (red, green, blue))

        print("RGB(%d %d %d)" % (red, green, blue))

        print()
        
        # wating for 2 seconds before reading the next set of data
        time.sleep(2) 

getAndUpdateColour()

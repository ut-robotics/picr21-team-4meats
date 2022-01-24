import serial
import struct

s = serial.Serial("/dev/ttyACM0", baudrate=115200)
speeds = 0
s.write(struct.pack('<hhhHBH', speeds, speeds, speeds, 0, 0, 0xAAAA))
received = s.read(struct.calcsize('<hhhH'))
values = struct.unpack('<hhhH', received)
print(values)
s.close()

# wheels: 0 -stopped + one way - the other way, range about 70
# thrower 0 -stopped one way only, range 0 to 2047

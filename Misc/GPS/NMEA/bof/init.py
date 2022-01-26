import calandigital as calan
import numpy as np
import time, struct

IP = '192.168.1.18'
boffile = 'gps.bof.gz'

fpga = calan.initialize_roach(boffile=boffile, ip=IP, upload=1)
time.sleep(1)

fpga.write_int('ctrl',1)    #rst
fpga.write_int('ctrl',0)
print("To continue.. the gps receiver must have located some sources...")
conf = raw_input('Its ready?')
if(conf=='y'):
    #print('Programming ublox')
    #fpga.write_int('ctrl',2)
    #time.sleep(1)
    print('reading time from gps')
    fpga.write_int('ctrl', 0b100)
    time.sleep(0.1)
    fpga.write_int('ctrl',0)
    time.sleep(0.1)
    fpga.write_int('ctrl',1)
    time.sleep(1)

dat = struct.unpack('>22B', fpga.read('time',22))

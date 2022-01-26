import numpy as np
import calandigital as calan
import time

def actual_time(time_data):
    secs = time_data&63
    mins = (time_data&(63<<6))>>6
    hour = (time_data&(31<<12))>>12
    day = (time_data&((2**9-1)<<17))>>17
    return [secs,mins,hour,day]



roach_ip = '192.168.0.40'
boffile = 'irig_b00x.bof.gz'

fpga_clk = 135.*10**6
sec_parameter = 1.05

##irig values
zero_val = int(0.2*fpga_clk/100*sec_parameter)
one_val = int(0.5*fpga_clk/100*sec_parameter)
id_pos = int(0.8*fpga_clk/100*sec_parameter)

debounce = 50

#initialize roach
roach = calan.initialize_roach(roach_ip, boffile=boffile, upload=1)

fpga.write_int('control',1) #rst
fpga.write_int('zero_count', zero_val)
fpga.write_int('one_count', one_val)
fpga.write_int('id_count', id_pos)


time.sleep(0.2)
fpga.write_int('control',2)

time.sleep(2)

#check if the data is ready
valid = fpga.read_int('bcd_valid')
if(valid):
    print('time ready')

time_data = fpga.read_int('first_time1')
subsec = fpga.read_int('subsec')/fpga_clk
secs,mins,hrs,days=actual_time(time_data)
print("gps time:")
print(str(days)+':'+str(hrs)+':'+str(mins)+':'+str(secs))


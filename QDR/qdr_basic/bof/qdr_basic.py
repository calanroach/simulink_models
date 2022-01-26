import calandigital as calan
import numpy as np
import time

IP = '192.168.0.40'
bof = 'qdr_basic.bof.gz'

fpga = calan.initialize_roach(IP, boffile=bof, upload=1)
time.sleep(1)

my_qdr = calan.Qdr(fpga, 'qdr0')
my_qdr.qdr_cal(fail_hard=1, verbosity=1)

time.sleep(1)

fpga.write_int('addr',0)
fpga.write_int('din', 1234)
fpga.write_int('wen',1)
fpga.write_int('wen',0)

fpga.write_int('din', 5678)
for i in range(20):
    fpga.write_int('addr', 2**i)
    fpga.write_int('wen',1)
    fpga.write_int('wen',0)
    fpga.write_int('addr',0)
    fpga.write_int('ren',1)
    val = fpga.read_int('dout')
    fpga.write_int('ren',0)
    if(val!=1234):
        print("You overwrite 0 address at: 2**"+str(i)+'='+str(2**i))
        break

##check that the previous addr is writteable

fpga.write_int('din', 90)
fpga.write_int('addr', 2**i-1)
fpga.write_int('wen',1)
fpga.write_int('wen',0)
fpga.write_int('ren',1)
val = fpga.read_int('dout')
fpga.write_int('addr', 0)
val0 = fpga.read_int('dout')

if(val==val0):
    print('oh oh')






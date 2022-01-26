import calandigital as calan
import numpy as np
import time, struct
import matplotlib.pyplot as plt


IP = '192.168.0.40'
bof = 'qdr_counter.bof.gz'

fpga = calan.initialize_roach(IP, boffile=bof, upload=1)
time.sleep(1)

my_qdr = calan.Qdr(fpga, 'qdr0')
my_qdr.qdr_cal(fail_hard=1, verbosity=1)

time.sleep(1)

fpga.write_int('sel',0) ##just single cycle of data at input qdr
                        ##(diferent from what says the wiki)
fpga.write_int('rst',1)
fpga.write_int('rst',0)
fpga.write_int('wen',1)
time.sleep(4)
##finish writting
fpga.write_int('wen',0)
fpga.write_int('rst',1)
fpga.write_int('rst',0)
fpga.write_int('ren',1)
time.sleep(4)
fpga.write_int('ren',0)
##read the data
qdr_data = struct.unpack('>1024I',fpga.read('dout',1024*4))

plt.plot(qdr_data,label='qdr_data')
plt.plot(np.arange(1024), label='gold data')
plt.grid()

##there is a 2 delay in the cast that i didnt see when compiling
##either way, the data is consistent :P

##read the data with the ppc interface
##the addressing is really weird.. study this!!
fpga.write_int('qdr0_ctrl', 0)
dat = fpga.read('qdr0_memory', 4*1024*4)
vals = np.array(struct.unpack('>4096I', dat))
vals = vals.reshape([-1,4])
vals = vals[::2,:].flatten()
vals = vals[1::2]

plt.plot(vals, label='PPC data')
plt.legend()
plt.show()


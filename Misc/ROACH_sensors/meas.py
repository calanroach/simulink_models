from read_sensors import *
import time
import numpy as np
import matplotlib.pyplot as plt

ip = '192.168.1.168'
sleep_time = 30
meas_time = int(60*60/sleep_time)

fpga = np.zeros(meas_time+1)
ppc = np.zeros(meas_time+1)
ambient = np.zeros(meas_time+1)

t = np.arange(meas_time)*sleep_time
plt.ion()

fig = plt.figure()
ax1 = fig.add_subplot(131); ax2 = fig.add_subplot(132); ax3 = fig.add_subplot(133)

for i in range(meas_time):
    fpga_data = read_fpga_temp(ip)
    ppc_data = read_ppc_temp(ip)
    amb_data = read_ambient_temp(ip)
    print("fpga: %.2f \t ppc: %.2f \t amb: %.2f" %(fpga_data, ppc_data, amb_data))
    fpga[i] = fpga_data
    ppc[i] = ppc_data
    ambient[i] = amb_data
    ax1.cla(); ax2.cla(); ax3.cla()
    ax1.set_title('PPC'); ax2.set_title('FPGA'); ax3.set_title('Ambient')
    ax1.set_ylabel('$C^o$'); ax2.set_ylabel('$C^o$'); ax3.set_ylabel('$C^o$');
    ax1.set_xlabel('min'); ax2.set_xlabel('min'); ax3.set_xlabel('min')
    ax1.plot(t[:i+1]/60., ppc[:i+1], '*-')
    ax2.plot(t[:i+1]/60., fpga[:i+1], '*-')
    ax3.plot(t[:i+1]/60., ambient[:i+1], '*-')
    plt.tight_layout()
    fig.canvas.draw()
    time.sleep(sleep_time)





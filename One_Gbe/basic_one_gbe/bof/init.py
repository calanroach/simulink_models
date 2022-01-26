import corr
import struct, socket, time
import matplotlib.pyplot as plt
import numpy as np

##hyperparameters
pkt_period = 8192
payload_len = 1024

#connection settings
pc_ip = '192.168.1.30'      #your computer eth dev
dest_port = 1234
ppc_ip = '192.168.1.14'     #roach ip
fpga_ip = '192.168.1.45'    #fpga eth, you could put whatever you want

#fpga mac
mac_base=(2<<40) + (2<<32)


#binary address
pc_eth = pc_ip.split('.')
dest_ip = int(pc_eth[0])*(2**24)+int(pc_eth[1])*(2**16)+int(pc_eth[2])*(2**8)+int(pc_eth[3]) 
fpga_eth = fpga_ip.split('.')
source_ip = int(fpga_eth[0])*(2**24)+int(fpga_eth[1])*(2**16)+int(fpga_eth[2])*(2**8)+int(fpga_eth[3])


#program fpga
print('programing fpga')
fpga = corr.katcp_wrapper.FpgaClient(ppc_ip)
time.sleep(1)
bof = 'one_gbe.bof.gz'
fpga.upload_program_bof(bof,3000)
time.sleep(1)
print('ok')

#configure the gbe core
print('Configuring the one gbe core')
tx_core_name = 'one_GbE'
fpga.tap_start('tx_tap',tx_core_name,mac_base+source_ip,source_ip,dest_port)
time.sleep(1)
fpga.write_int('rst_gbe',1)
fpga.write_int('packet_period',pkt_period)
fpga.write_int('packet_payload_len',payload_len)
fpga.write_int('dest_ip',dest_ip)
fpga.write_int('dest_port',dest_port)
fpga.write_int('rst_gbe',0)

print('ok')
#create udp socket to receive the data
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
print('starting socket on {} port {}'.format(*(pc_ip, dest_port)))
sock.bind((pc_ip, dest_port))

plt.ion()

fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_ylim(0,256)
ax.set_xlim(0,payload_len*20)
line, = ax.plot([],[])
plt.show()


x_data = np.arange(payload_len*20)
y_data = np.zeros(payload_len*20)

print('Start transmition')
fpga.write_int('packet_enable',1)
while(1):
    try:
        while(1):
            data_b = sock.recv(payload_len)
            data = np.array(struct.unpack(str(payload_len)+'B',data_b))
            print(data)
            #y_data = np.roll(y_data)
            #y_data[:payload_len] = data
            #line.set_data(x_data, y_data)
            #fig.canvas.draw()
            #fig.canvas.flush_events()
    except:
        pass
    finally:
        sock.close()
        









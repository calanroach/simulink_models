import corr, time, numpy, struct, sys,socket
import matplotlib.pyplot as plt

roach_ip = '192.168.1.18'

##with 512, 511 we transmit.. but in the recv side we lost some packages
pkt_period = 60#512#255#100  #in FPGA clocks (200MHz) la cague
payload_len = 50#511#254#50   #in 64bit words
fpga_clk = 100

data_rate = 1.*payload_len/pkt_period*fpga_clk
tge_rate = data_rate/(8./10*156.25)

print("10gb rate: %.4f" %(tge_rate*10))


#dest_ip  =10*(2**24) + 30 #10.0.0.30
dest_ip =  192*(2**24)+168*(2**16)+2*(2**8)+10 ##for computer test comment them in loopback mode
source_ip= 192*(2**24) + 168*(2**16) + 2*(2**8)+3 ##for computer test comment them 
fabric_port=1234#60000         
#source_ip=10*(2**24) + 20 #10.0.0.20
mac_base=(2<<40) + (2<<32)
ip_prefix='10. 0. 0.'     #Used for the purposes of printing output.



dest_ip1  =10*(2**24) + 50 #10.0.0.30
fabric_port1= 50000         
source_ip1 =10*(2**24) + 40 #10.0.0.20


tx_core_name = 'gbe0'
rx_core_name = 'gbe1'
tx_core_name1 = 'gbe2'
rx_core_name1 = 'gbe3'





fpga = corr.katcp_wrapper.FpgaClient(roach_ip)
time.sleep(1)
bof = 'loopback.bof.gz'
fpga.upload_program_bof(bof, 3000)
time.sleep(1)


fpga.tap_start('rx_tap',rx_core_name,mac_base+dest_ip,dest_ip,fabric_port)
fpga.tap_start('tx_tap',tx_core_name,mac_base+source_ip,source_ip,fabric_port)

fpga.tap_start('rx_tap1',rx_core_name1,mac_base+dest_ip1,dest_ip1,fabric_port1)
fpga.tap_start('tx_tap1',tx_core_name1,mac_base+source_ip1,source_ip1,fabric_port1)

fpga.write_int('packet_period',pkt_period)
fpga.write_int('packet_payload_len',payload_len)

fpga.write_int('dest_ip',dest_ip)
fpga.write_int('dest_port',fabric_port)

fpga.write_int('dest_ip1',dest_ip1)
fpga.write_int('dest_port1',fabric_port1)




fpga.write_int('gbe_rst',1)
fpga.write_int('gbe_rst',0)
fpga.write_int('cnt_rst',1)
fpga.write_int('cnt_rst',0)

fpga.write_int('packet_enable',1)
time.sleep(2)


rx_data = struct.unpack('>1024Q',fpga.read('rx_data',1024*8))
tx_data = struct.unpack('>1024Q',fpga.read('tx_data',1024*8))

rx_data1 = struct.unpack('>1024Q',fpga.read('rx_data1',1024*8))
#tx_data1 = struct.unpack('>1024Q',fpga.read('tx_data1',1024*8))

fig = plt.figure()
ax1 = fig.add_subplot(121)
ax2 = fig.add_subplot(122)


ax1.plot(tx_data)
ax1.set_title('tx_data')
ax1.grid()
ax2.plot(rx_data)
ax2.set_title('rx_data')
ax2.grid()

fig = plt.figure()
ax1 = fig.add_subplot(121)
ax2 = fig.add_subplot(122)


ax1.plot(tx_data)
ax1.set_title('tx_data1')
ax1.grid()
ax2.plot(rx_data1)
ax2.set_title('rx_data1')
ax2.grid()
plt.show()


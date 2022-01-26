import corr, time, numpy, struct, sys,socket
import matplotlib.pyplot as plt


pkt_period = 8192#100  #in FPGA clocks (200MHz) la cague
payload_len = 40#50   #in 64bit words

gen_rate = 1.*payload_len/pkt_period*135
tge_rate = gen_rate/(8./10*156.25)*10
print('data rate: %.2f GSa/s' %(tge_rate))

dest_ip  =192*(2**24) + 168*(2**16) + 0*(2**8)+29
fabric_port=10000

source_ip= 192*(2**24) + 168*(2**16) + 0*(2**8)+45 #10.0.0.20



tx_core_name = 'one_GbE'
mac_base=(2<<40) + (2<<32)

fpga = corr.katcp_wrapper.FpgaClient('192.168.0.40')
time.sleep(1)
bof = 'one_gbe.bof.gz'

fpga.upload_program_bof(bof,3000)
time.sleep(1)
fpga.tap_start('tx_tap',tx_core_name,mac_base+source_ip,source_ip,fabric_port)
time.sleep(1)

fpga.write_int('rst_gbe',1)
fpga.write_int('packet_period',pkt_period)
fpga.write_int('packet_payload_len',payload_len)
fpga.write_int('dest_ip',dest_ip)
fpga.write_int('dest_port',fabric_port)
fpga.write_int('rst_gbe',0)
fpga.write_int('packet_enable',1)





